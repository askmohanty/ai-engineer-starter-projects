# Runbook: TLS or signing certificate expiring

**Alert:** `CertificateExpiringSoon` fires 14 days before expiry and pages on-call at 3 days.

## Check

1. Which certificate: the alert label `secret_name` gives the Kubernetes Secret.
2. Expiry date: `kubectl get certificate -A` (cert-manager) or
   `echo | openssl s_client -connect <host>:443 2>/dev/null | openssl x509 -noout -enddate`.
3. Why it did not renew: `kubectl describe certificate <name> -n <namespace>` and the cert-manager logs.

## Fix

- cert-manager certificates renew automatically 30 days before expiry. If one has not, the usual cause is a failing DNS-01 or HTTP-01 challenge.
- Force a renewal: `cmctl renew <name> -n <namespace>`.
- The auth-service JWT signing certificate is **not** managed by cert-manager. It is rotated by the security team using the key-rotation pipeline; raise a ticket in the SEC queue at least 5 days before expiry.

**Owner:** Platform team for TLS; Security team for signing keys.
