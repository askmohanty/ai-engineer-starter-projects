"""Project 06: review a Dockerfile or Kubernetes manifest.

One model call with a checklist and a forced JSON schema. Then a tiny eval:
for the sample files we know which problems exist, so we can measure how many
the model found.

    python 06-config-reviewer-agent/agent.py 06-config-reviewer-agent/samples/Dockerfile
    python 06-config-reviewer-agent/agent.py --check      # score against the known issues
"""

import json
import sys
from pathlib import Path

from agentkit import extract

HERE = Path(__file__).parent

SYSTEM = """You are a senior platform engineer reviewing infrastructure config.
Check at least: running as root, unpinned or :latest image tags, secrets in the
file, missing resource requests/limits, missing health checks/probes, privileged
or host access, image size and layer hygiene, and anything else that would fail
a production review. Report only real problems, each with a concrete fix."""

FINDINGS_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
                    "line": {"type": "integer"},
                    "issue": {"type": "string"},
                    "fix": {"type": "string"},
                },
                "required": ["severity", "issue", "fix"],
            },
        },
    },
    "required": ["summary", "findings"],
}


def review(path: Path) -> dict:
    numbered = "\n".join(f"{n}: {line}" for n, line in enumerate(path.read_text().splitlines(), 1))
    return extract(
        f"Review this file ({path.name}):\n\n{numbered}",
        name="report_findings",
        description="Report the review findings",
        schema=FINDINGS_SCHEMA,
        system=SYSTEM,
    )


def print_review(path: Path, result: dict) -> None:
    print(f"\n== {path.name}: {result['summary']}")
    for f in sorted(result["findings"], key=lambda f: ["critical", "high", "medium", "low"].index(f["severity"])):
        print(f"  [{f['severity'].upper():8}] line {f.get('line', '?')}: {f['issue']}\n             fix: {f['fix']}")


def check() -> None:
    """Score the reviewer: did it find each known problem in the samples?"""
    expected = json.loads((HERE / "samples" / "expected.json").read_text())
    found_total = expected_total = 0
    for name, issues in expected.items():
        path = HERE / "samples" / name
        result = review(path)
        print_review(path, result)
        text = json.dumps(result).lower()
        for issue in issues:
            hit = any(keyword in text for keyword in issue["any_of"])
            found_total += hit
            expected_total += 1
            print(f"  {'FOUND ' if hit else 'MISSED'} {issue['name']}")
    print(f"\nScore: {found_total}/{expected_total} known issues found")


if __name__ == "__main__":
    if sys.argv[1:] == ["--check"]:
        check()
    else:
        for arg in sys.argv[1:] or [str(HERE / "samples" / "Dockerfile")]:
            print_review(Path(arg), review(Path(arg)))
