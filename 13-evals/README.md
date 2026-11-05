# 13 · Evaluate your agent

Anyone can build an AI demo that works once. An AI engineer can show **how often** it works, and prove a change made it better rather than worse. That's what evals are for.

This project evaluates the RAG assistant from project 08 on ten questions ([`questions.jsonl`](questions.jsonl)), including one it *should* refuse to answer. Each question gets three checks:

| Check | How | Catches |
|---|---|---|
| **Retrieval** | was the right runbook among the retrieved chunks? | search problems |
| **Facts** | does the answer contain the must-have facts? | missing or wrong details |
| **Judge** | a second model call grades correctness and groundedness, given the sources | hallucination, vague answers |

```bash
python 08-chat-with-docs-rag/ingest.py
python 13-evals/run_evals.py
```

Results print as a table and are saved to `13-evals/results/` as JSON, so you can compare runs.

## The workflow to practise

1. Run the evals and note the scores. This is your **baseline**.
2. Change one thing: chunk size, the number of chunks `k`, the system prompt in `rag.py`, or the model.
3. Run the evals again. Better, worse, or the same?
4. Keep the change only if the scores went up.

## Try this

1. Add 10 harder questions, including ones whose answer spans two runbooks.
2. A failing *facts* check with a passing *judge* (or the reverse): which one was right? Read the answer. Judges make mistakes too.
3. Run the same eval three times. How much do the scores vary between runs?
4. Write an eval for project 04: does the incident report name `reporting-job` as the root cause?
5. Run the evals in CI (a GitHub Actions workflow) on every pull request that changes a prompt, and fail the build if the scores drop. If you know CI/CD, this is familiar ground.
