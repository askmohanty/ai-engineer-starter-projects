# 12 · Multi-agent DevOps assistant with Google ADK

[Google's Agent Development Kit (ADK)](https://google.github.io/adk-docs/) is Google's open-source framework for building agents and multi-agent systems. It runs with Gemini by default and deploys to Google Cloud (Vertex AI Agent Engine, Cloud Run).

This project is a **multi-agent** assistant:

```
devops_assistant (root)  ──►  log_agent   (tools: summarise_log, search_log)
                         └─►  cost_agent  (tools: cost_change_by)
```

The root agent reads each question and hands it to the right specialist. It reuses the sample log from project 04 and the bill from project 07, so you can compare ADK with the hand-written agents.

**You learn:**
- ADK's structure: `root_agent`, `sub_agents`, `instruction` and `description`
- **Tools are plain functions:** ADK reads the docstring and type hints, so write good docstrings
- `adk web`, a built-in UI that shows every model call, tool call and hand-off between agents (great for debugging)

## Setup

```bash
cp 12-google-adk-agent/devops_assistant/.env.example 12-google-adk-agent/devops_assistant/.env
# put a free Gemini API key from https://aistudio.google.com/apikey in that .env

cd 12-google-adk-agent
adk web                       # open http://localhost:8000 and pick devops_assistant
# or, in the terminal:
adk run devops_assistant
```

Ask: *"Why did orders fail this morning?"*, then *"Which service's cost grew the most?"* In `adk web`, open the **Events** tab to see the root agent transfer to each specialist.

## Try this

1. Remove the docstring from `search_log`. Does the agent still use it correctly?
2. Add a third specialist, `k8s_agent`, using the read-only `kubectl` function from project 05.
3. Connect the **MCP server from project 10** with ADK's `MCPToolset`, instead of duplicating the log tools. Look up "MCP tools" in the ADK docs; the class names have changed between versions, so follow the docs for your installed version.
4. Run it on Claude instead of Gemini: `pip install litellm`, then use `model=LiteLlm(model="anthropic/claude-sonnet-5-5")` (`from google.adk.models.lite_llm import LiteLlm`) and set `ANTHROPIC_API_KEY`.
5. Try ADK's workflow agents (`SequentialAgent`, `ParallelAgent`, `LoopAgent`) and rebuild project 11's flow. Compare it with LangGraph.
6. Deploy it: `adk deploy cloud_run`. If you've worked with containers and Cloud Run, this will feel familiar.
