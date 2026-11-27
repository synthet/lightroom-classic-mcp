"""Broker access token (lrcmcp-squyr).

The broker makes a random token at startup and writes it to a discovery file that only this user can
read. Clients (lrc_client.py and the Lightroom plugin's BrokerAuth.lua) send it in the X-LrC-MCP-Token
header; the broker refuses /request, /poll, /response, /auto_edit and /api/* without it.

The file is <home>/.lightroom-classic-mcp/broker.json, because the plugin can resolve the same folder
with LrPathUtils.getStandardFilePath("home"). LRC_BROKER_DISCOVERY overrides the path for the Python
side only (tests).
"""

import json
import os
import secrets
import tempfile
from pathlib import Path
from typing import Optional

TOKEN_HEADER = "X-LrC-MCP-Token"
DISCOVERY_ENV = "LRC_BROKER_DISCOVERY"


def discovery_path() -> Path:
    override = os.environ.get(DISCOVERY_ENV)
    return Path(override) if override else Path.home() / ".lightroom-classic-mcp" / "broker.json"


def new_token() -> str:
    return secrets.token_urlsafe(32)


def write_discovery(token: str, port: int, path: Optional[Path] = None) -> Path:
    """Write {token, port, pid} atomically, readable by this user only."""
    path = Path(path or discovery_path())
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(path.parent, 0o700)
    except OSError:
        pass
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".broker-", suffix=".tmp")   # created 0600 on POSIX
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump({"token": token, "port": port, "pid": os.getpid()}, f)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    return path


def read_token(path: Optional[Path] = None) -> Optional[str]:
    """The token in the discovery file, or None when it is missing or unreadable."""
    try:
        data = json.loads(Path(path or discovery_path()).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    token = data.get("token") if isinstance(data, dict) else None
    return token if isinstance(token, str) and token else None
