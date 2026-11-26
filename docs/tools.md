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
| `expected_photos` | yes | The ids (`localId` from `get_selection`) or file names of **all** the photos the write should change. A file name matches with or without its extension (`DSC_0001` or `DSC_0001.NEF`). |
| `confirmed` | to write | Must be `true`, or nothing is written (`InvalidParams`). |
| `dry_run` | no | `true` returns the plan and writes nothing. It needs no confirmation. |

The plugin checks the selection against `expected_photos` before it writes. If a selected photo isn't listed, or a listed photo isn't selected, it writes nothing and returns `TargetMismatch`, naming both lists. That catches a selection that changed (a click in Lightroom) between the agent's read and its write.

Results:
- **Dry run:** `{"dryRun": true, "photos": [{"localId", "fileName", "before": {...}, "after": {...}}]}`. `before` holds the current values of the fields the write touches; `after` the planned ones.
- **Write:** `{"success": true, "photos": [{"localId", "fileName"}]}`.
- **Develop readback:** after `set_develop_settings` writes, the plugin reads each photo's develop settings back. Numbers must match within 0.01, anything else exactly. If not, the result is `ReadbackMismatch`, naming the photo, key, wanted and actual value. The other values may already be written by then.

Typical use:
1. `get_selection`: note the `localId` or file names.
2. Call the write with `expected_photos` and `dry_run: true`, and check the plan.
3. Resend with `confirmed: true` and without `dry_run`.

Not covered yet: `apply_develop_preset`, `create_snapshot`, `create_virtual_copy`, `rotate_photo` and `add_to_collection` still act on the selection without this contract.
