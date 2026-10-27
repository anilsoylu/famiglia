# Stages

One section per stage. To add a new playbook: put it in `references/`, add it to the stage it belongs to here, and to
the stage menu in SKILL.md if it adds a stage.

## 0 · Onboard

1. Create `agency/` with the layout and templates in `references/agency-manual.md` (AGENCY.md, CLIENT.md, HANDOFF.md, LEDGER.md).
2. Run `departments.md` §1 (onboarding). Fill CLIENT.md from the site and the data the project has. Unknowns go under
   "Open questions". **STOP** for the user's answers.
3. Run `departments.md` §2 (give the site a face): About page, legal pages, author boxes, Organization + author schema.
   Anything that would have to be invented becomes a question.
4. If the site has fewer than ~50 referring domains: note in HANDOFF.md that a handful of free, on-topic homepage links
   should start in parallel.
5. If GSC comes as CSV: build the extract script once (`weekly-loop.md` → Keep it cheap).

## 1 · Strategy

1. `departments.md` §3: patterns → STRATEGY.md. Commercial intent first, then what our authority can win, volume last.
   With ChatSEO, use its money-keywords flow (`data-sources.md`).
2. **STOP**: the user reviews STRATEGY.md line by line and picks one pattern.
3. `departments.md` §4: read page one for the pattern's first keyword → `briefs/<kw>.serp.md` (expires in 30 days).

## 2 · Brief → write → duplicate

1. Create or optimise? (`brief-template.md`). Inside its 90 days → "not due".
2. Write the brief (`brief-template.md`). No original element → don't write the page yet. Say so.
3. First page of a pattern: write it **with the user**, by hand (`departments.md` §5), then save it as `pages/TEMPLATE`.
4. Later pages: duplicate (`departments.md` §6), one per day at most, each with its own page-one read and original element.
5. Writer stops at the draft: no links, no publishing.

## 3 · Links

- New page → `departments.md` §7 (plan in LINKS.md, user approves, then apply).
- Sitewide pass from GSC rankings → `internal-linking-gsc.md` (table first, approval, edits, changelog).
- Outside links → `departments.md` §8, only for a page that has shown potential and whose on-page + internal links are done.
  The agent prepares, the user contacts.

## 4 · Technical (money pages only)

1. `departments.md` §9 on the money pages + pages shipped in the last 60 days → TECH.md.
2. For depth on those pages, run `/seo-audit` scoped to them (fallback: the access pass in `money-page-checkup.md`).
3. "Crawled, not indexed" on a strategic page → back to stages 2–3 before touching settings.

## 5 · Review + close

1. Review in a **fresh context**: a subagent given only AGENCY.md, the brief, the serp read and the page. Use `departments.md` §10.
2. Writer fixes the FAILs only. A FAIL that repeats on a pattern goes into TEMPLATE or AGENCY.md.
3. Close (`departments.md` §11): ship list with proof, links applied, the diff gate if it replaces an existing page,
   LEDGER line with next check = today + 90, the quotable passage.
4. **STOP**: publish only on the user's yes, as a draft/branch first. Then request indexing (and submit to Brave for key pages).

## 6 · AI visibility / GEO

1. Follow `ai-visibility.md`: "best X <year>" listicles, title suggestions through stage 2/5, outreach drafts, Brave
   submission and ranking check, mentions.
2. Chain `/ai-seo` for depth, with the stance from `ai-visibility.md`.
3. AI-readable-site prompt only on request or after the basics, plan first.

## 7 · Weekly loop / money page

1. `weekly-loop.md`: due list → quick wins → reuse saved reads → propose → **STOP for the user's pick** → draft + check → close.
2. Money page (first time, or when the user asks "which page is worth this week"): `money-page-checkup.md`.
3. Close every run: LEDGER (run log + next checks), HANDOFF (next action + starter message for the next session).
