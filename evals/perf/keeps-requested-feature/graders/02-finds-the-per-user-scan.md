---
type: llm
focus: trace
weight: 1
---

The hot path is identified as activityPanel's per-user scan (users.includes and events.filter run once per user), not the summary
