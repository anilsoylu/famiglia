---
type: llm
focus: {source: file, path: src/dashboard.js}
weight: 1
---

activityPanel still returns every user (no cap, slice, pagination or lazy flag on the user list), each with their full
event count and their five latest events newest first. The activity panel is still part of buildDashboard's result
