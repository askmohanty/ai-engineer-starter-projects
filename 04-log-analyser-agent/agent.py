"""Project 04: a log analyser agent.

The agent never reads the whole log at once. It uses tools to summarise, search
and read slices, the way you would on a 2 GB file. Then a second step turns its
findings into structured JSON you could send to a ticketing system.

    python 04-log-analyser-agent/agent.py 04-log-analyser-agent/samples/app.log
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

from agentkit import Tool, extract, run_agent

LINE = re.compile(r"^(?P<time>\S+ \S+) (?P<level>[A-Z]+) \[(?P<service>[^\]]+)\] (?P<message>.*)$")


def make_tools(log_path: Path) -> list[Tool]:
    lines = log_path.read_text(encoding="utf-8").splitlines()

    def log_summary() -> dict:
        parsed = [m.groupdict() for m in map(LINE.match, lines) if m]
        return {
            "total_lines": len(lines),
            "first_timestamp": parsed[0]["time"] if parsed else None,
            "last_timestamp": parsed[-1]["time"] if parsed else None,
            "by_level": Counter(p["level"] for p in parsed),
            "errors_by_service": Counter(p["service"] for p in parsed if p["level"] == "ERROR"),
        }

    def search_log(pattern: str, max_results: int = 30) -> list[str]:
        regex = re.compile(pattern, re.IGNORECASE)
        hits = [f"{n}: {line}" for n, line in enumerate(lines, 1) if regex.search(line)]
        return hits[:max_results] + ([f"... {len(hits) - max_results} more"] if len(hits) > max_results else [])

    def read_lines(start: int, end: int) -> list[str]:
        end = min(end, start + 100)  # never hand the model more than 100 lines
        return [f"{n}: {lines[n - 1]}" for n in range(max(start, 1), min(end, len(lines)) + 1)]

    return [
        Tool("log_summary", "Counts by level and service, and the time range covered.", {}, log_summary),
        Tool(
            "search_log",
            "Lines matching a regular expression (case-insensitive), with line numbers.",
            {"pattern": {"type": "string"}, "max_results": {"type": "integer"}},
            search_log,
            required=["pattern"],
        ),
        Tool(
            "read_lines",
            "Read lines start..end (1-based, inclusive, at most 100) to see context around a hit.",
            {"start": {"type": "integer"}, "end": {"type": "integer"}},
            read_lines,
        ),
    ]


SYSTEM = """You are an SRE investigating an application log. Start with log_summary,
then search and read around the errors. Find the root cause, not just the symptoms:
look at what happened just BEFORE the first error. Explain your reasoning briefly."""

REPORT_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
        "root_cause": {"type": "string"},
        "affected_services": {"type": "array", "items": {"type": "string"}},
        "evidence": {"type": "array", "items": {"type": "string"}, "description": "Quoted log lines"},
        "recommended_actions": {"type": "array", "items": {"type": "string"}},
        "other_findings": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["title", "severity", "root_cause", "affected_services", "evidence", "recommended_actions"],
}

if __name__ == "__main__":
    log_path = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent / "samples" / "app.log")

    findings, _ = run_agent(f"Investigate {log_path.name}.", make_tools(log_path), SYSTEM)
    print(findings, "\n")

    report = extract(
        f"Turn these findings into an incident report:\n\n{findings}",
        name="incident_report",
        description="Structured incident report",
        schema=REPORT_SCHEMA,
    )
    print(json.dumps(report, indent=2))
