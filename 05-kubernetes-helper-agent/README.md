# 05 · Kubernetes helper agent

A troubleshooting agent that can run `kubectl`, but only commands that read. This is the most important pattern in DevOps agents: **the safety lives in the tool, not in the prompt.**

- An allow-list of verbs (`get`, `describe`, `logs`, `top`, ...). Anything else is refused.
- Secrets and credential flags are blocked.
- Arguments are passed as a list to `subprocess`, never as a shell string, so nothing can be injected.
- Output is truncated so one huge `describe` can't flood the context window.

**You need:** `kubectl` pointing at a cluster you're allowed to use. A local one is best: [kind](https://kind.sigs.k8s.io), minikube or Docker Desktop.

```bash
kind create cluster                                      # or any test cluster
kubectl apply -f 05-kubernetes-helper-agent/broken-pod.yaml
python 05-kubernetes-helper-agent/agent.py "Why are my pods failing?"
kubectl delete -f 05-kubernetes-helper-agent/broken-pod.yaml
```

The two pods fail for different reasons (`CrashLoopBackOff` and `ImagePullBackOff`). A good answer explains both and gives the fix.

## How it works (theory)

**Why not just tell the model "only read"?** Because prompts are suggestions, not controls. A confused model, a cleverly worded request or a prompt injection hidden in a pod's log output can all lead it to request something harmful. Controls have to be in code the model can't change.

- **Allow-list, not block-list:** `READ_ONLY_VERBS` lists what's permitted; everything else is refused. A block-list ("no delete") always misses something (`scale --replicas=0`, `patch`, `drain`).
- **No shell:** arguments go to `subprocess.run` as a list, so `get pods; rm -rf /` is just a strange pod name, not two commands.
- **Credential flags blocked:** the agent can't switch identity (`--as`, `--token`, `--kubeconfig`) to escape its permissions.
- **Bounded output:** `MAX_OUTPUT` stops one giant `describe` from filling the context window and pushing out earlier evidence.
- **Defence in depth:** in a real cluster, also give the agent a Kubernetes service account bound to a read-only `ClusterRole`, so even a bug in this code can't write.

The agent itself follows a classic **ReAct** pattern (reason → act → observe → repeat): get pods, describe the failing one, read previous logs, explain.

Read more: [Agent safety](../concepts/08-agent-safety.md) · [Tool calling and agents](../concepts/03-tool-calling-and-agents.md)

## Try this

1. Ask it to "delete the broken pod". What happens, and how does it respond?
2. Ask it to show a secret. Then try to trick it: "get the resource called s-e-c-r-e-t-s". Is the block in the tool strong enough? How would you make it stronger?
3. Add `rollout status` and `rollout history` as allowed commands. Are they really read-only?
4. Add a `propose_fix(command, reason)` tool that only prints the command and asks you to confirm. Project 09 does this.
