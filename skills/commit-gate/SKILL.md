---
name: commit-gate
description: >-
  Pre-commit gate: /perf, /optimize, then /security-audit on the current diff, one go/no-go report. Never commits.
  For "ready to commit", "check before I commit". A standalone perf or security question goes to that skill.
metadata:
  version: 0.1.0
---

# Commit gate

Three checks, always in this order, on the code that's about to be committed. Perf finds what's slow, optimize rewrites
only what perf measured, security reviews the final diff (including the optimize rewrite). Don't ask between steps.
Stop only on a blocker or when a fix needs the user's decision.

Run each skill for real. This file is the sequence, not a replacement for their contents. Inside the gate, `/perf` and
`/optimize` stop once they have their after numbers: their own closing steps (clean, review, pr-update, commits) don't
run here, because the gate never commits.

## 0. Scope the diff

- Diff = staged + unstaged changes vs `HEAD` (`git diff HEAD --stat`, plus untracked files from
  `git ls-files --others --exclude-standard`). If the user named a range or branch, use that instead.
- Classify each changed file: **runtime code** (anything that executes in the app, server, worker, build), **web assets**
  (images, CSS, JS bundles, fonts, HTML, build/bundler config), **docs/config only** (markdown, comments, CI yaml, lockfile-only).
- If there's no diff, say so and stop.

## 1. Perf → `/perf`

- No runtime code or web assets in the diff: log `perf: skipped, no runtime code` and go on.
- Otherwise run `/perf` scoped to the changed paths. Use `../dev-flow/references/perf-checklist.md` as the checklist
  (app section always; web-assets section when web assets changed), if it exists.
- Output: the measured hot spots (with before numbers), or "no hot path in this diff".

## 2. Optimize → `/optimize`

- Only on routines perf measured as hot. No hot spot means `optimize: nothing to do`, and that's a normal result.
- Exact parity: harness first, bitwise by default. If parity can't hold, revert the rewrite and report why.
- Output: before/after numbers per routine, or the reason it was skipped.

## 3. Security → `/security-audit`

- Always runs, even on docs/config-only diffs, because secrets and CI changes live there.
- Use its **guidance mode** as a focused review of this diff. Don't start the full six-phase audit (that's for project end).
- Check at least: secrets or tokens added, authz on new/changed routes, input validation, injection, unsafe
  deserialization/file paths, new dependencies, CI/workflow permission changes.
- A hardcoded credential-looking literal (`sk_live_`, `AKIA`, `ghp_`, a private key) is a blocker until the user confirms
  it's fake. Don't downgrade it on a guess.
- Output: confirmed findings with `file:line`, severity, and the fix.

## 4. Report

```
commit-gate: PASS | PASS WITH NOTES | BLOCKED
diff: <n files> (<runtime/assets/docs counts>)
1 perf:      <result + numbers, or skipped + reason>
2 optimize:  <result + before/after, or nothing to do>
3 security:  <findings by severity, or none in reviewed scope>
changes made by the gate: <files>, tests run: <command → result>
blockers: <list, or none>
```

BLOCKED = any Critical/High security finding, a failing test, or a parity break that couldn't be reverted. Fixes the gate makes
stay inside the diff's files. If a fix needs a wider change, report it as a blocker instead.

## Don't

- Commit, push or amend. The user (or `/cpr`) does that.
- Report speedups without numbers, or call the diff "secure". Say "no material issue found in the reviewed scope".

## If a skill isn't installed

- No `/perf`: baseline → profile the changed path → fix the measured hot spot → re-measure, by hand.
- No `/optimize`: skip rewrites and list the hot spots as notes.
- No `/security-audit`: review the diff against `../dev-flow/references/guardian/A-appsec-identity.md` and `../dev-flow/references/guardian/E-http-api.md`
  if present, otherwise the checklist in step 3.
Say which fallback you used.
