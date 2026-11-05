# Concepts: the theory behind the projects

Short, plain-English explanations of the ideas the projects use. Read a concept, then do the project that puts it into practice, then do that project's **Try this** experiments.

| # | Concept | What you'll understand | Put it into practice |
|---|---|---|---|
| 1 | [How LLMs work](01-how-llms-work.md) | tokens, context windows, temperature, hallucination | all projects |
| 2 | [Prompting and structured output](02-prompting-and-structured-output.md) | system prompts, good instructions, reliable JSON | [04](../04-log-analyser-agent/), [06](../06-config-reviewer-agent/) |
| 3 | [Tool calling and agents](03-tool-calling-and-agents.md) | the agent loop, workflows versus agents, memory, tool design | [01](../01-first-agent-calculator/), [02](../02-weather-currency-agent/), [03](../03-file-organiser-agent/), [07](../07-cloud-cost-agent/) |
| 4 | [Embeddings and RAG](04-embeddings-and-rag.md) | vectors, chunking, retrieval, grounding, RAG versus fine-tuning | [08](../08-chat-with-docs-rag/), [09](../09-runbook-agent/) |
| 5 | [MCP](05-mcp.md) | hosts, clients, servers; tools, resources, prompts; transports | [10](../10-mcp-server/) |
| 6 | [Agent frameworks](06-agent-frameworks.md) | LangGraph graphs, Google ADK multi-agent systems, how to choose | [11](../11-langgraph-incident-assistant/), [12](../12-google-adk-agent/) |
| 7 | [Evals](07-evals.md) | datasets, graders, LLM-as-judge, evals in CI | [06](../06-config-reviewer-agent/), [13](../13-evals/) |
| 8 | [Agent safety](08-agent-safety.md) | prompt injection, least privilege, human in the loop | [03](../03-file-organiser-agent/), [05](../05-kubernetes-helper-agent/), [09](../09-runbook-agent/) |
| 9 | [LLMOps](09-llmops.md) | serving models, observability, cost, reliability, fine-tuning | deploy any project |

## Glossary

| Term | Meaning |
|---|---|
| **Agent** | A model using tools in a loop until a task is done |
| **Context window** | The maximum tokens a model can consider in one request |
| **Embedding** | A vector of numbers representing a text's meaning |
| **Eval** | A repeatable test that scores an AI system's outputs |
| **Few-shot** | Showing the model a few examples in the prompt |
| **Fine-tuning** | Further training a model on your own examples |
| **Grounding** | Making the model answer from given sources, not memory |
| **Hallucination** | Fluent, confident output that isn't true |
| **Human in the loop** | A person approves an agent's action before it happens |
| **LLM** | Large language model: a neural network that predicts the next token |
| **LLM-as-judge** | Using a model to grade another model's output |
| **MCP** | Model Context Protocol, the open standard for connecting AI apps to tools and data |
| **Prompt injection** | Instructions hidden in data that hijack a model |
| **RAG** | Retrieval-augmented generation: retrieve relevant documents, then answer from them |
| **Structured output** | Model output that follows a JSON schema |
| **System prompt** | Standing instructions that shape every response |
| **Temperature** | How random the model's sampling is |
| **Token** | A chunk of text, about ¾ of a word; the unit of cost |
| **Tool calling** | The model asking your code to run a function |
| **Vector database** | A store that finds the vectors nearest to a query |
