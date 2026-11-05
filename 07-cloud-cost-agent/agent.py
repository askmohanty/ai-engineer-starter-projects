"""Project 07: ask questions about a cloud bill.

Pandas does the maths; the model decides which questions to ask of the data and
explains the answer. The model never sees the raw rows, only tool results, so
the numbers are exact.

    python 07-cloud-cost-agent/agent.py "What grew most from September to October, and why might that be?"
"""

import sys
from pathlib import Path

import pandas as pd

from agentkit import Tool, chat, run_agent


def make_tools(csv_path: Path) -> list[Tool]:
    df = pd.read_csv(csv_path)

    def describe_data() -> dict:
        return {
            "rows": len(df),
            "columns": {c: str(t) for c, t in df.dtypes.items()},
            "months": sorted(df["month"].unique().tolist()),
            "distinct_values": {c: sorted(df[c].unique().tolist()) for c in ["service", "region", "team"]},
        }

    def cost_by(group_by: list[str], month: str | None = None) -> list[dict]:
        data = df if month is None else df[df["month"] == month]
        totals = data.groupby(group_by)["cost_usd"].sum().round(2).sort_values(ascending=False)
        return totals.reset_index().to_dict("records")

    def month_over_month(group_by: str = "service") -> list[dict]:
        pivot = df.pivot_table(index=group_by, columns="month", values="cost_usd", aggfunc="sum")
        first, last = pivot.columns.min(), pivot.columns.max()
        pivot["change_usd"] = pivot[last] - pivot[first]
        pivot["change_pct"] = (pivot["change_usd"] / pivot[first] * 100).round(1)
        return pivot.round(2).sort_values("change_usd", ascending=False).reset_index().to_dict("records")

    return [
        Tool("describe_data", "Columns, months and the distinct services, regions and teams.", {}, describe_data),
        Tool(
            "cost_by",
            "Total cost grouped by one or more columns (service, region, team, month), optionally for one month.",
            {
                "group_by": {"type": "array", "items": {"type": "string"}},
                "month": {"type": "string", "description": "e.g. 2026-10"},
            },
            cost_by,
            required=["group_by"],
        ),
        Tool(
            "month_over_month",
            "Change between the first and last month, by service, region or team, biggest increase first.",
            {"group_by": {"type": "string", "enum": ["service", "region", "team"]}},
            month_over_month,
            required=[],
        ),
    ]


SYSTEM = """You are a FinOps analyst. Answer with exact figures from the tools (in
USD), never estimate. When costs change, suggest the most likely technical causes
an engineer should check (for example NAT Gateway traffic that should go through
a VPC endpoint, or log volume)."""

if __name__ == "__main__":
    tools = make_tools(Path(__file__).parent / "samples" / "billing.csv")
    if len(sys.argv) > 1:
        answer, _ = run_agent(" ".join(sys.argv[1:]), tools, SYSTEM)
        print(answer)
    else:
        chat(tools, SYSTEM)
