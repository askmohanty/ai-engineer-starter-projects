# Runbook: Database connection timeouts

**Symptoms:** services log `Timed out ... waiting for a database connection`; the API gateway returns 504 on write endpoints.

## Check

1. Pool usage in the service logs (`Connection pool usage 10/10` means exhausted).
2. Active queries on Postgres: `SELECT pid, now() - query_start AS runtime, query FROM pg_stat_activity WHERE state = 'active' ORDER BY runtime DESC;`
3. Is a batch job running? The nightly `reporting-job` export starts at 10:05 and is the most common cause.

## Common causes

- A long-running query holding connections (usually the reporting export without a `LIMIT`).
- Connection leak after a deploy: pool usage rises and never falls.
- Postgres `max_connections` (set to 200) reached across all services.

## Fix

- If a reporting query is the cause, cancel it: `SELECT pg_cancel_backend(<pid>);` Use `pg_terminate_backend` only if cancel does not work.
- Long term, the reporting job must run against the read replica `db-replica:5432`, never the primary.
- The payment-service pool size is 10. Do not raise it above 20 without asking the database team.

**Owner:** Payments team, with the database team for Postgres changes.
