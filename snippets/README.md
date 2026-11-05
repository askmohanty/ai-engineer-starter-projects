# Snippets

Copy-paste starting points for building AI agents in Python. Each file stands on its own; install what its header says and run it.

| File | What it shows |
|---|---|
| `01-agent-loop.py` | The tool-calling loop every agent is built on (Anthropic SDK) |
| `02-structured-output.py` | Reliable JSON from a model by forcing a tool call |
| `03-safe-kubectl-tool.py` | A read-only tool: allow-list, no shell, truncated output |
| `04-rag-chroma.py` | Retrieval-augmented generation in under 60 lines |
| `05-mcp-server.py` | An MCP server any MCP client can use (MCP Python SDK v2) |
| `06-langgraph-router.py` | A LangGraph graph with structured output and conditional routing |
| `07-google-adk-multi-agent.py` | A Google ADK root agent with two specialist sub-agents |
| `08-llm-as-judge.py` | Grading answers with a second model call |

Set `ANTHROPIC_API_KEY` for the Claude snippets, or `GOOGLE_API_KEY` for the ADK one.

The full projects these come from, with sample data, explanations and experiments to try: **https://github.com/askmohanty/ai-engineer-starter-projects**

**Learning?** Fork that repo (https://github.com/askmohanty/ai-engineer-starter-projects/fork), work through the projects in your fork, and commit your experiments as you go. Your fork becomes your portfolio.
