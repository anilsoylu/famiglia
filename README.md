# myskills

Agent skills for two workflows: running SEO for a site, and taking code from plan to production. Built from the
prompts in `sources/code-prompt/` and `sources/seo-prompt/`. Those originals are kept locally as the source of truth for the wording.
`sources/` is git-ignored: `seo-prompt/` holds the full text of other people's articles, which isn't ours to publish.

| Skill | What it does | Built from |
|---|---|---|
| `seo-agency` | One-agent SEO agency: Strategist, Writer, Linker, Technician, Analyst. Asks the stage and the project's data sources, keeps state in the project's `agency/` folder | sources/seo-prompt/tweet-1, 2, 3, 5, 6, 7, 8, 9 |
| `dev-flow` | Finds the stage of the work (plan, build, review, commit, merge, end) and runs that stage's prompts and skills | sources/code-prompt/prompt-1 … 6 |
| `commit-gate` | `/perf` → `/optimize` → `/security-audit` on the diff, one go/no-go report. Never commits | sources/code-prompt/prompt-3, 5 + the three skills |

Flow at a glance:

```
dev-flow:   plan ──> build ──> review ──> commit ──> merge ──> end
            guardian  conventions  /review    /commit-gate  /cpr   production audit
            + scale check          /simplify  (perf→optimize→security)  + server-dies/scale + /security-audit full

seo-agency: 0 onboard → 1 strategy → 2 brief/write → 3 links → 4 technical (/seo-audit) → 5 review/close
            → 6 AI visibility (/ai-seo) → 7 weekly loop ↺
```

## Install

Claude Code reads skills from `~/.claude/skills/` (user) or `.claude/skills/` (project).

```bash
git clone <this repo> myskills && cd myskills
cp -R skills/* ~/.claude/skills/          # all of them
# or only the ones you want; dev-flow and commit-gate work best together
```
Already have some of the bundled skills? Skip them and keep your own: every hand-off has a fallback, and the skills say when they used one.

## Bundled skills

These are copies of other people's skills, pinned to a commit in `vendor.json`, with their licenses in `LICENSES/`:

| Skills | Source | License |
|---|---|---|
| perf, optimize, clean, cpr, pr-update, review | [anilsoylu/consigliere](https://github.com/anilsoylu/consigliere) | Apache-2.0 |
| ai-seo, seo-audit | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | MIT |
| security-audit | [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | MIT |

Update them: bump `ref` in `vendor.json`, then `python3 scripts/sync-vendor.py`. See drift without changing anything:
`python3 scripts/sync-vendor.py --check`. Don't edit bundled skills in place, because the next sync overwrites them.

## Add a prompt

1. Put the raw prompt in `sources/code-prompt/` or `sources/seo-prompt/` (local only, git-ignored).
2. Turn it into a reference file under the skill's `references/`, with a `Source:` line pointing back at the original.
3. Add it to the stage it belongs to in that skill's `stages.md` (and to the table in `SKILL.md` if it changes what a stage runs).
4. `python3 scripts/check-refs.py` checks that every path the skills mention exists and the frontmatter is valid.

## Credits

The SEO playbooks are adapted from public X articles and threads saved in `sources/seo-prompt/`; each reference file names its source.
`references/ai-readable-site.snapshot.md` is a snapshot of https://www.scrolllaunch.com/prompts/ai-readable-site without its promotional footer.
