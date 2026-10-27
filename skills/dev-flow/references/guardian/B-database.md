<!-- Source: sources/code-prompt/prompt-2.md (verbatim slice, lines 112-149). -->

### B. Database design, correctness, and recovery (41–75)

- [ ] **41. Indexes** — Index important filter, join, sort, and constraint paths based on observed queries and trade-offs.
- [ ] **42. `EXPLAIN ANALYZE`** — Inspect real query plans carefully; remember that `ANALYZE` executes the query.
- [ ] **43. N+1 Queries** — Detect repeated per-record queries and use appropriate joins, batching, or eager loading.
- [ ] **44. Full Table Scans** — Determine whether scans are expected or costly; optimize from measured plans, not assumption alone.
- [ ] **45. Connection Pooling** — Set pool sizes and timeouts to fit database and application limits.
- [ ] **46. Database Migrations** — Make schema changes versioned, repeatable, and safe for the deployed application.
- [ ] **47. Down Migrations** — Decide whether rollback is safe; document irreversible operations and use forward fixes when appropriate.
- [ ] **48. Transactions** — Keep related writes atomic and handle failed or retried operations correctly.
- [ ] **49. ACID** — Understand and preserve the required atomicity, consistency, isolation, and durability guarantees.
- [ ] **50. Isolation Levels** — Choose isolation appropriate to the invariants and concurrency patterns.
- [ ] **51. Deadlocks** — Use consistent lock ordering where possible, keep transactions short, and safely retry recognized deadlocks.
- [ ] **52. Optimistic Locking** — Detect conflicting updates with versions or equivalent checks where appropriate.
- [ ] **53. Pessimistic Locking** — Lock deliberately, keep lock duration bounded, and account for contention.
- [ ] **54. Normalization** — Avoid unnecessary duplication and update anomalies in relational data models.
- [ ] **55. Denormalization** — Document duplicated data, ownership, synchronization, and repair strategy.
- [ ] **56. Foreign Keys** — Use referential integrity constraints when appropriate; do not rely only on application convention.
- [ ] **57. Unique Constraints** — Enforce uniqueness in the database for invariants that must hold under concurrency.
- [ ] **58. Cascading Deletes** — Review destructive cascades and ensure they match retention and business rules.
- [ ] **59. Soft Deletes** — Define visibility, uniqueness, restoration, retention, and eventual purge semantics.
- [ ] **60. UUIDs vs Auto-Increment** — Choose identifiers based on privacy, index locality, distribution, and operational needs.
- [ ] **61. Cursor-Based Pagination** — Use stable ordering and opaque/validated cursors for large or changing datasets.
- [ ] **62. Full-Text Search** — Choose appropriate indexing, tokenization, ranking, and access restrictions.
- [ ] **63. Read Replicas** — Account for stale reads and define which operations require the primary.
- [ ] **64. Replication Lag** — Measure lag and design read-after-write flows and alerts accordingly.
- [ ] **65. Sharding** — Define shard keys, cross-shard operations, rebalancing, and operational complexity before adopting it.
- [ ] **66. Partitioning** — Choose partition keys and lifecycle strategy based on query patterns and maintenance needs.
- [ ] **67. Hot Partitions** — Detect skew and hotspots; avoid concentrating load on a small subset of partitions.
- [ ] **68. Postgres VACUUM** — Monitor table bloat, vacuum progress, and transaction patterns that block cleanup.
- [ ] **69. Materialized Views** — Define refresh frequency, staleness tolerance, and refresh-failure handling.
- [ ] **70. Backups** — Define backup coverage, retention, encryption, access controls, and monitoring.
- [ ] **71. Testing Your Restores** — Regularly test realistic restore procedures and validate restored data.
- [ ] **72. Point-in-Time Recovery** — Verify recovery prerequisites, achievable recovery window, and documented procedure.
- [ ] **73. Change Data Capture** — Handle ordering, duplicates, schema evolution, and consumer recovery.
- [ ] **74. Outbox Pattern** — Atomically persist domain changes and publishable events; process delivery idempotently.
- [ ] **75. ORM Lazy Loading** — Understand when queries are triggered and avoid hidden latency or N+1 behavior.


<!-- Additions (not in prompt-2). -->
#### Additions

- [ ] **213. Composite Indexes** — Order columns to match the queries: equality filters first, then range or sort columns; a query can only use a leftmost prefix. Consider covering indexes for hot reads and drop single-column indexes a composite one already serves.
