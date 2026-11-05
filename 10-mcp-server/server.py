"""Project 10: expose your tools as an MCP server.

MCP (Model Context Protocol) is the standard way to give tools to any AI app:
Claude Desktop, Claude Code, Cursor, VS Code, Google ADK, LangGraph. Write the
tools once here; every MCP client can use them.

    mcp dev 10-mcp-server/server.py        # opens the MCP Inspector in a browser
    python 10-mcp-server/client.py         # a tiny client that calls the server
"""

import re
from collections import Counter
from pathlib import Path

from mcp.server.mcpserver import MCPServer

LOGS = Path(__file__).resolve().parent.parent / "04-log-analyser-agent" / "samples"
LINE = re.compile(r"^(?P<time>\S+ \S+) (?P<level>[A-Z]+) \[(?P<service>[^\]]+)\] (?P<message>.*)$")

mcp = MCPServer("devops-tools")


def _read(name: str) -> list[str]:
    path = (LOGS / name).resolve()
    if not path.is_relative_to(LOGS):
        raise PermissionError("only files in the samples folder can be read")
    return path.read_text(encoding="utf-8").splitlines()


@mcp.tool()
def list_logs() -> list[str]:
    """List the log files this server can read."""
    return sorted(p.name for p in LOGS.glob("*.log"))


@mcp.tool()
def log_summary(name: str) -> dict:
    """Counts by level, errors by service and the time range of a log file."""
    parsed = [m.groupdict() for m in map(LINE.match, _read(name)) if m]
    return {
        "first": parsed[0]["time"] if parsed else None,
        "last": parsed[-1]["time"] if parsed else None,
        "by_level": dict(Counter(p["level"] for p in parsed)),
        "errors_by_service": dict(Counter(p["service"] for p in parsed if p["level"] == "ERROR")),
    }


@mcp.tool()
def search_log(name: str, pattern: str, max_results: int = 30) -> list[str]:
    """Lines in a log file matching a regular expression (case-insensitive)."""
    regex = re.compile(pattern, re.IGNORECASE)
    return [f"{n}: {line}" for n, line in enumerate(_read(name), 1) if regex.search(line)][:max_results]


@mcp.resource("runbook://{name}")
def runbook(name: str) -> str:
    """A runbook from project 08, as a readable resource."""
    docs = Path(__file__).resolve().parent.parent / "08-chat-with-docs-rag" / "docs"
    path = (docs / f"{name}.md").resolve()
    if not path.is_relative_to(docs):
        raise PermissionError("unknown runbook")
    return path.read_text(encoding="utf-8")


if __name__ == "__main__":
    mcp.run()  # stdio transport: the client starts this process and talks over stdin/stdout
