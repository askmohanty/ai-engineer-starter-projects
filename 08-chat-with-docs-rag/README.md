# 08 · Chat with your docs (RAG)

Answers questions from a folder of documents, here five sample on-call runbooks in [`docs/`](docs/), and cites its sources.

**You learn: retrieval-augmented generation (RAG)**, the most common AI feature in companies today.

1. **Ingest:** load documents, split them into chunks, turn each chunk into an *embedding* (a vector capturing its meaning) and store the vectors in a vector database (Chroma, locally).
2. **Retrieve:** embed the question and find the closest chunks.
3. **Generate:** give the model only those chunks and tell it to answer from them and cite them.

All of it is in [`rag.py`](rag.py), about 100 lines.

```bash
python 08-chat-with-docs-rag/ingest.py
python 08-chat-with-docs-rag/ask.py "Payments are timing out, what should I check?"
python 08-chat-with-docs-rag/ask.py --show-chunks "What does exit code 137 mean?"
```

The first `ingest` downloads a small embedding model (about 80 MB) and then runs offline.

> **Windows:** if `ingest.py` exits with no message, a "Segmentation fault", or `DLL load failed while importing onnxruntime_pybind11_state`, install the latest [Microsoft Visual C++ Redistributable (x64)](https://learn.microsoft.com/cpp/windows/latest-supported-vc-redist) and run it again. Chroma and its embedding model use native libraries that need it.

## Try this

1. Ask something the docs don't cover ("How do I reset a user's password?"). Does it say it doesn't know?
2. Use `--show-chunks` to see exactly what the model was given. When an answer is wrong, was retrieval wrong (wrong chunks) or generation wrong (right chunks, bad answer)? This is the main debugging skill for RAG.
3. Change `max_chars` in `chunk()` to 200, then to 3000. Re-ingest each time and ask the same questions.
4. Drop your own PDFs or Markdown into `docs/`, re-ingest and ask about them.
5. Replace Chroma with **pgvector** in Postgres (`CREATE EXTENSION vector`). Only `build_index` and `search` change.
6. Add a re-ranking step: fetch 10 chunks, ask the model to pick the best 4.
