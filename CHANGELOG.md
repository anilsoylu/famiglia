# Changelog

## 0.1.0 — 2026-10-27
- `seo-agency`: stage-aware SEO agency (5 departments, 8 stages) built from sources/seo-prompt/ playbooks; chains /seo-audit and /ai-seo.
- `dev-flow`: plan → build → review → commit → merge → end, built from sources/code-prompt/1–6; chains /review, /simplify, /commit-gate, /cpr, /security-audit.
- `commit-gate`: /perf → /optimize → /security-audit on the diff, one go/no-go report.
- Bundled third-party skills pinned in vendor.json (consigliere, marketingskills, security-audit-skill).
- After eval round 1: dev-flow end stage runs /security-audit in guidance mode and asks before full mode; hardcoded credential literals stay blockers until the user confirms they're fake.
