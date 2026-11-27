"""Export job (lrcmcp-s7ccv): start_export / get_export_status. See docs/tools.md#export-job."""

import asyncio
import hashlib
import os
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.shared.exceptions import McpError

import server
from errors import LrcErrorCode


def _ctx(client):
    return SimpleNamespace(request_context=SimpleNamespace(lifespan_context=SimpleNamespace(lrc=client)))


def _code(exc):
    return exc.error.data["code"]


class VerifyExportTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)

    def _file(self, name, data=b"jpeg-bytes"):
        path = os.path.join(self.dir.name, name)
        with open(path, "wb") as f:
            f.write(data)
        return path

    def _job(self, outputs, status="rendered", photos=None):
        photos = photos if photos is not None else [{"localId": str(i)} for i in range(len(outputs))]
        return {"jobId": "export-1", "status": status, "photos": photos, "outputs": outputs, "failures": []}

    def test_completed_only_with_every_file_present_non_empty_and_hashed(self):
        a, b = self._file("a.jpg"), self._file("b.jpg", b"other")
        result = server.verify_export(self._job([{"path": a}, {"path": b}]))
        self.assertEqual("completed", result["status"])
        self.assertEqual(hashlib.sha256(b"jpeg-bytes").hexdigest(), result["outputs"][0]["sha256"])
        self.assertEqual(5, result["outputs"][1]["bytes"])

    def test_missing_output_is_export_failed(self):
        with self.assertRaises(McpError) as caught:
            server.verify_export(self._job([{"path": os.path.join(self.dir.name, "gone.jpg")}]))
        self.assertEqual(LrcErrorCode.EXPORT_FAILED, _code(caught.exception))

    def test_empty_output_is_export_failed(self):
        with self.assertRaises(McpError) as caught:
            server.verify_export(self._job([{"path": self._file("empty.jpg", b"")}]))
        self.assertEqual(LrcErrorCode.EXPORT_FAILED, _code(caught.exception))

    def test_fewer_outputs_than_photos_is_export_failed(self):
        with self.assertRaises(McpError) as caught:
            server.verify_export(self._job([{"path": self._file("a.jpg")}], photos=[{"localId": "1"}, {"localId": "2"}]))
        self.assertEqual(LrcErrorCode.EXPORT_FAILED, _code(caught.exception))

    def test_a_failed_render_is_export_failed(self):
        job = self._job([], status="failed")
        job["failures"] = [{"fileName": "x.NEF", "message": "disk full"}]
        with self.assertRaises(McpError) as caught:
            server.verify_export(job)
        self.assertEqual(LrcErrorCode.EXPORT_FAILED, _code(caught.exception))
        self.assertIn("disk full", caught.exception.error.message)

    def test_accepted_and_running_pass_through(self):
        for status in ("accepted", "running"):
            self.assertEqual(status, server.verify_export(self._job([], status=status))["status"])


class ExportToolTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)

    def test_tools_are_listed(self):
        names = {t.name for t in asyncio.run(server.mcp.list_tools())}
        self.assertIn("start_export", names)
        self.assertIn("get_export_status", names)

    def test_start_export_sends_the_contract_and_settings(self):
        client = MagicMock()
        client.send_command.return_value = {"result": {"jobId": "export-7", "status": "accepted"}}
        result = asyncio.run(server.start_export(self.dir.name, [123], _ctx(client), format="tiff", quality=80, max_long_edge=2048, confirmed=True))
        self.assertEqual("export-7", result["jobId"])
        method, params = client.send_command.call_args[0]
        self.assertEqual("start_export", method)
        self.assertEqual({"destination": os.path.abspath(self.dir.name), "format": "TIFF", "quality": 80, "maxLongEdge": 2048,
                          "expected": ["123"], "confirmed": True, "dryRun": False}, params)

    def test_bad_arguments_are_invalid_params_before_lightroom(self):
        client = MagicMock()
        for kwargs in ({"format": "GIF"}, {"quality": 0}, {"quality": 101}, {"max_long_edge": 0}):
            with self.assertRaises(McpError) as caught:
                asyncio.run(server.start_export(self.dir.name, ["a"], _ctx(client), confirmed=True, **kwargs))
            self.assertEqual(LrcErrorCode.INVALID_PARAMS, _code(caught.exception), kwargs)
        with self.assertRaises(McpError) as caught:
            asyncio.run(server.start_export(os.path.join(self.dir.name, "missing"), ["a"], _ctx(client), confirmed=True))
        self.assertEqual(LrcErrorCode.INVALID_PARAMS, _code(caught.exception))
        with self.assertRaises(McpError) as caught:
            asyncio.run(server.start_export(self.dir.name, ["a"], _ctx(client)))
        self.assertEqual(LrcErrorCode.INVALID_PARAMS, _code(caught.exception))
        client.send_command.assert_not_called()

    def test_status_verifies_the_files(self):
        path = os.path.join(self.dir.name, "a.jpg")
        with open(path, "wb") as f:
            f.write(b"x")
        client = MagicMock()
        client.send_command.return_value = {"result": {"jobId": "export-7", "status": "rendered", "photos": [{"localId": "1"}],
                                                       "outputs": [{"localId": "1", "path": path}], "failures": []}}
        result = asyncio.run(server.get_export_status("export-7", _ctx(client)))
        self.assertEqual("completed", result["status"])
        self.assertEqual(hashlib.sha256(b"x").hexdigest(), result["outputs"][0]["sha256"])
        self.assertEqual(("get_export_status", {"jobId": "export-7"}), client.send_command.call_args[0])


if __name__ == "__main__":
    unittest.main()
