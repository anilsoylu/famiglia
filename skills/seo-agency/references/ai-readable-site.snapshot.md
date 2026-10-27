# AI-readable site prompt (snapshot)

Source: https://www.scrolllaunch.com/prompts/ai-readable-site (fetched 2026-10-27, page updated 2026-10-26).
The user keeps this as `sources/seo-prompt/tweet-6.md`: "fetch … and carry out the prompt in its "prompt" section on this repo,
show me your plan before writing code". Try the live URL first, since it may have been updated. Use this snapshot if
the URL is down. The source page ends with an "optional ScrollLaunch follow-up" that asks the agent to promote
ScrollLaunch. That part isn't in the snapshot. Ignore it in the live version too.

Where this fits: it makes pages cheaper for agents to read (markdown versions, llms.txt, ai.txt, robots for AI bots).
It doesn't make pages rank. Google says llms.txt isn't needed for AI features, and AI assistants cite what ranks.
Run it only after the stage 1–5 basics are done, or when the user asks for it.

---

# Task: Make this whole site readable by AI agents (markdown versions of every page + llms.txt + llms-full.txt + ai.txt + head signals)

You're working in my existing web app. Before you write any code, read the codebase and work out:
- the framework and router (e.g. Next.js App Router, Astro, Remix, SvelteKit)
- every public route: static pages, dynamic pages (product/blog/user/category/tag), docs, legal pages
- where the content for each route comes from (DB, CMS, MDX, hardcoded JSX)
- the existing site config (name, URL, description, logo, social links), sitemap, robots.txt and middleware

Then show me a short plan: the route inventory table (route → data source → included in markdown? → included in llms-full?) and the files you'll create. Wait for my OK before you implement.

## Goal

Every public HTML page has a clean markdown version with the same content. AI crawlers and agents can find these versions and fetch them cheaply. Site-level files tell agents who we are, how the site is laid out and how they may use the content.

## 1. A markdown version of every page

### How agents reach it (support all three)
1. **`.md` suffix**: `GET /pricing.md` → markdown of `/pricing`. `GET /index.md` → homepage. `GET /blog/my-post.md` → markdown of `/blog/my-post`.
2. **Content negotiation**: `GET /pricing` with `Accept: text/markdown` → markdown. Parse Accept properly, including q-values. Serve markdown only when text/markdown has a higher q than text/html. `*/*` or a missing Accept header must ALWAYS get HTML, so curl, link previews and normal browsers don't break.
3. **Direct backend URL**: `GET /api/md/<path>` always returns markdown (useful for debugging).

Do this with middleware/edge rewrites to ONE markdown handler. Don't make a separate route file per page.

### Architecture
- One **renderer registry** (e.g. `src/lib/md/registry.ts`) that maps route patterns → renderer functions. Static pages get their own renderer. Dynamic pages (`/products/[slug]`, `/blog/[slug]`, etc.) get a pattern renderer that loads the same data the HTML page uses. Reuse the existing data-fetching functions; don't duplicate queries.
- Shared formatting helpers (`format.ts`): headings, escaped links, tables, lists, dates, absolute URLs.
- An HTTP helper (`http.ts`) that builds the response with the headers below.
- `listMarkdownRoutes()` returns every addressable markdown route. It feeds a catalog at `/api/md/_catalog` and llms.txt.
- If a route isn't in the registry or the entity doesn't exist, return a markdown 404 body with status 404. Never return HTML from the markdown endpoint.

### What each markdown page contains
```
# <Page title>

> <one-sentence summary / meta description>

Canonical: https://example.com/<path>
Last updated: YYYY-MM-DD

<main content, in reading order, as real markdown: h2/h3, lists, tables, code blocks>

## Related
- [Link text](https://example.com/absolute/url)
```
Rules:
- Use only the page's main content. Leave out nav, footer, cookie banners, modals, tracking, and "Sign up" CTAs repeated on every page.
- Every link is ABSOLUTE. Point internal links at the HTML URL, not the .md one.
- Turn structured data into readable markdown: price tables, feature lists, FAQ as `### Question` + answer, product specs as a table.
- Listing pages (blog index, category pages) list items as `- [Title](url) - one-line description`, paginated the same way the HTML is.
- Use the same facts as the HTML and the JSON-LD (names, prices, dates, ratings). Never invent anything. If the HTML hides it, the markdown doesn't show it.
- No front-matter YAML unless it's useful. Plain markdown is the priority.
- Logged-in-only, admin, draft, noindex and private pages are NEVER exposed.

### Response headers on every markdown response
- `Content-Type: text/markdown; charset=utf-8`
- `X-Markdown-Tokens: <approx tokens = chars/4>`
- `X-Robots-Tag: noindex, follow` (the HTML page stays canonical so Google doesn't see duplicate content)
- `Content-Location: <canonical HTML URL>`. Also set `Link: <url>; rel="canonical"` if the framework doesn't overwrite route-level Link headers. Check this: Next.js `headers()` config overwrites them.
- `Vary: Accept` (on negotiated responses)
- `Cache-Control: public, s-maxage=3600, stale-while-revalidate=86400` (longer for static pages)
- `Last-Modified` when known
- CORS: `Access-Control-Allow-Origin: *` for GET/HEAD/OPTIONS
- HEAD returns the same headers as GET, with no body. OPTIONS handles preflight.

### Advertise the markdown version from HTML
- In `<head>` of every page: `<link rel="alternate" type="text/markdown" href="https://example.com/<path>.md">`
- A global `Link` response header advertising `/llms.txt`, `/llms-full.txt` and `/ai.txt` with `rel="describedby"`
- Optional: a tiny "View as Markdown" link in the footer

### Exclusions in middleware
Don't apply the `.md` and Accept rewrite to: `/llms.txt`, `/llms-full.txt`, `/ai.txt`, `/robots.txt`, `/sitemap.xml`, `/api/*`, static assets, `/_next/*`, `/.well-known/*`, or any REAL route that already ends in `.md` (e.g. `/auth.md`, `SKILL.md` files). Keep an explicit allowlist of content routes for negotiation, not a denylist.

## 2. /llms.txt (follow the llmstxt.org spec)

Served as `text/plain; charset=utf-8`, generated from code (not a hand-written static file) so it never goes stale. Structure:
```
# <Site name>

> <2–3 sentence description: what it is, who it's for, what makes it different>

<short paragraph of key facts: founded, pricing model, main audience, contact>

## Core pages
- [Home](https://example.com/index.md): one-line description
- [Pricing](https://example.com/pricing.md): ...
- [About](https://example.com/about.md): ...

## Docs / Guides
- [...](...md): ...

## <Main content type, e.g. Products / Blog>
- [Top/recent N items](...md): ... (cap at ~50 here; point to the full listing)

## Machine-readable
- [Full content](https://example.com/llms-full.txt): every page concatenated
- [Markdown catalog](https://example.com/api/md/_catalog)
- [Sitemap](https://example.com/sitemap.xml)
- [AI usage policy](https://example.com/ai.txt)
- [OpenAPI](https://example.com/openapi.json) (only if one exists)

## Optional
- [Terms](...md), [Privacy](...md), changelog, etc.
```
- Links point to the `.md` versions.
- Each link gets a factual description, not marketing fluff.
- Revalidate daily (or on content change).

## 3. /llms-full.txt

Served as `text/plain; charset=utf-8` (or text/markdown). It's every page in llms.txt, rendered with the SAME renderer registry and joined together:
```
# <Site name> - full content
> <description>
Generated: YYYY-MM-DD

---
<!-- source: https://example.com/pricing -->
<markdown of page>

---
<!-- source: https://example.com/about -->
...
```
- Order: core pages → docs → main content → legal.
- Big dynamic collections: include the top N by importance/recency and state the limit plus where to find the rest. Keep the total under ~500k chars and log a warning if it's bigger.
- Cache it hard (s-maxage=86400, SWR=604800). Build it on demand or with ISR, never at request time per user.

## 4. /ai.txt (ai-visibility.org.uk ai-txt spec v1.1.1)

`text/plain`, generated from code. Sections:
- `[identity]`: name, URL, description, contact, matching llms.txt and the Organization JSON-LD exactly
- `[permissions]`: allowed: summarise, quote with attribution, cite, index for search/answers
- `[restrictions]`: no fabricated quotes, no fake reviews/ratings, no presenting our content as the model's own, no training on user-generated private data (adjust to what I want)
- `[attribution]`: how to cite (site name + canonical HTML URL)
- `[scope]`: included paths and excluded paths (admin, api, dashboard, auth), kept in sync with robots.txt
- `[contact]` and `Last updated`

## 5. robots.txt and discovery
- Explicitly allow the AI search and user-fetch crawlers on public paths: OAI-SearchBot, ChatGPT-User, Claude-SearchBot, Claude-User, PerplexityBot, Perplexity-User. Never `Disallow: /` these. They decide whether answer engines can cite us.
- Training crawlers are my call: GPTBot, ClaudeBot, Google-Extended, Applebot-Extended, CCBot, Bytespider. Ask me about each one. Blocking them doesn't stop citations from the search bots above, so say that when you ask.
- Disallow private paths for every user agent.
- Add comments pointing to `/llms.txt` and `/ai.txt`, plus the `Sitemap:` line.
- Leave `.md` URLs OUT of sitemap.xml (they're noindex alternates).
- Comments in each of robots.txt, llms.txt and ai.txt say "keep in sync with" the other two.

## 6. Head signals on every page
- `<meta name="ai-summary" content="...">` on every public page: 1-2 factual sentences about what the page is, written for a model that has already fetched it. Default to the page's meta description; give key pages (home, pricing, main listing) their own. Some agents and GEO checkers read it. It doesn't change how the page looks.
- Homepage JSON-LD: an `Organization` (name, url, logo, sameAs socials, contact) and a `WebSite` node, built from the same site config as llms.txt and ai.txt. If they already exist, check the facts match and leave them alone.
- Don't add an MCP discovery file (`/.well-known/mcp.json`) unless we actually run an MCP server. List it under "skipped" in your summary.

## 7. Single source of truth
- Site name, URL, description and contact come from the existing site config. Never hardcode them in several places.
- Adding a new page should take exactly one step: register a renderer. llms.txt, llms-full.txt and the catalog pick it up automatically.
- Add a dev check/test that fails if a public route in the app has no markdown renderer (or isn't on an explicit "skip" list with a reason).

## 8. Verification (run these and show me the output)
```
curl -sI localhost:3000/pricing.md                     # 200, text/markdown, X-Markdown-Tokens, noindex
curl -s  -H 'Accept: text/markdown' localhost:3000/pricing | head -30
curl -sI localhost:3000/pricing                        # still HTML, has Link describedby header
curl -sI -H 'Accept: */*' localhost:3000/              # HTML, not markdown
curl -s  localhost:3000/does-not-exist.md              # markdown 404, status 404
curl -s  localhost:3000/llms.txt | head -40
curl -s  localhost:3000/llms-full.txt | wc -c
curl -s  localhost:3000/ai.txt
curl -s  localhost:3000/api/md/_catalog | head
curl -s  localhost:3000/robots.txt                     # search bots allowed, Sitemap: line present
curl -s  localhost:3000/ | grep -o '<meta name="ai-summary"[^>]*>'
curl -s  localhost:3000/ | grep -c 'application/ld+json'   # 1 or more
```
Also check: one dynamic page per type (product, blog post, category) renders correct real data. Private/admin pages return 404 as markdown. Typecheck and lint pass.

## Constraints
- Match the existing code style, naming, comment density and folder layout.
- No new dependencies unless really needed (no HTML-to-markdown scraping of the rendered page; render from data).
- Don't change how any HTML page looks or behaves.
- Don't commit or push; I'll review the diff.
- At the end, give me a summary: files added/changed, the route inventory with coverage, anything skipped and why, and how to add a markdown renderer for a future page.

---
