# Guide for agents

How to change famiglia without breaking its skills or the skills it bundles.

## What this repo is

A set of agent skills in `skills/<name>/SKILL.md`, following the [Agent Skills spec](https://agentskills.io). No build
step. The repo is also a Claude Code, Codex and Cursor plugin (`.claude-plugin/`, `.codex-plugin/`, `.cursor-plugin/`,
`.agents/plugins/`).

Keep every skill portable. Write instructions any agent can follow. Name a tool from one agent only as an example
("ask one question, with AskUserQuestion in Claude Code"), and give the fallback when other agents lack it.

## Two kinds of skill

- **Ours**: `commit-gate`, `dev-flow`, `optimize`, `review`, `seo-agency`. Edit them directly. Keep their descriptions
  short, because every description is read in every session (`python3 scripts/skill-size.py` shows the sizes).
- **Vendored**: everything listed in `vendor.json`. These are byte-for-byte copies of upstream, so `npx skills update`
  can replace them without conflict. **Never edit them.** To update one, bump its `ref` (or run `--latest`) and sync.
  If a vendored skill does something we don't want, change our own skill that calls it.

## Commands

```bash
python3 scripts/sync-vendor.py            # re-copy vendored skills at their pinned refs, refresh vendor.lock.json
python3 scripts/sync-vendor.py --latest   # bump every ref to upstream HEAD, then sync
python3 scripts/sync-vendor.py --check    # exit 1 if a vendored skill drifted from upstream
python3 scripts/check-refs.py             # frontmatter + spec checks, every file a skill points to exists
python3 scripts/sync-readme.py            # regenerate the README skill and credits tables (--check to verify)
npx skills add . --list                   # what the Skills CLI sees
claude plugin validate .                  # plugin manifests
```

A new skill goes into `GROUPS` in `scripts/sync-readme.py`, and its third-party license goes in `LICENSES/<repo>/`.

## Evals

Cases live in `evals/<skill>/<case>/`: real failures from past sessions plus routing checks between neighbouring skills.
Run them before and after a change, and keep the change only if nothing drops:

```bash
claude plugin eval . --model claude-opus-5-5 --scaffold --trust-plugin --allow-tools Bash Write Edit -j 4 --no-publish
```

## Before you commit

Run `sync-vendor.py --check`, `check-refs.py` and `sync-readme.py --check`. Add a `CHANGELOG.md` line for any change in
behavior. Keep the version the same in all four manifests.

## Writing style

Plain language: the main point first, common words, active voice, short sentences, one term for one thing. Keep exact
commands, paths and identifiers.
