<!-- Source: sources/code-prompt/prompt-2.md (verbatim slice, lines 150-175). -->

### C. Distributed systems and resilience (76–98)

- [ ] **76. CAP Theorem** — Make consistency and availability trade-offs explicit under network partition assumptions.
- [ ] **77. Eventual Consistency** — Define acceptable staleness, convergence, and user-facing behavior.
- [ ] **78. Strong Consistency** — Use stronger guarantees where business invariants truly require them and understand their cost.
- [ ] **79. Raft Consensus** — Understand consensus guarantees and operational requirements before introducing or operating consensus systems.
- [ ] **80. Leader Election** — Handle leadership changes, fencing, and stale leaders safely.
- [ ] **81. Split Brain** — Prevent or contain concurrent leaders and conflicting writes.
- [ ] **82. Quorums** — Understand read/write quorum settings and their consistency and availability implications.
- [ ] **83. Clock Skew** — Avoid assuming clocks are perfectly synchronized; use monotonic time for elapsed durations where appropriate.
- [ ] **84. Distributed Locks** — Use only when needed; consider lease expiry, fencing tokens, partitions, and lock-service failure.
- [ ] **85. Consistent Hashing** — Consider load distribution and rebalancing behavior if adopting it.
- [ ] **86. Bloom Filters** — Account for false positives and use them only as a probabilistic optimization, not a source of truth.
- [ ] **87. Two-Phase Commit** — Understand coordinator failure and blocking risks before using distributed transactions.
- [ ] **88. CQRS** — Introduce separate read/write models only when the added complexity is justified.
- [ ] **89. Event Sourcing** — Plan event schema evolution, replay safety, retention, privacy, and projections.
- [ ] **90. Race Conditions** — Identify shared mutable state and timing-sensitive operations; enforce invariants atomically.
- [ ] **91. Backpressure** — Bound queues and in-flight work so consumers can signal or enforce overload limits.
- [ ] **92. Load Shedding** — Reject or defer low-priority work predictably under overload.
- [ ] **93. Bulkheads** — Isolate resources and failure domains to limit blast radius.
- [ ] **94. Jitter** — Add randomized delay to retries or scheduled work when synchronized bursts are a risk.
- [ ] **95. Retry Storms** — Bound retries, use backoff and jitter, set budgets, and avoid retrying permanent failures.
- [ ] **96. Cascading Failures** — Use timeouts, isolation, limits, graceful degradation, and dependency-aware failure handling.
- [ ] **97. Thundering Herd** — Prevent synchronized cache misses, refreshes, and reconnects from overwhelming dependencies.
- [ ] **98. Cache Invalidation** — Define invalidation/update semantics and consistency expectations; test stale-data cases.

