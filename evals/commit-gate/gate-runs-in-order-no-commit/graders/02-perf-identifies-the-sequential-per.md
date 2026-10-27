---
type: llm
focus: trace
weight: 1
---

Perf identifies the sequential per-email loop (a query, an insert and a mailer fetch awaited one by one per email) as the hot path
