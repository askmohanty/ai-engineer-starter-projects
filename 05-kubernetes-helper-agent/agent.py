"""Project 05: a read-only Kubernetes helper.

The agent can run kubectl, but only verbs that read, and never against secrets.
It cannot delete, exec, apply, scale or edit anything.

    python 05-kubernetes-helper-agent/agent.py "Why is a pod in the default namespace crashing?"
"""

import shutil
import subprocess
import sys

from agentkit import Tool, run_agent

READ_ONLY_VERBS = {"get", "describe", "logs", "top", "events", "explain", "api-resources", "version"}
BLOCKED_WORDS = {"secret", "secrets", "--kubeconfig", "--token", "--as"}
MAX_OUTPUT = 8000


def kubectl(args: list[str]) -> str:
    if not args or args[0] not in READ_ONLY_VERBS:
        raise PermissionError(f"only these verbs are allowed: {sorted(READ_ONLY_VERBS)}")
    if any(word in arg.lower() for arg in args for word in BLOCKED_WORDS):
        raise PermissionError("secrets and credential flags are not allowed")
    if shutil.which("kubectl") is None:
        raise FileNotFoundError("kubectl is not installed or not on PATH")

    # A list of arguments, never a shell string, so nothing can be injected.
    result = subprocess.run(["kubectl", *args], capture_output=True, text=True, timeout=30)
    output = (result.stdout + result.stderr).strip()
    if len(output) > MAX_OUTPUT:
        output = output[:MAX_OUTPUT] + f"\n... truncated ({len(output)} characters)"
    return output or "(no output)"


TOOLS = [
    Tool(
        "kubectl",
        "Run a read-only kubectl command. Pass the arguments after 'kubectl' as a list, "
        "e.g. ['get', 'pods', '-n', 'default'] or ['logs', 'my-pod', '--previous', '--tail', '50'].",
        {"args": {"type": "array", "items": {"type": "string"}}},
        kubectl,
    )
]

SYSTEM = """You are a Kubernetes troubleshooting assistant with read-only access.
Work like an experienced engineer: get pods, describe the failing one, read its
events and (previous) logs, then explain the cause in plain English. If a fix
needs a write action, give the exact command for the human to run; you cannot
run it yourself."""

if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "Are any pods unhealthy in any namespace? If so, why?"
    answer, _ = run_agent(question, TOOLS, SYSTEM, max_turns=15)
    print(answer)
