--[[----------------------------------------------------------------------------
BrokerAuth.lua - the broker's access token (lrcmcp-squyr)

The broker writes a random token to <home>/.lightroom-classic-mcp/broker.json each time it starts
(mcp-server/broker_auth.py) and refuses /poll, /response and /auto_edit without it.
------------------------------------------------------------------------------]]

local LrPathUtils = import 'LrPathUtils'
local LrFileUtils = import 'LrFileUtils'

local BrokerAuth = { HEADER = "X-LrC-MCP-Token" }

local cached = nil

function BrokerAuth.discoveryPath()
    local dir = LrPathUtils.child( LrPathUtils.getStandardFilePath( "home" ), ".lightroom-classic-mcp" )
    return LrPathUtils.child( dir, "broker.json" )
end

-- The token, read once and again on refresh (after the broker answered 401)
function BrokerAuth.token( refresh )
    if refresh or not cached then
        local ok, text = pcall( LrFileUtils.readFile, BrokerAuth.discoveryPath() )
        cached = ok and type( text ) == "string" and text:match( '"token"%s*:%s*"([^"]+)"' ) or nil
    end
    return cached
end

-- A copy of the headers list ({ field, value } entries) with the token added when there is one
function BrokerAuth.headers( base, refresh )
    local list = {}
    for _, h in ipairs( base or {} ) do list[#list + 1] = h end
    local token = BrokerAuth.token( refresh )
    if token then list[#list + 1] = { field = BrokerAuth.HEADER, value = token } end
    return list
end

return BrokerAuth
