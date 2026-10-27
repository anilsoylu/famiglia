# Stages

One section per stage. To add a prompt: put it in `references/`, add a line to the stage where it belongs, and add a
row to the table in SKILL.md if it changes what the stage runs.

## plan

Goal: decide how to build it before writing it, with the failure modes on the table.

1. Read `references/guardian/core.md` (role, core instructions, working procedure). It's the standing brief for the whole flow.
2. Map the feature's data flows and trust boundaries. Pick the guardian sections that apply and read only those:
   auth/users/input → `references/guardian/A-appsec-identity.md` · schema/queries → `references/guardian/B-database.md` · multiple services/retries → `references/guardian/C-distributed.md` ·
   cache/queue/async → `references/guardian/D-cache-queues.md` · new endpoints/webhooks → `references/guardian/E-http-api.md` · infra/deploy → `references/guardian/F-cloud-infra.md`, `references/guardian/H-delivery-release.md` ·
   load/latency/logging → `references/guardian/G-capacity-observability.md` · uploads/buckets/spend → `references/guardian/I-storage-cost.md` · client data fetching/real-time UI → `references/frontend-data.md`.
   Check the repo's manifests first (package.json, go.mod, compose/infra files) so you know which technologies exist.
   Skip items whose `Only if` condition doesn't hold and items for tech the repo doesn't use; don't evaluate them one by
   one. List them in a single report line, e.g. `N/A: GraphQL, gRPC, mTLS (not used)`.
3. If the feature matches a row in `references/backend-patterns.md`, use that row as the design checklist.
4. Run the **short** resilience check: two lines each from `references/review-questions.md` → "If the server dies"
   and "When it scales". It's for decisions that are expensive to change later (where state lives, idempotency,
   what's synchronous). Leave the rest to the end stage.
5. For non-trivial work, write the plan to a file: Plan mode's plan file when available, else the repo's `plans/` folder
   in its naming style (e.g. 004-team-invites.md), else a new `plans/<feature>.md`. End with that file's full
   absolute path and get approval before coding.

## build

Goal: write the change the way this repo already writes code.

1. Follow existing conventions (CLAUDE.md, neighbors of the file being changed). Extend existing helpers instead of adding parallel ones.
2. UI work: use `/frontend-design` or `/ui-ux-pro-max` if installed. React/Next.js: `vercel-react-best-practices`
   (and `vercel:nextjs` / `vercel:shadcn` when the repo uses them). Skip any that aren't installed. Client code that
   fetches or subscribes to backend data: `references/frontend-data.md`.
3. Keep the guardian sections chosen in plan in mind as you write: server-side authz, input validation, timeouts,
   idempotency, no secrets in code or logs. Add tests for the meaningful behavior.
4. Run the repo's own checks that are cheap (typecheck, unit tests for touched code) before calling it done.

## review

Goal: catch what's wrong with the code just written while it's fresh, before it's committed.

1. Answer `references/review-questions.md` → "After implementing" against the diff, in its own section of the reply:
   each inefficiency with `file:line`, or "none found".
2. Run `/review` on the diff. It picks a tier first; `none` or `medium` means no reviewer runs, and that's a normal result.
3. Run `/simplify` for reuse and dead code.
4. Fix what the user agrees to. Suspected performance issues go to the commit stage's perf step to be measured. Don't fix them by guess here.
5. End by naming the next stages: `/commit-gate` (perf → optimize → security-audit) on the final diff, then `/cpr`
   (clean → PR) into the default branch (main/master).

## commit

Goal: nothing gets committed without going through perf, optimize and security.

1. Run `/commit-gate`. It classifies the diff, runs perf → optimize → security-audit on it, and returns one report.
2. Blockers in the report: fix them (or get the user's call) and run the gate again on the new diff.
3. Commit only when the user asked to. Use topical commits that describe the change.

## merge

Goal: get the branch into the default branch (main/master) through a clean PR.

1. Make sure the commit gate passed on the final diff. If commits landed after the last gate run, run it again.
2. Run `/cpr`. It runs clean → pr-update and ends with the PR link.
3. If the user asked to merge, `/cpr` merges once checks are green and pulls the default branch. Otherwise stop at the PR. Failing
   CI and review threads go to `pr-ready`.

## end

Goal: the honest "is this production ready" answer, with evidence.

1. Run the full production-readiness audit, read-only. Read `references/audit/` in order:
   `references/audit/00-principles-and-format.md` → `references/audit/phase-0-docs.md` → `references/audit/phase-1-repo-facts.md` → `references/audit/phase-2-checklist.md` →
   `references/audit/phase-3-engineering.md` → `references/audit/phase-4-report.md`. The report format in phase-4 is required.
2. Answer the full `references/review-questions.md` → "Resilience and scale" (improve / server dies / scale) for
   this system, and put it in the report next to the scorecard.
3. Cover the audit's security items with `/security-audit` in **guidance mode**. Then offer its **full audit mode** as a
   separate step: it's multi-agent and expensive (a 7-file repo took ~20 min and ~250k tokens in testing). Run it only when
   the user says yes or asked for a full security audit. Its artifacts go outside the repo. Link its findings into the
   prioritized fix list without copying them twice.
4. No fixes during the audit. After the user picks fixes, each one goes back through build → review → commit.
