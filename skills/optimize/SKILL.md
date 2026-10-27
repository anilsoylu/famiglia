---
name: optimize
description: >-
  Exact-parity speed rewrite of a named routine or the diff's hot spot: shorter, measurably faster, same behavior.
  For "make it faster", "vectorize this". With no known target ("why is this slow"), use /perf.
---

# Optimize

Make the routine shorter and measurably faster with identical behavior. The
target is a routine the user names or the current diff's hot spot, never a
project-wide sweep.

## Loop

1. Parity harness first. Existing tests that cover the routine count; otherwise
   write a characterization test: fixed inputs, golden outputs, bitwise
   comparison by default. Vectorization and JIT reorder float ops, so a stated
   tolerance is allowed only with the user's sign-off. Unattended runs are
   bitwise-only: if bitwise parity cannot hold, revert the rewrite, keep the
   cleaned code, and state why in the report.
   UI/render code has no golden value to compare, so parity there means: the
   same rendered pixels at a fixed clock (screenshot diff at endpoints and
   midpoint), the same DOM/a11y tree, and the same event, request and
   side-effect counts, with each animation's initial play state preserved. A
   faster run that changes the design, or a blank canvas, is not parity. The
   per-runtime details are in `../perf/field-notes.md` (Live Electron, Browser
   idle and retention, SSR responsive-image sections).
2. Capture a baseline timing on a representative input.
3. Rewrite shorter and faster. The means are per stack: numpy/numba vectorize
   and JIT the hot loop; TS/JS improve the algorithm and cut allocations,
   measured only. Delete scaffolding the rewrite obsoletes.
4. Re-run the harness (green) and the timing; report before/after numbers.
5. Then review and pr-update; review tier at least high — this pass rewrites
   behavior-adjacent code. Invoked standalone, run clean first; in a handoff
   clean already ran.

## Don't

- Optimize by guess or sweep the project — one named routine at a time.
- Trade parity for speed without the user's explicit sign-off.
- Report "faster" without numbers.
