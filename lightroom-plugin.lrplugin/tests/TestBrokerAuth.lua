-- TestBrokerAuth.lua
-- The plugin reads the broker token from the same discovery file the broker writes.

local Mocks = require 'Mocks'
local BrokerAuth = dofile("../BrokerAuth.lua")

local Tests = {}
local PATH = "/home/test/.lightroom-classic-mcp/broker.json"

local function headerValue( headers, field )
    for _, h in ipairs( headers ) do
        if h.field == field then return h.value end
    end
end

function Tests.test_discovery_path_is_under_home()
    assert( BrokerAuth.discoveryPath() == PATH, BrokerAuth.discoveryPath() )
end

function Tests.test_headers_carry_the_token()
    Mocks.state.files[PATH] = '{"token": "abc-123", "port": 8085, "pid": 1}'
    local headers = BrokerAuth.headers( { { field = "Content-Type", value = "application/json" } }, true )
    assert( headerValue( headers, "Content-Type" ) == "application/json" )
    assert( headerValue( headers, "X-LrC-MCP-Token" ) == "abc-123", tostring( headerValue( headers, "X-LrC-MCP-Token" ) ) )
end

function Tests.test_token_is_cached_until_refresh()
    Mocks.state.files[PATH] = '{"token": "first"}'
    assert( BrokerAuth.token( true ) == "first" )
    Mocks.state.files[PATH] = '{"token": "second"}'
    assert( BrokerAuth.token() == "first" )
    assert( BrokerAuth.token( true ) == "second" )
end

function Tests.test_missing_file_gives_no_token_header()
    Mocks.state.files[PATH] = nil
    Mocks.state.missing = { [PATH] = true }
    local headers = BrokerAuth.headers( {}, true )
    Mocks.state.missing = nil
    assert( headerValue( headers, "X-LrC-MCP-Token" ) == nil )
end

local passed, failed = 0, 0
for name, func in pairs( Tests ) do
    local ok, err = pcall( func )
    if ok then passed = passed + 1 else print( "FAIL: " .. name .. " - " .. tostring( err ) ); failed = failed + 1 end
end
print( string.format( "\nBrokerAuth results: %d Passed, %d Failed", passed, failed ) )
if failed > 0 then os.exit( 1 ) end
