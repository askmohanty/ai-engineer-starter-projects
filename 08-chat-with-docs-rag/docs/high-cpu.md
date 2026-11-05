# Runbook: High CPU on a service

**Alert:** `ServiceCPUHigh` fires when a service uses more than 80% of its CPU limit for 15 minutes.

## Check

1. `kubectl top pods -n <namespace> -l app=<service>`: is it every pod or one?
2. Request rate on the service dashboard. If traffic doubled, CPU doubling is expected.
3. CPU throttling: `container_cpu_cfs_throttled_periods_total` in Grafana. Throttling with low usage means the limit is too low.

## Fix

- Traffic growth: the HorizontalPodAutoscaler scales between 2 and 10 replicas at 70% CPU. Check it is not already at max: `kubectl get hpa -n <namespace>`.
- One hot pod: likely a stuck request or a retry loop. Take a thread dump (Java: `jcmd <pid> Thread.print`) before restarting it.
- Raise the HPA maximum only with the service owner's agreement; it increases cost.

**Owner:** the team that owns the service.
