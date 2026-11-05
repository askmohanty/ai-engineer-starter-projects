# Learning path: from Java, DevOps and cloud to AI engineer

This path is for someone who already writes software and runs it in production: Java, Git, Linux, Docker, Kubernetes, CI/CD and a cloud platform. Those skills carry over. What's new is Python, how models work, and how to build and run reliable applications on top of them.

Roughly 5–6 months part-time. Do the projects in this repo alongside: each phase lists the ones that go with it.

## Phase 1: Python and maths refresher (3–4 weeks)

- Python for a Java developer: syntax, comprehensions, type hints, dataclasses, `async`, virtual environments, `pip` and `uv`
- NumPy, Pandas, Jupyter
- Maths, only what's needed: vectors, dot product, cosine similarity, probability basics, the idea of gradient descent
- Resources: the official Python tutorial; 3Blue1Brown, *Essence of Linear Algebra*

**Projects:** 01, 02, 03

## Phase 2: Machine learning and deep learning basics (5–6 weeks)

Not to become a researcher, but to understand what's happening inside the models.

- Supervised learning, overfitting, train/validation/test splits; precision, recall and F1
- Neural networks, backpropagation, PyTorch basics
- **Transformers and attention**
- Resources: Andrew Ng, *Machine Learning Specialization* (Coursera); Andrej Karpathy, *Neural Networks: Zero to Hero* (YouTube)

## Phase 3: LLM application engineering (8–10 weeks, the core of the job)

- How LLMs behave: tokens, context windows, temperature, cost and latency
- Model APIs (Claude, Gemini, OpenAI), streaming, **structured output**
- Prompt engineering
- **Tool use and the agent loop**
- Embeddings, vector databases (Chroma, pgvector, Qdrant), **RAG**: chunking, hybrid search, re-ranking
- **MCP (Model Context Protocol)**
- **Agent frameworks:**
  - **LangGraph**: agents as graphs with state, conditional edges, human-in-the-loop and checkpoints
  - **Google ADK (Agent Development Kit)**: multi-agent systems, workflow agents, `adk web`, deploying to Google Cloud
  - Claude Agent SDK, LlamaIndex
  - On the Java side: **Spring AI** and **LangChain4j**, so Java skills count directly
- **Evals:** test sets, LLM-as-judge, regression testing for prompts
- Resources: Anthropic's free courses and prompt engineering tutorial; DeepLearning.AI short courses on RAG, agents, LangGraph and evals; the LangGraph and ADK official docs and tutorials; Hugging Face LLM course

**Projects:** 04, 05, 06, 07, 08, 09, 10, 11 (LangGraph), 12 (ADK), 13 (evals)

## Phase 4: LLMOps, where DevOps experience is the advantage (4–6 weeks)

- Serving open models: vLLM, Ollama, TGI; GPUs on Kubernetes
- Managed AI platforms: AWS Bedrock, Google Vertex AI (and ADK's Agent Engine), Azure OpenAI
- Observability: Langfuse or LangSmith, OpenTelemetry for model and tool calls
- Cost control: prompt caching, model routing, rate limits
- **AI security:** prompt injection, PII handling, guardrails, least-privilege tools
- Fine-tuning basics (LoRA, QLoRA), and knowing when *not* to fine-tune

**Project ideas:** deploy project 08 or 12 to Kubernetes or Cloud Run with CI/CD; add tracing to project 09; run the evals from project 13 in a GitHub Actions workflow on every pull request.

## Phase 5: Portfolio

Three projects that show **Java + DevOps + AI** together:

1. A RAG assistant in **Spring Boot with Spring AI and pgvector**, deployed on Kubernetes with CI/CD
2. A multi-agent DevOps assistant (**LangGraph** or **ADK**) using your own **MCP server**, with evals
3. A self-hosted open model on Kubernetes (vLLM) with monitoring, evals and a cost dashboard

For each one, write a README covering the architecture, how quality was measured, and what it costs to run.

**Roles to target:** AI Engineer, LLMOps / MLOps Engineer, AI Platform Engineer.

**Certifications worth having:** AWS Certified AI Practitioner or Machine Learning Engineer – Associate; Google Cloud Professional Machine Learning Engineer; Azure AI Engineer Associate (AI-102). Pick the cloud you already know.
