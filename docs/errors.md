# Error codes

Every tool failure starts with `[<Code>]`, then the message, then `Hint:` and a recovery step. The same code and hint are in the error's `data` (`{"code", "hint"}`). Codes are defined in `mcp-server/errors.py`.

| Code | When | Recovery |
|---|---|---|
| `BrokerUnavailable` | The broker on 127.0.0.1:8085 isn't running and couldn't be started, or refused the connection | Run `mcp-server/start_broker.py`, then retry |
| `PluginDisconnected` | The broker runs, but the Lightroom plugin isn't polling it (checked after a timeout) | Open Lightroom Classic; check File > Plug-in Manager > MCP Bridge is enabled |
| `LightroomTimeout` | The plugin is connected but didn't answer in time, or a handler timed out (for example waiting for a thumbnail) | Wait and retry. For a write, read the photo first to see whether it applied |
| `InvalidParams` | An argument is missing, has the wrong type or is out of range (checked by the server or the plugin) | Fix the arguments as the message says |
| `NoCatalog` | Lightroom has no active catalog | Open a catalog |
| `NoSelection` | The tool works on the selected photos and none are selected | Select the photos in Lightroom, or call `select_photos` |
| `NotFound` | A preset, collection, photo or file doesn't exist | List what exists first (`list_develop_presets`, `list_collections`, `search_photos`) |
| `MethodNotFound` | The installed plugin doesn't know the command: it's older than the server | Reinstall `lightroom-plugin.lrplugin` and reload it in Plug-in Manager |
| `PluginError` | The plugin reported another error | See the message and `plugin_debug.log` |
| `TargetMismatch` | Reserved for the write contract (lrcmcp-aiakw): the photos a write would change aren't the ones named | Re-read the selection and resend |
| `ReadbackMismatch` | Reserved for the write contract (lrcmcp-aiakw): a value didn't read back as written | Read the settings and retry |
| `InternalError` | Anything unexpected in the server | See the message and `mcp_debug.log` |

Before this list existed, a plugin handler that couldn't act (for example "No photos selected") returned its error inside a normal result, and write tools reported "Success". The server now treats any result of the form `{"error": "..."}` as a failure with the matching code.
