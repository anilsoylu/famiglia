<!-- Source: sources/code-prompt/prompt-2.md (verbatim slice, lines 176-195). -->

### D. Caching, messaging, and asynchronous work (99–115)

- [ ] **99. Cache Hit Ratio** — Measure hit rate alongside latency, cost, and correctness; avoid optimizing the ratio alone.
- [ ] **100. TTLs** — Set expiration based on data freshness and risk; understand expiry jitter and synchronized expiration.
- [ ] **101. Cache Warming** — Warm deliberately without stampeding dependencies or exposing data across tenants.
- [ ] **102. Write-Through vs Write-Back** — Make durability, consistency, and lost-write trade-offs explicit.
- [ ] **103. Redis Eviction Policies** — Choose an eviction strategy that fits workload and monitor memory pressure.
- [ ] **104. CDNs** — Configure cache keys, private content rules, purge behavior, and origin protections.
- [ ] **105. Cache-Control Headers** — Set public/private, freshness, and revalidation directives correctly for each response type.
- [ ] **106. ETags** — Use validators correctly and avoid leaking sensitive data through cache behavior.
- [ ] **107. Dead Letter Queues** — Capture failed messages with enough safe diagnostics and define review, replay, and retention processes.
- [ ] **108. Poison Messages** — Prevent a repeatedly failing message from blocking healthy work; quarantine it safely.
- [ ] **109. At-Least-Once Delivery** — Assume duplicates and make handlers idempotent.
- [ ] **110. Exactly-Once Semantics** — Do not claim end-to-end exactly-once delivery without a precise guarantee; use deduplication and transactional boundaries where needed.
- [ ] **111. Message Ordering** — Define the required ordering scope and ensure partitioning and consumer behavior preserve it when necessary.
- [ ] **112. Kafka Consumer Groups** — Understand partition assignment, rebalances, offsets, and duplicate processing.
- [ ] **113. Partition Keys** — Pick keys that preserve required ordering while avoiding hotspots.
- [ ] **114. Background Jobs** — Make jobs idempotent, observable, bounded, retryable, and safe across deploys.
- [ ] **115. Webhook Retries** — Use bounded retry schedules, idempotency, signature validation, and delivery diagnostics.

