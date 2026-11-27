"""Broker access control (lrcmcp-squyr): token on relay and /api/* endpoints, dashboard Origin on /ws.

These tests never write the real discovery file or bind the broker port: a live broker may be running.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.shared.exceptions import McpError

import broker
import broker_auth
import lrc_client
from errors import LrcErrorCode

TOKEN = "test-token-123"
HEADER = broker_auth.TOKEN_HEADER
EVIL = "http://evil.example"


class BrokerAccessTests(unittest.TestCase):
    def setUp(self):
        self._token = broker.BROKER_TOKEN
        broker.BROKER_TOKEN = TOKEN
        self.client = broker.app.test_client()
        broker.pending_requests.clear()
        broker.request_queue.clear()
        self.addCleanup(setattr, broker, "BROKER_TOKEN", self._token)

    def test_relay_and_api_endpoints_need_the_token(self):
        for method, path in [("post", "/request"), ("post", "/poll"), ("post", "/response"), ("post", "/auto_edit"),
                             ("get", "/api/status"), ("get", "/api/requests"), ("get", "/api/logs"),
                             ("get", "/api/config"), ("post", "/api/test"), ("post", "/api/history/clear")]:
            for headers in ({}, {HEADER: "wrong"}):
                r = getattr(self.client, method)(path, json={"jsonrpc": "2.0", "method": "get_selection", "id": 1}, headers=headers)
                self.assertEqual(401, r.status_code, (path, headers))
        self.assertEqual(0, len(broker.pending_requests))
        self.assertEqual(0, len(broker.request_queue))

    def test_the_token_lets_requests_through(self):
        r = self.client.get("/api/status", headers={HEADER: TOKEN})
        self.assertEqual(200, r.status_code)

    def test_no_token_configured_refuses_everything(self):
        broker.BROKER_TOKEN = None
        self.assertEqual(401, self.client.get("/api/status", headers={HEADER: ""}).status_code)
        self.assertEqual(401, self.client.get("/api/status", headers={HEADER: "None"}).status_code)

    def test_exit_without_the_token_does_nothing(self):
        with patch("broker.threading.Thread") as thread:
            r = self.client.post("/api/exit")
        self.assertEqual(401, r.status_code)
        thread.assert_not_called()

    def test_exit_with_the_token_shuts_down(self):
        with patch("broker.threading.Thread") as thread:
            r = self.client.post("/api/exit", headers={HEADER: TOKEN})
        self.assertEqual(200, r.status_code)
        self.assertIn("delayed_exit", [c.kwargs.get("target").__name__ for c in thread.call_args_list if c.kwargs.get("target")])

    def test_cross_origin_page_cannot_exit_or_clear_history(self):
        with broker.stats_lock:
            broker.broker_stats["recent_requests"].append({"uuid": "keep-me"})
        self.addCleanup(broker.broker_stats["recent_requests"].clear)
        with patch("broker.threading.Thread") as thread, patch("broker.os.remove") as remove:
            for headers in ({"Origin": EVIL}, {"Origin": EVIL, HEADER: TOKEN}):
                self.assertIn(self.client.post("/api/exit", headers=headers).status_code, (401, 403))
                self.assertIn(self.client.post("/api/history/clear", headers=headers).status_code, (401, 403))
            # a form post, the simple request a page can send without a preflight
            self.assertIn(self.client.post("/api/exit", data={"x": "1"}, headers={"Origin": EVIL}).status_code, (401, 403))
        thread.assert_not_called()
        remove.assert_not_called()
        self.assertEqual([{"uuid": "keep-me"}], list(broker.broker_stats["recent_requests"]))

    def test_ws_accepts_only_the_dashboard_origin(self):
        for headers in ({}, {"Origin": EVIL}, {"Origin": "null"}):
            r = self.client.get(f"/ws?token={TOKEN}", headers=headers)
            self.assertEqual(403, r.status_code, headers)
        r = self.client.get("/ws", headers={"Origin": f"http://{broker.BROKER_HOST}:{broker.BROKER_PORT}"})
        self.assertEqual(401, r.status_code)

    def test_dashboard_page_carries_no_secret(self):
        r = self.client.get("/")
        self.assertEqual(200, r.status_code)
        self.assertNotIn(TOKEN, r.get_data(as_text=True))

    def test_second_broker_does_not_replace_the_running_brokers_token(self):
        with patch("broker.is_port_in_use", return_value=True), patch("broker_auth.write_discovery") as write:
            with self.assertRaises(SystemExit):
                broker.run_broker()
        write.assert_not_called()


class DiscoveryFileTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.path = Path(self.dir.name) / "sub" / "broker.json"

    def test_write_then_read(self):
        broker_auth.write_discovery("abc", 8085, self.path)
        self.assertEqual("abc", broker_auth.read_token(self.path))
        broker_auth.write_discovery("def", 8085, self.path)   # a restart replaces it
        self.assertEqual("def", broker_auth.read_token(self.path))
        self.assertEqual(["broker.json"], [p.name for p in self.path.parent.iterdir()])   # no temp file left

    @unittest.skipIf(sys.platform == "win32", "POSIX permissions; on Windows the home folder is user-only")
    def test_only_the_user_can_read_it(self):
        broker_auth.write_discovery("abc", 8085, self.path)
        self.assertEqual(0o600, self.path.stat().st_mode & 0o777)

    def test_missing_or_bad_file_reads_as_no_token(self):
        self.assertIsNone(broker_auth.read_token(self.path))
        self.path.parent.mkdir(parents=True)
        self.path.write_text("not json", encoding="utf-8")
        self.assertIsNone(broker_auth.read_token(self.path))

    def test_new_tokens_are_random_and_long(self):
        a, b = broker_auth.new_token(), broker_auth.new_token()
        self.assertNotEqual(a, b)
        self.assertGreaterEqual(len(a), 32)


def _response(status, body=None):
    r = MagicMock()
    r.status_code = status
    r.json.return_value = body or {}
    r.raise_for_status.return_value = None
    return r


class ClientTokenTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.path = Path(self.dir.name) / "broker.json"
        broker_auth.write_discovery("tok-1", 8085, self.path)
        env = patch.dict(os.environ, {broker_auth.DISCOVERY_ENV: str(self.path)})
        env.start()
        self.addCleanup(env.stop)

    def test_requests_carry_the_token(self):
        client = lrc_client.LrCClient()
        ok = _response(200, {"jsonrpc": "2.0", "id": 1, "result": {"ok": True}})
        with patch("lrc_client.requests.get", return_value=_response(200)) as get, \
             patch("lrc_client.requests.post", return_value=ok) as post:
            client.send_command("get_selection")
        self.assertEqual("tok-1", get.call_args.kwargs["headers"][HEADER])
        self.assertEqual("tok-1", post.call_args.kwargs["headers"][HEADER])

    def test_a_refused_token_is_reread_once(self):
        client = lrc_client.LrCClient()
        ok = _response(200, {"jsonrpc": "2.0", "id": 1, "result": {"ok": True}})

        def restart_then_answer(*args, **kwargs):
            if kwargs["headers"][HEADER] == "tok-1":
                broker_auth.write_discovery("tok-2", 8085, self.path)   # the broker restarted meanwhile
                return _response(401)
            return ok

        with patch("lrc_client.requests.get", return_value=_response(200)), \
             patch("lrc_client.requests.post", side_effect=restart_then_answer) as post:
            client.send_command("get_selection")
        self.assertEqual(2, post.call_count)
        self.assertEqual("tok-2", post.call_args.kwargs["headers"][HEADER])

    def test_a_token_refused_twice_is_broker_unauthorized(self):
        client = lrc_client.LrCClient()
        with patch("lrc_client.requests.get", return_value=_response(401)), \
             patch("lrc_client.requests.post", return_value=_response(401)), \
             patch("lrc_client.subprocess.Popen") as popen:
            with self.assertRaises(McpError) as caught:
                client.send_command("get_selection")
        self.assertEqual(LrcErrorCode.BROKER_UNAUTHORIZED, caught.exception.error.data["code"])
        popen.assert_not_called()   # a broker answering 401 is running; don't start a second one


if __name__ == "__main__":
    unittest.main()
