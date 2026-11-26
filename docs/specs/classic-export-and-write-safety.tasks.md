# Tasks: Lightroom Classic export job and write safety

Spec: [classic-export-and-write-safety.md](classic-export-and-write-safety.md).

| ID | Task | Owner role | Files / areas | Depends on | ACs | Verification |
|----|------|------------|---------------|------------|-----|--------------|
| T-1 | Typed error codes plus real Lightroom version, plugin version and capabilities in `get_studio_info`. Pattern: lightroom-mcp `docs/errors.md` and its `LrErrorCodes` | backend | `mcp-server/server.py`, `mcp-server/lrc_client.py`, `lightroom-plugin.lrplugin/CommandHandlers.lua`, `lightroom-plugin.lrplugin/Info.lua`, `docs/errors.md` | - | AC-1, AC-2 | Lua tests (`lightroom-plugin.lrplugin/tests/RunTests.lua`) and `pytest mcp-server/tests` |
| T-2 | Write contract (`confirmed`, expected photo ids or file names, `dryRun`, develop readback) for every write tool. Pattern: lightroom-mcp `src/LightroomMcp/Tools/LrToolService.cs` and the write contract in its `docs/tools.md` | backend | `mcp-server/server.py`, `lightroom-plugin.lrplugin/CommandHandlers.lua`, `lightroom-plugin.lrplugin/tests/`, `docs/tools.md` | T-1 | AC-3, AC-4, AC-5, AC-6 | Lua tests with `Mocks.lua` and `pytest mcp-server/tests`; live check in Lightroom recorded or marked not run |
| T-3 | Async export job: start returns a job id, status is polled, completion requires verified outputs. Spec the tool names in `docs/tools.md` first | backend | `lightroom-plugin.lrplugin/CommandHandlers.lua`, `mcp-server/server.py`, `mcp-server/lrc_client.py`, `docs/tools.md` | T-1 | AC-7, AC-8, AC-9 | Lua tests with a mocked `LrExportSession` and `pytest mcp-server/tests`; live LrC export recorded or marked not run |
