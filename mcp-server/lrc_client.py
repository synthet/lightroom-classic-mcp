"""
Lightroom Classic Client - HTTP client for MCP Broker

Communicates with the Lightroom plugin via the HTTP broker server.
Much simpler than the previous socket-based implementation.
"""

import json
import logging
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

from mcp.shared.exceptions import McpError

import requests

import broker_auth
from errors import LrcErrorCode, raise_for_response, tool_error

logger = logging.getLogger(__name__)

# Version
__version__ = "1.0.0"

# Broker configuration with environment variable overrides
BROKER_URL = os.environ.get("LRC_BROKER_URL", "http://127.0.0.1:8085")
BROKER_SCRIPT = Path(__file__).parent / "broker.py"


def auth_headers() -> Dict[str, str]:
    """The broker's access token, read fresh: the broker writes a new one each time it starts."""
    token = broker_auth.read_token()
    return {broker_auth.TOKEN_HEADER: token} if token else {}
REQUEST_TIMEOUT = int(os.environ.get("LRC_REQUEST_TIMEOUT", "35"))  # Slightly longer than broker's internal timeout


class LrCClient:
    """Client for communicating with Lightroom Classic via the MCP Broker."""

    def __init__(self, broker_url: str = BROKER_URL):
        self.broker_url = broker_url
        self._request_id = 0
        self._broker_process = None

    def _ensure_broker_running(self) -> bool:
        """Check if broker is running, optionally start it."""
        try:
            response = requests.get(f"{self.broker_url}/api/status", headers=auth_headers(), timeout=2)
            # 401: a broker is running but refuses the token; send_command reports BrokerUnauthorized
            return response.status_code in (200, 401)
        except requests.exceptions.ConnectionError:
            return False
        except Exception as e:
            logger.warning(f"Error checking broker status: {e}")
            return False

    def start_broker(self) -> bool:
        """Start the broker server if not already running."""
        if self._ensure_broker_running():
            logger.debug("Broker already running")
            return True

        logger.info("Starting broker server...")
        try:
            # Start broker as subprocess
            self._broker_process = subprocess.Popen(
                [sys.executable, str(BROKER_SCRIPT)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )

            # Wait for broker to start
            for _ in range(10):
                time.sleep(0.5)
                if self._ensure_broker_running():
                    logger.info("Broker started successfully")
                    return True

            logger.error("Broker failed to start within timeout")
            return False

        except Exception as e:
            logger.error(f"Failed to start broker: {e}")
            return False

    def send_command(self, method: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Send a JSON-RPC command to Lightroom via the broker."""

        # Ensure broker is running
        if not self._ensure_broker_running():
            if not self.start_broker():
                raise tool_error(LrcErrorCode.BROKER_UNAVAILABLE, "Broker not running and failed to start.")

        self._request_id += 1
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": self._request_id
        }

        try:
            logger.debug(f"Sending request: {method}")
            response = requests.post(
                f"{self.broker_url}/request",
                json=request,
                headers=auth_headers(),
                timeout=REQUEST_TIMEOUT
            )
            if response.status_code == 401:
                # The broker may have restarted with a new token: read it again and retry once
                response = requests.post(
                    f"{self.broker_url}/request",
                    json=request,
                    headers=auth_headers(),
                    timeout=REQUEST_TIMEOUT
                )
                if response.status_code == 401:
                    raise tool_error(LrcErrorCode.BROKER_UNAUTHORIZED, f"The broker refused the access token ({method}).")

            if response.status_code == 504:
                raise self._timeout_error(method)

            response.raise_for_status()
            result = response.json()
            logger.debug(f"Received response for: {method}")
        except McpError:
            raise
        except requests.exceptions.Timeout:
            logger.error("Request timeout")
            raise self._timeout_error(method)
        except requests.exceptions.ConnectionError:
            logger.error("Connection error - broker not available")
            raise tool_error(LrcErrorCode.BROKER_UNAVAILABLE, "Broker not available.")
        except Exception as e:
            logger.error(f"Communication error: {e}")
            raise tool_error(LrcErrorCode.INTERNAL, f"Communication error: {e}")

        if isinstance(result, dict) and isinstance(result.get("error"), dict) and result["error"].get("code") == -32000:
            raise self._timeout_error(method)
        return raise_for_response(result)

    @staticmethod
    def _timeout_error(method: str) -> McpError:
        """PluginDisconnected when the plugin is not polling the broker, else LightroomTimeout."""
        if not check_plugin_status().get("lightroom_connected", False):
            return tool_error(LrcErrorCode.PLUGIN_DISCONNECTED, f"Lightroom plugin is not connected to the broker ({method}).")
        return tool_error(LrcErrorCode.LIGHTROOM_TIMEOUT, f"Lightroom did not answer {method} in time.")

    def close(self):
        """Close the client and terminate broker if started by this instance."""
        if self._broker_process:
            logger.info("Terminating broker process...")
            try:
                self._broker_process.terminate()
                self._broker_process.wait(timeout=2)
            except Exception as e:
                logger.error(f"Error terminating broker: {e}")
                self._broker_process.kill()
            self._broker_process = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


def check_plugin_status() -> dict:
    """Check if the broker and Lightroom plugin are running."""
    status = {
        "broker_running": False,
        "lightroom_connected": False,
        "broker_url": BROKER_URL,
    }

    try:
        response = requests.get(f"{BROKER_URL}/api/status", headers=auth_headers(), timeout=2)
        if response.status_code == 200:
            status["broker_running"] = True
            data = response.json()
            status["lightroom_connected"] = data.get("lightroom_connected", False)
            status["requests_total"] = data.get("requests_total", 0)
            status["avg_latency_ms"] = data.get("avg_latency_ms", 0)
    except Exception:
        pass

    return status


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    print("Checking plugin status...")
    status = check_plugin_status()
    print(f"Status: {status}")

    if status["broker_running"] and status["lightroom_connected"]:
        print("\nTesting get_studio_info...")
        client = LrCClient()
        try:
            result = client.send_command("get_studio_info")
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")
