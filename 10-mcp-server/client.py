"""A minimal MCP client: start the server, list its tools, call two of them.

This is what Claude Desktop or Google ADK do behind the scenes.

    python 10-mcp-server/client.py
"""

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = Path(__file__).parent / "server.py"


async def main() -> None:
    params = StdioServerParameters(command=sys.executable, args=[str(SERVER)])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Tools:", [t.name for t in tools.tools])

            result = await session.call_tool("log_summary", {"name": "app.log"})
            print("\nlog_summary(app.log):\n", result.content[0].text)

            result = await session.call_tool("search_log", {"name": "app.log", "pattern": "reporting-job"})
            print("\nsearch_log(reporting-job):")
            for item in result.content:
                print(" ", item.text)


if __name__ == "__main__":
    asyncio.run(main())
