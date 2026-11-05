# 07 · Cloud cost agent

Ask plain-English questions about a cloud bill. [`samples/billing.csv`](samples/billing.csv) is a made-up two-month AWS bill with three stories in it:
- one cost that jumped
- one that grew because of a configuration left on
- one saving

**You learn:** combining Pandas tools with a model. The model never does the arithmetic; it chooses which analysis to run and explains the result. This is how you stop a model inventing numbers.

```bash
python 07-cloud-cost-agent/agent.py "What grew most from September to October, and why might that be?"
python 07-cloud-cost-agent/agent.py      # chat mode: ask follow-up questions
```

In chat mode the agent keeps the conversation history, so "and for the platform team only?" works as a follow-up.

## How it works (theory)

**Models explain; code calculates.** A model reading 48 rows of CSV and adding them up will usually be close and sometimes wrong, and in finance "close" is wrong. Here the model never sees the raw data. It chooses an analysis (`cost_by`, `month_over_month`), Pandas computes exact figures, and the model interprets them. This split, deterministic tools for facts and the model for reasoning and language, is the most important pattern for trustworthy AI over data. (Text-to-SQL agents are the same idea with a database.)

**`describe_data` first.** The agent can discover the columns, months and distinct values before querying, so it doesn't guess names that don't exist. Giving an agent a way to inspect its environment cuts errors.

**Memory is resent history.** In chat mode, `agentkit.chat` keeps the message list and sends it all on every turn, so "and for the platform team only?" makes sense. The model itself remembers nothing; long chats grow in cost because the whole history is sent each time.

**Domain hints in the system prompt** (NAT Gateway versus VPC endpoints, log volume) steer the explanation towards what a FinOps engineer would check first.

Read more: [Tool calling and agents: memory](../concepts/03-tool-calling-and-agents.md#memory) · [How LLMs work: hallucination](../concepts/01-how-llms-work.md#hallucination)

## Try this

1. Ask "how much did we spend on Lambda?" (it isn't in the data). Does it say so, or make something up?
2. Ask for a forecast for November. Should a FinOps agent forecast with only two months of data?
3. Export a real cost report from AWS Cost Explorer or Azure Cost Management, rename the columns to match, and ask about your own bill.
4. Add a `plot(group_by)` tool that saves a bar chart with matplotlib and returns the file path.
