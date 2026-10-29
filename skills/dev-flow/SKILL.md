---
name: dev-flow
description: >-
  Stage-aware delivery flow for a feature or project: plan with the guardian risk review, build, review, commit
  gate, merge through /cpr, and the production-readiness audit at the end. For "the usual flow", "what's next", "the
  feature is done", "is it production ready", "what if the server dies / how does it scale". A single narrow ask
  goes to its own skill.
metadata:
  version: 0.1.0
---

# Dev flow

The user's engineering workflow, one stage at a time. Each stage has its own prompts (in `references/`) and its own
skills. The point is that the right check runs at the right moment: risk thinking before code is written, an
inefficiency review right after, the commit gate before every commit, `/cpr` into the default branch, and the full audit at the end.
Running the full audit on every commit wastes hours. Skipping the gate lets problems pile up.

## 1. Find the stage

Read the situation before asking: the user's words, `git status`, `git diff --stat`, the branch, whether a PR exists.

| Signal | Stage |
|---|---|
| new feature/project, "how should we build", no code yet | **plan** |
| writing code, "implement", "add" | **build** |
| "done", "finished the feature", working tree has a fresh feature diff | **review** |
| "commit", "ready to commit", staged changes | **commit** |
| "merge", "master"/"main", "PR", branch is ahead and gate already passed | **merge** |
| "project is finished", "production ready?", "before launch", "server dies / scale" | **end** |

If two stages fit, or there's no signal, ask once (AskUserQuestion in Claude Code; options = the stages, the most
likely one first). Say which stage you're running in your first line, e.g. `dev-flow → commit stage`.

## 2. Run the stage

Open `stages.md` and follow the section for that stage. It names the reference files to read and the skills to call.
Load only that stage's references. The guardian catalog and the audit are large, and reading them all every time
wastes context.

Short version:

| Stage | Runs |
|---|---|
| plan | `references/guardian/core.md` working procedure · the guardian sections for the touched areas · `backend-patterns.md` if it matches · the short "server dies / scale" check from `review-questions.md` · Plan mode for non-trivial work |
| build | repo conventions · UI work → `/frontend-design` or `/ui-ux-pro-max` · React/Next → `vercel-react-best-practices` · client data fetching → `frontend-data.md` · tests and bug fixes → `testing.md` · proportionate guardian review of what's touched |
| review | `review-questions.md` → "After implementing" · `/review` · `/simplify` |
| commit | `/commit-gate` (perf → optimize → security-audit on the diff) |
| merge | `/cpr` (clean → PR), then merge and pull when asked |
| end | `references/audit/` full production-readiness audit · full "server dies / scale" from `review-questions.md` · `/security-audit` guidance mode (full mode only on the user's yes) |

Stages chain forward when the user wants that ("finish it up" after review → commit → merge). Stop between stages
when a step reports a blocker.

## 3. When a skill isn't installed

Every hand-off has a fallback, so the flow still works when someone installs only this skill. Use the fallback and say so in one line.

| Skill | Fallback |
|---|---|
| `/commit-gate` | run its three steps yourself: `perf-checklist.md`, then an exact-parity rewrite of any measured hot spot, then guardian A + E on the diff |
| `/review` | read the diff for bugs, against repo conventions (CLAUDE.md, lint config) and against the task/issue. Blocking findings first |
| `/simplify` | look at the diff again for reuse, dead code and needless abstraction |
| `/cpr` | clean the diff by hand, topical commits, `gh pr create`/`gh pr edit` with a body describing the whole change, print the PR link (the merge steps stay this stage's either way) |
| `/security-audit` | `references/guardian/A-appsec-identity.md` + `references/guardian/E-http-api.md` + audit checklist sections B, C, D, F |
| `/frontend-design`, `/ui-ux-pro-max`, `vercel-react-best-practices`, `vercel:*` | follow the repo's existing UI patterns |

## Rules that hold in every stage

- Ask, don't assume. When ambiguity could change behavior, data, security or cost, ask one focused question. Never ask
  something the repo can answer.
- Simplest correct change. Don't touch unrelated code. No new dependencies or paid services without asking.
- Measure before claiming performance. Keep exact behavior for any refactor or optimization.
- Evidence, not confidence: `file:line`, the command that ran and its result. Never invent test results or line numbers.
- Never print secrets. A hardcoded credential-looking literal (`sk_live_`, `AKIA`, `ghp_`, a private key) stays a blocker
  until the user confirms it's fake. Don't downgrade it because it looks like a placeholder.
- Don't commit, push, merge or deploy unless the user asked for that step.
- No subtitle/helper text under headings, labels or cards by default (from the user's audit rules).
