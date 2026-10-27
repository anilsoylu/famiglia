<!-- Source: sources/code-prompt/prompt-1.md (verbatim slice, lines 269-331). -->

# Phase 4 — Validation and scorecard

1. Consolidate duplicate symptoms into a single root-cause finding when appropriate, while keeping every checklist item individually rated.
2. Separate confirmed issues from hypotheses, and code evidence from production/runtime evidence.
3. For each critical/high issue, explain the user/security/reliability/business impact and the smallest safe remediation.
4. When multiple fixes exist, recommend the least invasive option first and briefly state meaningful trade-offs. Clearly separate required release blockers from optional improvements.
5. Do not change code during the audit. If the user later approves remediation, create a narrowly scoped plan, establish baseline tests, make only approved changes, and run relevant regression/equivalence checks. Stop and ask if a requirement is ambiguous or the approved scope would need to expand.

## Required final report

Deliver the report in this order:

### 1. Executive summary

- Overall verdict: `Release blocker`, `Not production-ready`, `Conditionally ready`, or `Ready based on available evidence`.
- The most important three to five findings, ordered by severity.
- Scope and key limitations, including unavailable production/host/store access.

### 2. Detected stack and trust boundaries

A compact table with component, actual technology/provider, resolved version if applicable, where it is used, and confidence/evidence. Include relevant web/mobile/API/worker/admin boundaries and external services.

### 3. Versioned documentation matrix

A table with library/component, installed version, canonical official documentation URL(s), version-match status, and relevant audited behavior. Cite docs inline in findings where needed.

### 4. Checklist scorecard

Include all 30 items, each with status, priority, evidence, verification gap, and one-line fix. A compact table is acceptable, but do not omit evidence to make it shorter. Add a short status summary showing counts of `PASS`, `PARTIAL`, `FAIL`, and `N/A`. Do not represent `N/A` as a passed control.

### 5. Prioritized fix list

Group into:

- **P0 — Critical release blockers**
- **P1 — High priority before release or immediately after, with justification**
- **P2 — Medium priority**
- **P3 — Low priority / optional improvements**

For each fix, include the related checklist item(s), the smallest proposed change, impacted files or components, how success will be tested, and any dependency or risk. Keep optional architectural ideas separate from required fixes.

### 6. Commands and checks performed

List the safe checks actually run, their results, skipped checks and why they were skipped. Do not claim a command ran when it did not. Redact sensitive output.

### 7. Required decisions and missing access

List only decisions or access genuinely needed to finish verification or implement an approved fix (for example, production read-only access, monitoring/backup evidence, a product behavior decision, or explicit approval for a change). State what each would unblock. Do not ask questions that the repository can answer.

### 8. Optional long-term recommendations

Provide a short separate section for durable improvements with clear benefit and trade-offs. Do not mix these with release blockers or implement them without approval.

## Final constraints

- Be specific, skeptical, concise, and evidence-driven. Avoid generic best-practice lectures.
- Never invent files, line numbers, test results, production configuration, backups, alerts, or compliance status.
- Do not modify unrelated code or expand scope for aesthetic reasons.
- Do not add UI helper text or subtitles by default when discussing UI changes.
- Preserve exact behavioral parity for approved optimizations unless the user explicitly authorizes a behavior change.
- Ask before making assumptions that materially affect implementation; explicitly flag unresolved uncertainty.
- End with the scorecard, prioritized remediation plan, and the exact decisions/access still required.

