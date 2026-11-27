# Lightroom MCP

Bridge between [Adobe Lightroom Classic](https://www.adobe.com/products/photoshop-lightroom-classic.html) and AI agents via the [Model Context Protocol](https://modelcontextprotocol.io/) (MCP). Enables automated photo management, metadata editing, and catalog operations from Cursor and other MCP-capable clients.

## Architecture

- **Lightroom Plugin** (`lightroom-plugin.lrplugin/`) — Lua plugin running inside Lightroom Classic.
  - Connects to the Broker by HTTP long polling (port 8085), sending the access token from `~/.lightroom-classic-mcp/broker.json`.
- **MCP Broker** (`mcp-server/broker.py`) — A lightweight Flask server that acts as a bridge.
  - Relays requests between the Python MCP server and the Lua plugin.
  - Provides a dashboard at `http://localhost:8085`. Open it from the broker's tray icon (**Open Dashboard**) or from the link the broker prints at startup: both carry the access token the dashboard needs.
- **MCP Server** (`mcp-server/server.py`) — Python [FastMCP](https://github.com/jlowin/fastmcp) server.
  - Exposes Lightroom tools to Cursor/Claude.
  - Communicates with the Broker via HTTP.

```mermaid
graph LR
    Agent[Cursor / Agent] <-->|MCP| Server[MCP Server]
    Server <-->|HTTP| Broker[Broker :8085]
    Broker <-->|HTTP polling| Plugin[Lightroom Plugin]
```

## Prerequisites

- **Adobe Lightroom Classic** (LrSdk 10.0+)
- **Python 3.10+** (for the MCP server and Broker)
- **Lightroom** running with the plugin enabled

## Setup

### 1. Install the Lightroom plugin

1. Copy `lightroom-plugin.lrplugin` into your Lightroom plugins folder:
   - **macOS:** `~/Library/Application Support/Adobe/Lightroom/Modules/`
   - **Windows:** `%APPDATA%\Adobe\Lightroom\Modules\`
2. In Lightroom: **File → Plug-in Manager → Add** and select the plugin folder.
3. Ensure the plugin is **Enabled**. It polls the Broker on port 8085 and reconnects within a couple of seconds after the Broker restarts.

### 2. Configure & Run MCP Server

The MCP server handles starting the Broker automatically.

1. Set up the Python environment:
   ```bash
   cd mcp-server
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   # source .venv/bin/activate   # macOS / Linux
   pip install -r requirements.txt
   ```

2. Add to your Cursor MCP config (e.g. **Settings → MCP** or `.cursor/mcp.json`):

   ```json
   {
     "mcpServers": {
       "lightroom": {
         "command": "d:/Projects/lightroom-classic-mcp/mcp-server/.venv/Scripts/python.exe",
         "args": ["d:/Projects/lightroom-classic-mcp/mcp-server/server.py"]
       }
     }
   }
   ```
   **Note:** Use absolute paths to your venv python and `server.py`.

## Usage

1. Open **Lightroom Classic**.
2. **Start the MCP Server** (Cursor does this automatically when you open the project or use the tool).
   - The **Broker** will be started automatically by the MCP server if not running.
   - You can view the Broker Dashboard to see connection status and logs: use the tray icon's **Open Dashboard**, or the `Dashboard:` link the broker prints at startup (a bare `http://localhost:8085` has no access token).
3. Select photos in Lightroom.
4. Use Cursor to interact with your library!

**Examples:**
- "Get info about selected photos"
- "Rate these 5 stars"
- "Apply 'Vivid' preset"
- "Create a collection named 'Best of 2024'"

See **[agents.md](./agents.md)** for detailed tool semantics and agent workflows.

## Project layout

```
lightroom-classic-mcp/
├── README.md           # This file
├── docs/               # Knowledge index, including TourBox vs this server
├── agents.md           # Documentation for AI Agents
├── SDK_INTEGRATION.md  # Deep dive into LrSDK integration
├── lightroom-plugin.lrplugin/   # Lua Plugin
│   ├── Init.lua        # Startup & Server connection
│   ├── Server.lua      # Socket client implementation
│   └── ...
└── mcp-server/         # Python Components
    ├── server.py       # MCP Server (FastMCP)
    ├── broker.py       # Relay Broker (Flask)
    ├── lrc_client.py   # Client for Broker communication
    └── ...
```

## Troubleshooting

Tool errors start with a code such as `[NoSelection]` or `[PluginDisconnected]` and a recovery hint; see [docs/errors.md](docs/errors.md).


- **"Lightroom not connected"**:
  - Check the Broker Dashboard (tray icon > **Open Dashboard**).
  - Ensure the Lightroom Plugin is **Enabled** (Green light in Plug-in Manager).
  - Reload the plugin in Plug-in Manager to force a reconnection attempt.
  - Check `plugin_debug.log` for connection errors.

- **"Broker not running"**:
  - The MCP server should start it automatically.
  - You can manually start it: `python mcp-server/start_broker.py`

- **Port Conflicts**:
  - Broker uses port **8085** (HTTP). Ensure it is free.

## License

See repository license file.
