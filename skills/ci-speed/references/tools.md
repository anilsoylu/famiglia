# CI speed: tools

Setup, checks and known gaps for each default in the budget table. Versions and prices move fast: check the tool's
current docs or pricing page before you rely on a detail here (notes checked 2026-11).

## Contents

- [Runners and waiting](#runners-and-waiting)
- [Setup: clone and caches](#setup-clone-and-caches)
- [Install: bun](#install-bun)
- [Lint: oxlint](#lint-oxlint)
- [Typecheck: bun check, TypeScript 7, tsrs](#typecheck-bun-check-typescript-7-tsrs)
- [Format: oxfmt](#format-oxfmt)
- [Tests](#tests)
- [Selection and the merge queue](#selection-and-the-merge-queue)
- [Local pre-push hook](#local-pre-push-hook)
- [Budget enforcement](#budget-enforcement)
- [Other stacks and CI systems](#other-stacks-and-ci-systems)

## Runners and waiting

- **Blacksmith** runs GitHub Actions jobs only. You switch a job by changing its `runs-on` label to one of theirs
  (the label names vCPU count and OS). It needs an account and the GitHub app installed, so it goes on the "needs you"
  list until the user has done that.
- Price: per minute, set by OS and vCPU count, and it doubles with each doubling of vCPU (about $0.004/min for 2 vCPU
  Ubuntu x64 in late 2026). GitHub has announced a per-minute platform fee that may also apply to third-party runners.
  Read both current pricing pages before you write a cost.
- Alternatives with the same shape: Depot, Namespace, RunsOn (in the user's own AWS account), or self-hosted runners.
  Compare queue time and price on this repo's audit, not on vendor claims.
- Cancel superseded runs on PR branches, but never on the default branch or in the merge queue:

  ```yaml
  concurrency:
    group: ${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}
    cancel-in-progress: ${{ github.event_name == 'pull_request' }}
  ```

## Setup: clone and caches

- Clone blobless, not shallow. A shallow clone (`fetch-depth: 1`) has no merge base, so affected-only selection and
  changed-file checks either fail or fall back to running everything.

  ```yaml
  - uses: actions/checkout@v4
    with:
      fetch-depth: 0
      filter: blob:none
  ```

- On GitHub, a cache saved on a PR branch is visible only to that branch. A cache saved on the default branch is
  visible to every PR. So run the cache-saving job on every push to the default branch, and let PRs restore only.
  That is what gets PR hit rates above 95%.
- Cache `node_modules` itself (plus the package manager's cache). Key it on OS, runtime version and the lockfile hash.
  On an exact hit, skip the install step completely. On a miss, install and save.
- Measure the hit rate: count restore hits against total PR jobs in the audit window.

## Install: bun

- `bun install` reads an existing `package-lock.json`, `yarn.lock` or `pnpm-lock.yaml` and writes `bun.lock`. Commit
  `bun.lock`, delete the old lockfile, and set `packageManager` in `package.json`.
- Diff the resolved versions before and after (`bun pm ls` against the old tool's list). A silent major-version
  change is a behavior change, not a speed change.
- Move scripts to `bun run`. Check the lifecycle scripts the repo relies on (`prepare`, `postinstall`): bun runs the
  root project's own scripts but blocks dependency scripts unless they are in `trustedDependencies`.

## Lint: oxlint

- Convert the ESLint config with `npx @oxlint/migrate`. Then turn on every category and disable rules one by one, each
  with a comment saying why it is off.
- Type-aware rules: install `oxlint-tsgolint` and run with `--type-aware`. It needs TypeScript 7 and covers most of
  typescript-eslint's type-aware rules. In a monorepo, build dependent packages first so their `.d.ts` files exist.
- Known gaps: oxlint's support for running ESLint JS plugins is still alpha, and some popular plugins have partial or
  no coverage (accessibility rules like `jsx-a11y`, import cycle detection, security plugins). Framework file formats
  like `.vue` and `.svelte` have limited support. The side-by-side run in SKILL.md step 3 finds which of these this repo
  uses.
- Side by side: run ESLint and oxlint on the whole repo, normalize to `file:line rule`, and diff. List every finding
  ESLint reports that oxlint doesn't.

## Typecheck: bun check, TypeScript 7, tsrs

- `bun check` is Bun's built-in type checker (Bun 1.4.3 and later). It reads `tsconfig.json` and aims to report
  exactly what TypeScript 7's `tsc` reports. `tsc --noEmit` maps to `bun check`, `tsc -b` to `bun check -b`.
- Trap: if `package.json` has a script named `check`, `bun check` runs that script, not the type checker. Rename the
  script (for example to `typecheck`) and confirm the output really comes from the checker.
- Fallback when `bun check` can't check this repo: TypeScript 7 (stable since July 2026). The command is still `tsc`.
  TypeScript 7 has no full programmatic API until 7.1, so tools that drive the compiler from code (some bundler
  loaders, type-aware typescript-eslint) may not work with it yet. That is one more reason to lint with oxlint.
- tsrs (Cloudflare and VoidZero's Rust port of the TypeScript 7 checker) is experimental: use it locally and in
  editors for fast feedback, and keep `bun check` or `tsc` as the CI gate.
- Side by side: run the old checker and the new one on the whole repo, diff the `file:line code` lists, and plant one
  known type error to confirm both catch it.

## Format: oxfmt

- oxfmt is Prettier-compatible and much faster. Its migrate command reads `.prettierrc` or `prettier.config.js` and
  writes `.oxfmtrc.json` (see `oxfmt --help` for the current flag).
- Gaps: it was still in beta in late 2026, Prettier plugins (for example Tailwind class sorting) were not supported,
  and a few Prettier options were missing. A plugin the repo depends on is a measured reason to keep Prettier for those
  files only.
- Side by side: format the repo with each tool into two copies and diff them. Commit the reformat as its own PR so
  `git blame` can skip it (add the commit to `.git-blame-ignore-revs`).

## Tests

- **Stop reloading per file.** Vitest `test.isolate: false` (with `pool: 'threads'` or `'forks'`) reuses one module
  graph per worker instead of rebuilding it for every file. State now leaks between files, so:
  - add a setup file that resets after every file: restore mocks and timers, clear module-level caches and singletons,
    reset the DOM, truncate or roll back the database;
  - write those cleanup rules into the repo's `AGENTS.md`, so agents writing new tests follow them;
  - run in random order (`sequence.shuffle: true`) to flush out leaks. A test that fails only in some orders has a
    leak: fix the leak, never pin the order.
- **Shard by recorded duration.** Vitest and Jest `--shard=i/n` split by file count, which leaves one slow shard.
  Record per-file durations on the default branch (`--reporter=json --outputFile=...`), save them as a cache or
  artifact, and on PRs assign files to shards longest-first, each to the currently lightest shard. Files with no
  record get the average. Pass each shard its file list.
- **One database per shard.** A service container per job, or one schema per worker inside a shard.
- **Cores before shards.** Each shard pays setup again. Move to 8-core machines first and set workers to the core
  count (`maxWorkers`), then add shards only when one machine can't stay under 60 s.
- Jest: `--shard`, `--maxWorkers`, `workerIdleMemoryLimit` for leaky suites. Playwright: `fullyParallel: true` and
  `--shard`, with the same duration-based assignment.

## Selection and the merge queue

- Monorepo tools: `nx affected -t lint typecheck test build --base=origin/<default>` or
  `turbo run lint typecheck test build --affected`. Single package: `vitest --changed origin/<default>` or
  `jest --changedSince=origin/<default>`.
- Both need the merge base, so they need the blobless full-history clone above.
- GitHub merge queue: turn it on in the branch ruleset, and add `merge_group:` to the `on:` triggers of every workflow
  whose checks are required. In `merge_group` runs and on pushes to the default branch, run the full suite with no
  selection. It exists only for public repos owned by an organization and for repos on GitHub Enterprise Cloud. If
  the ruleset has no merge queue option, SKILL.md rule 1 says what to do.
- Selection misses what the dependency graph can't see: files read at runtime, env and config files, code generation,
  dynamic imports, assets. Declare those as inputs (Nx `namedInputs`, Turbo `inputs`) or treat changes to them as
  "run everything".

## Local pre-push hook

- A real git hook, installed for everyone: lefthook, or a committed `.githooks/pre-push` plus
  `git config core.hooksPath .githooks` run from the `prepare` script.
- Run format check and lint on the files changed since the upstream (`git diff --name-only --diff-filter=ACMR
  @{upstream}...HEAD`, falling back to the default branch's merge base). Typecheck can't run per file, so run the whole
  `bun check`; it fits in the budget.
- Measure the hook on a typical change. Over 9 s means people skip it with `--no-verify`.

## Budget enforcement

- Fail a step that exceeds its budget. That is a tighter limit, not a wider timeout, so it fits rule 2. Wrap the
  command (`timeout 10s bun check` on Linux runners), or set the job's `timeout-minutes` to the budget rounded up and
  add a last step that compares elapsed time with the budget in seconds.
- Budget the job's running time, not its queue time. Queue time is the runner's problem, and the audit tracks it.
- When a budget fails, fix the cause or raise the budget in its own PR with numbers. Don't delete the check.

## Other stacks and CI systems

Same rules and budgets, with the fastest tool for the stack. Usual picks, still subject to the side-by-side check:

| Stack | Install | Lint and format | Typecheck | Tests |
|---|---|---|---|---|
| Python | uv | ruff (lint and format) | the fastest checker that checks this repo cleanly (ty, pyright, mypy) | pytest-xdist, pytest-split for duration-based shards |
| Go | module cache | golangci-lint with its cache | `go vet` | `go test` with the build and test cache restored |
| Rust | cached `target/` (or sccache) | clippy, rustfmt | `cargo check` | cargo-nextest with partitions |

| CI | Cancel superseded runs | Full suite before merge | Duration-based shards |
|---|---|---|---|
| GitLab | `interruptible: true` + auto-cancel redundant pipelines | merge trains | `parallel:` plus a timing file |
| CircleCI | auto-cancel redundant workflows | a required job on the default branch with no selection | `circleci tests split --split-by=timings` |
| Buildkite | cancel intermediate builds | a merge-queue pipeline with no selection | test engine splitting |
