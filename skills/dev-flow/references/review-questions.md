# Review questions

## After implementing (sources/code-prompt/prompt-4.md)

> can you tell me the inefficiency in these implementation?

Answer it about the code just written, not the whole repo:
- repeated work: loops inside loops over the same data, re-fetching, re-parsing, recomputing in render
- N+1 queries and network round trips that could be one batch
- unbounded work: no pagination, no limits, whole-file reads, growing in-memory lists
- wrong data structure: list scans where a map/set lookup fits
- needless abstraction or code that duplicates an existing helper (point at the helper)
- blocking work on a hot or user-facing path that could be deferred or queued

Every finding gets: `file:line`, why it costs (time, memory, money, round trips), and the smallest fix. Mark it
"measured" or "suspected". Suspected items go to `/perf` to measure before anything changes.

## Resilience and scale (sources/code-prompt/prompt-4-1.md)

> how can i improve and what happens if the server dies? also what happens when you want to scale?

Answer as three short sections with concrete answers for *this* system. Generic advice doesn't count.

**Improve**: the 3 to 5 changes with the best value-to-effort ratio, ranked.

**If the server dies** (walk through each one that exists):
- a request that was mid-flight: is it retried? Is the retry safe (idempotency key, unique constraint)?
- a job or webhook being processed: lost, run twice, or resumed? Is there a dead-letter path?
- in-memory state: sessions, caches, rate-limit counters, websocket presence. What is lost, and does it matter?
- writes: is a multi-step write in one transaction, or can it leave half-written data?
- recovery: health check, auto-restart, backups that have actually been restored once, time to recover.

**When it scales** (10x users, data, or instances):
- what breaks first: DB connections, a hot table without an index, a single worker, a local file or in-process cache
  that isn't shared across instances, a cron that would run on every instance
- where the state has to move (Redis, DB, object storage) so instances are stateless
- what needs a limit: rate limits, queue depth, payload size, pagination
- rough capacity math: requests/s × cost per request vs current limits

Patterns for the usual answers are in `backend-patterns.md`.
