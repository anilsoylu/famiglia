---
type: llm
focus: trace
weight: 1
---

If the agent adds affected-only or changed-only test selection for PRs, the full suite still runs before merge (merge_group or the default branch); if it adds no selection, this passes
