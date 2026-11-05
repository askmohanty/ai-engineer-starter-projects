# 01 · First agent: calculator

The agent loop, written by hand with the Anthropic SDK. Language models are bad at exact arithmetic, so the agent gets a calculator and a unit converter and decides for itself when to use them.

**You learn:** the tool-calling loop. The model either answers or asks for a tool; your code runs the tool and sends back the result; repeat until it answers. Every agent framework (LangGraph, Google ADK, the Claude Agent SDK) is this loop underneath.

```bash
python 01-first-agent-calculator/agent.py "What is 18% GST on 45,000 rupees, and the total?"
```

The `-> calculate(...)` lines show each tool call the model made.

## Try this

1. Ask something that needs no tool ("What is GST?"). Does it still call one?
2. Ask for a conversion it doesn't support ("10 litres in gallons"). Read how the error goes back to the model and what it does with it.
3. Add a `percentage_change(old, new)` tool. Write the function, describe it in `TOOLS`, register it in `FUNCTIONS`.
4. Make the tool description vague ("does maths"). Does the model use it less reliably? Tool descriptions are prompts.
5. Why does `calculate` parse the expression instead of calling `eval()`? Try asking it to calculate `__import__('os').getcwd()`.
