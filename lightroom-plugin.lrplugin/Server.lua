--[[----------------------------------------------------------------------------
Server.lua - MCP Bridge Client
Connects to the broker server by HTTP long polling. (The socket fallback on 8086 was removed:
LrSocket could not connect to the broker, and the port had no authentication.)
------------------------------------------------------------------------------]]

local LrLogger = import 'LrLogger'
local LrHttp = import 'LrHttp'
local LrTasks = import 'LrTasks'
local LrDialogs = import 'LrDialogs'
local JSON = require 'JSON'
local CommandHandlers = require 'CommandHandlers'
local BrokerAuth = require 'BrokerAuth'

local logger = LrLogger( 'MCPBridge' )
logger:enable( 'print' )
logger:enable( 'logfile' )

-- Global flags for shutdown coordination
_G.mcpServerRunning = false
_G.mcpShutdownComplete = false

-- Broker configuration
local BROKER_HOST = "127.0.0.1"
local BROKER_HTTP_PORT = 8085
local BROKER_URL = "http://" .. BROKER_HOST .. ":" .. BROKER_HTTP_PORT
local POLL_INTERVAL = 0.1  -- seconds between polls
local MAX_RETRY_WAIT = 2  -- seconds; the longest wait between polls while the broker is down
local LOG_FILE = "D:\\Projects\\lightroom-classic-mcp\\plugin_debug.log"

local function logToFile( msg )
    local f = io.open( LOG_FILE, "a" )
    if f then
        f:write( os.date() .. " [Server]: " .. tostring(msg) .. "\n" )
        f:close()
    end
end

local Server = {}

-- Process a JSON-RPC request and return the response
-- Note: Uses LrTasks.pcall to support yielding in handlers (e.g., withWriteAccessDo)
local function processRequest( request )
    local response = { jsonrpc = "2.0", id = request.id }

    local handler = CommandHandlers[ request.method ]

    if handler then
        -- Use LrTasks.pcall instead of pcall to allow handlers to yield
        local status, result = LrTasks.pcall( handler, request.params or {} )

        if status then
            response.result = result
            logToFile( "Handler success for: " .. tostring(request.method) )
        else
            logToFile( "Handler error for " .. tostring(request.method) .. ": " .. tostring(result) )
            response.error = { code = -32603, message = "Internal error: " .. tostring(result) }
        end
    else
        logToFile( "Method not found: " .. tostring(request.method) )
        response.error = { code = -32601, message = "Method not found: " .. tostring(request.method) }
    end

    return response
end

-- ============================================================================
-- HTTP Mode (Primary)
-- ============================================================================

local function runHttpMode( headers )
    logToFile( "Running in HTTP mode" )

    local consecutiveErrors = 0
    local shown = false
    local authHeaders = BrokerAuth.headers( headers )   -- refreshed when the broker answers 401

    while _G.mcpServerRunning do
        -- Use LrTasks.pcall instead of regular pcall to support yielding
        local success, errorMsg = LrTasks.pcall( function()
            local responseBody, responseHeaders = LrHttp.post(
                BROKER_URL .. "/poll",
                "{}",
                authHeaders,
                "POST",
                5
            )

            if responseHeaders and responseHeaders.status == 401 then
                -- The broker restarted with a new token (or none is readable yet): read it again
                logToFile( "Broker refused the token; rereading " .. tostring( BrokerAuth.discoveryPath() ) )
                authHeaders = BrokerAuth.headers( headers, true )
                LrTasks.sleep( 1 )
                return
            end

            if responseBody and responseBody ~= "" then
                if not shown then
                    LrDialogs.showBezel( "MCP Bridge Ready (HTTP)\n" .. BROKER_URL, 3 )
                    logToFile( "Connected to broker (HTTP)" )
                    shown = true
                end

                consecutiveErrors = 0

                -- Regular pcall is fine here since JSON.decode doesn't yield
                local requestStatus, request = pcall( JSON.decode, responseBody )

                if requestStatus and request then
                    logToFile( "Received request: " .. tostring(request.method) )

                    local brokerUuid = request._broker_uuid
                    local response = processRequest( request )
                    response._broker_uuid = brokerUuid

                    local responseJson = JSON.encode( response )
                    logToFile( "Sending response for: " .. tostring(request.method) )

                    local sendBody, sendHeaders = LrHttp.post(
                        BROKER_URL .. "/response",
                        responseJson,
                        authHeaders,
                        "POST",
                        10
                    )
                    if sendHeaders and sendHeaders.status == 401 then
                        -- The broker restarted between our poll and this answer: reread the token, resend once
                        logToFile( "Broker refused the token on /response; rereading and resending" )
                        authHeaders = BrokerAuth.headers( headers, true )
                        sendBody, sendHeaders = LrHttp.post( BROKER_URL .. "/response", responseJson, authHeaders, "POST", 10 )
                    end

                    if sendBody then
                        logToFile( "Response sent successfully" )
                    else
                        logToFile( "Failed to send response" )
                    end
                else
                    logToFile( "Failed to parse request JSON" )
                end
            else
                if responseHeaders then
                    consecutiveErrors = 0
                    if not shown then
                        LrDialogs.showBezel( "MCP Bridge Ready (HTTP)\n" .. BROKER_URL, 3 )
                        logToFile( "Connected to broker (HTTP)" )
                        shown = true
                    end
                end
            end
        end )

        if not success then
            consecutiveErrors = consecutiveErrors + 1
            if consecutiveErrors <= 3 or consecutiveErrors % 10 == 0 then
                logToFile( "HTTP error (" .. consecutiveErrors .. "): " .. tostring(errorMsg) )
            end
            -- Broker down or restarting: keep polling, backing off to at most MAX_RETRY_WAIT,
            -- so a restarted broker is picked up within a couple of seconds
            LrTasks.sleep( math.min( 0.25 * consecutiveErrors, MAX_RETRY_WAIT ) )
        else
            LrTasks.sleep( POLL_INTERVAL )
        end
    end

    return "shutdown"
end

-- ============================================================================
-- Main Entry Point
-- ============================================================================

function Server.start( context )
    logToFile( "Starting MCP Bridge client..." )
    logToFile( "HTTP endpoint: " .. BROKER_URL )

    _G.mcpServerRunning = true
    _G.mcpShutdownComplete = false

    local headers = {
        { field = "Content-Type", value = "application/json" },
    }

    runHttpMode( headers )   -- returns when _G.mcpServerRunning is cleared

    logToFile( "Server shutting down..." )
    _G.mcpShutdownComplete = true
    logToFile( "Server shutdown complete" )
end

return Server
