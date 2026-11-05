# 10 · Your own MCP server

[MCP (Model Context Protocol)](https://modelcontextprotocol.io) is the open standard for connecting AI apps to tools and data. Instead of writing tools separately for every framework, you write an **MCP server** once, and any MCP client can use it: Claude Desktop, Claude Code, VS Code, Cursor, Google ADK, LangGraph.

This server exposes the log tools from project 04 and the runbooks from project 08:

| Kind | Name | What it does |
|---|---|---|
| tool | `list_logs` | log files it can read |
| tool | `log_summary` | counts by level and service |
| tool | `search_log` | regex search with line numbers |
| resource | `runbook://{name}` | a runbook, e.g. `runbook://disk-full` |

**You learn:** MCP tools versus resources; the stdio transport; the client side of the protocol; and that tools are an API you design.

```bash
python 10-mcp-server/client.py          # a minimal client calls the server
mcp dev 10-mcp-server/server.py         # MCP Inspector: click through tools in the browser
```

## Use it from Claude Desktop

Add this to Claude Desktop's config (Settings → Developer → Edit Config), with your own absolute paths:

```json
{
  "mcpServers": {
    "devops-tools": {
      "command": "C:/path/to/ai-engineer-starter-projects/.venv/Scripts/python.exe",
      "args": ["C:/path/to/ai-engineer-starter-projects/10-mcp-server/server.py"]
    }
  }
}
```

Restart Claude Desktop and ask: *"Use devops-tools to find out why payments failed in app.log."*

## Try this

1. Add the read-only `kubectl` tool from project 05 as an MCP tool.
2. Add a resource listing all runbook names, so a client can discover them.
3. Project 12 connects Google ADK to this same server. One server, two frameworks.
4. Run it over HTTP instead of stdio (`mcp.run(transport="streamable-http")`) so it could run in Kubernetes. What does it now need that stdio didn't? (Hint: authentication.)
