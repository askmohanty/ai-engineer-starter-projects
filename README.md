# AI Engineer starter projects

Thirteen small, hands-on Python projects for learning to build AI agents, from a first tool-calling loop to RAG, MCP, LangGraph, Google ADK and evals. Most use realistic DevOps problems (logs, Kubernetes, cloud bills, on-call runbooks), so they suit engineers coming from backend, DevOps or cloud work.

Each project is a single short file you can read in ten minutes, plus a README with **experiments to try**. The experiments are where the learning happens.

See **[LEARNING-PATH.md](LEARNING-PATH.md)** for the full study plan these projects go with.

## Projects

| # | Project | You learn | Stack |
|---|---|---|---|
| 01 | [First agent: calculator](01-first-agent-calculator/) | the tool-calling loop, by hand | Anthropic SDK |
| 02 | [Weather and currency](02-weather-currency-agent/) | calling live APIs, handling errors | httpx |
| 03 | [File organiser](03-file-organiser-agent/) | agents that change things: dry run, sandboxing | pathlib |
| 04 | [Log analyser](04-log-analyser-agent/) | inputs bigger than the context window, structured output | regex |
| 05 | [Kubernetes helper](05-kubernetes-helper-agent/) | safe tools: read-only allow-lists | kubectl |
| 06 | [Config reviewer](06-config-reviewer-agent/) | prompt design, JSON schemas, a first eval | |
| 07 | [Cloud cost agent](07-cloud-cost-agent/) | exact numbers via Pandas tools, chat memory | Pandas |
| 08 | [Chat with your docs](08-chat-with-docs-rag/) | **RAG**: chunking, embeddings, vector search, citations | Chroma |
| 09 | [On-call runbook agent](09-runbook-agent/) | RAG plus tools, human-in-the-loop approval | |
| 10 | [Your own MCP server](10-mcp-server/) | **MCP** tools and resources, server and client | MCP SDK |
| 11 | [Incident assistant](11-langgraph-incident-assistant/) | graphs, state, conditional routing | **LangGraph** |
| 12 | [Multi-agent DevOps assistant](12-google-adk-agent/) | sub-agents, `adk web` | **Google ADK** |
| 13 | [Evals](13-evals/) | measuring quality: retrieval, facts, LLM-as-judge | |

Do them in order: each builds on ideas from the ones before. Projects 02 onwards use a small helper, [`src/agentkit`](src/agentkit/agent.py), which is the same loop you write by hand in project 01.

## Setup

Requires Python 3.11 or newer.

```bash
git clone https://github.com/askmohanty/ai-engineer-starter-projects.git
cd ai-engineer-starter-projects

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[all]"            # or only what you need, e.g. ".[rag]" or ".[langgraph]"

cp .env.example .env               # then add your ANTHROPIC_API_KEY
```

- Projects 01–11 and 13 use Claude: get an API key at [console.anthropic.com](https://console.anthropic.com). Set `ANTHROPIC_MODEL` in `.env` to try a different model.
- Project 12 uses Gemini: a free key from [Google AI Studio](https://aistudio.google.com/apikey).

Run every project from the repository root, for example `python 04-log-analyser-agent/agent.py`.

## Ground rules the projects follow

- **Safety lives in the tool, not the prompt.** Agents get read-only tools, allow-lists, sandboxed paths and dry runs. A model can be talked into anything; a tool that can't delete can't be talked into deleting.
- **Models explain; code calculates.** Exact numbers come from Python tools, never from the model's head.
- **Measure it.** If you can't say how often it's right, you don't know whether a change helped (projects 06 and 13).

## License

MIT
