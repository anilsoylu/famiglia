# famiglia

Agent skills for three jobs: shipping code from plan to production, running SEO for a site, and writing that doesn't
read as AI. Works with Claude Code, Codex, Cursor and any agent that supports the
[Agent Skills spec](https://agentskills.io).

famiglia is five skills of its own (`dev-flow`, `review`, `commit-gate`, `optimize`, `seo-agency`) plus the best
skills they hand work to, bundled unchanged from their authors. See [Credits](#credits) for those.

## Install

### Any agent (recommended)

```bash
npx skills add anilsoylu/famiglia                          # pick skills and agents interactively
npx skills add anilsoylu/famiglia --skill dev-flow review   # only some skills
npx skills add anilsoylu/famiglia --list                    # see what's in here
```

Add `-g` to install for your user instead of the current project. If you run the command from inside an agent
session, name the agent (`-a claude-code`, `-a codex`, `-a cursor`), or the CLI may install only to `.agents/skills/`.

### Claude Code plugin

```text
/plugin marketplace add anilsoylu/famiglia
/plugin install famiglia@famiglia
```

Outside an interactive session: `claude plugin marketplace add anilsoylu/famiglia`, then
`claude plugin install famiglia@famiglia`.

### Codex plugin

```bash
codex plugin marketplace add anilsoylu/famiglia
```

Then run `/plugins` inside Codex and pick **famiglia**.

### Copy by hand

```bash
git clone https://github.com/anilsoylu/famiglia.git
cp -R famiglia/skills/* ~/.claude/skills/                   # or your agent's skills folder
cp famiglia/skills/review/reviewer.md ~/.claude/agents/    # optional, Claude Code only
```

Installing replaces any skill you already have with the same name (for example a local `ui-ux-pro-max`).

## Use

Just talk. The right skill picks itself up. You can also call one directly with `/name`.

**Code**

| You say | What runs |
|---|---|
| "let's build team invites" | `dev-flow` → plan: risk review, "what if the server dies / scales" check, a plan file for approval |
| "make this screen look premium" | `ui-ux-pro-max` or `frontend-design`, then `ui-only` while you iterate on the look |
| "feature's done, what's next?" | `dev-flow` → review: inefficiency review, `/review`, `/simplify` |
| "ready to commit" / `/commit-gate` | `/perf` → `/optimize` → `/security-audit` on the diff, one go/no-go report. Never commits |
| "open a PR" / `/cpr` | `clean` → `pr-update`, ends with the PR link |
| "merge to master" | `dev-flow` → merge: `/cpr`, then waits for green checks, merges and pulls |
| "fix CI", "address the reviews" | `pr-ready` |
| "is it production ready?" | `dev-flow` → end: production audit with a scorecard and the "server dies / scale" answers |

**SEO**

| You say | What runs |
|---|---|
| "start SEO for mysite.com" | `seo-agency` → onboarding: asks the stage and your data sources, sets up `agency/` in your project |
| "what should we rank for?" | strategy: keyword patterns with buying intent, a read of page one |
| "write a page for <keyword>" | brief → write → fresh-context review → ship list |
| "weekly SEO pass" | Search Console quick wins, respects the 90-day wait, stops for your pick |
| "get us cited by ChatGPT/Claude" | AI visibility, with `/ai-seo` |
| "add structured data" | `schema` |

`seo-agency` keeps its state in your project's `agency/` folder, so the next session picks up where the last one stopped.

**Writing**

Two skills remove AI tells. Install both and pick per job, or keep the one you like.

| Skill | Use it for |
|---|---|
| `no-tropes` | a quick self-check on text the agent writes: PR bodies, commit messages, comments, docs |
| `humanizer` | rewriting existing text so it reads like its writer: 26 patterns, strongest first, voice matching |

**Growth**

| You say | What runs |
|---|---|
| "who almost paid?", "win back abandoned checkouts" | `almost-paid`: segments, value, an offer per segment, never sends |
| "this landing page doesn't convert" | `cro` |

## How the skills fit together

```text
dev-flow: one stage at a time

  plan     risk review, "what if the server dies or scales?",
           a plan file you approve before any code
  build    frontend-design, ui-ux-pro-max, ui-only,
           vercel-react-best-practices, tests first for bug fixes
  review   inefficiency pass, /review, /simplify
  commit   commit-gate: perf → optimize → security-audit,
           one go/no-go report, never commits
  merge    /cpr (clean → pr-update), then green checks → merge
           pr-ready handles red CI and review threads
  end      production audit + security-audit

seo-agency: strategy → pages → links → technical → AI visibility → weekly loop

  pages          copywriting, schema, programmatic-seo, site-architecture
  technical      seo-audit
  AI visibility  ai-seo
```

Every hand-off has a fallback, so a skill still works when you install it alone.

## Skills

<!-- SKILLS:START -->
### Code: plan to production

| Skill | What it does | From |
|---|---|---|
| [dev-flow](skills/dev-flow/) | Stage-aware delivery flow for a feature or project: plan with the guardian risk review, build, review, commit gate, merge through /cpr, and the… | famiglia |
| [review](skills/review/) | Review a finished diff: tier check, one reviewer, findings routed. | famiglia |
| [commit-gate](skills/commit-gate/) | Pre-commit gate: /perf, /optimize, then /security-audit on the current diff, one go/no-go report. | famiglia |
| [perf](skills/perf/) | The general profile-driven perf loop for any language or runtime: baseline, profile, fix the real hot path, re-measure. | [OutThisLife/brooklyn-skills](https://github.com/OutThisLife/brooklyn-skills) |
| [optimize](skills/optimize/) | Exact-parity speed rewrite of a named routine or the diff's hot spot: shorter, measurably faster, same behavior. | famiglia |
| [security-audit](skills/security-audit/) | Security guidance and vulnerability review for codebases, APIs, services, CLI tools, libraries, and daemons. | [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) |
| [clean](skills/clean/) | Polish your own diff by hand with KISS/DRY and local style — the pre-handoff pass, not a test run and not a subagent sweep. | [OutThisLife/brooklyn-skills](https://github.com/OutThisLife/brooklyn-skills) |
| [cpr](skills/cpr/) | Clean the diff, then open or refresh the PR/MR — one pass, ending in the linked URL. | [OutThisLife/brooklyn-skills](https://github.com/OutThisLife/brooklyn-skills) |
| [pr-update](skills/pr-update/) | Open a PR/MR if missing, or refresh an existing one's title and description so they match the current diff. | [OutThisLife/brooklyn-skills](https://github.com/OutThisLife/brooklyn-skills) |
| [pr-ready](skills/pr-ready/) | Clear everything blocking an existing PR/MR from merging — rebase onto the default branch, get CI green, and resolve review threads (Copilot and… | [OutThisLife/brooklyn-skills](https://github.com/OutThisLife/brooklyn-skills) |
| [pr-triage](skills/pr-triage/) | Maintainer triage on OTHER people's PRs/MRs — verdict of approve, supersede, or close, salvage with credit, close the cluster. | [OutThisLife/brooklyn-skills](https://github.com/OutThisLife/brooklyn-skills) |
| [stacked-pr](skills/stacked-pr/) | Handle dependent/stacked PRs and same-code-on-multiple-bases correctly. | [OutThisLife/brooklyn-skills](https://github.com/OutThisLife/brooklyn-skills) |
| [list-open-work](skills/list-open-work/) | List my open MRs/PRs in the current repo/worktree, each with its tracker ticket. | [OutThisLife/brooklyn-skills](https://github.com/OutThisLife/brooklyn-skills) |

### UI and frontend

| Skill | What it does | From |
|---|---|---|
| [frontend-design](skills/frontend-design/) | Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. | [anthropics/skills](https://github.com/anthropics/skills) |
| [ui-ux-pro-max](skills/ui-ux-pro-max/) | UI/UX design intelligence for web, mobile, and desktop. | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) |
| [ui-only](skills/ui-only/) | While iterating on UI, do not waste time on tsc, lint, typecheck, format, full test suites, commit, or push until the user likes how it looks and… | [OutThisLife/brooklyn-skills](https://github.com/OutThisLife/brooklyn-skills) |
| [ui-system](skills/ui-system/) | Reuse existing UI primitives, CSS vars, and DESIGN.md patterns instead of inventing new buttons, colors, borders, shadows, or helpers — including… | [OutThisLife/brooklyn-skills](https://github.com/OutThisLife/brooklyn-skills) |
| [visual-verify](skills/visual-verify/) | Use to verify rendered UI against its design reference. | [OutThisLife/brooklyn-skills](https://github.com/OutThisLife/brooklyn-skills) |
| [vercel-react-best-practices](skills/vercel-react-best-practices/) | React and Next.js performance optimization guidelines from Vercel Engineering. | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) |

### SEO and AI search

| Skill | What it does | From |
|---|---|---|
| [seo-agency](skills/seo-agency/) | Run SEO for a site as a staged one-agent agency (strategy, pages, links, technical checks, reports, AI visibility, the weekly Search Console loop),… | famiglia |
| [seo-audit](skills/seo-audit/) | When the user wants to audit, review, or diagnose SEO issues on their site. | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) |
| [ai-seo](skills/ai-seo/) | When the user wants to optimize content for AI search engines, get cited by LLMs, or appear in AI-generated answers. | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) |
| [schema](skills/schema/) | When the user wants to add, fix, or optimize schema markup and structured data on their site. | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) |
| [programmatic-seo](skills/programmatic-seo/) | When the user wants to create SEO-driven pages at scale using templates and data. | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) |
| [site-architecture](skills/site-architecture/) | When the user wants to plan, map, or restructure their website's page hierarchy, navigation, URL structure, or internal linking. | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) |
| [link-building](skills/link-building/) | When the user wants to earn backlinks or third-party mentions that lift rankings and AI citations. | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) |
| [competitors](skills/competitors/) | When the user wants to create competitor comparison or alternative pages for SEO and buyer-facing use. | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) |
| [content-strategy](skills/content-strategy/) | When the user wants to plan a content strategy, decide what content to create, or figure out what topics to cover. | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) |

### Writing

| Skill | What it does | From |
|---|---|---|
| [no-tropes](skills/no-tropes/) | Detect and eliminate common AI writing tropes from generated text. | [OutThisLife/brooklyn-skills](https://github.com/OutThisLife/brooklyn-skills) |
| [humanizer](skills/humanizer/) | Rewrite AI-sounding text so it reads like the writer without changing what it says. | [blader/humanizer](https://github.com/blader/humanizer) |
| [copywriting](skills/copywriting/) | When the user wants to write, rewrite, or improve marketing copy for any page, including homepage, landing pages, pricing pages, feature pages,… | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) |

### Growth and analytics

| Skill | What it does | From |
|---|---|---|
| [cro](skills/cro/) | When the user wants to optimize, improve, or increase conversions on any marketing page or form — including homepage, landing pages, pricing pages,… | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) |
| [analytics](skills/analytics/) | When the user wants to set up, improve, or audit analytics tracking and measurement. | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) |
| [lead-magnets](skills/lead-magnets/) | When the user wants to create, plan, or optimize a lead magnet for email capture or lead generation. | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) |
| [almost-paid](skills/almost-paid/) | Find the users who almost paid — saw the paywall, started checkout, ran out of free credits, let a trial lapse — size what they are worth, and turn… | [nestyme/awesome-prompts](https://github.com/nestyme/awesome-prompts) |
<!-- SKILLS:END -->

## Updating

- Installed with `npx skills`: run `npx skills update`. It tracks this repo, so you get a bundled skill's new version
  once famiglia picks it up.
- Claude Code plugin: `/plugin marketplace update famiglia`. Codex: `codex plugin marketplace upgrade`.

## Contributing

Issues and PRs are welcome. [AGENTS.md](AGENTS.md) explains the layout, the scripts and the evals. In short: edit our
five skills directly; never edit a bundled one, bump its pin in `vendor.json` instead.

## Credits

The bundled skills are byte-for-byte copies from their authors, pinned in `vendor.json`. Their licenses are in
[LICENSES/](LICENSES/).

<!-- CREDITS:START -->
| Source | Skills | License | Pinned at |
|---|---|---|---|
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | `ai-seo`, `analytics`, `competitors`, `content-strategy`, `copywriting`, `cro`, `lead-magnets`, `link-building`, `programmatic-seo`, `schema`, `seo-audit`, `site-architecture` | MIT | `0cd9b3a` |
| [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | `security-audit` | MIT | `c1c8a8c` |
| [OutThisLife/brooklyn-skills](https://github.com/OutThisLife/brooklyn-skills) | `clean`, `cpr`, `list-open-work`, `no-tropes`, `perf`, `pr-ready`, `pr-triage`, `pr-update`, `stacked-pr`, `ui-only`, `ui-system`, `visual-verify` | MIT | `b28c329` |
| [anthropics/skills](https://github.com/anthropics/skills) | `frontend-design` | Apache-2.0 | `ca45fc4` |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | `vercel-react-best-practices` | MIT | `1a2c79d` |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | `ui-ux-pro-max` | MIT | `28b3b8d` |
| [blader/humanizer](https://github.com/blader/humanizer) | `humanizer` | MIT | `0ef9fe5` |
| [nestyme/awesome-prompts](https://github.com/nestyme/awesome-prompts) | `almost-paid` | none (shared publicly by the author) | `d200ba5` |
<!-- CREDITS:END -->

`review` started from Matt Pocock's [`code-review`](https://github.com/mattpocock/skills) skill (MIT) and has since
been rewritten. `almost-paid` comes from a repo with no license file. Its author shared it publicly, and it stays theirs
(see [LICENSES/awesome-prompts](LICENSES/awesome-prompts/README.md)).

## License

famiglia's own code and skills are [Apache-2.0](LICENSE). Bundled skills keep their own licenses.
