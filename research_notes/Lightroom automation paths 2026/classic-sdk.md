# Classic SDK support for proposed automation

Research date: 2026-10-20. Documentation only. No repository code was changed.

## Source basis used for every verdict

### Takeaway
Classic plug-ins are documented as Lua. The API judgments below come from the © 2007–2022 Programmers Guide PDF and a third-party HTML mirror of the SDK reference whose newest “first supported” stamps found here are SDK 14.3. That mirror is not an Adobe host, and it may lag Classic 15.x, which Adobe’s help navigation already names.

### Cited Findings
- Adobe’s Classic developer landing page says: “Build plug-ins in Lua, the scripting language built into Lightroom.” It also says Lightroom “incorporates Lua” and “enhances Lua with a custom object-oriented infrastructure.” The fetched page has no version or “last updated” date. — [Creative Cloud - Lightroom Classic](https://developer.adobe.com/lightroom-classic/)
- The Programmers Guide PDF retrieved from the SDK installer CDN is titled “Adobe Photoshop Lightroom Classic SDK Programmers Guide,” copyright line “© 2007-2022 Adobe.” The CDN path includes `sdk/2023/.../v5`. The guide says the SDK download lives at `https://www.adobe.io/apis/creativecloud/lightroomclassic.html` and that the kit contains `LrC_SDK/Manual/Lightroom Classic SDK Guide.pdf` plus `LrC_SDK/API Reference/index.html`. That logged-in SDK zip was not opened. — [Lightroom Classic SDK Programmers Guide PDF](https://ioconsolerykerprodcdn.azureedge.net/static/installers/lr/sdk/2023/cross_platform/v5/doc/Lightroom%20Classic%20SDK%20Guide_1670563540.pdf)
- The same guide, section “The Lua language,” says: “The SDK defines a Lua-language scripting API. … Lightroom Classic uses version 5.1.4 of the Lua language.” — [Lightroom Classic SDK Programmers Guide PDF](https://ioconsolerykerprodcdn.azureedge.net/static/installers/lr/sdk/2023/cross_platform/v5/doc/Lightroom%20Classic%20SDK%20Guide_1670563540.pdf)
- The HTML reference actually opened is `https://lrc.mcor.dev/`, titled “Adobe® Photoshop® Lightroom® Classic SDK.” It is not `adobe.com`. On pages opened from it, the newest “First supported” lines found were version 14.3 (`LrApplication.shutdown`, `LrSelection.removeFromCatalog`). `catalog:deleteAllEmptyMasks` is “version 14.0 of the Lightroom Classic SDK.” `photo:updateAISettings` is “version 13.3.” — [SDK index](https://lrc.mcor.dev/); [LrApplication](https://lrc.mcor.dev/modules/LrApplication.html); [LrSelection](https://lrc.mcor.dev/modules/LrSelection.html); [LrCatalog](https://lrc.mcor.dev/modules/LrCatalog.html); [LrPhoto](https://lrc.mcor.dev/modules/LrPhoto.html)
- Adobe help navigation on the Classic vs ecosystem comparison, “Last updated on Feb 20, 2026,” includes a troubleshooting link titled “Denoise is not working in Lightroom Classic version 15.3 and earlier.” That shows Adobe’s help site, as fetched, is talking about Classic 15.3. The opened API mirror’s highest stamp found was 14.3. — [Feature comparison](https://helpx.adobe.com/lightroom-classic/kb/lightroom-feature-comparison.html)

### Inferences
- Verdicts of “documents support” mean the symbol or parameter name appears on a page that was opened. Verdicts of “silent” mean it was not found on those pages, not that a newer console-only SDK is proven empty.
- The 2022 Programmers Guide describes export, publish, metadata, UI, and web engines. Masking, color-grading parameter names, snapshots-as-currently-listed, and `LrUndo` come from the HTML reference, not from that older guide’s chapter list.

### Gaps
- The current official API Reference HTML inside the SDK zip from the Adobe developer console was not downloaded. Anything added after the 14.3 stamps in the mcor.dev mirror is unseen.
- Forum posts and third-party GitHub command lists were not treated as proof of an SDK method.

## 1. Read and write develop settings, including Exposure, Contrast, Highlights, Shadows, HSL, and color grading

### Takeaway
The SDK documents read and write of those slider names through `LrDevelopController.getValue` / `setValue`, and documents a settings-table read/write on `LrPhoto`, with an explicit experimental-API warning. Color-grading names such as `SplitToningShadowHue` and `ColorGradeMidtoneHue` are in the controller parameter list. The enumerated `photo:getDevelopSettings()` member list includes the split-toning names and the HSL names, and does not list the `ColorGrade*` names.

### Cited Findings
- `LrDevelopController` “provides functions for controlling the Develop module.” Functions that take a `param` string “will accept any of the following Develop parameter names.” The `adjustPanel` list includes `"Exposure"`, `"Highlights"` (annotated “controls Recovery in Version 1 and Version 2”), `"Shadows"` (annotated “controls Fill Light in Version 1 and Version 2”), and `"Contrast"`. — [LrDevelopController](https://lrc.mcor.dev/modules/LrDevelopController.html)
- The same parameter block’s `mixerPanel` lists HSL names per color: `SaturationAdjustmentRed` through `SaturationAdjustmentMagenta`, `HueAdjustmentRed` through `HueAdjustmentMagenta`, and `LuminanceAdjustmentRed` through `LuminanceAdjustmentMagenta`, for Red, Orange, Yellow, Green, Aqua, Blue, Purple, and Magenta. — [LrDevelopController](https://lrc.mcor.dev/modules/LrDevelopController.html)
- The same block’s `colorGradingPanel` lists `"SplitToningShadowHue"`, `"SplitToningShadowSaturation"`, `"ColorGradeShadowLum"`, `"SplitToningHighlightHue"`, `"SplitToningHighlightSaturation"`, `"ColorGradeHighlightLum"`, `"ColorGradeMidtoneHue"`, `"ColorGradeMidtoneSat"`, `"ColorGradeMidtoneLum"`, `"ColorGradeGlobalHue"`, `"ColorGradeGlobalSat"`, `"ColorGradeGlobalLum"`, `"SplitToningBalance"`, and `"ColorGradeBlending"`. — [LrDevelopController](https://lrc.mcor.dev/modules/LrDevelopController.html)
- `LrDevelopController.getValue(param)` “Gets the value of a Develop adjustment for the current photo.” `LrDevelopController.setValue(param, value, withClippingOn)` “Sets the value of a Develop adjustment for the current photo.” Both say “Must be called while the Develop module is active” and “First supported in version 6.0 of the Lightroom SDK.” `setValue` adds: “Temperature adjustment is logarithmic for RAW and DNG images, rest all are linear.” — [LrDevelopController](https://lrc.mcor.dev/modules/LrDevelopController.html)
- `photo:getDevelopSettings()` “Retrieves the current develop settings for this photo.” “First supported in version 3.0.” It “Must be called from within a task started using `LrTasks`.” The page warns: “The develop settings APIs are considered experimental. You should not depend on the contents of the settings table remaining compatible in future versions of Lightroom. The definitive list is the one shown in the UI.” — [LrPhoto](https://lrc.mcor.dev/modules/LrPhoto.html)
- The enumerated `getDevelopSettings()` members include `Exposure`, `Contrast`, `Shadows`, `SaturationAdjustmentRed` (and the other seven HSL saturation colors), `HueAdjustmentRed` (and the other hue colors), `LuminanceAdjustmentRed` (and the other luminance colors), `SplitToningBalance`, `SplitToningHighlightHue`, `SplitToningHighlightSaturation`, `SplitToningShadowHue`, and `SplitToningShadowSaturation`. SDK 4.0 additions on that list include `Exposure2012`, `Contrast2012`, `Highlights2012`, `Shadows2012`, and `Whites2012`. The opened enumeration does not include `ColorGradeMidtoneHue` or the other `ColorGrade*` names. Two names are printed with apparent typos: `HueAdjustmentMagenha` and `LuminanceAdjustmentAque`. — [LrPhoto](https://lrc.mcor.dev/modules/LrPhoto.html)
- `photo:applyDevelopSettings(settings, optHistoryName, optFlattenAutoNow)` “apply develop settings to an image.” “First supported in version 6.0.” The caller “must ensure that the photo exists and it is an image not a video.” `settings` is a “table of settings to be applied.” `optHistoryName` is an optional “name of the history step.” — [LrPhoto](https://lrc.mcor.dev/modules/LrPhoto.html)
- `LrDevelopPreset:getSetting()` repeats the experimental warning and lists an older settings-member set that includes `Exposure`, `Contrast`, `Shadows`, `SplitToningShadowHue`, and `SplitToningHighlightHue`, and does not list `ColorGradeMidtoneHue`. Its HSL names use a different plural style (`HueAdjustmentReds`, `SaturationAdjustmentBlues`) than `LrDevelopController`. — [LrDevelopPreset](https://lrc.mcor.dev/modules/LrDevelopPreset.html)

### Inferences
- Writing Exposure, Contrast, Highlights, Shadows, per-color HSL, and the named color-grading / split-toning parameters is documented for the current Develop photo via `setValue`, because those strings are in the controller’s accepted parameter list.
- Reading them back is documented via `getValue` for any name in that list. Reading them from `getDevelopSettings()` is documented for Exposure, Contrast, Shadows, the HSL names, and the `SplitToning*` names. `ColorGradeMidtoneHue` was not in the enumerated settings-table members on the page opened, so a plugin that only trusts that member list is not shown those color-grade keys, even though the controller accepts them.
- `applyDevelopSettings` documents writing a settings table and naming the history step. It does not publish a separate allowed-key list; the experimental warning points at the UI as the definitive list.
- `setValue` / `getValue` are limited to the active Develop module and “the current photo,” not an arbitrary catalog photo passed by id.

### Gaps
- Whether `applyDevelopSettings` accepts `ColorGradeMidtoneHue` inside the settings table is not stated on the page opened.
- The `getDevelopSettings()` list may be stale relative to the controller parameter list. The page itself says not to depend on the table remaining compatible.

## 2. Create a develop snapshot or history state before an edit, and restore it

### Takeaway
The SDK documents creating, listing, applying, and deleting develop snapshots, and it documents undo/redo of the last history state. It does not document an API that lists arbitrary history steps and restores a chosen step. Product help describes snapshots and the History panel as Develop UI features.

### Cited Findings
- `photo:createDevelopSnapshot(snapshotName, updateInPlace)` “Creates a develop snapshot of this photo.” It “Must be called from within a `catalog:withWriteAccessDo` or `catalog:withProlongedWriteAccessDo` gate.” “First supported in version 3.0.” `updateInPlace` true “update[s] the snapshot in place, if one already exists with this name.” Returns true on success, or false “if a snapshot with this name already exists and was not updated.” — [LrPhoto](https://lrc.mcor.dev/modules/LrPhoto.html)
- `photo:getDevelopSnapshots()` “Get all the snapshots of the photo.” “First supported in version 3.2.” Returns “a table of tables, one for each snapshot. Each snapshot entry contains snapshotID, name and id_global.” — [LrPhoto](https://lrc.mcor.dev/modules/LrPhoto.html)
- `photo:applyDevelopSnapshot(id)` “Applies a snapshot to the photo.” “First supported in version 3.2.” `id` is the “ID of the snapshot to be applied.” `photo:deleteDevelopSnapshot(id)` “Deletes a snapshot of the photo.” “First supported in version 5.0.” — [LrPhoto](https://lrc.mcor.dev/modules/LrPhoto.html)
- `photo:applyDevelopSettings` takes optional `optHistoryName`, “name of the history step.” — [LrPhoto](https://lrc.mcor.dev/modules/LrPhoto.html)
- `LrDevelopController.startTracking(param)` “Temporarily puts the Develop module into its tracking state, causing faster, lower-quailty redraw and preventing history states from being generated.” `stopTracking` “Causes Develop module to exit its tracking state immediately, creating a single history state for all changes that were made to the parameter that was being tracked.” Both “Must be called while the Develop module is active” and were “First supported in version 6.0.” — [LrDevelopController](https://lrc.mcor.dev/modules/LrDevelopController.html)
- `LrUndo` “provides access to undo/redo commands.” `LrUndo.undo()` “Undoes the last history state.” `LrUndo.redo()` “Redoes the last undone history state.” `canUndo` / `canRedo` report whether the command is enabled. All four are “First supported in version 6.0 of the Lightroom SDK.” — [LrUndo](https://lrc.mcor.dev/modules/LrUndo.html)
- Adobe help, Develop module options: “you can name and save any state of a photo as a snapshot.” “All the settings for the selected history state are recorded in the snapshot.” The History panel “saves that adjustment as a state.” “In the History panel, select a state to reapply it to the photo or to save it as a snapshot.” The fetched page does not show a “last updated” date. — [Develop module options](https://helpx.adobe.com/lightroom-classic/desktop/process-and-develop-photos/develop-module-options.html)
- A 2022 Adobe community bug, “P: SDK: Document LrPhoto snapshot methods,” reported that `getDevelopSnapshots`, `applyDevelopSnapshot`, and `deleteDevelopSnapshot` were undocumented in the LR 11 SDK. A follow-up on that thread said the LR 11.3 SDK documents them. Community report, not an SDK page. The methods are present on the `LrPhoto` page opened for this research. — [Community thread](https://community.adobe.com/bug-reports-674/p-sdk-document-lrphoto-snapshot-methods-663151)

### Inferences
- “Create a snapshot before an edit, then restore it” is documented: `createDevelopSnapshot`, then later `applyDevelopSnapshot` with the stored id.
- “Create a history state, then undo” is partly documented: `applyDevelopSettings` can name the history step, `startTracking` / `stopTracking` group changes into one history state, and `LrUndo.undo` restores only the last history state. A plugin cannot, from the pages opened, pick an older history row the way the History panel can.
- The help page places both snapshots and history in the Develop module UI. The SDK snapshot calls are on `LrPhoto` and do not say the Develop module must be active. `LrUndo`’s page does not say which module must be active.

### Gaps
- No symbol was found that returns the history-step list or restores a history step by id. `LrUndo.undo` is only “the last history state.”
- The opened `applyDevelopSnapshot` entry does not repeat the write-access gate that `createDevelopSnapshot` requires. Whether apply must also run inside `withWriteAccessDo` is not stated there.

## 3. requestJpegThumbnail or an equivalent preview after a settings change

### Takeaway
`photo:requestJpegThumbnail` is documented and can trigger a render when the preview system lacks that size. The text does not say the JPEG includes a develop change that was just written, and it does not describe a second vision pass. Export rendering is a separate, documented way to have Classic’s engine write a file.

### Cited Findings
- `photo:requestJpegThumbnail(width, height, callback)` “Requests a JPEG thumbnail of this photo. If the preview system does not already contain a preview for this photo at the requested size, one will be rendered. Request sizes are treated as minimums; the preview that is returned may be larger. If both dimensions are specified, the smallest preview that satisfies either one is returned.” It “must be called from within an asynchronous task started using `LrTasks`.” “First supported in version 5.0.” The callback “receives either one or two parameters: the JPEG data if it is successful, or nil and an error string if it fails.” The return value is a request object: “Hold a reference to this object until your callback is called, then release it.” — [LrPhoto](https://lrc.mcor.dev/modules/LrPhoto.html)
- The Programmers Guide’s export-filter chapter says that after filters intercept rendition requests, “the requests are finally passed to Lightroom Classic's built-in rendering engine.” That chapter is about export and post-process filters, not about a Develop preview hook. — [SDK Programmers Guide PDF](https://ioconsolerykerprodcdn.azureedge.net/static/installers/lr/sdk/2023/cross_platform/v5/doc/Lightroom%20Classic%20SDK%20Guide_1670563540.pdf)
- The SDK index lists `LrExportSession` and `LrExportRendition` as export rendition classes. Those class pages were not opened. — [SDK index](https://lrc.mcor.dev/)
- No function whose name contains render, preview, or thumbnail, other than `requestJpegThumbnail`, was found on the `LrPhoto` or `LrDevelopController` pages opened. `LrDevelopController` was searched for a preview/render symbol and none was found in the function list that was read.

### Inferences
- A plugin can ask for JPEG bytes of an `LrPhoto`. The documented trigger for a new render is “the preview system does not already contain a preview … at the requested size,” which is a cache-size condition, not “develop settings just changed.”
- Using that call as a guaranteed post-edit frame for a second vision model is not what the sentence documents. A cached preview of an older state would satisfy the wording.
- A full export through the built-in rendering engine is the documented path that is tied to producing a rendered file from current export settings. It is a different workflow from `requestJpegThumbnail`.

### Gaps
- The page does not state maximum width/height, color space, whether the JPEG is pre- or post-crop, or whether virtual-copy settings are what get rendered.
- `LrExportRendition` / `LrExportSession` method lists were not opened, so no export-rendition symbol is quoted beyond the guide’s description of the built-in rendering engine.

## 4. Apply an adaptive preset that uses Select Subject, Sky, Background, or similar AI masks, including a user .xmp

### Takeaway
The SDK documents creating an AI mask with `LrDevelopController.createNewMask("aiSelection", subtype)` for subject, sky, background, and related subtypes, and it documents applying an existing develop preset with an `updateAISettings` flag. It does not use the product name “adaptive preset,” and the preset class page that was opened has no method that loads an arbitrary `.xmp` file from disk. Adobe help describes Adaptive Presets and batch AI masks as Develop UI actions.

### Cited Findings
- `LrDevelopController.createNewMask(maskType, maskSubtype)` “Create a new mask.” “Must be called while the Develop module is active.” “First supported in version 11.0 of the Lightroom SDK.” `maskType` is one of `"brush"`, `"gradient"`, `"radialGradient"`, `"rangeMask"`, `"aiSelection"`. `maskSubtype`, “only used when maskType is `rangeMask` or `aiSelection`,” is one of `"color"`, `"luminance"`, `"depth"`, `"subject"`, `"sky"`, `"background"`, `"objects"`, `"people"`, `"landscape"`. The same subtype list is documented for `addToCurrentMask`, `intersectWithCurrentMask`, and `subtractFromCurrentMask`. — [LrDevelopController](https://lrc.mcor.dev/modules/LrDevelopController.html)
- `photo:applyDevelopPreset(preset, plugin, presetAmount, updateAISettings)` “Applies a develop preset to this photo,” inside a write-access gate. “First supported in version 3.0.” `preset` is an `LrDevelopPreset`. `updateAISettings` is an optional boolean: “Specifies if AI Settings should be auto updated after applying the preset. Default is false.” — [LrPhoto](https://lrc.mcor.dev/modules/LrPhoto.html)
- `photo:updateAISettings()` “Updates AI Settings for this photo,” inside a write-access gate. “First supported in version 13.3 of the Lightroom Classic SDK.” The page does not define which features “AI Settings” includes. — [LrPhoto](https://lrc.mcor.dev/modules/LrPhoto.html)
- `photo:getDevelopSettings()` lists, “first provided in version 11.0,” `EnableMaskGroupBasedCorrections` (boolean) and `MaskGroupBasedCorrections` (table). It does not document the table’s fields. — [LrPhoto](https://lrc.mcor.dev/modules/LrPhoto.html)
- `LrApplication.developPresetFolders()` “Retrieves all defined develop preset folders.” `LrApplication.developPresetByUuid(uuid)` “Retrieves a develop preset from its unique identifier.” `LrDevelopPreset:getFile()` “Retrieves the file path of this preset.” `preset:getSetting()` returns the settings table. The functions listed on the opened `LrDevelopPreset` page are only `getFile`, `getName`, `getParent`, `getSetting`, `getUuid`, and `type`. No load-from-path or `.xmp` symbol appears there. — [LrApplication](https://lrc.mcor.dev/modules/LrApplication.html); [LrDevelopPreset](https://lrc.mcor.dev/modules/LrDevelopPreset.html)
- `LrApplication.addDevelopPresetForPlugin(plugin, presetName, presetValue)` “Adds a preset hidden within a plug-in.” `presetValue` is “The setting values for the preset. For allowed values, see `LrDevelopPreset:getSetting`.” The same paragraph says “To apply the preset, use `LrPhoto:applyDevelopPresetFromPlugin`.” That symbol was not found on the `LrPhoto` page opened, which documents `photo:applyDevelopPreset` instead. — [LrApplication](https://lrc.mcor.dev/modules/LrApplication.html); [LrPhoto](https://lrc.mcor.dev/modules/LrPhoto.html)
- Adobe help, Masking tool: “Select Subject allows you to automatically select the subject in the photo.” The batch section, “Applicable from Lightroom Classic 11.4 (June 2022 release),” says Select Subject, Select Sky, Select Background, Select Objects, and Select People “can now be applied to multiple photos” via Copy, Paste, Sync, and Auto-sync. It also says: “From the Presets panel on the left, open and apply any AI mask from User Presets. You can also use one of the Adaptive Presets for Subject, Sky and Portrait.” — [Masking tool](https://helpx.adobe.com/lightroom-classic/desktop/process-and-develop-photos/masking.html)
- The Classic vs ecosystem comparison, last updated Feb 20, 2026, lists as Classic editing features, with “Yes” in the Classic column of the table that rendered: Masking - Select Subject, Select Sky, Select Objects, Select People, Select Background, Select Landscape, and “Adaptive Presets.” — [Feature comparison](https://helpx.adobe.com/lightroom-classic/kb/lightroom-feature-comparison.html)
- The Programmers Guide’s menu/export discussion identifies Lightroom preset files for export with “the .lrtemplate extension.” It does not, in the passages searched, describe develop `.xmp` presets. — [SDK Programmers Guide PDF](https://ioconsolerykerprodcdn.azureedge.net/static/installers/lr/sdk/2023/cross_platform/v5/doc/Lightroom%20Classic%20SDK%20Guide_1670563540.pdf)
- Community report, unverified: an Adobe community thread shows the call `LrDevelopController.createNewMask('aiSelection', 'people')` and a reply that `photo:applyDevelopSettings()` can carry person-mask settings read from `photo:getDevelopSettings()`, with a reported behavior that a person mask becomes an “All People” mask on the target. — [Changes to the Lightroom 12.0 SDK](https://community.adobe.com/questions-675/changes-to-the-lightroom-12-0-sdk-965518)

### Inferences
- A plugin can ask the Develop module to create a Select Subject, Select Sky, or Select Background mask by the documented subtype strings. The page does not say the call blocks until the mask has been computed, and it does not say local adjustments are applied in the same call.
- A preset that is already in Classic’s preset folders can be retrieved as an `LrDevelopPreset` and applied with `applyDevelopPreset`. Passing `updateAISettings = true` is the documented switch “if AI Settings should be auto updated.” The docs do not say that flag recomputes Select Subject / Sky / Background.
- Applying a loose `.xmp` the user has on disk, but that Classic has not already loaded as a preset, was not found. `getFile` returns the path of a preset object the catalog already has. `addDevelopPresetForPlugin` takes a Lua settings table, not a file path.
- “Adaptive preset” is a help-page / feature-comparison name. That phrase was not found on the SDK pages opened.

### Gaps
- `LrDevelopPresetFolder` was not opened, so a folder method that imports an `.xmp` cannot be ruled out from a page that was not read. It was not on the preset class page or the `LrApplication` preset functions that were read.
- The contents of `MaskGroupBasedCorrections` are undocumented on the page opened, so whether a plugin can round-trip an AI mask through `applyDevelopSettings` is not specified there.
- `applyDevelopPresetFromPlugin`, named from `LrApplication`, was not found on `LrPhoto`.

## 5. Create a virtual copy, apply settings to it, and render its preview without changing the master

### Takeaway
The SDK documents creating virtual copies, treating each copy as its own `LrPhoto`, and applying develop settings to a specific photo object. `requestJpegThumbnail` is a method on that same class. The pages do not explicitly say the master is left unchanged, and they do not explicitly say the thumbnail is rendered from the copy’s settings rather than a shared preview.

### Cited Findings
- `LrPhoto` “represents a single photo or virtual copy in Lightroom's active catalog.” — [LrPhoto](https://lrc.mcor.dev/modules/LrPhoto.html)
- `catalog:createVirtualCopies(copyName)` “Creates a virtual copy for each of the currently selected photos and videos.” It “must be called from within an asynchronous task started using `LrTasks`.” “After this call, the new virtual copies will be selected.” “First supported in version 5.0.” `copyName` is an optional “name to apply to each of the virtual copies.” Returns “(array of `LrPhoto`) The new virtual copies.” — [LrCatalog](https://lrc.mcor.dev/modules/LrCatalog.html)
- `photo:getRawMetadata` keys include `countVirtualCopies` (“Zero if this photo is itself a virtual copy”), `virtualCopies` (“All virtual copies of this photo”), `masterPhoto` (“The master photo from which this virtual copy is derived”), and `isVirtualCopy`. `photo:setRawMetadata` accepts `copyName`, “The name associated with this copy.” — [LrPhoto](https://lrc.mcor.dev/modules/LrPhoto.html)
- `photo:applyDevelopSettings` applies a settings table to “an image” identified by that `LrPhoto` call. `LrDevelopController.setValue` sets a value “for the current photo” and requires the Develop module to be active. — [LrPhoto](https://lrc.mcor.dev/modules/LrPhoto.html); [LrDevelopController](https://lrc.mcor.dev/modules/LrDevelopController.html)
- `requestJpegThumbnail` is documented on `LrPhoto`, quoted in section 3. — [LrPhoto](https://lrc.mcor.dev/modules/LrPhoto.html)
- The feature comparison, last updated Feb 20, 2026, lists “Create copies” as “Virtual” for Lightroom Classic and “Duplicate” for the Lightroom ecosystem. — [Feature comparison](https://helpx.adobe.com/lightroom-classic/kb/lightroom-feature-comparison.html)

### Inferences
- The documented sequence is: select the master, `createVirtualCopies`, then call `applyDevelopSettings` on one of the returned `LrPhoto` objects rather than on `masterPhoto`. Because the settings call is on a photo object, the API shape is per photo, which is the basis for editing the copy rather than the master. The reference never states “does not modify the master.”
- After `createVirtualCopies`, “the new virtual copies will be selected.” A following `LrDevelopController.setValue` hits “the current photo,” which is a weaker target than `applyDevelopSettings` on a specific returned object when more than one copy was created.
- A virtual copy is an `LrPhoto`, so `requestJpegThumbnail` is available on it. Section 3’s cache wording still applies: the docs do not promise a freshly rendered view of the copy’s new settings.

### Gaps
- No sentence was found that previews of a virtual copy are stored separately from the master.
- `createVirtualCopies` as opened does not say it must run inside `withWriteAccessDo`, unlike `createDevelopSnapshot`. Whether a write gate is still required in practice is not stated.

## 6. AI Denoise, Super Resolution, and HDR merge

### Takeaway
On the SDK pages opened, AI Denoise, Super Resolution, and Photo Merge HDR are not SDK methods. Adobe help documents them as Classic desktop commands. The settings table does document HDR edit/output fields (`HDREditMode` and related SDR keys), which are not the merge command. Symbols such as `setEnhance` were not found.

### Cited Findings
- The opened `LrDevelopController` page was searched for Denoise, Super Resolution, Enhance, Photo Merge, and `setEnhance`. No matches. — [LrDevelopController](https://lrc.mcor.dev/modules/LrDevelopController.html)
- `photo:getDevelopSettings()` lists, “first provided in version 13.0 of the Lightroom Classic SDK,” `HDREditMode`, `HDRMaxValue`, `SDRBrightness`, `SDRContrast`, `SDRClarity`, `SDRHighlights`, `SDRShadows`, `SDRWhites`, and `SDRBlend`. The page does not describe a merge of several exposures. — [LrPhoto](https://lrc.mcor.dev/modules/LrPhoto.html)
- Adobe help, “Improve image quality using Enhance,” “Last updated on May 1, 2026”: “Enhance provides a set of features such as Denoise, Raw Details and Super Resolution.” “In the Detail panel, select Denoise.” “In the Detail panel, select Super Resolution.” Super Resolution “will have 2x the width and 2x the height of the original image.” The page says these features “now run in the background” and “You can enhance an image only once.” It does not mention the Lua SDK. — [Enhance](https://helpx.adobe.com/lightroom-classic/desktop/process-and-develop-photos/enhance-details.html)
- Adobe help, “HDR photo merge in Lightroom Classic,” “Updated in Lightroom Classic CC 7.4 (June 2018 release)”: “Select Photo > Photo Merge > HDR or press Ctrl+H.” The steps are a preview dialog (Auto Align, Auto Tone, deghosting) and a Merge button. No SDK symbol is on the fetched page. — [HDR photo merge](https://helpx.adobe.com/lightroom-classic/help/hdr-photo-merge.html)
- The feature comparison, last updated Feb 20, 2026, lists “AI-powered Denoise,” “HDR Edit and Output,” and “Create an HDR file” as Classic product rows. In the editing table that rendered with cell text, “AI-powered Denoise” and “HDR Edit and Output” are “Yes” for Classic. The Photo Merge table’s Yes/No cells did not survive the fetch. — [Feature comparison](https://helpx.adobe.com/lightroom-classic/kb/lightroom-feature-comparison.html)
- Third-party report, unverified, and not an Adobe SDK page: a GitHub command reference claims a Denoise call via “SDK 15.3+ `setEnhance`,” and another project’s contributing notes say `EnableAIDenoise` can be accepted while “Enhance → Denoise…” “cannot be programmatically invoked” as of “15.3.” `setEnhance` and `EnableAIDenoise` were not on the `LrDevelopController` page opened. — [lightroom-ai-bridge command reference](https://github.com/aslanoov/lightroom-ai-bridge/blob/main/docs/COMMAND-REFERENCE.md); [lightroom-py CONTRIBUTING](https://github.com/drshy-org/lightroom-py/blob/main/CONTRIBUTING.md)

### Inferences
- As of the reference that was opened, Denoise, Super Resolution, and HDR merge are product UI features, not documented Lua calls. Help places Denoise and Super Resolution in the Detail panel and HDR merge under Photo > Photo Merge > HDR.
- `HDREditMode` and the `SDR*` keys are documented develop settings for HDR edit/output of a photo. That is a different feature from merging a bracket into a new HDR file.
- Because the opened reference tops out at “first supported in version 14.3” and Adobe help already discusses Classic 15.3, a newer SDK could have added Enhance calls that this research did not see. The third-party `setEnhance` claim is not proof, and the symbol was not found in the docs opened.

### Gaps
- The current SDK 15.x API Reference, if Adobe has shipped one, was not opened.
- No page opened says “these features are intentionally unavailable to plug-ins.” Silence plus a UI-only help article is the evidence, not an Adobe prohibition sentence.

## 7. Keywords, star rating, pick flag, title, and caption

### Takeaway
The SDK documents all five. Ratings, pick flag, title, and caption are `photo:setRawMetadata` keys, with selection-scoped helpers for rating and flags. Keywords are `LrKeyword` objects created on the catalog and added to the photo.

### Cited Findings
- `photo:setRawMetadata(key, value)` “Sets metadata for this photo” inside `catalog:withWriteAccessDo` or `withProlongedWriteAccessDo`. “First supported in version 2.0.” Documented keys include `rating` (“nil or number of stars”), `title` (“The title of this photo”), and `caption` (“The caption for this photo”). “The following items are first supported in version 4.0”: `pickStatus` “1 for flag status 'picked', 0 for 'not set', -1 for 'rejected'.” — [LrPhoto](https://lrc.mcor.dev/modules/LrPhoto.html)
- `photo:getRawMetadata` / `getFormattedMetadata` document readback of `rating`, `title`, `caption`, and `keywords` (“array of `LrKeyword`”). `pickStatus` is documented on `getRawMetadata` as “1 if the photo's flag status is 'picked', 0 if the photo's flag is not set, -1 if the photo's flag status is 'rejected'.” — [LrPhoto](https://lrc.mcor.dev/modules/LrPhoto.html)
- `LrSelection.setRating(rating)` “Sets the rating of the selection.” `rating` is “A number between 0 and 5.” `LrSelection.flagAsPick`, `flagAsReject`, and `removeFlag` set or clear the flag. The namespace intro says these commands “behave just like the main menu commands: if the grid view is currently visible then they apply to all selected photos, otherwise they only apply to the active photo.” “First supported in version 6.0.” — [LrSelection](https://lrc.mcor.dev/modules/LrSelection.html)
- `catalog:createKeyword(keywordName, synonyms, includeOnExport, parent, returnExisting)` “Creates a keyword in this catalog. This is the equivalent of creating a keyword in the KeywordList panel.” It must run inside a write-access gate. “First supported in version 3.0.” `returnExisting` true returns an existing keyword with the same name and parent; that parameter “is first supported in Lightroom 4.0.” — [LrCatalog](https://lrc.mcor.dev/modules/LrCatalog.html)
- `photo:addKeyword(keyword)` “Adds a keyword to this photo” inside a write-access gate. The argument is an `LrKeyword`, not a string. “This call can be used within the same `catalog:with___WriteAccessDo` call that created this keyword.” `photo:removeKeyword(keyword)` removes it. Both “First supported in version 3.0.” — [LrPhoto](https://lrc.mcor.dev/modules/LrPhoto.html)
- The SDK index lists the class `LrKeyword`: “access to a Lightroom keyword, any contained keywords, and photos associated with the keyword.” The class page was not opened. — [SDK index](https://lrc.mcor.dev/)

### Inferences
- A plugin can set stars, pick/reject/none, title, and caption on a known `LrPhoto` without going through the Develop module. `LrSelection` covers rating and flags for the current selection only, and does not list title or caption.
- Keywords are not a string array on `setRawMetadata`. The documented write path is create-or-reuse an `LrKeyword`, then `addKeyword`. Hierarchical keywords are implied by the `parent` argument on `createKeyword`.

### Gaps
- `LrKeyword` methods for renaming or reading the keyword path were not opened.
- The pages do not state a maximum caption length or what happens if `rating` is outside 0–5 on `setRawMetadata`. `LrSelection.setRating` does say 0 to 5.

## 8. Invoke a menu command or keyboard shortcut inside Classic

### Takeaway
The SDK documents adding the plug-in’s own Plug-in Extras menu items. It does not document a general “run this Classic menu command” or “send this shortcut” function. A fixed set of Library-style commands exists on `LrSelection`, and a fixed set of Develop tool openers exists on `LrDevelopController`.

### Cited Findings
- Programmers Guide, “What you can do” style overview: “Menu customization: Plug-ins can add new menu items in the Plug-in Extras menu.” `LrExportMenuItems`, `LrLibraryMenuItems`, and `LrHelpMenuItems` “allow you to add new script-defined menu items to the Plug-in Extras submenus” of File, Library, and Help. — [SDK Programmers Guide PDF](https://ioconsolerykerprodcdn.azureedge.net/static/installers/lr/sdk/2023/cross_platform/v5/doc/Lightroom%20Classic%20SDK%20Guide_1670563540.pdf)
- Guide section “Defining menu items for a plug-in” (chapter 2, pages 34–35 in that PDF): a menu item table has `title`, `file` (Lua file “executed when the menu item is chosen”), and optional `enabledWhen`. “In Windows, the title string can include an ampersand (`&`) character in the name to make the following character a keyboard shortcut or accelerator that invokes that item. (This feature is not available in macOS…).” The example creates “a command in the File > Plug-in Extras menu” that runs the plug-in’s own script, not a built-in Classic command. — [SDK Programmers Guide PDF](https://ioconsolerykerprodcdn.azureedge.net/static/installers/lr/sdk/2023/cross_platform/v5/doc/Lightroom%20Classic%20SDK%20Guide_1670563540.pdf)
- The SDK index opened lists no namespace named `LrMenu`, `LrCommands`, or similar. Namespaces that do exist include `LrSelection`, `LrApplication`, `LrApplicationView`, `LrDevelopController`, `LrSlideshow`, and `LrTether`. — [SDK index](https://lrc.mcor.dev/)
- `LrApplication` functions opened are catalog, version, preset, backup, and `shutdown` (“Quits the Lightroom Application,” “First supported in version 14.3”). No execute-menu, send-keys, or shortcut function is in that summary. — [LrApplication](https://lrc.mcor.dev/modules/LrApplication.html)
- `LrSelection` “provides access to the selection-based commands” and says they “behave just like the main menu commands,” then lists specific calls: select all/none/inverse, next/previous photo, rating, flags, color labels, `removeFromCatalog`. There is no function that takes a menu path or shortcut string. — [LrSelection](https://lrc.mcor.dev/modules/LrSelection.html)
- `LrDevelopController` documents specific tool entry points rather than arbitrary menus, including `goToMasking` (“Open Masking for the current photo”), `goToRemove`, `editInPhotoshop` (“Edit the current photo in Photoshop”), and the graduated/radial filter openers. Those were in the summary of the page opened. A general menu invoker was not in that summary. — [LrDevelopController](https://lrc.mcor.dev/modules/LrDevelopController.html)
- `LrApplicationView` is described on the index as access to “the active module, main view mode, secondary view mode, and zoom level.” Its method page was not opened. — [SDK index](https://lrc.mcor.dev/)

### Inferences
- A plugin can add its own commands under Plug-in Extras and, on Windows only, give that new item an accelerator. That is the opposite of invoking Photo > Photo Merge > HDR or a built-in shortcut.
- Where Adobe wanted a menu-equivalent, it added a named function (`LrSelection.flagAsPick`, `LrDevelopController.goToMasking`). Features that only appear as help-page menu steps, such as Photo > Photo Merge > HDR, have no matching symbol on the pages opened.

### Gaps
- `LrApplicationView` was not opened, so a view-switch method is not quoted. The index description does not mention menu commands or shortcuts.
- Undocumented private globals are outside this research. None were found in the public pages opened, and none are asserted.

## Plugin language, and whether cloud Lightroom loads Classic plug-ins

### Takeaway
Adobe states that Classic plug-ins are written in Lua 5.1.4 and packaged as `.lrplugin` folders. Adobe’s cloud Lightroom FAQ says Lightroom does not currently support third-party plug-ins. That FAQ does not use the word `.lrplugin`.

### Cited Findings
- Developer landing page: “Build plug-ins in Lua, the scripting language built into Lightroom.” — [Creative Cloud - Lightroom Classic](https://developer.adobe.com/lightroom-classic/)
- Programmers Guide, “The Lua language”: “Lightroom Classic uses version 5.1.4 of the Lua language.” Sample plug-ins in the same guide use the `.lrdevplugin` suffix (`flickr.lrdevplugin`, `helloworld.lrdevplugin`). — [SDK Programmers Guide PDF](https://ioconsolerykerprodcdn.azureedge.net/static/installers/lr/sdk/2023/cross_platform/v5/doc/Lightroom%20Classic%20SDK%20Guide_1670563540.pdf)
- Adobe developer blog, 2022: “Lightroom Classic is also scriptable, and it’s possible to create Lightroom plugins. Scripts are written in Lua.” A typical plug-in is shown as `myLrCplugin.lrplugin` containing `info.lua` and other Lua files, installed with File > Plug-in Manager. — [Lightroom Classic Plugin Support for the Adobe Exchange](https://blog.developer.adobe.com/en/publish/2022/07/lightroom-classic-plugin-support-for-the-adobe-exchange-for-creative-cloud)
- Adobe help, “Lightroom | Common questions,” “Last updated on Aug 27, 2025,” in the Basics answers: “Yes; Lightroom has an 'Edit in Photoshop' feature. Lightroom doesn't currently support third-party plug-ins.” The fetched page dropped the question headings, so the answer text is what can be quoted. The page is the cloud Lightroom FAQ (`lightroom-cc`), not the Classic FAQ. It does not mention `.lrplugin`. — [Lightroom common questions](https://helpx.adobe.com/lightroom-cc/faq.html)
- The Classic vs ecosystem comparison, “Last updated on Feb 20, 2026,” has a section “External editors and plug-ins” with a row “Third-party plug-ins.” The Yes/No cells for that row did not come through in the fetch, so they are not quoted. — [Feature comparison](https://helpx.adobe.com/lightroom-classic/kb/lightroom-feature-comparison.html)
- Community report, unverified as an SDK source: Adobe staff replies on the Lightroom cloud ideas forum have said “Adobe Lightroom currently does not have support for plugins or extensions. Plugins are supported with Lightroom Classic.” — [Plugin support idea thread](https://community.adobe.com/t5/lightroom-ecosystem-cloud-based-ideas/p-3rd-party-plugin-support-for-lightroom-desktop-external-editors/idc-p/13722735)

### Inferences
- The official language statement for Classic plug-ins is Lua, and the Programmers Guide pins the version at Lua 5.1.4.
- Cloud Lightroom’s own FAQ is the Adobe page that says third-party plug-ins are unsupported. Combined with the Classic-only `.lrplugin` packaging docs, that is the Adobe basis for “cloud Lightroom does not load Classic plug-in packages.” The FAQ does not itself name the `.lrplugin` extension.

### Gaps
- The feature-comparison Yes/No cell for “Third-party plug-ins” was not recoverable from the fetched markdown, so that table is not used as the proof sentence.
- No Adobe page opened says the exact phrase “does not load .lrplugin packages.”
