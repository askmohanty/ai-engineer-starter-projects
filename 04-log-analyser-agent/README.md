# 04 · Log analyser agent

An agent that investigates an application log the way an SRE would: summarise first, search for errors, then read around them to find what happened just before.

The sample log [`samples/app.log`](samples/app.log) has a real-looking incident. Payment timeouts are the symptom; the cause is earlier in the file.

**You learn:**
- **Working with inputs too big for the context window.** The agent never sees the whole file, only what its tools return.
- **Structured output.** `agentkit.extract` forces the model to fill a JSON schema, so the report can go straight into Jira, PagerDuty or a database.

```bash
python 04-log-analyser-agent/agent.py                       # the sample log
python 04-log-analyser-agent/agent.py /path/to/your/app.log
```

## Try this

1. Did it find the root cause, or stop at "database timeouts"? If it stopped, improve the system prompt.
2. Did it notice the unrelated warning near the end of the file (look at `other_findings`)?
3. Run it on a real log from your own systems (remove secrets first). Does the regex in `LINE` match your format?
4. Add a `time_window(start, end)` tool that returns lines between two timestamps.
5. Change `severity` in the schema to a number from 1 to 5 and see how the output changes.
