# 02 · Weather and currency agent

An agent that calls two real, free APIs (no keys needed): [Open-Meteo](https://open-meteo.com) for weather and [Frankfurter](https://frankfurter.dev) for exchange rates.

From here on, projects use `agentkit.run_agent` (in [`src/agentkit/agent.py`](../src/agentkit/agent.py)). It's the same loop you wrote in project 01, so each project only has to define its tools.

**You learn:** connecting an agent to live data; how API errors reach the model; how the system prompt shapes the answer.

```bash
python 02-weather-currency-agent/agent.py "Should I carry an umbrella in Pune tomorrow? And what's 500 USD in INR?"
```

## Try this

1. Ask about a city that doesn't exist. What does the agent say?
2. Ask "Is it warmer in Delhi or Bengaluru right now?" Count the tool calls. Did it call `get_weather` twice in one turn?
3. Turn off your network and run it. How should an agent tell the user an API is down?
4. Add a tool using another free API, for example public holidays from [Nager.Date](https://date.nager.at).
