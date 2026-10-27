<!-- Source: sources/code-prompt/prompt-1.md (verbatim slice, lines 63-73). -->

# Phase 1 — Establish repository facts and audit boundaries

Before rating controls:

- Inspect the current branch, commit, repository status, root layout, workspace structure, relevant manifests/lockfiles, scripts, CI workflows, deployment configuration, infrastructure definitions, migrations, route/handler entry points, and tests.
- Identify the product surfaces: web, API, background jobs/workers, mobile apps, admin tools, integrations, and AI/agent workflows.
- Trace important flows from entry point to authorization, validation, business logic, persistence, third-party calls, and response.
- Identify which checks are possible locally and which require host, cloud, store, account, secret-manager, monitoring, or production access.
- Start from the current working tree. Do not revert, reset, clean, or overwrite pre-existing user changes. Do not reveal sensitive contents from `.env` files; inspect only safe metadata or redacted key names when needed.
- Do not claim to have checked the live production system unless you actually completed a read-only check against the correct environment.

