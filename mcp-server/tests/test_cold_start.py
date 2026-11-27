"""lrcmcp-11zro: the first call after a cold start waits long enough for the broker to come up."""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import lrc_client


class FakeClock:
    def __init__(self):
        self.now = 1000.0

    def monotonic(self):
        return self.now

    def sleep(self, seconds):
        self.now += seconds


def _ok(body):
    r = MagicMock()
    r.status_code = 200
    r.json.return_value = body
    r.raise_for_status.return_value = None
    return r


class ColdStartTests(unittest.TestCase):
    def setUp(self):
        self.clock = FakeClock()
        for target, fake in (("lrc_client.time.sleep", self.clock.sleep), ("lrc_client.time.monotonic", self.clock.monotonic)):
            p = patch(target, side_effect=fake)
            p.start()
            self.addCleanup(p.stop)
        self.started_at = None

    def _broker_ready_after(self, seconds):
        """A fake broker that answers /api/status only once `seconds` have passed since Popen."""
        def popen(*args, **kwargs):
            self.started_at = self.clock.now
            proc = MagicMock()
            proc.poll.return_value = None
            return proc

        def status(*args, **kwargs):
            if self.started_at is None or self.clock.now - self.started_at < seconds:
                raise lrc_client.requests.exceptions.ConnectionError()
            return _ok({})
        return popen, status

    def test_first_call_after_a_cold_start_waits_for_a_slow_broker(self):
        popen, status = self._broker_ready_after(7)
        with patch("lrc_client.subprocess.Popen", side_effect=popen) as p, \
             patch("lrc_client.requests.get", side_effect=status), \
             patch("lrc_client.requests.post", return_value=_ok({"jsonrpc": "2.0", "id": 1, "result": {"ok": True}})):
            result = lrc_client.LrCClient().send_command("get_selection")
        self.assertEqual({"ok": True}, result["result"])
        p.assert_called_once()

    def test_gives_up_after_the_configured_timeout_and_logs_elapsed(self):
        popen, status = self._broker_ready_after(10_000)
        with patch.dict(os.environ, {"LRC_BROKER_START_TIMEOUT": "3"}), \
             patch("lrc_client.subprocess.Popen", side_effect=popen), \
             patch("lrc_client.requests.get", side_effect=status), \
             self.assertLogs("lrc_client", level="INFO") as logs:
            self.assertFalse(lrc_client.LrCClient().start_broker())
        self.assertTrue(3 <= self.clock.now - 1000.0 < 4, self.clock.now - 1000.0)
        self.assertTrue(any("3.0 s" in line or "after 3" in line for line in logs.output), logs.output)

    def test_success_is_logged_with_elapsed_time(self):
        popen, status = self._broker_ready_after(2)
        with patch("lrc_client.subprocess.Popen", side_effect=popen), \
             patch("lrc_client.requests.get", side_effect=status), \
             self.assertLogs("lrc_client", level="INFO") as logs:
            self.assertTrue(lrc_client.LrCClient().start_broker())
        self.assertTrue(any("ready after" in line for line in logs.output), logs.output)

    def test_default_timeout_is_about_twenty_seconds(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("LRC_BROKER_START_TIMEOUT", None)
            self.assertEqual(20.0, lrc_client.broker_start_timeout())

    def test_a_broker_that_exits_stops_the_wait(self):
        def popen(*args, **kwargs):
            proc = MagicMock()
            proc.poll.return_value = 1
            proc.returncode = 1
            return proc
        with patch("lrc_client.subprocess.Popen", side_effect=popen), \
             patch("lrc_client.requests.get", side_effect=lrc_client.requests.exceptions.ConnectionError()):
            self.assertFalse(lrc_client.LrCClient().start_broker())
        self.assertLess(self.clock.now - 1000.0, 2)


if __name__ == "__main__":
    unittest.main()
