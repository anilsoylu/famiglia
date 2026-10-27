---
name: perf
description: >-
  Profile-driven perf loop for any stack: baseline, profile, fix the real hot path, re-measure. For "this is slow"
  with no known cause. A known routine that needs an exact-parity rewrite goes to /optimize.
---

# Perf

The general performance loop. Profiling (CPU profile, flamegraph, memory
snapshot, trace) is the usual tool, but the loop is the same regardless of which
one fits.

## Loop

1. Reproduce the slow path and capture a baseline number — time, memory, FPS,
   request latency, whatever matters here.
2. Profile to find the real hot path: CPU profile / flamegraph / memory snapshot
   / trace as fits. Reuse the repo's existing profiler; don't build a parallel
   harness.
3. Read the profile, not your intuition — fix the actual hot path.
4. Re-measure. Record before/after in the PR title/description.
5. `clean` first, then ship in topical commits (`pr-update`); keep CI green.

## Field notes

`field-notes.md` holds stack-specific lessons. Open it only when the stack matches a section, and read just that section:
Live Electron / hgui · Web loading contracts · Product-grid browsing · Serverless catalog caches · Browser idle and
retention · SSR responsive-image request selection.

## Don't

- Optimize by guess before profiling.
- Fiddle with the measurement system instead of improving perf.
- Run a full suite or profile that overwhelms the machine — scope the run.
- Report gains you didn't measure.
