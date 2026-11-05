"""Project 09: an on-call agent that combines RAG, read-only checks and a human.

Give it an alert. It finds the matching runbook (RAG from project 08), runs the
read-only checks it can, and when a fix needs a change it PROPOSES the command
and waits for you to approve. Approved commands are printed, never executed:
running them is your job.

    python 08-chat-with-docs-rag/ingest.py      # once, builds the index
    python 09-runbook-agent/agent.py
"""

import shutil
import socket
import sys
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "08-chat-with-docs-rag"))
import rag  # noqa: E402  (project 08's RAG module)

from agentkit import Tool, chat  # noqa: E402


def search_runbooks(query: str) -> list[dict]:
    return rag.search(query, k=3)


def check_disk(path: str = "/") -> dict:
    usage = shutil.disk_usage(path)
    return {"path": path, "used_pct": round(usage.used / usage.total * 100, 1), "free_gb": round(usage.free / 1e9, 1)}


def check_http(url: str) -> dict:
    try:
        response = httpx.get(url, timeout=5, follow_redirects=True)
        return {"url": url, "status": response.status_code, "ms": round(response.elapsed.total_seconds() * 1000)}
    except httpx.HTTPError as exc:
        return {"url": url, "error": f"{type(exc).__name__}: {exc}"}


def check_port(host: str, port: int) -> dict:
    try:
        with socket.create_connection((host, port), timeout=3):
            return {"host": host, "port": port, "open": True}
    except OSError as exc:
        return {"host": host, "port": port, "open": False, "error": str(exc)}


def check_dns(hostname: str) -> dict:
    try:
        return {"hostname": hostname, "addresses": sorted({a[4][0] for a in socket.getaddrinfo(hostname, None)})}
    except socket.gaierror as exc:
        return {"hostname": hostname, "error": str(exc)}


def propose_action(command: str, reason: str) -> str:
    """Human in the loop: the agent asks, a person decides."""
    print(f"\n  PROPOSED ACTION: {command}\n  REASON: {reason}")
    decision = input("  Approve? [y/N] ").strip().lower()
    if decision == "y":
        return f"APPROVED by the human. They will run it themselves: {command}"
    return "REJECTED by the human. Do not propose it again; suggest an alternative or stop."


TOOLS = [
    Tool("search_runbooks", "Search the team's runbooks. Always do this first for any alert.",
         {"query": {"type": "string"}}, search_runbooks),
    Tool("check_disk", "Disk usage on THIS machine for a path.", {"path": {"type": "string"}}, check_disk, required=[]),
    Tool("check_http", "HTTP GET a URL and report status and latency.", {"url": {"type": "string"}}, check_http),
    Tool("check_port", "Check whether a TCP port is reachable.",
         {"host": {"type": "string"}, "port": {"type": "integer"}}, check_port),
    Tool("check_dns", "Resolve a hostname.", {"hostname": {"type": "string"}}, check_dns),
    Tool("propose_action",
         "Propose a command that CHANGES something. A human approves or rejects it; you never run it.",
         {"command": {"type": "string"}, "reason": {"type": "string"}}, propose_action),
]

SYSTEM = """You are an on-call assistant. For every alert or question:
1. Search the runbooks and follow the matching one. Quote which runbook you use.
2. Run the read-only checks you have tools for. Say plainly which runbook checks
   you cannot run yourself, and give the human the exact command.
3. Any change (delete, restart, cancel, scale, cordon) must go through
   propose_action, one at a time.
4. Remember what was already checked in this conversation; do not repeat it.
End each reply with a one-line status: RESOLVED, WAITING ON HUMAN, or ESCALATE TO <team>."""

if __name__ == "__main__":
    print("On-call assistant. Example: 'NodeDiskUsageHigh fired on this machine'")
    chat(TOOLS, SYSTEM, max_turns=20)
