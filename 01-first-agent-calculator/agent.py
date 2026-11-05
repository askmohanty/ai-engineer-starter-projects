"""Project 01: the agent loop, written by hand.

The model cannot do reliable arithmetic, so we give it a calculator and a unit
converter. Read this file top to bottom: every later project is this loop with
different tools (via agentkit.run_agent).

    python 01-first-agent-calculator/agent.py "What is 18% GST on 45,000 rupees, and the total?"
"""

import ast
import operator
import sys

import anthropic
from dotenv import load_dotenv

load_dotenv()
MODEL = "claude-sonnet-5-5"

# --- Tools: plain Python functions ------------------------------------------

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calculate(expression: str) -> str:
    """Evaluate arithmetic safely. Never use eval() on text a model produced."""

    def evaluate(node: ast.AST) -> float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            left, right = evaluate(node.left), evaluate(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 100:
                raise ValueError("exponent too large")
            return OPERATORS[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](evaluate(node.operand))
        raise ValueError("only numbers and + - * / % ** ( ) are allowed")

    return str(evaluate(ast.parse(expression, mode="eval").body))


CONVERSIONS = {
    ("km", "miles"): lambda v: v * 0.621371,
    ("miles", "km"): lambda v: v / 0.621371,
    ("kg", "lb"): lambda v: v * 2.20462,
    ("lb", "kg"): lambda v: v / 2.20462,
    ("celsius", "fahrenheit"): lambda v: v * 9 / 5 + 32,
    ("fahrenheit", "celsius"): lambda v: (v - 32) * 5 / 9,
}


def convert_units(value: float, from_unit: str, to_unit: str) -> str:
    convert = CONVERSIONS.get((from_unit.lower(), to_unit.lower()))
    if convert is None:
        raise ValueError(f"cannot convert {from_unit} to {to_unit}; supported: {sorted(CONVERSIONS)}")
    return f"{convert(value):.4f} {to_unit}"


# --- Tool descriptions: what the model sees ----------------------------------

TOOLS = [
    {
        "name": "calculate",
        "description": "Evaluate an arithmetic expression, e.g. '45000 * 0.18'. Use it for every calculation.",
        "input_schema": {
            "type": "object",
            "properties": {"expression": {"type": "string", "description": "Arithmetic expression"}},
            "required": ["expression"],
        },
    },
    {
        "name": "convert_units",
        "description": "Convert between km/miles, kg/lb and celsius/fahrenheit.",
        "input_schema": {
            "type": "object",
            "properties": {
                "value": {"type": "number"},
                "from_unit": {"type": "string"},
                "to_unit": {"type": "string"},
            },
            "required": ["value", "from_unit", "to_unit"],
        },
    },
]
FUNCTIONS = {"calculate": calculate, "convert_units": convert_units}


# --- The loop ----------------------------------------------------------------

def main(question: str) -> None:
    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": question}]

    while True:
        response = client.messages.create(model=MODEL, max_tokens=1024, tools=TOOLS, messages=messages)
        messages.append({"role": "assistant", "content": response.content})

        # No tool requested: the model has its final answer.
        if response.stop_reason != "tool_use":
            print("".join(b.text for b in response.content if b.type == "text"))
            return

        # Run each requested tool and send the results back.
        results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            print(f"  -> {block.name}({block.input})")
            try:
                output, is_error = FUNCTIONS[block.name](**block.input), False
            except Exception as exc:
                output, is_error = str(exc), True
            results.append({"type": "tool_result", "tool_use_id": block.id, "content": output, "is_error": is_error})
        messages.append({"role": "user", "content": results})


if __name__ == "__main__":
    main(" ".join(sys.argv[1:]) or "What is 18% GST on 45,000 rupees, and the total? Also, 42 km in miles?")
