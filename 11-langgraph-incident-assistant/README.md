# 11 · Incident assistant with LangGraph

[LangGraph](https://langchain-ai.github.io/langgraph/) builds agents as **graphs**: each step is a node, and edges (some of them conditional) decide what runs next. Use it when you want *control* over the flow rather than leaving every decision to the model.

```
gather_logs ──► diagnose ──► severity high? ──► human_review ──► write_summary
                                  └── low ─────────────────────────┘
```

- `gather_logs` is plain Python with no model. Not every step needs AI.
- `diagnose` returns a typed Pydantic object (`with_structured_output`).
- A conditional edge sends high-severity incidents to a human before the summary is written.

**You learn:** state, nodes, edges and conditional routing in LangGraph; mixing deterministic code with model calls; where a person fits in an automated flow.

```bash
python 11-langgraph-incident-assistant/graph.py
python 11-langgraph-incident-assistant/graph.py --show-graph   # paste into https://mermaid.live
```

## Try this

1. Add a `check_runbook` node between `diagnose` and `human_review` that uses `rag.search` from project 08.
2. Replace the `input()` in `human_review` with LangGraph's built-in `interrupt()` and a checkpointer (`MemorySaver`), so the graph can pause, wait hours for approval, and resume. Read the LangGraph "human-in-the-loop" docs.
3. Turn `diagnose` into a ReAct agent that calls the project 10 MCP server's tools through `langchain-mcp-adapters`.
4. Add a retry loop: if the human rejects the plan, go back to `diagnose` with their feedback in the state.
5. Compare with project 09, where the model decides every step. When would you choose a graph, and when a free agent?
