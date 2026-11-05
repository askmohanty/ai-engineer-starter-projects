"""Project 12: a multi-agent DevOps assistant with Google's Agent Development Kit (ADK).

A root agent routes each question to a specialist sub-agent: one for logs, one
for cloud cost. In ADK, tools are plain Python functions; ADK builds the tool
description from the function's name, type hints and docstring.

    cd 12-google-adk-agent
    adk web                 # chat UI at http://localhost:8000, shows every step
    adk run devops_assistant
"""

import os
import re
from collections import Counter
from pathlib import Path

import pandas as pd
from google.adk.agents import Agent

MODEL = os.getenv("ADK_MODEL", "gemini-2.5-flash")
ROOT = Path(__file__).resolve().parents[2]
LOG = ROOT / "04-log-analyser-agent" / "samples" / "app.log"
BILLING = ROOT / "07-cloud-cost-agent" / "samples" / "billing.csv"
LINE = re.compile(r"^(?P<time>\S+ \S+) (?P<level>[A-Z]+) \[(?P<service>[^\]]+)\] (?P<message>.*)$")


# --- Tools for the log specialist ---------------------------------------------

def summarise_log() -> dict:
    """Summarise the application log: counts by level, errors by service, and time range."""
    parsed = [m.groupdict() for m in map(LINE.match, LOG.read_text(encoding="utf-8").splitlines()) if m]
    return {
        "status": "success",
        "first": parsed[0]["time"],
        "last": parsed[-1]["time"],
        "by_level": dict(Counter(p["level"] for p in parsed)),
        "errors_by_service": dict(Counter(p["service"] for p in parsed if p["level"] == "ERROR")),
    }


def search_log(pattern: str) -> dict:
    """Return log lines matching a case-insensitive regular expression, with line numbers.

    Args:
        pattern: A regular expression, for example "ERROR" or "reporting-job".
    """
    regex = re.compile(pattern, re.IGNORECASE)
    lines = LOG.read_text(encoding="utf-8").splitlines()
    return {"status": "success", "lines": [f"{n}: {l}" for n, l in enumerate(lines, 1) if regex.search(l)][:40]}


# --- Tools for the cost specialist --------------------------------------------

def cost_change_by(group_by: str) -> dict:
    """Cloud cost change from September to October 2026, biggest increase first.

    Args:
        group_by: One of "service", "region" or "team".
    """
    if group_by not in {"service", "region", "team"}:
        return {"status": "error", "error_message": "group_by must be service, region or team"}
    df = pd.read_csv(BILLING)
    pivot = df.pivot_table(index=group_by, columns="month", values="cost_usd", aggfunc="sum").round(2)
    pivot["change_usd"] = (pivot["2026-10"] - pivot["2026-09"]).round(2)
    rows = pivot.sort_values("change_usd", ascending=False).reset_index().to_dict("records")
    return {"status": "success", "rows": rows}


# --- Agents --------------------------------------------------------------------

log_agent = Agent(
    name="log_agent",
    model=MODEL,
    description="Investigates the application log: errors, timeouts, root causes.",
    instruction=(
        "You are an SRE. Use summarise_log first, then search_log around the errors. "
        "Find the root cause: what happened just BEFORE the first error. Quote log lines as evidence."
    ),
    tools=[summarise_log, search_log],
)

cost_agent = Agent(
    name="cost_agent",
    model=MODEL,
    description="Answers questions about the cloud bill and cost changes.",
    instruction=(
        "You are a FinOps analyst. Use cost_change_by for exact figures in USD; never estimate. "
        "Suggest likely technical causes for big changes."
    ),
    tools=[cost_change_by],
)

root_agent = Agent(
    name="devops_assistant",
    model=MODEL,
    description="Front door for DevOps questions.",
    instruction=(
        "Greet the user briefly. Send questions about logs, errors or incidents to log_agent, "
        "and questions about cloud spend to cost_agent. If a question is about neither, say what you can help with."
    ),
    sub_agents=[log_agent, cost_agent],
)
