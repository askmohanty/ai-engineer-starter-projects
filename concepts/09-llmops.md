# 9 · LLMOps: running AI in production

Building an agent that works on your laptop is half the job. Running it reliably, cheaply and observably for real users is the other half. This is where DevOps and cloud experience is the biggest advantage.

## Ways to run a model

| Option | What it is | Trade-offs |
|---|---|---|
| **Provider API** | Anthropic, OpenAI, Google Gemini | Fastest start, best models; data leaves your network; pay per token |
| **Cloud-managed** | AWS Bedrock, Google Vertex AI, Azure OpenAI / AI Foundry | Same models inside your cloud account, IAM, VPC and billing |
| **Self-hosted open models** | Llama, Mistral, Qwen, Gemma served with **vLLM**, **TGI** or **Ollama** | Full control and data stays in; you own the GPUs, scaling and upgrades |

Self-hosting on Kubernetes means GPU node pools, the NVIDIA device plugin, autoscaling on queue depth or tokens per second rather than CPU, and large container images with model weights.

## Deploying an agent

An agent is usually just a web service: FastAPI (Python) or Spring Boot (Java) in a container, behind your normal CI/CD. AI-specific concerns:
- **Streaming** responses (server-sent events) so users see tokens as they arrive.
- **Long-running work:** agent runs can take minutes; use queues and background workers, not one HTTP request.
- **State:** conversation history and checkpoints in Redis or Postgres, not in memory.
- **Secrets:** API keys in a secret manager, rotated, never in images or prompts.
- **Framework deploy paths:** `adk deploy cloud_run` or Vertex AI Agent Engine (ADK); LangGraph Platform; or your own container.

## Observability

Logs and metrics aren't enough; you need **traces of every step**: each model call (prompt, response, tokens, latency, cost), each tool call and its result, and how they chain together.

- **Tools:** Langfuse (open source), LangSmith, Arize Phoenix, plus OpenTelemetry, which now has semantic conventions for generative AI.
- **Dashboards:** requests, error rate, latency (time to first token and total), tokens and cost per request, tool error rates, eval scores over time.

## Cost control

Cost is roughly *tokens × price per token × requests*. Levers:
- **Pick the right model per step:** small models for routing and classification, large ones for hard reasoning.
- **Prompt caching:** providers discount repeated prompt prefixes (long system prompts, tool definitions, documents).
- **Trim context:** fewer, better RAG chunks; summarise long histories.
- **Cache answers** to repeated questions.
- **Batch APIs** for non-urgent bulk jobs, usually at a discount.
- **Limits:** per-user rate limits, `max_tokens`, `max_turns`, budget alerts.

## Reliability

- **Retries with back-off** for rate limits (HTTP 429) and overloaded errors; the SDKs retry by default.
- **Timeouts** on model and tool calls.
- **Fallback models** or providers.
- **Validate structured output** and retry on failure.
- **Evals in CI** so a prompt or model change can't silently degrade quality ([concept 7](07-evals.md)).
- **Version prompts** like code, and roll out changes gradually.

## Fine-tuning, briefly

Fine-tuning trains an existing model further on your examples. Parameter-efficient methods like **LoRA** and **QLoRA** make this possible on a single GPU. It can teach a consistent format, style or narrow skill, or let a small model match a big one on one task. It's rarely the first step: try prompting, tools and RAG first, and fine-tune only when evals show they aren't enough ([concept 4](04-embeddings-and-rag.md#rag-versus-fine-tuning)).

## Further reading

- vLLM docs (docs.vllm.ai) and Ollama (ollama.com)
- Langfuse docs (langfuse.com); OpenTelemetry semantic conventions for generative AI
- Anthropic docs, *Prompt caching* and *Message batches*
- Hugging Face, *PEFT* library docs (LoRA)
