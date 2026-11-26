# Spec: Lightroom Classic export job and write safety

Source: review of the deep-research report "Headless and CLI Automation of Adobe and DxO RAW Processing" (2026-11-26). The report ranks the Classic Lua SDK as the best supported path for catalog, develop and export. Its version and product claims are unverified; the gaps below are confirmed in this repo.

## Problem
- No tool exports photos. The plugin never uses `LrExportSession`.
- Every broker request blocks on one call with a 35 s timeout (`mcp-server/lrc_client.py` `REQUEST_TIMEOUT`), too short for an export.
- `set_develop_settings` and the other write tools apply to whatever is selected (`catalog:getTargetPhotos()`) and return a bare "Success". Nothing checks the target or reads values back.
- Errors are free-text `INTERNAL_ERROR`. An agent can't tell "broker down" from "plugin disconnected" from "Lightroom timed out".
- `get_studio_info` returns a hard-coded `pluginVersion = "0.1.0"` and no Lightroom version, so nobody can tell whether a run used a tested build.

## Goal
Agents can export photos as a polled job with verified outputs. Writes hit only the photos the agent named, and every failure carries a typed code.

## Acceptance criteria
- **AC-1**: WHEN any tool fails THEN the error carries a stable code from a documented list (at least BrokerUnavailable, PluginDisconnected, LightroomTimeout, InvalidParams, NoSelection, TargetMismatch, ReadbackMismatch), a message and a recovery hint, and `docs/errors.md` documents the list. (`AGENTS.md` is gitignored, so it cannot hold the reference.)
- **AC-2**: WHEN `get_studio_info` runs THEN it reports the Lightroom Classic version and build from `LrApplication.versionTable()`, the plugin version from `Info.lua` (not a literal), and a `capabilities` object with `ai_denoise: false`, `super_resolution: false` and `hdr_merge: false`, citing `research_notes/Lightroom automation paths 2026/classic-sdk.md` §6.
- **AC-3**: WHEN a write tool (develop settings, rating, label, flag, title, caption, keywords, metadata, IPTC, GPS) runs without `confirmed: true` or without the expected photo ids or file names THEN it writes nothing and returns InvalidParams.
- **AC-4**: WHEN the target photos differ from the expected ids or file names THEN the write is refused with TargetMismatch and nothing is written.
- **AC-5**: WHEN a write runs with `dryRun: true` THEN it returns the planned before/after values per photo and writes nothing.
- **AC-6**: WHEN a develop write completes THEN the tool reads the settings back per photo and returns ReadbackMismatch for any value that didn't stick.
- **AC-7**: WHEN an export is started THEN the tool returns a job id within the normal request timeout, and the export runs in an async Lightroom task (`LrExportSession`).
- **AC-8**: WHEN the export status is polled THEN it reports accepted, running, completed or failed. It reports completed only when every expected output file exists, is non-empty and has a SHA-256 in the result, and failed with a typed code otherwise.
- **AC-9**: WHEN a new tool name is introduced THEN `docs/tools.md` (tracked; see lrcmcp-ut1qg) documents its name and schema before the code lands. The proposed names `start_export` and `get_export_status` are not final.

## Out of scope
- AI Denoise, Super Resolution and HDR merge: the SDK has no method (classic-sdk.md §6).
- Photoshop COM, ACR batch and cloud APIs.
