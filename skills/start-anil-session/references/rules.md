# Anil's working rules

These rules apply to every task in this project, including after `/clear` and in new sessions. They are loaded from the
project's `CLAUDE.md`, which `/start-anil-session` wires up.

## Language

- Talk to the user in Turkish.
- Everything that lands in the repo is professional English: code, comments, file and folder names, docs, commit
  messages, PR titles and bodies, test names, log messages.

## Git identity

- Commits are authored as the GitHub user `anilsoylu`. Before the first commit of a session, check that
  `git config user.name` is `anilsoylu` and `gh auth status` shows `anilsoylu` as the active account
  (`gh auth switch -u anilsoylu` if not). No `Co-Authored-By` trailers.
- Work on a feature branch named in kebab-case (`feat/user-avatar-upload`). Never commit straight to the default branch.
- Commit messages follow Conventional Commits in English (`feat(auth): add refresh token rotation`).

## Code style

- KISS and DRY: extend the existing helper instead of writing a parallel one; no abstraction with a single caller; the
  small, readable version wins over the clever one.
- Kebab-case for file names, folder names, URL slugs, CSS classes, branch names and CLI flags. Identifiers inside code
  follow the language's own convention (camelCase in JS/TS, snake_case in Python, PascalCase for types), because
  kebab-case is not a valid identifier in most languages.
- Match the surrounding code's style before your own preferences.

## Main thread orchestrates, subagents write code

The main conversation plans, splits the work into tasks, briefs subagents, and verifies their results. It does not edit
code itself. This keeps the main context small and focused on decisions.

Route each task to its agent:

| Task | Agent |
|---|---|
| Write or fix code | `worker` |
| `/commit-gate` | `worker` |
| Write and run tests | `tester` |
| Search the codebase | `explorer` |
| Read known files | `reader` |
| Docs and version research | `researcher` |
| `/review` | `general-purpose` (it spawns `reviewer` itself) |
| Independent review of a diff | `reviewer` |

`/start-anil-session` installs these agents in `~/.claude/agents/`. If one is missing, fall back to `general-purpose`.

- Every code change, including one-line fixes, goes to a subagent (Agent tool). The brief names the goal, the files,
  the relevant rules from this file, and what "done" looks like, since the subagent sees nothing else.
- Independent tasks run in parallel in one message. Two subagents never edit the same files at once; when parallel
  writers might overlap, give them `isolation: "worktree"`.
- Checks run in subagents too: `/commit-gate` (perf, optimize, security-audit) in `worker`, test runs in `tester`,
  docs research in `researcher`.
- After a subagent finishes, the main thread reads the diff (`git diff`) and checks it against the brief before moving
  on. A subagent's summary is a claim, not proof.
- The main thread may still read files, run git/gh, and run read-only commands to plan and verify.
- When a skill or tool creates friction (a wrong step, a retry loop, a missing fallback), main thread or subagent logs
  it once with the `papercut` skill, then carries on.

## Testing uses local Docker, never production

- Tests, migrations, seeds and any script that writes data run against the local Docker database only.
- Before running them, check the database URL the command will use (env file, config, or env var) and confirm its host
  is `localhost`, `127.0.0.1`, or a docker-compose service name. Print only the host, never the full URL or password.
- If the host is anything else, or it is unclear, stop and ask. Never run a migration or a destructive query against a
  remote database.
- If the local stack is down, start it with the project's compose file (`docker compose up -d`).

## Headless only

- Browser tests and automation run headless (Playwright/Puppeteer `headless: true`, no visible windows).
- iOS work uses the simulator through command-line and screenshot tools; don't open the Simulator app or other GUI
  windows for verification.

## New stack or feature update: read the docs first

Adding a library, framework, service, or changing a feature built on one starts with research, because scaffold
defaults are rarely the recommended integration.

1. Find the installed (or to-be-installed) version from the lockfile or manifest.
2. Read that project's `llms.txt` / `llms-full.txt` if it publishes one, otherwise the official docs for that version
   (guides, migration notes, best practices). Run this research in the `researcher` agent.
3. Integrate the way the docs recommend for this project's setup (config, file layout, idioms), not the bare default.
4. Mention the docs used in the PR description.

## Finishing a task: gate, commit, PR, merge

For each finished unit of work, in this order and without asking between steps (stop only on a blocker):

1. **Gate**: run `/commit-gate` in the `worker` agent. It runs `/perf`, then `/optimize`, then `/security-audit` on the
   diff. A `BLOCKED` result is fixed (by a subagent) before anything is committed.
2. **Commit** as `anilsoylu` with an English Conventional Commit message.
3. **PR**: run `/cpr` (clean, then open or refresh the PR). Make sure the PR title and body pass `/no-tropes`.
4. **Lead review**: run `/review` on the PR branch inside one `general-purpose` subagent, so the diff and the
   reviewer's reasoning stay out of the main context; `/review` spawns the `reviewer` agent itself. The subagent
   returns only the tier and the findings (`[ADOPT]` / `[NOTE]`, with `file:line`).
   - Tier `none` or `medium`: `/review` skips by design; go to merge.
   - No `[ADOPT]` findings: write any `[NOTE]`s under `## Found while working` in the PR body, then merge.
   - `[ADOPT]` findings: post them as one PR comment (`gh pr comment`), fix them in a subagent, push, and re-review
     only the fix commits (not the whole PR again, since a fresh review of the same tree always finds something
     new). At most two fix rounds; if `[ADOPT]` findings remain after that, stop and ask the user.
   - Log each `[ADOPT]` finding as a papercut too, with `--ref` set to the skill that should have caught it
     (`commit-gate`, `dev-flow` or `review`).
5. **Merge**: when CI is green and the review is clear, `gh pr merge --squash --delete-branch`, then pull the default
   branch. If CI is red or review threads are open, run `/pr-ready` first.

## Full security audit

`/commit-gate` already reviews every diff. Beyond that, run a full `/security-audit` (ask the user first, it is long)
before a release, and when work touches authentication, authorization, payments, file uploads, secrets handling, or
CI/deploy permissions.
