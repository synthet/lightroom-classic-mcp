import asyncio
from mcp.server.fastmcp import FastMCP
from server import mcp, AppContext, get_selection, app_lifespan
from mcp.server.session import ServerSession
from dataclasses import dataclass

@dataclass
class MockContext:
    request_context: object

@dataclass
class MockReqCtx:
    lifespan_context: AppContext

async def main():
    async with app_lifespan(mcp) as ctx:
        context = MockContext(request_context=MockReqCtx(lifespan_context=ctx))
        print("Calling get_selection...")
        try:
            result = await get_selection(context)
            print("Success:", result)
        except Exception as e:
            print("Error:", repr(e))
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
