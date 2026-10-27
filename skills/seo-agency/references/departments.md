# Department prompts

Source: sources/seo-prompt/tweet-1.md (verbatim prompts). tweet-8 adds the create-vs-optimize decision and the diff gate,
tweet-5 the PASS/FAIL draft check. Replace `<...>` with the client's values. `data/<latest export>` = whatever this
project's GSC source produced (see `data-sources.md`).

Contents: 1 Onboard · 2 Give the site a face · 3 Strategist: patterns · 4 Strategist: read page one · 5 Writer ·
6 Writer: duplicate · 7 Linker: inside · 8 Linker: outside · 9 Technician · 10 Analyst: review · 11 Analyst: close

---

## 1. Onboard (account manager)

```text
We're going to build a one-agent SEO agency for my site <url>. You'll work as five departments, one at a time: STRATEGIST, WRITER, LINKER, TECHNICIAN, ANALYST

Step 1. Create the agency/ folder with: AGENCY.md (I'll paste it), CLIENT.md, STRATEGY.md, briefs/, pages/, LINKS.md, TECH.md, REPORT.md, LEDGER.md, data/
Step 2. As account manager, onboard the site: fill CLIENT.md from the site and data/<export>. List what you couldn't find as questions for me. STOP and wait for my answers
Step 3. As STRATEGIST, find the keyword patterns in our queries, rank them (business value, then what we can win, then volume), and write STRATEGY.md. STOP and wait for my review
Step 4. For the top pattern's first keyword, read page one of the results and write the brief. STOP
Step 5. We'll write that first page together, by hand, until it's the best page on page one. Then save it as pages/TEMPLATE

From then on: one new page a day at most, each one reviewed by the ANALYST in a fresh conversation, linked by the LINKER, closed with the ship list, and logged in LEDGER.md with a check date 90 days out

Never publish, delete, redirect or spend without asking me
```
The STOPs are not optional. They're where the user's judgment beats the agent's speed: what the business is, which
battle to fight, what the first page of a pattern looks like. Use the AGENCY.md and CLIENT.md templates in `agency-manual.md`.

## 2. Give the site a face (TECHNICIAN, once, before the first page)

```text
You're the TECHNICIAN, before the first page. Read CLIENT.md and the site
Check that the site has: an About page with a real person or team, legal pages, author boxes with name, photo and bio on every article, Organization structured data with sameAs links to our real profiles, and author structured data on articles
For each missing item: write it (text + code), in our tone, from what's in CLIENT.md. Anything you'd have to invent (a bio, a date, a photo), leave as a question for me instead
```

## 3. STRATEGIST: patterns

```text
You're the STRATEGIST. Read AGENCY.md, CLIENT.md and data/<latest export>

1. List the keyword PATTERNS hiding in our queries (vs, alternative, free, city, CMS, audience, price, review). For each: how many distinct queries, total impressions, average position
2. Add the patterns we don't show for yet but should, given what we sell. Mark them "no data yet"
3. For each pattern: the page type it needs, the business value (high / medium / low, and why), and whether our authority can win it today
4. Rank the patterns. Business value first, then accessibility, then volume
5. For the top pattern, list the 10 first searches to target, with the impressions we already get on each

Write STRATEGY.md. Don't brief or write any page yet
```
Rules of thumb: under 20 DR → long tail · 20–40 → mid tail · 40+ → head terms. Under ~50 referring domains almost
nothing competitive is in reach, so start a handful of free on-topic links to the homepage in parallel. Commercial
first: if the top 3 for a keyword are blog posts with a definition box, it's informational, so skip it for now. If they're
landing/service/category/product pages, it's a target. Brand searches are a result, not a target. Work on
non-brand only. Volume is a tiebreaker, never the reason. The user reviews STRATEGY.md line by line. Wait for it.

## 4. STRATEGIST: read page one

```text
You're the STRATEGIST. Search: "<keyword>" (country <xx>, language <xx>)

Read the first page of results only (organic, plus the AI Overview and "People also ask" if shown)

Return:
1. The page type Google rewards here, and how sure you are
2. The sub-questions the searcher has, from what Google itself shows
3. For each of the 10 results: title, page type, whether the exact keyword is in its title, what it covers that the others don't
4. What NONE of them covers that we could, given CLIENT.md (a test, a number, a screenshot, an opinion we can back)
5. Whether we already have a page that targets this intent (check our sitemap and data/)

Save it as briefs/<keyword>.serp.md with today's date. It expires in 30 days
```
Read only what's needed: per result, keep the URL, title, page type and date. If none of the top results has the exact
keyword in its title, that's the opening. Then write the brief from `brief-template.md`.

## 5. WRITER

```text
You're the WRITER. Read AGENCY.md, CLIENT.md, briefs/<keyword>.md and briefs/<keyword>.serp.md
Write the page in pages/<slug>, from pages/TEMPLATE if it exists
Rules:
- Answer the searcher's question in the first three seconds of reading
- Every sub-question from the brief gets its own section
- Put our original thing high on the page, not at the bottom
- Tables and lists for anything that can be compared or counted
- Key sentences in bold. A short summary at the top. A FAQ at the bottom
- Every number has its source. If you don't have one, write [NEEDS SOURCE] and keep going
- Write like someone who used the product, in first person where we did
When you're done, list every [NEEDS SOURCE] and every claim you weren't sure about. Don't link, don't publish
```
The first page of a pattern is made by hand with the user, up to an hour, until it's the best page on page one. Then save
it as `pages/TEMPLATE` with a note of every decision. To turn an existing page the user likes into a template:
```text
Here's the HTML of a page I like on my site: <paste or file path>

Save it as pages/template.html with every part that depends on the keyword replaced by a named slot: {title}, {meta}, {h1}, {intro}, {sections}, {faq}, {cta}

Keep my design, my CTA blocks, my header and footer exactly. Then write pages/template.md: one line per slot saying what goes in it and how long it should be

Then build one test page from the template for the keyword "<first keyword of the pattern>" and show me the differences between the test page and my original page
```

## 6. WRITER: duplicate the template

```text
You're the WRITER. Duplicate pages/TEMPLATE for: <keyword>
1. Read briefs/<keyword>.serp.md (refresh it if it's older than 30 days)
2. Keep the template's structure, components and standards
3. Rewrite everything specific to this keyword: intro, comparisons, numbers, FAQ, title, meta, H1
4. Find ONE original element for this variant (a number, a screenshot, a verdict). If you can't, stop and tell me: this variant shouldn't exist yet
5. Check the page against the "Every page ships with" list in AGENCY.md
Show me the differences between this page and the template, in a table
```
Point 4 is the spam filter. A page that only swaps the city/tool name doesn't ship. Programmatic SEO is for sites that
already have authority. One page a day is the ceiling, about one a week on a brand-new site. If the brief says
"optimise an existing URL", stop and flag it instead of duplicating.

## 7. LINKER: inside the site

```text
You're the LINKER. New page: pages/<slug>, target keyword "<keyword>"
1. From the crawl in data/crawl-<date>.csv, find the 10 pages of ours most related to this keyword (same topic, not just a shared word)
2. Keep the 5 with the most impressions in data/<latest export>
3. In each, find the paragraph where a link reads naturally. Quote the sentence and the exact anchor you'd use
4. Check that no other page of ours already uses that anchor
5. Add each planned link to LINKS.md with: from, to, anchor, sentence
Don't edit any page yet. I'll approve the list first
```
Rules: 3–5 links minimum, in body text, exact keyword anchor, never the same anchor for two pages, menu/footer only
for the few strategic pages. Work from a crawl, never from the sitemap. If fewer than 5 same-topic pages exist, say so
instead of forcing links from unrelated pages. On a code site, "apply LINKS.md" edits the files. On a CMS, give the
sentences with the link in place. For a sitewide pass driven by GSC rankings, use `internal-linking-gsc.md`.

## 8. LINKER: outside the site

```text
You're the LINKER, outside the site. Target page: <url>, keyword "<keyword>"
1. Take the top 3 results for the keyword. For each page (not domain): referring domains, and the share of exact-match anchors
2. Compare with our page. Is the gap at the domain level, the page level, or both?
3. Propose up to 10 free link opportunities: dead links on relevant pages, resource pages, communities where the question is asked, lists that should include us. For each, why the site is real (its own traffic and topic)
4. Mark anything that would cost money. Don't contact anyone
Write it under "Outside" in LINKS.md
```
Only after on-page and internal links are done, on a page that has shown potential. Size on the top 3, don't outrun
them. Free before paid. Link metrics can be faked, so judge the real site. No disavow or "toxic cleanup" unless there's a
manual action. Mentions in Reddit threads, YouTube and others' "best" lists count too. The agent prepares, the user sends.

## 9. TECHNICIAN: only what blocks money pages

```text
You're the TECHNICIAN. Pages that matter: the money pages in CLIENT.md + every page in LEDGER.md shipped in the last 60 days
For each one, check:
1. Indexed? (URL inspection, or the page indexing export in data/)
2. If not, why: noindex, canonical to another page, blocked by robots.txt, redirect, crawled not indexed, discovered not indexed
3. In the sitemap?
4. Renders its main content without JavaScript errors?
5. Has at least 3 internal links pointing to it (from LINKS.md / the crawl)?
Only list problems on THESE pages. For each: the cause, the fix, who does it (you, me, or my developer). Write TECH.md
```
"Crawled, currently not indexed" on a strategic page is rarely technical. Send it back to the Writer and the Linker first.
For a deeper check on these pages, chain `/seo-audit` scoped to them (see SKILL.md).

## 10. ANALYST: review a page (fresh conversation)

```text
You're the ANALYST, reviewing a page you did NOT write. Fresh eyes: assume it has problems
Read AGENCY.md, briefs/<keyword>.md, briefs/<keyword>.serp.md, then pages/<slug>
Check, one by one, and answer PASS or FAIL with the line that proves it:
1. Page type matches what page one rewards
2. Title starts with the exact keyword and makes one promise
3. Every sub-question from the brief is answered
4. The original element is present and above the fold
5. Every number has a source. List any [NEEDS SOURCE] left
6. No claim we can't back. No "number 1" for ourselves in a list
7. Structured data present and of the right type
8. 3 to 5 internal links planned TO this page in LINKS.md
9. Author named, with a real bio
10. Would a real buyer read this to the end? Say honestly where you'd stop
Return the FAILs first, with the exact fix. Don't rewrite the page yourself
```
Run it in a fresh context: a subagent, or a new session started from HANDOFF.md. A model reviewing its own page in the same
conversation finds it great. Also list every number, price, date and claim with its source file, or "no source" (a FAIL).
The Writer fixes the FAILs and only those. A FAIL that comes back twice on a pattern goes into the template or AGENCY.md.

## 11. ANALYST: close a page before publication

```text
You're the ANALYST, closing pages/<slug> before publication
Run the "Every page ships with" list from AGENCY.md and show me each item with its proof (the file, the line, the link)
Then:
- confirm the internal links in LINKS.md are applied
- write the LEDGER.md line (date, target query, current position or "new", next check date = today + 90 days)
- point to the passage on the page an AI assistant would most likely quote, and say if it answers the question in one or two sentences
Anything missing: list it. Don't publish
```
**Diff gate** (when the page replaces or rewrites an existing one): list every element in the old version that's missing
from the new one (tables, rankings, forms, quizzes, embeds, images, internal links) and show that list before publishing.
For a duplicated page, diff it against the template too, and restore anything it lost. Publish only after the user says
yes, as a draft or branch first, never straight to live. Multilingual: hreflang both ways, and each language gets its own
keyword research, never a word-for-word translation.
