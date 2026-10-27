# Changelog

## 0.1.0 — 2026-10-27
- `seo-agency`: stage-aware SEO agency (5 departments, 8 stages) built from sources/seo-prompt/ playbooks; chains /seo-audit and /ai-seo.
- `dev-flow`: plan → build → review → commit → merge → end, built from sources/code-prompt/1–6; chains /review, /simplify, /commit-gate, /cpr, /security-audit.
- `commit-gate`: /perf → /optimize → /security-audit on the diff, one go/no-go report.
- Bundled third-party skills pinned in vendor.json (marketingskills, security-audit-skill).
- After eval round 1: dev-flow end stage runs /security-audit in guidance mode and asks before full mode; hardcoded credential literals stay blockers until the user confirms they're fake.
- Repo named famiglia. perf, optimize, clean, cpr, pr-update and review are maintained here. Added pr-ready, pr-triage, list-open-work, no-tropes; updated perf and pr-update.
- review ships its own tier script (review-tier.mjs) and reviewer prompt (reviewer.md). perf points known routines to /optimize again and runs clean before pr-update. optimize defines parity for UI/render code.
- README rewritten as a short how-to.
