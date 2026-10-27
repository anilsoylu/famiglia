# Writing tests

Use this when the change adds or changes tests, and for every bug fix. Use the repo's own runner, helpers and layout.
A new test library, Testcontainers or a mutation tool is a new dependency and needs the user's yes.

## A test has to be able to fail

- **Bug fix: reproduce it first.** Write a test for the reported behavior, run it, and see it fail for the reason in
  the report. Then fix the code and see it pass. Fixing first and testing after proves nothing about the bug.
- **New test: watch it fail once.** Run it against the old code (stash the change) or break the behavior on purpose. A
  test that never failed may be testing nothing.
- **Red test: fix the code, not the test.** Change an existing test only when the test itself is wrong, and say why in
  the reply. Don't loosen an assertion, skip a test or update a snapshot just to get green.

## What to test

- **Public behavior.** Call what callers call: the exported function, the HTTP endpoint, the CLI. Assert what a caller
  or user sees (the response, the rendered text, the stored row), not private helpers, call counts or internal
  structure. A refactor that keeps behavior shouldn't break a test.
- **Mocks only at boundaries you don't own.** Payment, email, third-party APIs, the clock, randomness. Don't mock the
  repo's own modules. Use a real database when the repo already has a test DB or containers for one.
- **No logic in tests.** Literal expected values, no loops or conditionals that compute the answer. A table of inputs
  and literal outputs is fine.
- **Wide input space** (parsers, formatters, money and date math): add a property-based test if the repo has the
  library. Mutation testing is for critical modules, run now and then, not on every change.
- **User flows**: a test file for the repo's e2e runner (e.g. Playwright) that runs headless in CI. A browser driven by
  an MCP tool is for exploring and checking a flow, not the test itself.

## Report

Name the test that failed before the fix and passes after, with the command and its result. If no test could be run,
say so instead of claiming the change is tested.

## Review checks

- Every new or changed test was seen failing, or would fail on the old code.
- No existing test was weakened, skipped or rewritten to match new behavior without a stated reason.
- Tests go through the public API and mock only boundaries the repo doesn't own.
