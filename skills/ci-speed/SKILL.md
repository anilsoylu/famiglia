---
name: ci-speed
description: >-
  Make a repo's CI fast without letting it lie: audit real runs, hit per-stage budgets (PR result under 2 min p50),
  one PR per change. For "CI is slow", "speed up GitHub Actions". A red PR check goes to /pr-ready; slow app code to /perf.
argument-hint: "[optional workflow or job to start with]"
---

# CI speed

Make this repo's CI as fast as possible without letting it lie. Target: a PR gets its result in under 2 minutes at the
median and under 3 minutes at p95, measured from push to the last required check.

If the user named a workflow or job, start there. Otherwise cover every workflow that runs on PRs.

## Two rules that outrank speed

1. **The full suite runs before anything reaches the default branch**, in a merge queue (`merge_group` on GitHub
   Actions, merge trains on GitLab). Test selection only narrows PR feedback. If the repo has no merge queue, adding
   one comes before adding selection. Where no merge queue is available (on GitHub: personal repos, and private org
   repos without Enterprise Cloud), keep the full suite on PRs and skip selection, unless the user accepts the
   trade-off: selection on PRs plus the full suite on every push to the default branch, which catches a bad change
   only after it has merged. Put that choice on the "needs you" list.
2. **Never get faster by hiding failures.** No retries, wider timeouts, `continue-on-error`, `|| true`, skipped or
   quarantined tests. A check that needs a retry has a bug: find it. When the repo already has any of these, list each
   one with `file:line` as a bug, and find the cause instead of keeping it.

## 1. Audit

Measure before you change anything.

- Run `python3 scripts/ci-audit.py` from this skill's folder (it uses `gh`). It pulls the last 150 PR runs and splits
  every job into **waiting** (queued until a runner picks it up), **setup** (checkout, toolchain, cache, install) and
  **running** (the actual work), at p50 and p95. It also prints the PR result time and CI minutes per month.
  Run `--help` for the options (other repo, event, workflow, run count).
- No `gh`, no remote or no run history: say so plainly and don't invent p50/p95 numbers. Time each step once locally,
  label those numbers as estimates, and say that real numbers need run history.
- Fix the biggest bucket first. It is rarely the tests, so don't spend time deleting them.

## 2. Budgets

Hit these budgets in order of the audit's biggest bucket. `references/tools.md` has the setup, the checks and the
known gaps for every default tool below. Read the section for a tool before you switch to it.

| Stage | Budget | Default |
|---|---|---|
| Waiting | under 10 s | Every job on fast hosted runners (Blacksmith for GitHub Actions), even the 5-second ones: a 5-second job that queues 10 minutes is a 10-minute job. Cancel a branch's in-progress run when a new commit lands. |
| Setup | under 30 s | PR cache hits above 95%, by seeding caches from the default branch. Cache `node_modules` itself, not just the package cache. Blobless clone (`filter: blob:none`), not a shallow one. |
| Lint | under 5 s | oxlint with every rule you can turn on. Delete ESLint. |
| Typecheck | under 5 s | `bun check`. Fall back to TypeScript 7 `tsc` if it can't check this repo. tsrs locally. |
| Format | — | oxfmt. Delete Prettier. |
| Install and scripts | — | bun. Delete npm, yarn or pnpm. |
| Tests | under 60 s per shard | Stop reloading the app per test file (Vitest `isolate: false`), reset state after every file, and write the cleanup rules into the repo's `AGENTS.md`. Run in random order to flush out leaks. Shard by recorded duration onto 8-core machines, each shard with its own database. Buy cores before shards, and match concurrency to cores. |
| Shape | — | Lint, typecheck, build and tests run in parallel. Then move migration checks and other apps' tests out of the slowest job into their own. |
| Selection | — | On PRs, run only what the diff can reach (`nx affected`, `turbo --affected`). Then check it (step 4). |
| Local | under 9 s | A pre-push hook that runs format, lint and typecheck on changed files. A hook, not a line in `AGENTS.md`, because agents skip steps. |
| Keep it fast | — | Fail any job that exceeds its budget. |

The budget enforcement is what protects every later PR. Without it the gains decay one slow job at a time.

## 3. Switching a tool

The tools above are defaults. You need a measured reason to keep an old one. Take anything newer that is faster on
this repo.

Before each switch, run the old and new tool side by side on the whole repo and list everything the new one misses:
rules with no equivalent, errors it doesn't report, files it formats differently. Put that list in the PR. If a gap
matters (an accessibility rule, a type error class), keep the old tool for only that part and say why, with numbers.

Non-JS repos and other CI systems follow the same rules and budgets with that stack's fastest tools.
`references/tools.md` lists the usual equivalents.

## 4. Check the selection

Test selection that misses a change makes CI lie. After you add it, hide a real change from it on purpose: on a
throwaway branch, break behavior through a path the selection could miss (a file read at runtime, a shared config, a
dynamic import, a dependency edge outside the package graph). Confirm CI goes red, not green. If it goes green, widen
the selection or declare the missing dependency, then repeat. Close the throwaway branch when done.

## 5. Deliver

- One small PR per change, with before and after numbers from real CI runs, not local runs.
- Do everything you can without the user first.
- Bring everything that needs an account, a secret or a bigger bill as **one** list, each item with its expected
  monthly cost. Show the math: CI minutes per month × the rate from the vendor's current pricing page.
- Don't point `runs-on` at a paid runner label before the account exists. The job would sit in the queue forever.

## 6. Report

End with this report:

```
ci-speed: <repo>
PR result:     p50 <before> → <after>, p95 <before> → <after>  (source: <n> real runs | local estimate)
per bucket:    waiting <b → a>, setup <b → a>, running <b → a>  (p50 / p95)
CI per month:  <minutes before → after>, <cost before → after>
PRs:           <link — change — before/after numbers>
needs you:     <item — why — expected monthly cost>
new tools miss: <tool — what it misses — kept old tool for it? yes/no>
hiding failures found: <file:line — retry/timeout/skip — cause or status>
```

## Don't

- Retry, widen a timeout, skip or quarantine a test to turn a check green.
- Let selection decide what reaches the default branch. The merge queue runs everything.
- Report "faster" without before and after numbers, or present a local estimate as a CI number.
- Switch a tool without the side-by-side comparison.
- Bundle several changes into one PR. A regression must point at one change.
