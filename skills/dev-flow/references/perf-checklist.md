# Performance checklists

Two prompts the user runs for speed work. Use them as the checklist that drives `/perf`. They don't replace measuring:
every item gets a baseline number before the change and an after number once it's done. Items that don't apply to
this stack get one line, "N/A: <reason>".

## App performance (sources/code-prompt/prompt-3.md, verbatim)

> Your job is to make this app faster. Make the routine shorter, optimize, vectorize, JIT-compile, maintain the exact parity. Improve the startup time, how fast each screen opens, how fast its content loads, and the scrolling, so everything feels lighter and older content loads faster. Find where the real performance gap is, apply the fixes, and benchmark before and after each one to see if it actually works or not. Also check this list:
>
> 1) Detect and eliminate unnecessary renders.
> 2) Reduce the bundle with lazy loading.
> 3) Optimize requests and caching.
> 4) Find slow queries and N+1 problems.
> 5) Optimize images, fonts, and scripts.

## Web assets and delivery (sources/code-prompt/prompt-5.md)

Use this when the change touches a web frontend: images, CSS/JS, the build config, or static hosting.

> optimize assets: Compress all hero images to WebP and minify my CSS/Js files.
> minimize requests: Bundle my CSS into one file and create an image sprite for icons.
> smart loading: Implement lazy loading for images below the fold and defer non-critical Js.
> cache effectively: Set long expiry cache header for static assets and configure a CDN.

Before applying it, check what the stack already does. Modern bundlers (Next.js, Vite, Astro) already minify, split
and fingerprint, and `next/image` already serves WebP/AVIF. The job is to confirm that and fill the gaps, not to bolt
on a second pipeline. A CSS bundle or an icon sprite only helps on HTTP/1.1 or with many tiny requests. On HTTP/2+,
measure before you merge files. CDN config changes infrastructure, so ask before making it.

## Concurrency hot loops

Only for multithreaded native, JVM, Go or Rust code: false sharing. Per-thread counters or slots that sit on the same
cache line slow each other down. Pad or separate them, and confirm with a profiler (cache-miss counters) before and after.

## Parity

Every speed change keeps the same outputs, errors, ordering and precision (see `/optimize`). If parity can't be shown,
revert and report it instead of shipping.
