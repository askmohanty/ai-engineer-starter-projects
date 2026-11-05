# 01 · First agent: calculator

The agent loop, written by hand with the Anthropic SDK. Language models are bad at exact arithmetic, so the agent gets a calculator and a unit converter and decides for itself when to use them.

**You learn:** the tool-calling loop. The model either answers or asks for a tool; your code runs the tool and sends back the result; repeat until it answers. Every agent framework (LangGraph, Google ADK, the Claude Agent SDK) is this loop underneath.

```bash
python 01-first-agent-calculator/agent.py "What is 18% GST on 45,000 rupees, and the total?"
```

The `-> calculate(...)` lines show each tool call the model made.

## How it works (theory)

A language model only produces text, and it predicts plausible text rather than computing it, which is why "what is 18% of 45,000?" can come back slightly wrong. **Tool calling** fixes this. You describe a function to the model (name, description, JSON schema of its arguments). When the model decides it needs the function, it doesn't run it; it replies with a structured request (`stop_reason == "tool_use"`, plus the tool name and arguments). Your code runs the function and sends the result back as a `tool_result` message. The model reads it and either answers or asks for another tool.

That loop, **model → tool request → your code runs it → result → model**, is what "agent" means. Note three things in `agent.py`:
- The whole conversation is resent on every call, because the model has no memory between requests.
- Errors go back to the model as tool results (`is_error`), so it can recover instead of crashing.
- `calculate()` parses the expression instead of calling `eval()`: text from a model is untrusted input.

Read more: [How LLMs work](../concepts/01-how-llms-work.md) · [Tool calling and agents](../concepts/03-tool-calling-and-agents.md)

## Try this

1. Ask something that needs no tool ("What is GST?"). Does it still call one?
2. Ask for a conversion it doesn't support ("10 litres in gallons"). Read how the error goes back to the model and what it does with it.
3. Add a `percentage_change(old, new)` tool. Write the function, describe it in `TOOLS`, register it in `FUNCTIONS`.
4. Make the tool description vague ("does maths"). Does the model use it less reliably? Tool descriptions are prompts.
5. Why does `calculate` parse the expression instead of calling `eval()`? Try asking it to calculate `__import__('os').getcwd()`.
