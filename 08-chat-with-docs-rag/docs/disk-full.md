# Runbook: Disk almost full on a node

**Alert:** `NodeDiskUsageHigh` fires when disk usage on any node is above 85% for 10 minutes. It pages on-call at 92%.

## Check

1. Confirm usage: `df -h /` and `df -h /var/lib/docker`.
2. Find the biggest directories: `du -xh / --max-depth=2 | sort -h | tail -20`.
3. On Kubernetes nodes, check image usage: `crictl images` and `crictl rmi --prune` (dry run first with `crictl images -q`).

## Common causes

- Application logs in `/var/log/app` not rotated. Logrotate keeps 7 days; anything older can be removed.
- Old container images after many deploys. The kubelet garbage-collects images above 80% usage, but only images not used by a running container.
- A core dump in `/var/crash`.

## Fix

- Delete logs older than 7 days: `find /var/log/app -name '*.log' -mtime +7 -delete`. This is safe; logs are also shipped to Loki.
- Never delete files under `/var/lib/etcd` or `/var/lib/kubelet` by hand.
- If usage is above 95% and still climbing, cordon the node (`kubectl cordon <node>`) so no new pods land there, then fix.

**Owner:** Platform team. Escalate in #platform-oncall after 30 minutes.
