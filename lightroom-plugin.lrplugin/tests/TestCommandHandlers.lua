-- TestCommandHandlers.lua
-- Unit tests for CommandHandlers.lua using Mocks

-- Load Mocks
local Mocks = require 'Mocks'

-- Load CommandHandlers (it will use the global 'import' from Mocks)
local CommandHandlers = dofile("../CommandHandlers.lua")

-- Test Helpers
local function assertEqual(expected, actual, msg)
    if expected ~= actual then
        error(msg or string.format("Expected %s, got %s", tostring(expected), tostring(actual)))
    end
end

local function assertTable(t, msg)
    if type(t) ~= "table" then
         error(msg or "Expected table, got " .. type(t))
    end
end


-- Tests
local Tests = {}

function Tests.test_get_studio_info()
    print("Running test_get_studio_info...")
    local result = CommandHandlers.get_studio_info({})
    assertTable(result)
    assertEqual("Test Catalog", result.catalogName)
    assertEqual("0.1.0", result.pluginVersion)   -- read from the real Info.lua
    assertEqual("16.0.1", result.lightroomVersion)
    assertEqual(202611, result.lightroomBuild)
    print("PASS")
end

function Tests.test_get_studio_info_reads_plugin_version_from_info()
    print("Running test_get_studio_info_reads_plugin_version_from_info...")
    Mocks.state.files["../Info.lua"] = 'return { VERSION = { major = 9, display = "9.8.7" } }'
    local result = CommandHandlers.get_studio_info({})
    Mocks.state.files["../Info.lua"] = nil
    assertEqual("9.8.7", result.pluginVersion)
    print("PASS")
end

function Tests.test_get_selection_empty()
    print("Running test_get_selection_empty...")
    Mocks.state.photos = {} -- Clear selection
    local result = CommandHandlers.get_selection({})
    assertTable(result)
    assertTable(result.photos)
    assertEqual(0, #result.photos)
    print("PASS")
end

function Tests.test_get_selection_populated()
    print("Running test_get_selection_populated...")
    local p1 = Mocks.Photo.new("123", "test.jpg")
    p1:setRawMetadata("rating", 3)
    Mocks.state.photos = { p1 }

    local result = CommandHandlers.get_selection({})
    assertTable(result)
    assertEqual(1, #result.photos)
    assertEqual("123", result.photos[1].localId)
    assertEqual(3, result.photos[1].rating)
    print("PASS")
end

function Tests.test_set_rating()
    print("Running test_set_rating...")
    local p1 = Mocks.Photo.new("123", "test.jpg")
    Mocks.state.photos = { p1 }

    -- Valid rating, confirmed, expected photo named by file name
    local result = CommandHandlers.set_rating({ rating = 5, expected = { "test.jpg" }, confirmed = true })
    assertTable(result)
    assertEqual(true, result.success)
    assertEqual(5, p1:getRawMetadata("rating"))
    assertEqual("123", result.photos[1].localId)

    -- Invalid rating
    result = CommandHandlers.set_rating({ rating = 6, expected = { "test.jpg" }, confirmed = true })
    assertTable(result)
    assertEqual("Rating must be between 0 and 5", result.error)
    print("PASS")
end

function Tests.test_write_without_expected_photos_is_refused()
    print("Running test_write_without_expected_photos_is_refused...")
    local p1 = Mocks.Photo.new("123", "test.jpg")
    Mocks.state.photos = { p1 }
    local result = CommandHandlers.set_rating({ rating = 4, confirmed = true })
    assert(result.error and result.error:find("^Invalid expected"), tostring(result.error))
    assertEqual(0, p1:getRawMetadata("rating"))   -- mock photos start at 0; unchanged
    print("PASS")
end

function Tests.test_unconfirmed_write_is_refused()
    print("Running test_unconfirmed_write_is_refused...")
    local p1 = Mocks.Photo.new("123", "test.jpg")
    Mocks.state.photos = { p1 }
    local result = CommandHandlers.set_title({ title = "x", expected = { "123" } })
    assert(result.error and result.error:find("^Invalid confirmed"), tostring(result.error))
    assertEqual("", p1:getRawMetadata("title"))
    print("PASS")
end

function Tests.test_write_to_other_photos_is_a_target_mismatch()
    print("Running test_write_to_other_photos_is_a_target_mismatch...")
    local p1 = Mocks.Photo.new("123", "DSC_0001.NEF")
    local p2 = Mocks.Photo.new("124", "DSC_0002.NEF")
    Mocks.state.photos = { p1, p2 }
    -- the user's selection grew to two photos; the agent expected one
    local result = CommandHandlers.set_caption({ caption = "x", expected = { "DSC_0001" }, confirmed = true })
    assert(result.error and result.error:find("^Target mismatch"), tostring(result.error))
    assertEqual("", p1:getRawMetadata("caption"))
    -- expecting a photo that is not selected
    result = CommandHandlers.set_caption({ caption = "x", expected = { "DSC_0001", "DSC_0002", "DSC_0003" }, confirmed = true })
    assert(result.error and result.error:find("^Target mismatch"), tostring(result.error))
    -- ids and base names both match
    result = CommandHandlers.set_caption({ caption = "x", expected = { "123", "DSC_0002" }, confirmed = true })
    assertEqual(true, result.success)
    print("PASS")
end

function Tests.test_dry_run_plans_and_writes_nothing()
    print("Running test_dry_run_plans_and_writes_nothing...")
    local p1 = Mocks.Photo.new("123", "test.jpg")
    p1:setRawMetadata("rating", 2)
    Mocks.state.photos = { p1 }
    local result = CommandHandlers.set_rating({ rating = 5, expected = { "test.jpg" }, dryRun = true })
    assertEqual(true, result.dryRun)
    assertEqual(2, result.photos[1].before.rating)
    assertEqual(5, result.photos[1].after.rating)
    assertEqual(2, p1:getRawMetadata("rating"))
    print("PASS")
end

function Tests.test_develop_write_reads_back()
    print("Running test_develop_write_reads_back...")
    local p1 = Mocks.Photo.new("123", "test.jpg")
    Mocks.state.photos = { p1 }
    local ok = CommandHandlers.set_develop_settings({ settings = { Exposure2012 = 0.5 }, expected = { "123" }, confirmed = true })
    assertEqual(true, ok.success)
    Mocks.state.ignoreDevelopKeys = { Contrast2012 = true }
    local bad = CommandHandlers.set_develop_settings({ settings = { Contrast2012 = 20 }, expected = { "123" }, confirmed = true })
    Mocks.state.ignoreDevelopKeys = nil
    assert(bad.error and bad.error:find("^Readback mismatch") and bad.error:find("Contrast2012"), tostring(bad.error))
    print("PASS")
end

function Tests.test_develop_dry_run_shows_current_values()
    print("Running test_develop_dry_run_shows_current_values...")
    local p1 = Mocks.Photo.new("123", "test.jpg")
    p1:applyDevelopSettings({ Exposure2012 = 0.1 })
    Mocks.state.photos = { p1 }
    local plan = CommandHandlers.set_develop_settings({ settings = { Exposure2012 = 0.7 }, expected = { "123" }, dryRun = true })
    assertEqual(0.1, plan.photos[1].before.Exposure2012)
    assertEqual(0.7, plan.photos[1].after.Exposure2012)
    assertEqual(0.1, p1:getDevelopSettings().Exposure2012)
    print("PASS")
end

function Tests.test_one_expected_entry_cannot_approve_two_photos()
    print("Running test_one_expected_entry_cannot_approve_two_photos...")
    -- a raw and its JPEG share the base name
    local raw = Mocks.Photo.new("201", "DSC_0001.NEF")
    local jpg = Mocks.Photo.new("202", "DSC_0001.JPG")
    Mocks.state.photos = { raw, jpg }
    local result = CommandHandlers.set_caption({ caption = "x", expected = { "DSC_0001" }, confirmed = true })
    assert(result.error and result.error:find("^Target mismatch"), tostring(result.error))
    assertEqual("", raw:getRawMetadata("caption"))
    assertEqual("", jpg:getRawMetadata("caption"))
    -- the base name twice still names each photo ambiguously
    result = CommandHandlers.set_caption({ caption = "x", expected = { "DSC_0001", "DSC_0001" }, confirmed = true })
    assert(result.error and result.error:find("^Target mismatch"), tostring(result.error))
    assertEqual("", raw:getRawMetadata("caption"))
    -- full file names name one photo each
    result = CommandHandlers.set_caption({ caption = "x", expected = { "DSC_0001.NEF", "DSC_0001.JPG" }, confirmed = true })
    assertEqual(true, result.success)
    print("PASS")
end

function Tests.test_virtual_copies_need_ids()
    print("Running test_virtual_copies_need_ids...")
    -- a master and its virtual copy share the file name
    local master = Mocks.Photo.new("301", "IMG.CR3")
    local copy = Mocks.Photo.new("302", "IMG.CR3")
    Mocks.state.photos = { master, copy }
    local result = CommandHandlers.set_title({ title = "x", expected = { "IMG.CR3" }, confirmed = true })
    assert(result.error and result.error:find("^Target mismatch"), tostring(result.error))
    result = CommandHandlers.set_title({ title = "x", expected = { "IMG.CR3", "IMG.CR3" }, confirmed = true })
    assert(result.error and result.error:find("^Target mismatch"), tostring(result.error))
    assertEqual("", master:getRawMetadata("title"))
    assertEqual("", copy:getRawMetadata("title"))
    result = CommandHandlers.set_title({ title = "x", expected = { "301", "302" }, confirmed = true })
    assertEqual(true, result.success)
    assertEqual("x", copy:getRawMetadata("title"))
    print("PASS")
end

function Tests.test_dry_run_after_is_the_planned_value_of_the_same_fields()
    print("Running test_dry_run_after_is_the_planned_value_of_the_same_fields...")
    local p1 = Mocks.Photo.new("123", "test.jpg")
    p1:setRawMetadata("keywordTags", "bird, crow")
    p1:setRawMetadata("pickStatus", 0)
    p1:setRawMetadata("gpsAltitude", 12)
    Mocks.state.photos = { p1 }
    local plan = CommandHandlers.add_keywords({ keywords = { "Animals > fish", "crow" }, expected = { "123" }, dryRun = true })
    assertEqual("bird, crow", plan.photos[1].before.keywords)
    assertEqual("bird, crow, fish", plan.photos[1].after.keywords)
    plan = CommandHandlers.remove_keywords({ keywords = { "crow" }, expected = { "123" }, dryRun = true })
    assertEqual("bird", plan.photos[1].after.keywords)
    plan = CommandHandlers.set_pick_flag({ pickFlag = "reject", expected = { "123" }, dryRun = true })
    assertEqual(0, plan.photos[1].before.pickFlag)
    assertEqual(-1, plan.photos[1].after.pickFlag)
    plan = CommandHandlers.set_metadata({ field = "copyright", value = "(c) me", expected = { "123" }, dryRun = true })
    assertEqual("(c) me", plan.photos[1].after.copyright)
    assertEqual(nil, plan.photos[1].after.value)
    plan = CommandHandlers.set_gps_data({ latitude = 10, longitude = 20, expected = { "123" }, dryRun = true })
    assertEqual(10, plan.photos[1].after.gps.latitude)
    assertEqual(20, plan.photos[1].after.gps.longitude)
    assertEqual(12, plan.photos[1].after.gpsAltitude)   -- no altitude given: unchanged
    assertEqual(nil, p1:getRawMetadata("gps"))
    assertEqual("bird, crow", p1:getRawMetadata("keywordTags"))
    print("PASS")
end

function Tests.test_table_develop_values_read_back_by_content()
    print("Running test_table_develop_values_read_back_by_content...")
    local p1 = Mocks.Photo.new("123", "test.jpg")
    Mocks.state.photos = { p1 }
    local ok = CommandHandlers.set_develop_settings({ settings = { ToneCurvePV2012 = { 0, 0, 128, 140, 255, 255 } }, expected = { "123" }, confirmed = true })
    assertEqual(true, ok.success, tostring(ok.error))
    print("PASS")
end

function Tests.test_start_export_returns_a_job_and_runs_async()
    print("Running test_start_export_returns_a_job_and_runs_async...")
    local p1 = Mocks.Photo.new("501", "DSC_0501.NEF")
    Mocks.state.photos = { p1 }
    Mocks.state.dirs = { ["D:/out"] = true }
    Mocks.state.deferTasks = {}
    local started = CommandHandlers.start_export({ destination = "D:/out", format = "JPEG", quality = 85, expected = { "501" }, confirmed = true })
    assert(started.jobId, tostring(started.error))
    assertEqual("accepted", started.status)   -- returned before the export ran
    assertEqual(1, #Mocks.state.deferTasks)
    assertEqual("accepted", CommandHandlers.get_export_status({ jobId = started.jobId }).status)
    Mocks.runDeferredTasks()
    local done = CommandHandlers.get_export_status({ jobId = started.jobId })
    assertEqual("rendered", done.status)
    assertEqual(1, #done.outputs)
    assertEqual("D:/out/DSC_0501.jpg", done.outputs[1].path)
    assertEqual("501", done.outputs[1].localId)
    local s = Mocks.state.lastExportSettings
    assertEqual("JPEG", s.LR_format)
    assertEqual("D:/out", s.LR_export_destinationPathPrefix)
    assertEqual(0.85, s.LR_jpeg_quality)
    print("PASS")
end

function Tests.test_export_failure_is_reported()
    print("Running test_export_failure_is_reported...")
    local p1 = Mocks.Photo.new("502", "DSC_0502.NEF")
    local p2 = Mocks.Photo.new("503", "DSC_0503.NEF")
    Mocks.state.photos = { p1, p2 }
    Mocks.state.dirs = { ["D:/out"] = true }
    Mocks.state.deferTasks = nil
    Mocks.state.exportFailures = { ["503"] = "disk full" }
    local started = CommandHandlers.start_export({ destination = "D:/out", expected = { "502", "503" }, confirmed = true })
    Mocks.state.exportFailures = nil
    local job = CommandHandlers.get_export_status({ jobId = started.jobId })
    assertEqual("failed", job.status)
    assertEqual(1, #job.outputs)
    assertEqual("disk full", job.failures[1].message)
    assertEqual("DSC_0503.NEF", job.failures[1].fileName)
    print("PASS")
end

function Tests.test_missing_renditions_are_failures()
    print("Running test_missing_renditions_are_failures...")
    local p1 = Mocks.Photo.new("505", "DSC_0505.NEF")
    local p2 = Mocks.Photo.new("506", "DSC_0506.NEF")
    Mocks.state.photos = { p1, p2 }
    Mocks.state.dirs = { ["D:/out"] = true }
    Mocks.state.deferTasks = nil
    Mocks.state.exportSkip = { ["506"] = true }   -- Lightroom yields no rendition for this photo
    local started = CommandHandlers.start_export({ destination = "D:/out", expected = { "505", "506" }, confirmed = true })
    Mocks.state.exportSkip = nil
    local job = CommandHandlers.get_export_status({ jobId = started.jobId })
    assertEqual("failed", job.status)
    assertEqual(1, #job.failures)
    assertEqual("DSC_0506.NEF", job.failures[1].fileName)
    print("PASS")
end

function Tests.test_export_checks_its_arguments_and_the_contract()
    print("Running test_export_checks_its_arguments_and_the_contract...")
    local p1 = Mocks.Photo.new("504", "DSC_0504.NEF")
    Mocks.state.photos = { p1 }
    Mocks.state.dirs = { ["D:/out"] = true }
    Mocks.state.deferTasks = {}
    local r = CommandHandlers.start_export({ expected = { "504" }, confirmed = true })
    assert(r.error and r.error:find("^Invalid destination"), tostring(r.error))
    r = CommandHandlers.start_export({ destination = "D:/missing", expected = { "504" }, confirmed = true })
    assert(r.error and r.error:find("^Invalid destination"), tostring(r.error))
    r = CommandHandlers.start_export({ destination = "D:/out", format = "GIF", expected = { "504" }, confirmed = true })
    assert(r.error and r.error:find("^Invalid format"), tostring(r.error))
    r = CommandHandlers.start_export({ destination = "D:/out", expected = { "504" } })
    assert(r.error and r.error:find("^Invalid confirmed"), tostring(r.error))
    r = CommandHandlers.start_export({ destination = "D:/out", expected = { "999" }, confirmed = true })
    assert(r.error and r.error:find("^Target mismatch"), tostring(r.error))
    r = CommandHandlers.start_export({ destination = "D:/out", expected = { "504" }, dryRun = true })
    assertEqual(true, r.dryRun)
    assertEqual(0, #Mocks.state.deferTasks)   -- nothing was started
    print("PASS")
end

function Tests.test_unknown_export_job_is_not_found()
    print("Running test_unknown_export_job_is_not_found...")
    local r = CommandHandlers.get_export_status({ jobId = "export-nope" })
    assert(r.error and r.error:find("not found"), tostring(r.error))
    print("PASS")
end

function Tests.test_add_to_collection()
    print("Running test_add_to_collection...")
    local p1 = Mocks.Photo.new("123", "test.jpg")
    Mocks.state.photos = { p1 }
    Mocks.state.collections = {}

    local result = CommandHandlers.add_to_collection({ collectionName = "My Collection" })
    assertTable(result)
    assertEqual(true, result.success)

    assertEqual(1, #Mocks.state.collections)
    assertEqual("My Collection", Mocks.state.collections[1]:getName())
    assertEqual(1, #Mocks.state.collections[1].photos)
    print("PASS")
end


-- Run Runner
local function run()
    local passed = 0
    local failed = 0

    for name, func in pairs(Tests) do
        local status, err = pcall(func)
        if status then
            passed = passed + 1
        else
            print("FAIL: " .. name .. " - " .. err)
            failed = failed + 1
        end
    end

    print(string.format("\nResults: %d Passed, %d Failed", passed, failed))
    if failed > 0 then os.exit(1) end
end

run()
