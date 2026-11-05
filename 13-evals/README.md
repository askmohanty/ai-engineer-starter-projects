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

## How it works (theory)

**Why AI needs evals.** A unit test passes or fails the same way every time. A model's output varies between runs, and a prompt change that fixes one question can quietly break three others. So instead of a single assertion, you measure *rates* over a dataset: "9 of 10 correct, 10 of 10 grounded".

**Three graders, three questions.**
- **Retrieval check:** was the source runbook among the retrieved chunks? It isolates the search half of RAG.
- **Facts check:** does the answer contain the must-have facts? Cheap and deterministic, but brittle: "ninety-two percent" fails a check for "92".
- **LLM-as-judge:** a second model call with a rubric, the question, the sources and the answer returns structured grades. *Correct* means it answers the question; *grounded* means every claim is supported by the sources. Judges are flexible but can be wrong, so spot-check them yourself.

**The unanswerable question** (resetting an Active Directory password) checks that the system says "I don't know" instead of inventing an answer. Refusal behaviour is part of quality.

**Comparing runs.** Results are saved with a timestamp so you can compare a baseline with a change. That's the discipline: change one variable, re-run, keep the change only if the numbers improve.

Read more: [Evals](../concepts/07-evals.md)

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
