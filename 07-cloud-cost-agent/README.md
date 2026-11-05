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

## Try this

1. Ask "how much did we spend on Lambda?" (it isn't in the data). Does it say so, or make something up?
2. Ask for a forecast for November. Should a FinOps agent forecast with only two months of data?
3. Export a real cost report from AWS Cost Explorer or Azure Cost Management, rename the columns to match, and ask about your own bill.
4. Add a `plot(group_by)` tool that saves a bar chart with matplotlib and returns the file path.
