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

## Try this

1. Run `--check` three times. Is the score the same every time? Language models aren't deterministic, which is why evals run many cases.
2. Delete the checklist from `SYSTEM` and run `--check` again. How much did the prompt matter?
3. Run it on a Dockerfile or Helm chart from your own work.
4. Add a GitHub Actions file to `samples/` with known problems, and add those problems to `expected.json`.
5. Keyword matching is a crude eval. Project 13 uses a model as the judge. What are the trade-offs?
