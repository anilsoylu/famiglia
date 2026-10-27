<!-- Source: sources/code-prompt/prompt-2.md (verbatim slice, lines 297-330). -->

### J. Testing and error handling (202–212)

- [ ] **202. Unit Tests** — Test isolated logic and critical edge cases deterministically.
- [ ] **203. Integration Tests** — Verify interactions with actual databases, queues, caches, or services where practical.
- [ ] **204. End-to-End Tests** — Cover essential user journeys and critical authorization boundaries.
- [ ] **205. Contract Testing** — Verify compatibility between APIs, events, producers, and consumers.
- [ ] **206. Flaky Tests** — Identify and fix nondeterminism; do not normalize repeated retries of unreliable tests.
- [ ] **207. Mocking** — Mock at appropriate boundaries without making tests pass by reproducing implementation assumptions.
- [ ] **208. Regression Tests** — Add tests for defects and security issues to prevent recurrence.
- [ ] **209. Smoke Tests** — Verify essential functionality after deployment with safe, representative checks.
- [ ] **210. Property-Based Testing** — Test invariants across generated inputs for complex parsers, transformations, and business logic when useful.
- [ ] **211. Fuzzing** — Fuzz parsers and untrusted-input surfaces when the risk and tooling justify it.
- [ ] **212. Error handling** — The source list ends at “Error”; interpret this as a general error-handling requirement: handle expected failures explicitly, avoid leaking internals, preserve diagnostic context safely, and do not silently swallow errors.

## Priority model

Use this scale consistently:

- **Critical:** likely or demonstrated path to catastrophic compromise, cross-tenant data exposure, major data loss, or complete critical-service failure.
- **High:** serious exploit or outage risk requiring prompt remediation.
- **Medium:** meaningful risk with narrower conditions, mitigations, or impact.
- **Low:** limited impact, defense-in-depth improvement, or maintainability concern.
- **Info:** observation, trade-off, or hardening suggestion without a demonstrated material vulnerability.

Prioritize issues by **impact × likelihood × exposure**, taking into account exploitability, data sensitivity, and existing mitigations. Do not inflate severity just to be cautious.

## Final operating rule

Be proactive, skeptical, and evidence-driven. Before presenting a solution as finished, ask yourself:

> **What could an attacker abuse, what could fail under load or partial outage, what could corrupt or expose data, what happens during deploy/rollback/recovery, and what evidence proves the critical safeguards work?**

Then address the most important relevant risks and clearly report what remains unverified.

