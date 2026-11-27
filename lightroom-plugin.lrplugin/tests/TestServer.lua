-- TestServer.lua
-- The plugin talks to the broker over HTTP only and reconnects quickly after the broker restarts.

local Mocks = require 'Mocks'
package.path = "../?.lua;" .. package.path

local posts, sleeps, failuresLeft = {}, {}, 0
local queued = nil

local LrHttp = {
    post = function( url, body, headers, method, timeout )
        posts[#posts + 1] = { url = url, body = body }
        if failuresLeft > 0 then
            failuresLeft = failuresLeft - 1
            error( "connection refused" )   -- broker down
        end
        if url:find( "/poll$" ) and queued then
            local request = queued
            queued = nil
            return request, { status = 200 }
        end
        if url:find( "/response$" ) then
            _G.mcpServerRunning = false     -- end the test after the first answer
        end
        return "", { status = 200 }
    end
}
local LrDialogs = { showBezel = function() end }

local baseImport = import
function import( name )
    if name == 'LrHttp' then return LrHttp end
    if name == 'LrDialogs' then return LrDialogs end
    if name == 'LrSocket' then error( "Server.lua must not use LrSocket" ) end
    return baseImport( name )
end
Mocks.LrTasks.sleep = function( seconds ) sleeps[#sleeps + 1] = seconds end

local Tests = {}

function Tests.test_reconnects_over_http_after_the_broker_restarts()
    local Server = dofile( "../Server.lua" )
    posts, sleeps = {}, {}
    failuresLeft = 12                       -- broker stopped for a dozen polls, then back
    queued = '{"jsonrpc":"2.0","id":1,"method":"no_such_method","_broker_uuid":"u1"}'
    Server.start( {} )
    local polled, answered = 0, 0
    for _, p in ipairs( posts ) do
        assert( p.url:find( "^http://127%.0%.0%.1:8085/" ), "not HTTP to the broker: " .. p.url )
        if p.url:find( "/poll$" ) then polled = polled + 1 end
        if p.url:find( "/response$" ) then answered = answered + 1 end
    end
    assert( polled >= 13, "kept polling over HTTP through the outage: " .. polled )
    assert( answered == 1, "answered the request once the broker was back: " .. answered )
    local longest = 0
    for _, s in ipairs( sleeps ) do if s > longest then longest = s end end
    assert( longest <= 2, "waits at most 2 s between retries, waited " .. longest )
end

local passed, failed = 0, 0
for name, func in pairs( Tests ) do
    local ok, err = pcall( func )
    if ok then passed = passed + 1 else print( "FAIL: " .. name .. " - " .. tostring( err ) ); failed = failed + 1 end
end
print( string.format( "\nServer results: %d Passed, %d Failed", passed, failed ) )
if failed > 0 then os.exit( 1 ) end
