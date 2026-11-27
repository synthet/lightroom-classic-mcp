import asyncio
import os
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from mcp.shared.exceptions import McpError

import errors
import lrc_client
import server
from errors import LrcErrorCode


def _response(json_body, status=200):
    r = MagicMock()
    r.status_code = status
    r.json.return_value = json_body
    r.raise_for_status.return_value = None
    return r


def _ctx(client):
    return SimpleNamespace(request_context=SimpleNamespace(lifespan_context=SimpleNamespace(lrc=client)))


def _code(exc: McpError) -> str:
    return exc.error.data["code"]


class ClassifyTests(unittest.TestCase):
    def test_plugin_messages_map_to_codes(self):
        cases = {
            "No active catalog": LrcErrorCode.NO_CATALOG,
            "No photos selected": LrcErrorCode.NO_SELECTION,
            "Preset not found": LrcErrorCode.NOT_FOUND,
            "No matching photos found": LrcErrorCode.NOT_FOUND,
            "Timeout waiting for thumbnail": LrcErrorCode.LIGHTROOM_TIMEOUT,
            "Invalid rating parameter": LrcErrorCode.INVALID_PARAMS,
            "Rating must be between 0 and 5": LrcErrorCode.INVALID_PARAMS,
            "Failed to create or find collection": LrcErrorCode.PLUGIN_ERROR,
            "Target mismatch: Lightroom would change [a.NEF] but expected [b]": LrcErrorCode.TARGET_MISMATCH,
            "Readback mismatch: a.NEF.Exposure2012: wanted 1, got 0": LrcErrorCode.READBACK_MISMATCH,
            "Invalid expected parameter - list the ids": LrcErrorCode.INVALID_PARAMS,
        }
        for message, code in cases.items():
            self.assertEqual(code, errors.classify_plugin_message(message), message)

    def test_error_text_carries_code_and_hint(self):
        exc = errors.tool_error(LrcErrorCode.NO_SELECTION, "No photos selected")
        self.assertTrue(exc.error.message.startswith("[NoSelection] No photos selected"))
        self.assertIn("Hint:", exc.error.message)
        self.assertEqual("NoSelection", exc.error.data["code"])
        self.assertTrue(exc.error.data["hint"])

    def test_every_code_has_a_hint(self):
        for name, value in vars(LrcErrorCode).items():
            if name.isupper():
                self.assertIn(value, errors.HINTS, value)

    def test_handler_error_inside_a_result_is_a_failure(self):
        with self.assertRaises(McpError) as caught:
            errors.raise_for_response({"jsonrpc": "2.0", "id": 1, "result": {"error": "No photos selected"}})
        self.assertEqual(LrcErrorCode.NO_SELECTION, _code(caught.exception))

    def test_method_not_found_means_an_outdated_plugin(self):
        with self.assertRaises(McpError) as caught:
            errors.raise_for_response({"error": {"code": -32601, "message": "Method not found: start_export"}})
        self.assertEqual(LrcErrorCode.METHOD_NOT_FOUND, _code(caught.exception))

    def test_a_good_result_passes_through(self):
        response = {"result": {"success": True}}
        self.assertIs(response, errors.raise_for_response(response))

    def test_as_tool_error_keeps_typed_errors(self):
        typed = errors.tool_error(LrcErrorCode.NO_CATALOG, "No active catalog")
        self.assertIs(typed, errors.as_tool_error(typed))
        self.assertEqual(LrcErrorCode.INTERNAL, _code(errors.as_tool_error(ValueError("boom"))))


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.client = lrc_client.LrCClient()

    def test_broker_down_is_broker_unavailable(self):
        with patch.object(self.client, "_ensure_broker_running", return_value=False), \
             patch.object(self.client, "start_broker", return_value=False):
            with self.assertRaises(McpError) as caught:
                self.client.send_command("get_studio_info")
        self.assertEqual(LrcErrorCode.BROKER_UNAVAILABLE, _code(caught.exception))

    def test_http_timeout_is_lightroom_timeout(self):
        with patch.object(self.client, "_ensure_broker_running", return_value=True), \
             patch("lrc_client.requests.post", side_effect=requests.exceptions.Timeout()), \
             patch("lrc_client.check_plugin_status", return_value={"broker_running": True, "lightroom_connected": True}):
            with self.assertRaises(McpError) as caught:
                self.client.send_command("get_selection")
        self.assertEqual(LrcErrorCode.LIGHTROOM_TIMEOUT, _code(caught.exception))

    def test_broker_timeout_with_no_plugin_is_plugin_disconnected(self):
        timeout = _response({"error": {"code": -32000, "message": "Request timeout - Lightroom not responding"}})
        with patch.object(self.client, "_ensure_broker_running", return_value=True), \
             patch("lrc_client.requests.post", return_value=timeout), \
             patch("lrc_client.check_plugin_status", return_value={"broker_running": True, "lightroom_connected": False}):
            with self.assertRaises(McpError) as caught:
                self.client.send_command("get_selection")
        self.assertEqual(LrcErrorCode.PLUGIN_DISCONNECTED, _code(caught.exception))

    def test_broker_timeout_with_plugin_polling_is_lightroom_timeout(self):
        timeout = _response({"error": {"code": -32000, "message": "Request timeout - Lightroom not responding"}})
        with patch.object(self.client, "_ensure_broker_running", return_value=True), \
             patch("lrc_client.requests.post", return_value=timeout), \
             patch("lrc_client.check_plugin_status", return_value={"broker_running": True, "lightroom_connected": True}):
            with self.assertRaises(McpError) as caught:
                self.client.send_command("get_selection")
        self.assertEqual(LrcErrorCode.LIGHTROOM_TIMEOUT, _code(caught.exception))


class ToolCallTests(unittest.TestCase):
    """Errors as an MCP client sees them: through FastMCP's call_tool, text only."""

    def _call(self, name, arguments):
        with self.assertRaises(Exception) as caught:
            asyncio.run(server.mcp.call_tool(name, arguments))
        return str(caught.exception)

    def test_wrong_argument_type_is_invalid_params(self):
        text = self._call("set_rating", {"rating": "abc"})
        self.assertTrue(text.startswith("[InvalidParams]"), text)
        self.assertIn("rating", text)
        self.assertIn("Hint:", text)

    def test_missing_argument_is_invalid_params(self):
        text = self._call("set_rating", {})
        self.assertTrue(text.startswith("[InvalidParams]"), text)
        self.assertIn("rating", text)

    def test_list_argument_given_a_string_is_invalid_params(self):
        text = self._call("add_keywords", {"keywords": "x"})
        self.assertTrue(text.startswith("[InvalidParams]"), text)
        self.assertIn("keywords", text)

    def test_typed_errors_reach_the_client_without_the_fastmcp_prefix(self):
        text = self._call("set_rating", {"rating": 9, "expected_photos": ["a"], "confirmed": True})
        self.assertTrue(text.startswith("[InvalidParams] Rating must be between 0 and 5"), text)


class WriteContractTests(unittest.TestCase):
    WRITE_TOOLS = ["set_rating", "set_label", "set_caption", "set_title", "set_pick_flag", "add_keywords",
                   "remove_keywords", "set_metadata", "set_develop_settings", "set_iptc_data", "set_gps_data",
                   "clear_gps_data"]

    def _call(self, name, arguments):
        with self.assertRaises(Exception) as caught:
            asyncio.run(server.mcp.call_tool(name, arguments))
        return str(caught.exception)

    def test_every_write_tool_requires_expected_photos(self):
        for tool in self.WRITE_TOOLS:
            schema = next(t for t in asyncio.run(server.mcp.list_tools()) if t.name == tool).inputSchema
            self.assertIn("expected_photos", schema["required"], tool)
            self.assertIn("confirmed", schema["properties"], tool)
            self.assertIn("dry_run", schema["properties"], tool)

    def test_missing_expected_photos_is_invalid_params(self):
        text = self._call("set_rating", {"rating": 3, "confirmed": True})
        self.assertTrue(text.startswith("[InvalidParams]"), text)
        self.assertIn("expected_photos", text)

    def test_unconfirmed_write_is_refused_before_contacting_lightroom(self):
        client = MagicMock()
        with self.assertRaises(McpError) as caught:
            asyncio.run(server.set_rating(3, ["DSC_0001"], _ctx(client)))
        self.assertEqual(LrcErrorCode.INVALID_PARAMS, _code(caught.exception))
        self.assertIn("confirmed", caught.exception.error.message)
        client.send_command.assert_not_called()

    def test_expected_photos_accepts_numeric_local_ids(self):
        # get_selection returns localId as a number; passing it back must not fail schema validation
        text = self._call("set_rating", {"rating": 9, "expected_photos": [123], "confirmed": True})
        self.assertTrue(text.startswith("[InvalidParams] Rating must be between 0 and 5"), text)
        self.assertEqual(["123", "DSC_0001"], server._write_params({}, [123, "DSC_0001"], True, False)["expected"])

    def test_empty_expected_photos_is_refused(self):
        client = MagicMock()
        with self.assertRaises(McpError) as caught:
            asyncio.run(server.set_title("t", [], _ctx(client), confirmed=True))
        self.assertEqual(LrcErrorCode.INVALID_PARAMS, _code(caught.exception))
        client.send_command.assert_not_called()

    def test_contract_fields_reach_the_plugin_and_dry_run_needs_no_confirmation(self):
        client = MagicMock()
        client.send_command.return_value = {"result": {"dryRun": True, "photos": [{"localId": "1", "before": {"rating": 2}, "after": {"rating": 4}}]}}
        plan = asyncio.run(server.set_rating(4, ["DSC_0001"], _ctx(client), dry_run=True))
        self.assertTrue(plan["dryRun"])
        method, params = client.send_command.call_args[0]
        self.assertEqual("set_rating", method)
        self.assertEqual({"rating": 4, "expected": ["DSC_0001"], "confirmed": False, "dryRun": True}, params)

    def test_target_and_readback_mismatches_are_typed(self):
        for message, code in [("Target mismatch: Lightroom would change [a.NEF] but expected [b]", LrcErrorCode.TARGET_MISMATCH),
                              ("Readback mismatch: a.NEF.Exposure2012: wanted 1, got 0", LrcErrorCode.READBACK_MISMATCH)]:
            client = lrc_client.LrCClient()
            with patch.object(client, "_ensure_broker_running", return_value=True), \
                 patch("lrc_client.requests.post", return_value=_response({"result": {"error": message}})):
                with self.assertRaises(McpError) as caught:
                    asyncio.run(server.set_develop_settings({"Exposure2012": 1}, ["a"], _ctx(client), confirmed=True))
            self.assertEqual(code, _code(caught.exception))


class ServerTests(unittest.TestCase):
    def _client_returning(self, body):
        client = lrc_client.LrCClient()
        patcher_running = patch.object(client, "_ensure_broker_running", return_value=True)
        patcher_post = patch("lrc_client.requests.post", return_value=_response(body))
        patcher_running.start(); patcher_post.start()
        self.addCleanup(patcher_running.stop); self.addCleanup(patcher_post.stop)
        return client

    def test_a_write_that_did_nothing_no_longer_reports_success(self):
        client = self._client_returning({"jsonrpc": "2.0", "id": 1, "result": {"error": "No photos selected"}})
        with self.assertRaises(McpError) as caught:
            asyncio.run(server.set_develop_settings({"Exposure": 1.0}, ["DSC_0001"], _ctx(client), confirmed=True))
        self.assertEqual(LrcErrorCode.NO_SELECTION, _code(caught.exception))

    def test_tool_argument_errors_are_invalid_params(self):
        with self.assertRaises(McpError) as caught:
            asyncio.run(server.set_rating(9, ["DSC_0001"], _ctx(MagicMock()), confirmed=True))
        self.assertEqual(LrcErrorCode.INVALID_PARAMS, _code(caught.exception))

    def test_studio_info_reports_versions_and_capabilities(self):
        client = self._client_returning({"result": {
            "catalogName": "Test", "catalogPath": "C:/x.lrcat", "pluginVersion": "0.1.0",
            "lightroomVersion": "16.0.1", "lightroomBuild": 202611}})
        info = asyncio.run(server.get_studio_info(_ctx(client)))
        self.assertEqual("16.0.1", info["lightroomVersion"])
        self.assertEqual({"ai_denoise": False, "super_resolution": False, "hdr_merge": False},
                         {k: info["capabilities"][k] for k in ("ai_denoise", "super_resolution", "hdr_merge")})
        self.assertIn("classic-sdk.md", info["capabilities"]["source"])


if __name__ == "__main__":
    unittest.main()
