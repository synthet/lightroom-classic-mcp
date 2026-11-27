# Tools

The full tool reference is moving here from the untracked `AGENTS.md` (lrcmcp-ut1qg). Until then, this file holds the contracts that span several tools. Error codes are in [errors.md](errors.md).

## Write contract

These tools change catalog data:
- `set_rating`, `set_label`, `set_pick_flag`, `set_title`, `set_caption`
- `add_keywords`, `remove_keywords`
- `set_metadata`, `set_iptc_data`
- `set_gps_data`, `clear_gps_data`
- `set_develop_settings`

Lightroom applies them to the photos selected in Lightroom at that moment. Each one takes three extra arguments:

| Argument | Required | Meaning |
|---|---|---|
| `expected_photos` | yes | The ids (`localId` from `get_selection`, as a number or a string) or file names of **all** the photos the write should change, one entry per photo. A file name matches with or without its extension (`DSC_0001` or `DSC_0001.NEF`). |
| `confirmed` | to write | Must be `true`, or nothing is written (`InvalidParams`). |
| `dry_run` | no | `true` returns the plan and writes nothing. It needs no confirmation. |

The plugin checks the selection against `expected_photos` before it writes. Each entry must name exactly one selected photo, no photo may be named twice, and the counts must agree. If a selected photo isn't listed, a listed photo isn't selected, or an entry matches several photos, it writes nothing and returns `TargetMismatch`, naming both lists. That catches a selection that changed (a click in Lightroom) between the agent's read and its write. An entry that matches several photos is ambiguous: a base name shared by a raw and its JPEG (`DSC_0001`), or the file name of a master and its virtual copies. Name such photos by their full file name or by `localId`.

Results:
- **Dry run:** `{"dryRun": true, "photos": [{"localId", "fileName", "before": {...}, "after": {...}}]}`. `before` holds the current values of the fields the write touches; `after` holds the planned values of the same fields, in the same form. For keywords, `after` is the photo's keyword list after the change.
- **Write:** `{"success": true, "photos": [{"localId", "fileName"}]}`.
- **Develop readback:** after `set_develop_settings` writes, the plugin reads each photo's develop settings back. Numbers must match within 0.01, tables (tone curves) by content, anything else exactly. If not, the result is `ReadbackMismatch`, naming the photo, key, wanted and actual value. The other values may already be written by then.

Typical use:
1. `get_selection`: note the `localId` or file names.
2. Call the write with `expected_photos` and `dry_run: true`, and check the plan.
3. Resend with `confirmed: true` and without `dry_run`.

Not covered yet: `apply_develop_preset`, `create_snapshot`, `create_virtual_copy`, `rotate_photo` and `add_to_collection` still act on the selection without this contract.
