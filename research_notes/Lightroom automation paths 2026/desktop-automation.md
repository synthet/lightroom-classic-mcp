# Cloud Lightroom desktop automation evidence

Research date: 2026-10-20. Scope: published evidence about driving the cloud Lightroom desktop app on Windows from outside the process. Lightroom Classic is a different product and is cited only where a source names it. No control tree and no shortcut were inferred.

The claim under test is: use Windows UI Automation first, then keyboard shortcuts, then OpenCV template matching, and never fixed coordinates, and that this is viable because Lightroom’s editing UI may or may not expose accessible controls.

## Does Adobe publish an accessibility map, plug-in SDK, UXP host, CEP host, or COM object for cloud Lightroom on Windows?

### Takeaway

Adobe’s September 2026 extensibility post says the CEP-to-UXP transition does not affect Lightroom. That sentence does not inventory Lightroom’s extension surface. The pages Adobe publishes for the cloud product describe REST services, and the Lua plug-in SDK page is for Lightroom Classic. No page found publishes an accessibility tree, a UXP host, a CEP host, or a COM automation object for the cloud Lightroom Windows app.

### Cited Findings

- Exact sentence from the 16 September 2026 Adobe developer blog post “Investing in the Future of Creative Cloud Extensibility: UXP Comes to Our Flagship Applications”: “This transition applies to Creative Cloud desktop flagship apps only; Acrobat, Adobe Express, and Lightroom aren’t affected.” The same section lists UXP status only for Media Encoder, Premiere, After Effects, InDesign, Illustrator, and Photoshop. It says CEP will no longer be included in “these apps” starting December 2029, and that ExtendScripts are not affected. Lightroom is not given a UXP beta date. — [Adobe developer blog, 2026-09](https://blog.developer.adobe.com/en/publish/2026/09/investing-in-the-future-of-creative-cloud-extensibility-uxp-comes-to-our-flagship-applications)
- An October 2026 Adobe Developers Live recap covers the CEP-to-UXP roadmap, Express connectors, and agent plans. The retrieved summary does not announce a Lightroom desktop plug-in host. — [Adobe developer blog, 2026-10](https://blog.developer.adobe.com/en/publish/2026/10/adobe-developers-live-2026-recap-cep-to-uxp-migration-express-connectors-and-what-we-publish-next)
- Adobe’s Lightroom (cloud) developer page, “Build applications that work with Lightroom,” describes the cloud service and says an application can streamline workflows “through RESTful endpoints.” It does not describe an in-process plug-in SDK, UXP, CEP, or COM server. — [developer.adobe.com/lightroom](https://developer.adobe.com/lightroom/)
- The Creative Cloud developer platform lists “Lightroom Services” as “Streamline photography workflows for customers with content in Lightroom, through RESTful APIs,” and lists “Lightroom Classic” separately as “Create effects, define presets and brushes, manipulate metadata, and much more in Lightroom.” — [developer.adobe.com/creative-cloud](https://developer.adobe.com/creative-cloud)
- The Lightroom Classic SDK page is titled “Unleash Lightroom Classic with Lua” and says plug-ins are built in Lua, the scripting language built into Lightroom, for export, publish, metadata, Plug-in Manager UI, and web-engine galleries. — [developer.adobe.com/lightroom-classic](https://developer.adobe.com/lightroom-classic/)
- Adobe’s July 2022 Exchange post says, in its FAQ: “Does this mean Lightroom will now support CEP? No, neither Lightroom nor Lightroom Classic have plans for CEP support.” And: “Will Lightroom support UXP in the future? Neither Lightroom nor Lightroom Classic have UXP support on their roadmaps at the time of this writing.” That statement is explicitly time-bounded to July 2022. — [Adobe developer blog, 2022-07](https://blog.developer.adobe.com/en/publish/2022/07/lightroom-classic-plugin-support-for-the-adobe-exchange-for-creative-cloud)
- Adobe documents a separate Lightroom cloud imaging API, with end of life on 31 July 2026, and tells customers to migrate to Photoshop API v2. That is a service API, not a desktop UI automation interface. — [Lightroom API deprecation](https://developer.adobe.com/firefly-services/docs/lightroom/getting-started/deprecation-announcement/)
- The November 2019 Accessibility Conformance Report for “Adobe Lightroom Windows v2.4.1” says evaluation included “manual inspection of Accessibility API output.” It is a VPAT-style conformance report. It does not publish an element tree, AutomationIds, or an Inspect.exe dump. — [Lightroom Windows v2.4.1 ACR](https://www.adobe.com/trust/accessibility/conformance/adobe-lightroom-win-2019-acr.html)

### Inferences

- What the September 2026 sentence proves: the CEP retirement schedule and the UXP rollout dates in that post do not apply to the product Adobe calls Lightroom. Lightroom is outside the set of flagship apps for which that post announces a UXP plug-in host.
- What it does not prove: that Lightroom has a UXP host, a CEP host, a COM object, an accessibility map, or no extensibility of any kind. “Aren’t affected” means this transition does not change Lightroom. The post does not say “Lightroom Classic,” so it also does not by itself settle Classic.
- The July 2022 “no CEP / no UXP on the roadmap” answers are the last explicit Adobe statements found on those hosts, and they were qualified with “at the time of this writing.” They are not renewed by the 2026 post.
- A published in-process automation API for the cloud desktop app was not found. The published cloud interfaces are REST services. Those can operate on cloud photos from outside the desktop process. They are not a published way to drive the local editing UI.
- Classic’s Lua SDK confirms only that Classic is the Lua product. It is not a host inside the cloud app.

### Gaps

- No Adobe page found publishes a COM ProgID, type library, or Windows automation object for cloud Lightroom. That is an absence after searching the developer portal and the 2022 and 2026 extensibility posts, not a proof that no private COM interface exists.
- The October 2026 recap was not read in full beyond the retrieved summary. A Lightroom-specific aside could exist further down that page.
- No later Adobe page was found that withdraws or renews the July 2022 “no UXP on the roadmap” sentence.

## Has anyone published what Inspect.exe or Accessibility Insights sees in cloud Lightroom on Windows in 2024–2026?

### Takeaway

No reputable 2024–2026 report, Adobe community thread, or accessibility writeup found here shows an Inspect.exe or Accessibility Insights tree for cloud Lightroom on Windows. The UI Automation approach is unmeasured.

### Cited Findings

- Searches for Lightroom combined with “UI Automation,” Inspect.exe, and Accessibility Insights did not return a Lightroom control-tree dump, community thread, or 2024–2026 accessibility writeup. The only hit that mentioned Accessibility Insights was an unrelated freelance job. — search conducted 2026-10-20; no matching URL to cite
- Adobe’s cloud Lightroom Windows conformance report remains “Adobe Lightroom Windows v2.4.1,” dated November 2019. Evaluation methods include assistive technology, keyboard-only use, native platform accessibility features, and “manual inspection of Accessibility API output.” Product description: “The cloud-based service for people who love photography.” — [Lightroom Windows v2.4.1 ACR](https://www.adobe.com/trust/accessibility/conformance/adobe-lightroom-win-2019-acr.html)
- That 2019 report, criterion 4.1.2 Name, Role, Value: “Does Not Support.” Remarks: “User interface components in most product functions do not provide programmatic name, role, or state information. Examples include: Icon buttons. Slider controls.” Criterion 2.1.1 Keyboard: “Does Not Support.” Remarks: “most controls do not receive keyboard focus,” with examples “Navigating content sequentially,” “Activating slider and popup menu controls,” and “Setting interface Text Size in Preferences dialog.” — [Lightroom Windows v2.4.1 ACR](https://www.adobe.com/trust/accessibility/conformance/adobe-lightroom-win-2019-acr.html)
- A third-party index of Adobe ACRs still lists “Adobe Lightroom Windows v2.4.1 Nov 2019” and “Adobe Lightroom Mac v2.4.1 Nov 2019” as the cloud desktop reports, and lists Lightroom Classic (Windows) as August 2023. It does not list a 2024–2026 cloud Lightroom Windows report. — [ACR Index, Adobe](https://acrindex.com/adobe/)
- Lightroom Classic (Windows) has a separate ACR dated August 2023. It is Classic, not the cloud app. It also says testing included inspection of Accessibility API output, and that most controls do not receive keyboard focus. It likewise publishes no element tree. — [Lightroom Classic Windows ACR](https://www.adobe.com/trust/accessibility/conformance/adobe-lightroom-classic-win-acr.html)
- Microsoft’s Inspect documentation says Inspect.exe can show the UI Automation tree, and that Inspect is a legacy tool. It does not mention Lightroom. — [Inspect objects](https://learn.microsoft.com/en-us/windows/win32/winauto/inspect-objects)
- Accessibility Insights for Windows can show a UIA tree and properties. Its documentation does not mention Lightroom. — [Accessibility Insights for Windows](https://www.accessibilityinsights.io/docs/windows/overview/)

### Inferences

- “UIA first” is an untested architecture for this app. Nobody has published the tree, so it is not known whether the 2026 editing UI exposes accessible controls.
- The November 2019 ACR is evidence that, for cloud Lightroom Windows v2.4.1, Adobe’s own Accessibility API inspection found most icon buttons and sliders without programmatic name, role, or state, and most controls without keyboard focus. It is seven years and many versions before 2026-10-20. It is not a tree, and it does not measure the current app. It also does not support treating UIA-first as known to be viable.
- OpenCV template matching, fixed screen coordinates, and any fallback order among those techniques are also unpublished for this app. The proposed order is a general Windows automation habit, not a Lightroom result.

### Gaps

- No 2024–2026 Inspect.exe or Accessibility Insights dump was found. Current exposure of the edit panel, Denoise control, sliders, and menus is unmeasured.
- The 2019 report does not say which Accessibility API (UIA versus MSAA), which Lightroom panels were sampled, or what the raw tree contained.
- Adobe’s public compliance index page was not fully fetched; the ACR Index is a third-party catalog and could lag an unlisted Adobe PDF.

## What is the cloud Lightroom desktop UI built with, and what does that imply for UI Automation?

### Takeaway

No Adobe document found names the UI toolkit of the cloud Lightroom desktop app. A 2026 third-party Wine port records Direct2D use when Lightroom CC opens its main window, a static import of a UI Automation API-set symbol, and separately describes the Creative Cloud shell as WebView2/Electron. Those notes do not establish the edit-surface toolkit and do not imply a UIA result.

### Cited Findings

- Adobe’s cloud Lightroom developer and HelpX pages describe product behavior. They do not name WinUI, WPF, Win32, Qt, Electron, Chromium, WebView2, or CEF as the desktop UI toolkit. — [developer.adobe.com/lightroom](https://developer.adobe.com/lightroom/); [Lightroom desktop shortcuts](https://helpx.adobe.com/lightroom/desktop/using/keyboard-shortcuts.html)
- A Wine port of Lightroom CC 9.3.1, documented as working on 2026-05-16 with Wine 11.8, says the one fix that matters for Lightroom is a patched `d2d1.dll`: “When Lightroom CC opens its main window it asks Direct2D to give it a rendering context that supports the `CLSID_D2D1ColorManagement` builtin effect.” — [sander110419/lightroom-cc-on-linux GUIDE.md](https://github.com/sander110419/lightroom-cc-on-linux/blob/main/GUIDE.md)
- The same guide says Lightroom static-imports `ext-ms-win-uiacore-l1-1-2.dll`, described as “API-set DLL containing `UiaDisconnectAllProviders`,” because Wine 11.8’s `uiautomationcore` does not export it. The stub returns `S_OK`. — [GUIDE.md](https://github.com/sander110419/lightroom-cc-on-linux/blob/main/GUIDE.md)
- The same repository’s README summarizes a DXVK dummy composition swapchain “so WebView2 (Adobe’s Electron UI shell) can render at all.” Its methodology log applies that explanation to the Creative Cloud desktop sign-in window (`CreateSwapChainForComposition`), after installing WebView2 148.0.3967.70, not to a dumped Lightroom edit-panel control tree. The wording treats WebView2 and Electron as one shell. — [README](https://github.com/sander110419/lightroom-cc-on-linux); [history_methodology.md](https://github.com/sander110419/lightroom-cc-on-linux/blob/main/history_methodology.md)
- Electron’s own documentation says Electron and WebView2 are different hosts: Electron bundles Chromium and does not share Edge DLLs; WebView2 is an Edge/Chromium component embedded in another application framework. — [WebView2 and Electron](https://electronjs.org/blog/webview2)
- Lightroom Classic’s Map module has been described by a third-party technical note as using the Chromium Embedded Framework (`cef_toolkit.dll`, `libcef.dll`) for the map view, with the rest of Classic largely Lua. That note is about Classic’s map, not the cloud app’s edit UI. — [astuder/lightroom-map-fix notes.md](https://github.com/astuder/lightroom-map-fix/blob/master/notes.md)

### Inferences

- There is no credible Adobe source from which to deduce UIA exposure. A custom-drawn Direct2D window often has a thin UIA tree, and a WebView2 or Electron surface exposes web content to UIA only when that host’s accessibility bridge is on. Both conditionals are general platform behavior. Neither has been shown for Lightroom’s edit UI.
- The Wine author’s “WebView2 (Adobe’s Electron UI shell)” label is not a reliable architecture statement. The same project’s more specific observation about Lightroom’s own main window is the Direct2D color-management effect. A static import of `UiaDisconnectAllProviders` shows the process links a UIA API set. It does not show which controls, if any, are published to clients.
- Using that Wine repo to choose UIA versus pixel matching would be an inference beyond the evidence.

### Gaps

- Adobe has not published the UI toolkit for cloud Lightroom desktop.
- No binary inventory (loaded modules such as `libcef`, `msedgewebview2`, `electron.exe`, or WinUI) from an official or lab report was found.
- The Wine notes are one person’s install log for Lightroom CC 9.3.1 under Wine. They were not confirmed against a native Windows install.

## What is the maintenance status of WinAppDriver, the Appium Windows Driver, and FlaUI, and does Appium still proxy to WinAppDriver?

### Takeaway

As of 2026-10-20, WinAppDriver’s latest GitHub release is still the July 2021 pre-release v1.2.99, with a 2021 Microsoft statement that resourcing is paused. Appium Windows Driver 6.3.1, published 8 October 2026, still describes itself as a proxy to WinAppDriver. FlaUI’s latest GitHub release is v5.0.0, published 25 February 2025, with later commits on `main` and no newer release tag found.

### Cited Findings

- WinAppDriver GitHub repository `microsoft/WinAppDriver`: latest release listed as v1.2.99 (2021-07-01), marked prerelease; last push 2025-04-14. The README says it supports UWP, WinForms, WPF, and classic Win32 on Windows 10 PCs. — [microsoft/WinAppDriver](https://github.com/microsoft/WinAppDriver)
- Release v1.2.99 is titled “WinAppDriver v1.3 Release Candidate 1,” published 2021-07-01, pre-release. Notes: first build with x86, x64, and ARM64; moved from .NET Framework to .NET 5. — [v1.2.99](https://github.com/microsoft/WinAppDriver/releases/tag/v1.2.99)
- The releases index also lists a stable “WinAppDriver v1.2.1” before that release candidate. The snippet did not include a year for v1.2.1. No stable release newer than the July 2021 candidate was shown. — [WinAppDriver releases](https://github.com/microsoft/WinAppDriver/releases)
- Commits on `master` dated 10–14 April 2025 are described as version-compatibility updates (“Updating the versions in WinAppDriver,” “Changed the versions for compatibility”). They are not a new product release. — [WinAppDriver commits](https://github.com/microsoft/WinAppDriver/commits/master/)
- Pinned issue #1550, “Update on WinAppDriver,” opened 2021-07-01, label FAQ, still open, updated 2026-01-04. The issue body, from Microsoft, says development was paused in November 2020 for at least six months, and: “We don’t have a timeframe of when the level of resourcing for WinAppDriver will change as our team is currently focusing on making a great platform for the future of Windows 11 apps.” It also says Microsoft is “committed to bringing critical improvements,” citing ARM64 in v1.3. The 2026-01-04 update visible in the retrieved thread is a community comment, not a new Microsoft resumption date. — [issue #1550](https://github.com/microsoft/WinAppDriver/issues/1550)
- npm `appium-windows-driver` version 6.3.1, updated 2026-10-08. Description: “Appium bridge to WinAppDriver.” Peer dependency `appium` `^3.0.0-rc.2`. README: “acts as a proxy to Microsoft’s WinAppDriver server.” Since major version 5.0.0 it is only compatible with Appium 3. The README also says the host is Windows 10 and that developer mode must be enabled. Since driver 3.0.0 it does not auto-install WinAppDriver; `appium driver run windows install-wad` installs “the given or latest stable version” from GitHub releases. — [npm appium-windows-driver 6.3.1](https://www.npmjs.com/package/appium-windows-driver); [GitHub releases](https://github.com/appium/appium-windows-driver/releases)
- The same 6.3.1 README contains both “The server itself is maintained by Microsoft” and a warning: “WinAppDriver server has not been maintained by Microsoft for years.” The warning points at NovaWindows Driver as something to consider. That is the Appium maintainers’ characterization, recorded here without a recommendation. — [npm readme](https://www.npmjs.com/package/appium-windows-driver)
- Changelog: 6.3.1 (2026-10-08) is a bug fix, “winapi: report the real koffi load error.” 6.3.0 (2026-09-14) adds mouse-button selection for clickAndDrag. 6.0.0 (2026-06-18) made the package ESM-only. None of these entries say the WinAppDriver proxy was removed. — [CHANGELOG.md](https://github.com/appium/appium-windows-driver/blob/master/CHANGELOG.md)
- Source of `appium-windows-driver` 6.3.0, `lib/driver.ts`: `canProxy()` returns true with the comment “we can always proxy to the WinAppDriver server.” `startWinAppDriverSession()` constructs a `WinAppDriver` client and then sets `this.isProxyActive = true` so later session requests go to WinAppDriver. This file is one patch version before 6.3.1. — [driver.ts at 6.3.0](https://cdn.jsdelivr.net/npm/appium-windows-driver@6.3.0/lib/driver.ts)
- FlaUI GitHub release v5.0.0, published 2025-02-25. Breaking change: removed .NET Standard, .NET Core 3.1, and .NET 5. Enhancements include .NET 8 support. The in-repo changelog dates the 5.0.0 section 2024-12-08, which does not match the GitHub published time. — [FlaUI v5.0.0](https://github.com/FlaUI/FlaUI/releases/tag/v5.0.0); [CHANGELOG.md](https://github.com/FlaUI/FlaUI/blob/main/CHANGELOG.md); [releases](https://github.com/FlaUI/FlaUI/releases)
- Commits on FlaUI `main` continue after that release, including 2026-03-27 (“feat: Update dependencies, add .net 10, remove .net 6”) and 2026-06-17 (“fix: prevent RecordLoop & WriteLoop exceptions from being swallowed”). The tags page shown in search lists v5.0.0 as the latest tag. Those 2026 commits are not a release. — [FlaUI commits](https://github.com/FlaUI/FlaUI/commits/main/); [tags](https://github.com/FlaUI/FlaUI/tags)

### Inferences

- “Appium still proxies to WinAppDriver” is true of the published 6.3.1 README and of the 6.3.0 driver source. 6.3.1’s changelog does not describe a proxy removal. The 6.3.1 TypeScript was not opened line by line.
- WinAppDriver has release artifacts and a small 2025 commit, and Microsoft’s own 2021 FAQ still says there is no resourcing timeframe. “Maintained” in the Appium README and “not been maintained for years” in the same README disagree; the release history matches the warning more closely than the older sentence.
- FlaUI’s release cadence is a library release in February 2025 plus unreleased 2026 commits. That is a different maintenance picture from WinAppDriver’s 2021 pre-release. No ranking is implied.

### Gaps

- The year and exact notes of stable WinAppDriver v1.2.1 were not copied from the release body.
- FlaUI’s NuGet package version was not checked separately from the GitHub release.
- Whether every 6.3.1 command still forwards, or which routes are in the no-proxy list, was not re-read in the 6.3.1 tree. The 6.3.0 excerpt shows a no-proxy list for some routes (execute, screenshot, element search, and others) and proxy-on for the rest.
- NovaWindows Driver’s version and quality were not reviewed. A comment on WinAppDriver issue #1550 from 2025-09-04 only points at it.

## Which Lightroom keyboard shortcuts for AI Denoise, or similar UI-only commands, does Adobe Help document?

### Takeaway

Adobe Help for cloud Lightroom desktop documents Ctrl+Alt+E on Windows in two different roles on the same page: batch-applying Denoise, and opening the Enhance dialog. The desktop shortcut catalog does not list Denoise or Enhance. No HelpX shortcut is named “AI Denoise.” Lightroom Classic’s shortcut page documents different Enhance keys and is a different product.

### Cited Findings

- Cloud Lightroom, “Easily enhance image quality in Lightroom,” last updated 17 June 2025, URL under `/lightroom/desktop/`. It says Denoise “reduces noise while preserving detail” and “Currently, Denoise applies only to Bayer, X-Trans mosaic raw, Linear DNGs … and Apple ProRAW files.” A note says: “You can now access Denoise, Raw Details, and Super Resolution under the Detail section in the Edit panel. This allows you to make local editing adjustments to your photos directly instead of creating separate files for every enhancement.” The only “AI Denoise” phrase on the page is: “Apple Neural Engine is disabled for AI Denoise on Mac computers with Apple silicon.” — [Enhance in Lightroom](https://helpx.adobe.com/lightroom/desktop/edit-photos/enhance-details.html)
- Same page, “Apply Denoise”: “From the menu, select Photo > Enhance or select Denoise in the Detail panel.” Then: “Select Enhance to run Denoise. The result will be saved as a new DNG file with ‘Enhance-NR.dng’ appended to the source file name.” Under “Batch-apply Denoise”: “In the grid menu, select all the photos that you want to Enhance and then select Command + Option + E on macOS, and Ctrl + Alt + E on Windows.” — [Enhance in Lightroom](https://helpx.adobe.com/lightroom/desktop/edit-photos/enhance-details.html)
- Same page, “Use a keyboard shortcut”: “To quickly view the Enhance dialog box with the enhanced preview, press: (Mac) Control+Option+E (Windows) Ctrl+Alt+E.” A later section, “Enhance multiple images in one go,” says Photo > Enhance applies “Your last selected option in Enhance (Raw Details or Super Resolution)” and does not name Denoise. — [Enhance in Lightroom](https://helpx.adobe.com/lightroom/desktop/edit-photos/enhance-details.html)
- Cloud Lightroom, “Default keyboard shortcuts for Lightroom Desktop,” last updated 17 June 2025. The extracted tables include, on Windows, Detail = D, Edit = E, and “Expand/Retract Details Panel” = Ctrl+4. The extracted page does not contain the words Denoise or Enhance, and does not list Ctrl+Alt+E. Some rating rows were blank in the extraction, so missing cells in those rows are a fetch gap, not a claim that those rating keys do not exist. — [Lightroom desktop shortcuts](https://helpx.adobe.com/lightroom/desktop/using/keyboard-shortcuts.html)
- Lightroom Classic’s shortcut page at `helpx.adobe.com/lightroom-classic/desktop/introduction-to-lightroom-classic/keyboard-shortcuts.html` lists, for Windows: “Open enhance dialog box” = Ctrl+Alt+I, “Headless enhance” = Ctrl+Alt+Shift+I, and “Open in other editor” = Ctrl+Alt+E. The search extract of that page says “Last updated on Oct 29, 2025.” These rows are Classic. The page’s visible “Denoise” hits in the extract are navigation links to a Classic troubleshooting topic, not a Denoise shortcut row. — [Lightroom Classic shortcuts](https://helpx.adobe.com/lightroom-classic/desktop/introduction-to-lightroom-classic/keyboard-shortcuts.html)
- Classic’s Enhance article, separate from the shortcut catalog, says: open the Enhance dialog with Ctrl+Alt+I on Windows, and apply the last selected option without opening the dialog with Shift+Ctrl+Alt+I on Windows. That article is Lightroom Classic (`/lightroom-classic/help/enhance-details.html`). — [Classic Enhance](https://helpx.adobe.com/nz/lightroom-classic/help/enhance-details.html)

### Inferences

- For the cloud app, the only HelpX key sequence found that is tied to Denoise or Enhance is Windows Ctrl+Alt+E. The same article assigns it both to “Batch-apply Denoise” and to “view the Enhance dialog box.” Which of those the current app does was not established. The shortcut catalog does not corroborate either assignment.
- Ctrl+4 is documented only as expand/retract the Details panel. The Enhance article says Denoise lives in that panel. Ctrl+4 is not a Denoise command.
- There is no documented shortcut whose label is “AI Denoise,” and no documented shortcut that the HelpX text limits to a one-click Denoise of the current photo without the dialog, for the cloud app.
- Classic’s Ctrl+Alt+I / Ctrl+Alt+Shift+I Enhance shortcuts must not be copied onto the cloud app. On Classic’s own shortcut page, Ctrl+Alt+E is “Open in other editor,” which is yet a third meaning of that chord.
- A “shortcuts second” strategy therefore has one ambiguous documented chord for this feature, plus a panel-open chord. It does not have a published key for every edit control. The 2019 ACR already said many actions have no keyboard path; that statement is stale, and the 2025 shortcut page was not compared control-by-control with the edit UI.

### Gaps

- The cloud shortcut page may be longer than the extraction. A Denoise row below the rating table was not seen because the extraction ended at “Set rating to 5.”
- HelpX does not say whether Ctrl+Alt+E on cloud Lightroom still creates an Enhance-NR DNG or applies the in-panel Denoise mentioned in the note above those steps. The page asserts both “instead of creating separate files” and “saved as a new DNG file.”
- No Adobe Help page found documents a shortcut for other cloud-Lightroom UI-only AI edits (Generative Remove, Generative Expand, or prompt edits) beyond the keys present in the shortcut catalog extract. Those commands were not searched one by one.

## Which interactive-session limits does Microsoft document for UI Automation and SendInput?

### Takeaway

Microsoft documents three separate constraints: UIPI blocks `SendInput` into a higher-integrity window and does not report that failure clearly; `SetForegroundWindow` is limited by the foreground lock and cannot steal focus while the user is in another window; a locked desktop, the logon UI, and a UAC consent UI are outside normal cross-process input. UI Automation across integrity levels requires the UIAccess rules, and UIAccess still does not reach system-integrity UI.

### Cited Findings

- `SendInput`: “This function fails when it is blocked by UIPI. Note that neither GetLastError nor the return value will indicate the failure was caused by UIPI blocking.” “This function is subject to UIPI. Applications are permitted to inject input only into applications that are at an equal or lesser integrity level.” Requirements line: desktop apps only. If it returns zero, “the input was already blocked by another thread.” — [SendInput](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendinput)
- `SetForegroundWindow` remarks: a process may call it only if it is a desktop application rather than a UWP or Windows Store app, the foreground process has not disabled calls via `LockSetForegroundWindow`, and no menus are active; and at least one of: the foreground lock timeout has expired (`SPI_GETFOREGROUNDLOCKTIMEOUT`), the caller is the foreground process, the caller was started by the foreground process, there is no foreground window, the caller received the last input event, or either process is being debugged. “It is possible for a process to be denied the right to set the foreground window even if it meets these conditions.” “An application cannot force a window to the foreground while the user is working with another window. Instead, Windows flashes the taskbar button.” The foreground process can disable calls with `LockSetForegroundWindow`. — [SetForegroundWindow](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setforegroundwindow)
- UI Automation security overview: assistive technologies run at medium integrity and need UIAccess to reach higher-integrity UI. The UAC consent dialog and “the desktop logon screen” run at a higher integrity level “to protect it from cross-process communication, so that malicious software cannot simulate user input.” Without UIAccess, a medium-IL process “cannot access elevated (‘medium+’ IL) process UI.” UIAccess requires an Authenticode signature, installation in a secure location such as Program Files, and `uiAccess="true"` in the manifest. “None of the previously listed scenarios provide access to UI running under the system IL,” including the UAC desktop under SYSTEM, where setting UIAccess has no effect. — [Security considerations for assistive technologies](https://learn.microsoft.com/en-us/windows/win32/winauto/uiauto-securityoverview)
- Power Automate for desktop, Microsoft Learn: simulated UI or browser input can fail because of UIPI when processes are at different integrity levels. Listed causes include “a locked desktop,” an open UAC dialog, a minimized RDP window, the target running elevated, and an active screen saver. For “The desktop is locked during execution,” the documented solution is “Unlock the desktop to allow the automation process to proceed.” The quoted exception says simulated input commands were not sent, and “certain commands are restricted to Accessibility/UIAutomation applications.” A later note says that for UI automation, enabling the Simulate action parameter is the alternative to physical input. — [UIPI issues with UI and browser automation](https://learn.microsoft.com/en-us/troubleshoot/power-platform/power-automate/desktop-flows/ui-automation/uipi-issues)
- Windows App CLI UI Automation reference, Microsoft Learn: verbs that synthesize input (`click`, `hover`, `drag`, `touch`, `pen`, `scroll --wheel`, and `send-keys --via send-input`) “need an unlocked, interactive desktop with the target window in the foreground.” On a locked workstation or secure desktop (LogonUI/UAC) they fail with `no_interactive_desktop`. `send-keys --via send-input` “is blocked by UIPI when injecting from an elevated process into a lower-integrity (AppContainer/AppX) target” and fails with `foreground_not_target` if the target is not actually in the foreground. The same page says `inspect`, `search`, property and value reads, `set-value`, `invoke`, and pattern scrolling “drive the app through UIA patterns and [are] headless/locked-session friendly.” `post-message` key injection is described as bypassing UIPI, and as failing for windowless WinUI 3 / UWP controls. This is the CLI’s contract, not the UI Automation API reference. — [UI Automation (Windows App CLI)](https://learn.microsoft.com/en-us/windows/apps/dev-tools/winapp-cli/ui-automation)

### Inferences

- Any out-of-process driver that uses `SendInput` for Lightroom shortcuts has to be in an interactive, unlocked session, at an integrity level equal to or higher than Lightroom, and it has to get the foreground under the `SetForegroundWindow` rules. A locked screen or a UAC/logon secure desktop is a documented failure case for injected input.
- UIA pattern calls are a different channel from `SendInput`. Microsoft’s assistive-technology page ties cross-integrity UIA to UIAccess and still excludes system-integrity UI. The Windows App CLI page says that product’s pattern verbs still work in a locked session. That CLI sentence was not found in the UI Automation API reference, so it should not be treated as a guarantee for FlaUI, WinAppDriver, or a hand-written UIA client.
- These constraints are platform rules. They do not say whether Lightroom’s controls implement UIA patterns.

### Gaps

- The UI Automation API reference pages for `IUIAutomation` were not separately fetched for a locked-desktop sentence. The locked-session behavior above is from the Windows App CLI page and from the Power Automate simulated-input article.
- No Microsoft page found here mentions Lightroom.
