<!-- Source: sources/code-prompt/prompt-1.md (verbatim slice, lines 74-252). -->

# Phase 2 — Production-readiness checklist

## A. Input, validation, and data handling

1. **Input handling and output encoding**
   - Verify untrusted input is validated and encoded/sanitized appropriately for its actual sink: HTML/DOM, SQL, shell, prompts, file paths, logs, URLs, and serialized output.
   - Prefer context-appropriate output encoding and parameterized APIs over blanket sanitization. Do not render untrusted input as raw HTML unless a reviewed sanitization strategy is intentionally used.
   - Check for injection, path traversal, unsafe deserialization, prompt injection where relevant, and accidental leakage between tenants/users.

2. **Server-side validation**
   - Verify every API endpoint, server action, RPC handler, background-job entry point, and webhook validates untrusted input server-side with an appropriate schema or equivalent logic (for example, Zod, Pydantic, Valibot, or typed validation).
   - Check types, enums, required fields, ranges, maximum string lengths, array/list sizes, pagination bounds, and cross-field constraints.
   - Confirm malformed or invalid input receives a controlled 4xx response rather than an unexpected 500, and that validation cannot be bypassed by calling the server directly.

3. **Uploads and file processing**
   - Check server-enforced size and type limits, file signature/magic-byte or safe decoding checks, generated storage names, authorization, malware scanning when appropriate, and safe download headers.
   - For images shown to other users, check whether EXIF/GPS metadata is stripped when privacy requires it.
   - Verify temporary files and orphaned objects are cleaned up and upload processing cannot exhaust memory, CPU, or storage.

4. **Request and resource limits**
   - Verify maximum request-body size and appropriate timeouts at the application and/or proxy layer.
   - Check pagination, query complexity, concurrency, decompression, image/video processing, and other resource-intensive paths for bounded consumption.

## B. Authentication, authorization, and account lifecycle

5. **Authentication and sessions**
   - Identify the actual auth provider and verify session/token creation, validation, expiry, renewal, revocation, and logout behavior.
   - For cookie-based sessions, verify `HttpOnly`, `Secure` in production, appropriate `SameSite`, deliberate scope/path/domain, and CSRF protections where applicable.
   - Check email verification, password reset/recovery, OAuth callback validation, brute-force protections, and session lifetime against current official guidance.

6. **Production auth configuration**
   - Verify production callback/redirect URLs and trusted origins are explicit and correct; development schemes, localhost origins, wildcard origins, and debug modes are not unintentionally enabled in production.
   - Check redirect destinations against open-redirect risks and confirm secrets/configuration are sourced from the intended production environment.

7. **Authorization, tenant isolation, and IDOR**
   - Verify every handler scopes records and actions to the authenticated caller and tenant, not merely to an ID supplied by the request.
   - Check ownership checks on reads, writes, nested resources, exports, search, background jobs, and object-storage URLs.
   - Ensure privacy/visibility/role rules are consistent across feed, profile, search, detail, API, and alternate entry points. Check privilege escalation and mass assignment.

8. **Account lifecycle and session safety**
   - Verify account deletion and data-removal flows exist where required, re-check identity for sensitive actions, and address associated third-party data and stored files.
   - Check account recovery, email/identity changes, session revocation, secret rotation, and credential changes for account takeover and accidental lockout risks.
   - For mobile apps, assess app-store deletion requirements against the stores' current official rules and this app's account model.

9. **Admin surfaces and privileged operations**
   - Identify admin routes, support tools, internal dashboards, impersonation, bulk mutation, and export paths.
   - Verify strong authentication/2FA where appropriate, least privilege, non-public indexing/exposure controls, authorization on every operation, and audit logging for privileged mutations and exports.
   - Check database and cloud credentials follow least privilege rather than using broad owner/admin identities unnecessarily.

## C. Abuse prevention, AI, and cost controls

10. **Rate limits and abuse controls**
    - Check per-user and per-real-client-IP limits, with trusted-proxy configuration verified for the actual deployment (for example, the correct handling of `CF-Connecting-IP` behind Cloudflare).
    - Prefer shared state such as Redis or a database in multi-instance production; identify and explain any in-memory-only limits.
    - Apply appropriately stricter controls to authentication, password recovery, OTP, uploads, search, expensive reports, paid actions, and third-party API calls.
    - Check distributed bypasses, spoofable forwarded headers, retry behavior, and whether each endpoint should fail open or fail closed if the rate-limit store is unavailable.

11. **AI/LLM and paid API usage**
    - When applicable, verify prompt inputs and output sizes are bounded; per-user quotas, concurrency controls, timeouts, retry ceilings, and a global spend/budget ceiling exist.
    - Confirm provider keys are server-side only and not embedded in web/mobile bundles, source maps, logs, or client-delivered configuration.
    - Review prompt-injection and tool-use boundaries, data minimization, tenant separation, output validation, and disclosure of data sent to third parties.
    - Check retries and fallback models cannot multiply charges without a defined limit, and users cannot bypass usage metering or access another user's context/results.

## D. Secrets and environment configuration

12. **Secrets hygiene**
    - Check current tracked files and repository history for `.env` files, private keys, provider tokens, database credentials, signing secrets, and other sensitive values.
    - Inspect client-delivered variables such as `EXPO_PUBLIC_*`, `NEXT_PUBLIC_*`, and `VITE_*`; confirm no secret is exposed under the assumption that a public-prefix variable is private.
    - Verify development environment files do not contain production credentials and that logs, artifacts, source maps, and build output do not leak secrets.
    - If a secret appears exposed, do not print it. Identify its location safely and recommend revocation/rotation; do not rotate it without approval.

13. **Production configuration and fail-safe startup**
    - Verify the app refuses to start or disables unsafe behavior when required secrets are missing, default, weak, or misconfigured.
    - Check production environment variables are set on the actual host/secret manager, not only in local examples.
    - For mobile builds and OTA updates, verify environment selection, API base URLs, feature flags, and channel configuration; ensure release builds cannot silently target localhost, staging, or an unintended environment.

## E. Errors, logs, and observability

14. **Error handling and boundaries**
    - Verify users receive useful but non-sensitive error messages; no stack traces, SQL details, secrets, or raw upstream error text escape into public responses.
    - Check error boundaries and fallback states for web (including global/root boundaries where supported), React Native/mobile, API handlers, jobs, and critical asynchronous workflows.
    - Confirm expected validation/auth/not-found/conflict/rate-limit errors map to deliberate status codes and unexpected errors are captured without exposing internals.

15. **Logging and auditability**
    - Verify structured, leveled logs are centralized/searchable enough for the system's size and are correlated with request/job IDs where useful.
    - Check that passwords, tokens, session cookies, payment data, sensitive prompts, and unnecessary PII are not logged. Verify redaction, access control, and retention.
    - Ensure security-sensitive actions and admin mutations produce useful audit records without logging secrets.

16. **Error tracking, uptime, and alerts**
    - Check crash/error reporting for each relevant runtime: API, web, workers, scheduled tasks, and mobile.
    - Verify external uptime monitoring checks a meaningful readiness/health endpoint and that alerts reach an accountable person or channel.
    - Inspect whether alerts are actionable and whether failures in monitoring itself are detectable. Do not mark alerting `PASS` merely because an SDK is installed.

## F. Network, transport, and browser security

17. **Transport and security headers**
    - Verify HTTPS/TLS and appropriate security headers across the real response path, including CDN, reverse proxy, application server, and auth provider where relevant.
    - Check CSP (including legitimate auth/provider requirements), HSTS, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `Permissions-Policy`, and clickjacking protection through `frame-ancestors` and/or `X-Frame-Options` as appropriate.
    - Check CORS allowlists, credential handling, CSRF protection, cache-control for private responses, cookie scope, and redirect behavior.
    - Distinguish headers enforced by application code from those provided by a CDN/host. Verify live responses only when a safe read-only check and correct target are available.

## G. Dependencies, code quality, and testing

18. **Lint, type checks, and test quality**
    - Identify the project's real lint, formatter, type-check, unit, integration, end-to-end, and build commands from scripts and CI configuration.
    - Run suitable read-only checks where safe; do not auto-fix files. Report command, exit status, concise output, and any environmental limitation.
    - Check zero lint/type errors where the project has these checks, but also assess critical-path test coverage and whether tests verify behavior rather than implementation details alone.
    - Review edge cases, race conditions, asynchronous error paths, authorization boundaries, migrations, and regression risks. Group findings by category instead of producing a vague “fix everything” recommendation.

19. **Dependency security and maintenance**
    - Use the repository's actual package manager and lockfile. Run the appropriate read-only audit, such as `npm audit`, `pnpm audit`, `bun audit` where supported, `pip-audit`, `govulncheck`, or `cargo audit`.
    - Identify known critical/high runtime vulnerabilities, abandoned or incompatible packages, dependency confusion risks, unnecessary direct dependencies, and dangerous install/build scripts where relevant.
    - Distinguish production/runtime dependencies from development-only dependencies and explain reachability/exposure where possible. Do not blindly upgrade packages or run automatic fixes.
    - Check whether Dependabot, Renovate, or an equivalent security-update process is configured and active; configuration alone is not proof that updates are being reviewed.

## H. Persistence, data integrity, and recovery

20. **Database and persistence layer**
    - Identify the real production database and verify whether its configuration is appropriate for expected concurrency and reliability. Do not automatically fail a small or embedded product for using SQLite without evaluating its actual deployment and workload.
    - Check connection pooling, connection/query timeouts, transactions, isolation, parameterized queries, indexes for critical queries, constraints, and migration discipline.
    - Verify schema changes are deliberate and compatible with deployment order and rollback constraints. Check whether application code assumes data constraints that the database does not enforce.

21. **Backups and restore tests**
    - Verify backups are scheduled, monitored, retained, access-controlled, encrypted as appropriate, and stored separately from the failure domain of the primary system.
    - Confirm whether a restore has actually been tested into a non-production environment; record the last known restore-test date only if evidence supports it.
    - Identify RPO/RTO expectations if defined, and whether database, uploaded objects, encryption keys, and critical configuration all have a recovery plan.
    - If host access is unavailable, mark the runtime portion `PARTIAL` and list the exact evidence/access needed rather than assuming backups exist.

## I. Deployment, operations, and incidents

22. **Deployment reality and rollback**
    - Establish how deployments really happen from CI/CD and host configuration: automatic on push, release workflow, manual, or another process.
    - Document service deployment order, database migration timing, backward compatibility, worker coordination, health checks, post-deploy smoke tests, and rollback procedure.
    - Check for risky migrations, overlapping deployments, environment drift, incomplete rollbacks, and missing verification after release.
    - Separate verified pipeline configuration from actual host behavior that cannot be observed from this checkout.

23. **Incident response and recovery runbook**
    - Check for a usable runbook covering owners/contacts, severity triage, incident communication, secret rotation, service rollback, backup restore, evidence preservation, and post-incident review.
    - Where applicable, verify that the runbook identifies privacy/regulatory notification responsibilities and correct timelines based on current official legal sources and the jurisdictions/data involved. Do not present GDPR Article 33/34 or a 72-hour deadline as universally applicable without establishing applicability.
    - Identify missing operational ownership or access prerequisites; do not invent contact names or claim a runbook was tested without evidence.

## J. Privacy, legal basis, and app-store compliance

24. **Privacy consistency and data lifecycle**
    - Compare the actual data collected and shared by code/SDKs with the privacy policy, consent flows, in-app disclosures, analytics/advertising configuration, and relevant store privacy labels (Apple App Privacy / Google Play Data safety when applicable).
    - Check consent and opt-in requirements for relevant jurisdictions, tracking/advertising identifiers, data retention, deletion, export, user rights, third-party processors, and the identity/contact of the data controller.
    - Do not claim legal compliance from a policy file alone. Distinguish technical observations from legal conclusions and cite current official requirements where applicable.

25. **Mobile-store submission and release configuration**
    - When a mobile app exists, review current Apple App Store and Google Play requirements applicable to its features and account model.
    - Check review notes, demo/test account requirements when relevant, accurate release notes, encryption/export-compliance answers, required permission strings, privacy declarations, account deletion, purchase flows, and third-party SDK disclosures.
    - Verify actual release configuration, signing/build channels, deep links, notification permissions, and production endpoints where the available evidence permits. If no mobile app exists, mark the section `N/A` with a reason.

## K. AI-agent and workflow platform readiness (conditional)

Apply this section only if the repository implements AI agents, coding agents, tool-using LLM workflows, or an internal agent platform. Otherwise mark each applicable item `N/A` with a reason; do not add an agent platform simply because the project uses an AI API.

26. **Reusable agent definitions**
    - Check whether each agent has an explicit, reviewable definition of purpose, instructions, allowed tools, permitted repositories/resources, model/provider, input schema, output schema, timeout/retry policy, and approval requirements.
    - Prefer a shared, tested execution wrapper over every agent independently rebuilding authentication, tool access, repository setup, retries, logging, and result handling.

27. **Workspace isolation and permissions**
    - Verify each run receives the intended workspace/repository and only the minimum required credentials and tools. Check isolation between concurrent runs, cleanup of temporary workspaces, branch/commit boundaries, network permissions, and protection against cross-repository or cross-user access.
    - Ensure tools are allowlisted and privileged or destructive actions require explicit authorization. Agent instructions alone are not a security boundary.

28. **Reliable execution and observability**
    - Check bounded retries, timeouts, cancellation, concurrency limits, idempotency for retried actions, clear failure states, and safe handling of partial work.
    - Make tool calls, inputs/outputs where safe, execution identity, changed files, approvals, and run results observable without logging secrets or unnecessary personal data.
    - Verify an agent can be invoked consistently through the supported entry points (for example, CLI, chat integration, internal UI, scheduler, or another workflow) without duplicating core execution logic.

29. **Scenario-based evaluation of actual changes**
    - Check for versioned written scenarios that test expected agent behavior, failure modes, and edge cases—not merely whether the model's explanation sounds correct.
    - Evaluate the resulting diff and repository state. Fail a test if an agent claims it fixed a problem but made no effective fix, or claims no change was needed while editing files unexpectedly.
    - Include checks for tests/builds, unintended changes, security regressions, output schema, and preservation of existing behavior. Keep evaluation deterministic where practical and document model-related variance.

30. **Change scope and blast-radius limits**
    - Verify limits on files/paths changed, diff size, runtime, tool calls, spend, and permission escalation where appropriate.
    - Require a clear stop/escalation path when an agent exceeds its allowed scope, encounters ambiguity, sees destructive risk, or cannot establish correctness. Report the actual diff and test results, not just the agent's self-assessment.

