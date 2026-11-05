# 02 · Weather and currency agent

An agent that calls two real, free APIs (no keys needed): [Open-Meteo](https://open-meteo.com) for weather and [Frankfurter](https://frankfurter.dev) for exchange rates.

From here on, projects use `agentkit.run_agent` (in [`src/agentkit/agent.py`](../src/agentkit/agent.py)). It's the same loop you wrote in project 01, so each project only has to define its tools.

**You learn:** connecting an agent to live data; how API errors reach the model; how the system prompt shapes the answer.

```bash
python 02-weather-currency-agent/agent.py "Should I carry an umbrella in Pune tomorrow? And what's 500 USD in INR?"
```

## How it works (theory)

A model's knowledge is frozen at its training cutoff: it doesn't know today's weather or exchange rate, and if asked it may **hallucinate** a confident, plausible number. Giving it a tool that calls a live API **grounds** the answer in real data.

The **system prompt** (`SYSTEM`) sets standing rules for every turn, here "use the tools for live data and say which date a rate is from". Small instructions like this change behaviour a lot.

A question about two cities usually produces **two tool calls in one turn**: models can request several independent tools at once, and the loop runs them all before the next model call.

When an API fails, `raise_for_status()` raises; `run_agent` sends the error text back to the model, which can retry, try another approach, or explain the failure. Good agents degrade gracefully instead of inventing an answer.

Read more: [Tool calling and agents](../concepts/03-tool-calling-and-agents.md) · [Prompting](../concepts/02-prompting-and-structured-output.md)

## Try this

1. Ask about a city that doesn't exist. What does the agent say?
2. Ask "Is it warmer in Delhi or Bengaluru right now?" Count the tool calls. Did it call `get_weather` twice in one turn?
3. Turn off your network and run it. How should an agent tell the user an API is down?
4. Add a tool using another free API, for example public holidays from [Nager.Date](https://date.nager.at).
