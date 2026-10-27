# Internal linking from Search Console rankings

Source: sources/seo-prompt/tweet-3.md (@asaio87). A sitewide pass that turns each article's best-ranking queries into anchors
in other articles. Use it when the site already has several articles and GSC data. For one new page, use the Linker
prompt in `departments.md` instead.

Needs: 3 months of GSC (CSV in data/ or a GSC connector) and a way to edit the site: the repo itself, or a CMS MCP
(WordPress, Webflow...). Without an edit path, the output is the approved table plus ready-to-paste sentences.

```text
I've attached my Google Search Console export (or: pull it from the GSC connector) for the last 3 months. My website is connected through the [site name] MCP.

1. For each article, find the queries where it ranks best (position 1–10, decent impressions). Those are its target anchors.
2. Go through every published post. Wherever the text naturally mentions another article's top query (or a close variant), turn that phrase into a link to that article.
3. Rules:
   - Max 3–5 new internal links per post, spread through the body (no headings, intro sentence, or existing links)
   - Never link a post to itself, and only link each target once per post
   - Anchor text must read naturally. Don't rewrite sentences just to force a keyword in
   - Prioritize sending links to pages ranking 4–15 (they gain the most)
4. Before changing anything, show me a table: source post → anchor text → target URL → target's query and position. Wait for my OK.
5. After I approve, make the edits through the MCP, then give me a changelog so I can revert if needed.
```

Then: leave the site alone for a few days, and repeat weekly. Also apply AGENCY.md's rules: never the same anchor for two
different targets, and skip source pages that are inside their 90 days unless the user approves. Write the applied changes
to LINKS.md and the changelog to LEDGER.md.
