# 06 · Dockerfile and Kubernetes YAML reviewer

Reviews infrastructure files against a production checklist and returns structured findings: severity, line, issue and fix.

Not every useful AI feature needs a tool loop. This one is a single model call with a good prompt and a forced JSON schema.

**You learn:**
- prompt design: a checklist in the system prompt
- structured output with `agentkit.extract`
- **your first eval**: `--check` scores the reviewer against problems we know are in the sample files

```bash
python 06-config-reviewer-agent/agent.py 06-config-reviewer-agent/samples/Dockerfile
python 06-config-reviewer-agent/agent.py 06-config-reviewer-agent/samples/deployment.yaml
python 06-config-reviewer-agent/agent.py --check
```

## How it works (theory)

**Workflows before agents.** Reviewing one file is a known, fixed task, so there's no loop: a single model call with a strong prompt. Use the simplest design that works, and add autonomy only when the task needs it.

**The checklist is the expertise.** The system prompt lists what a production review covers (root user, unpinned tags, secrets, resources, probes, privileges). A model already "knows" these, but naming them makes it check every one consistently, the same reason human reviewers use checklists.

**Line numbers in the input.** The file is sent with numbered lines so the model can point to exact locations. Shaping the input is as important as wording the instructions.

**A first eval.** Because the sample files contain *known* problems ([`samples/expected.json`](samples/expected.json)), you can measure recall: how many known issues were found. Run it several times and the score changes, because models sample their output. One good run proves nothing; you need repeated, scored runs. Keyword matching is a crude grader; project 13 adds an LLM judge.

Read more: [Prompting and structured output](../concepts/02-prompting-and-structured-output.md) · [Evals](../concepts/07-evals.md)

## Try this

1. Run `--check` three times. Is the score the same every time? Language models aren't deterministic, which is why evals run many cases.
2. Delete the checklist from `SYSTEM` and run `--check` again. How much did the prompt matter?
3. Run it on a Dockerfile or Helm chart from your own work.
4. Add a GitHub Actions file to `samples/` with known problems, and add those problems to `expected.json`.
5. Keyword matching is a crude eval. Project 13 uses a model as the judge. What are the trade-offs?
