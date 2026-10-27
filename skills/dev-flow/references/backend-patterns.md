# Backend patterns

The user's reference list of production backend projects (sources/code-prompt/prompt-6.md). When a feature you're designing
looks like one of these, use the matching "why" as the design checklist, and say which pattern you're applying.
Don't build the whole project. Take only the part the feature needs.

| Feature looks like | Pattern | Check for |
|---|---|---|
| short IDs, redirects, hot reads | URL shortener | ID generation (collision-free), read-through cache, rate limit, capacity math |
| per-user/IP limits across instances | Distributed rate limiter | token bucket or sliding window in a shared store, never per-process memory |
| background work, emails, webhooks | Job queue with retries | backoff with jitter, dead-letter queue, idempotent jobs ("at least once" = "sometimes twice") |
| live updates, presence, chat | Chat server | reconnects, delivery receipts, presence cleanup on disconnect |
| money, credits, balances | Payments ledger | double-entry, idempotency keys, reconciliation job |
| schema change on a live table | Zero-downtime migration | expand → backfill → switch → contract, run under load |

## Original prompt (verbatim)

As a Backend Engineer, you must build these projects.

1.) URL shortener that survives 10x traffic
Build: Postgres + Redis cache + rate limiting, load tested to 5,000 requests a second.
Why: caching, ID generation and capacity math in one project.

2.) Distributed rate limiter
Build: token bucket and sliding window in Redis, shared by 3 app servers.
Why: it shows up in almost every Senior loop.

3.) Job queue with retries
Build: workers with backoff, a dead-letter queue and idempotent jobs.
Why: you learn that "at least once" means "sometimes twice."

4.) Chat server
Build: WebSockets, presence, delivery receipts, reconnects.
Why: real-time is where most candidates start guessing.

5.) Payments ledger
Build: double-entry ledger with idempotency keys and nightly reconciliation.
Why: money forces you to care about correctness.

6.) Zero-downtime migration
Build: rename a column on a 10M-row table while a load test runs.
Why: the Senior skill nobody practises.

Put the load test numbers in your README. That's your system design round, already rehearsed.

