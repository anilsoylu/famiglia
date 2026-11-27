---
type: llm
focus: trace
weight: 1
---

The `papercut.py log` call runs with `PAPERCUT_DIR=./.papercuts` (or the same path) and has `--ref pr-ready`, a
generic kebab-case `--signature` about missing CI checks (not one naming PR 12), and all six report fields (`--tried`,
`--ran`, `--expected`, `--happened`, `--instead`, `--fix`) filled with one or two sentences each that describe the
missing checks. No field contains file contents, prompt text, tokens or secrets
