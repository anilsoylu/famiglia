---
name: find-state-machines
description: Find implicit state machines, where one lifecycle's state, transitions, and ownership are scattered across flags, effects, callbacks, and async work, and make them explicit. Use when auditing lifecycle coordination, async flows, impossible states, or a proposed stateful refactor.
---

# Find State Machines

Find the app’s explicit and implicit state machines and document their states, invariants, and transition tables in one file. Identify invalid states or transitions the code can actually reach, with evidence, including through retries and concurrency. Prioritize confirmed bugs by impact, group related fixes into issues, then fix them with regression tests and keep the document updated.
