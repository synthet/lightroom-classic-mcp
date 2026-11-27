"""Typed tool errors for the Lightroom Classic MCP server.

Every failure an agent sees starts with "[<Code>]" and ends with a recovery hint. The McpError also carries
{"code", "hint"} in its data, but FastMCP passes only the text to clients (see LightroomMCP in server.py).
The codes and their recovery hints are documented in docs/errors.md.
"""

from typing import Any, Optional

from mcp.shared.exceptions import McpError
from mcp.types import INTERNAL_ERROR, INVALID_PARAMS, ErrorData


class LrcErrorCode:
    BROKER_UNAVAILABLE = "BrokerUnavailable"
    BROKER_UNAUTHORIZED = "BrokerUnauthorized"
    PLUGIN_DISCONNECTED = "PluginDisconnected"
    LIGHTROOM_TIMEOUT = "LightroomTimeout"
    INVALID_PARAMS = "InvalidParams"
    NO_CATALOG = "NoCatalog"
    NO_SELECTION = "NoSelection"
    NOT_FOUND = "NotFound"
    METHOD_NOT_FOUND = "MethodNotFound"
    PLUGIN_ERROR = "PluginError"
    TARGET_MISMATCH = "TargetMismatch"
    READBACK_MISMATCH = "ReadbackMismatch"
    INTERNAL = "InternalError"


HINTS = {
    LrcErrorCode.BROKER_UNAVAILABLE: "The broker on 127.0.0.1:8085 is not running and could not be started. Run mcp-server/start_broker.py, then retry.",
    LrcErrorCode.BROKER_UNAUTHORIZED: "The broker refused the access token. Its discovery file (~/.lightroom-classic-mcp/broker.json) is missing or belongs to an older broker. Restart the broker (mcp-server/start_broker.py), then retry.",
    LrcErrorCode.PLUGIN_DISCONNECTED: "The broker runs but the Lightroom plugin is not polling it. Open Lightroom Classic and check File > Plug-in Manager > MCP Bridge is enabled.",
    LrcErrorCode.LIGHTROOM_TIMEOUT: "Lightroom is connected but did not answer in time; it may be busy (import, export, modal dialog). Wait, then retry; for a write, read the photo first to see whether it applied.",
    LrcErrorCode.INVALID_PARAMS: "Fix the arguments as the message says and resend.",
    LrcErrorCode.NO_CATALOG: "Open a catalog in Lightroom Classic.",
    LrcErrorCode.NO_SELECTION: "Select the target photos in Lightroom (or use select_photos), then retry.",
    LrcErrorCode.NOT_FOUND: "Check the name, id or path; list what exists first (list_collections, list_develop_presets, search_photos).",
    LrcErrorCode.METHOD_NOT_FOUND: "The installed plugin is older than this server. Reinstall lightroom-plugin.lrplugin and reload it in Plug-in Manager.",
    LrcErrorCode.PLUGIN_ERROR: "The plugin reported an error; see the message and plugin_debug.log.",
    LrcErrorCode.TARGET_MISMATCH: "The selected photos are not exactly the ones in expected_photos. Call get_selection, then resend with all selected ids or file names (or select the right photos first).",
    LrcErrorCode.READBACK_MISMATCH: "A develop value did not read back as written (out of range, or another controller changed it). Call get_develop_settings, then retry.",
    LrcErrorCode.INTERNAL: "Unexpected server error; see the message and mcp_debug.log.",
}


def tool_error(code: str, message: str, details: Optional[dict] = None) -> McpError:
    """An McpError whose text starts with [code] and ends with the recovery hint."""
    hint = HINTS.get(code)
    text = f"[{code}] {message}" + (f" Hint: {hint}" if hint else "")
    data: dict[str, Any] = {"code": code, "hint": hint}
    if details:
        data["details"] = details
    return McpError(ErrorData(code=INVALID_PARAMS if code == LrcErrorCode.INVALID_PARAMS else INTERNAL_ERROR,
                              message=text, data=data))


def as_tool_error(exc: Exception) -> McpError:
    """Keep a typed McpError as it is; wrap anything else as InternalError."""
    return exc if isinstance(exc, McpError) else tool_error(LrcErrorCode.INTERNAL, str(exc))


def classify_plugin_message(message: str) -> str:
    """Map a plugin handler's error string to a code."""
    text = (message or "").lower()
    if text.startswith("target mismatch"):
        return LrcErrorCode.TARGET_MISMATCH
    if text.startswith("readback mismatch"):
        return LrcErrorCode.READBACK_MISMATCH
    if "no active catalog" in text:
        return LrcErrorCode.NO_CATALOG
    if "no photos selected" in text:
        return LrcErrorCode.NO_SELECTION
    if "not found" in text or "no matching" in text:
        return LrcErrorCode.NOT_FOUND
    if "timeout" in text:
        return LrcErrorCode.LIGHTROOM_TIMEOUT
    if text.startswith("invalid") or "must be" in text or "required" in text:
        return LrcErrorCode.INVALID_PARAMS
    return LrcErrorCode.PLUGIN_ERROR


def plugin_error(error: Any) -> McpError:
    """A typed error for a JSON-RPC error object or a handler's error string."""
    if isinstance(error, dict):
        number = error.get("code")
        message = str(error.get("message", "Lightroom error"))
        detail = error.get("data")
        if detail:
            message = f"{message}: {detail}"
        if number == -32601:
            return tool_error(LrcErrorCode.METHOD_NOT_FOUND, message)
        if number == -32000:
            return tool_error(LrcErrorCode.LIGHTROOM_TIMEOUT, message)
        return tool_error(classify_plugin_message(message), message)
    message = str(error)
    return tool_error(classify_plugin_message(message), message)


def raise_for_response(response: Any) -> dict:
    """Return the JSON-RPC response if it carries a usable result; raise a typed error otherwise.

    Plugin handlers report failures as a result of the form {"error": "..."}; those are failures too.
    """
    if not response:
        raise tool_error(LrcErrorCode.PLUGIN_DISCONNECTED, "No response from Lightroom.")
    if response.get("error"):
        raise plugin_error(response["error"])
    result = response.get("result")
    if isinstance(result, dict) and isinstance(result.get("error"), str):
        raise plugin_error(result["error"])
    return response
