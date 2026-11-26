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
