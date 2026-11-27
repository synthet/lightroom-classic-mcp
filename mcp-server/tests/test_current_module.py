"""lrcmcp-hqk7b: get_current_module returned the plugin's {module: ...} dict from a tool declared -> str."""

import asyncio
import os
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import server


def _ctx(client):
    return SimpleNamespace(request_context=SimpleNamespace(lifespan_context=SimpleNamespace(lrc=client)))


class CurrentModuleTests(unittest.TestCase):
    def _run_tool(self, reply):
        client = MagicMock()
        client.send_command.return_value = reply
        tool = server.mcp._tool_manager.get_tool("get_current_module")
        # convert_result=True runs FastMCP's output validation, where the live call failed
        return asyncio.run(tool.run({}, context=_ctx(client), convert_result=True))

    def test_plugin_reply_becomes_the_module_name(self):
        result = self._run_tool({"jsonrpc": "2.0", "id": 1, "result": {"module": "library"}})
        text = result[0][0].text if isinstance(result, tuple) else result[0].text
        self.assertEqual("library", text)

    def test_direct_call_returns_a_string(self):
        client = MagicMock()
        client.send_command.return_value = {"result": {"module": "develop"}}
        self.assertEqual("develop", asyncio.run(server.get_current_module(_ctx(client))))


if __name__ == "__main__":
    unittest.main()
