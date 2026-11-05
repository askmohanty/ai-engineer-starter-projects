# Runbook: Pod in CrashLoopBackOff

**Meaning:** the container starts, exits, and Kubernetes keeps restarting it with a growing back-off (10s, 20s, 40s ... up to 5 minutes).

## Check

1. `kubectl get pods -n <namespace>`: note the RESTARTS count.
2. `kubectl describe pod <pod> -n <namespace>`: read **Last State**, **Exit Code** and **Events**.
3. `kubectl logs <pod> -n <namespace> --previous`: the logs of the crashed container, not the current one.

## Exit codes

- **1**: application error. Read the previous logs; often a missing environment variable or config file.
- **137**: killed with SIGKILL, usually **OOMKilled**. Raise the memory limit or fix the leak.
- **143**: SIGTERM; the liveness probe may be failing and Kubernetes is restarting it.

## Fix

- Missing config: check the Deployment's `env` and `envFrom`, and that the referenced ConfigMap or Secret exists.
- OOMKilled: compare `kubectl top pod` with the limit. Raise the limit by at most 50% at a time.
- Do not delete the pod to "fix" it; the ReplicaSet recreates it with the same problem.

**Owner:** the team that owns the service. Platform team helps with cluster issues.
