# Frontend data layer

Use this when the change touches how the client fetches, mutates or subscribes to backend data. The original prompt
is at the bottom. It names specific libraries; the checklist below keeps the intent and drops the brand names.

Check what the repo already uses before anything else: TanStack Query, SWR, RTK Query, Apollo, Next.js server
components with `fetch`, or a plain fetch wrapper. Extend that. Don't add axios or TanStack just to follow this list;
a new dependency needs the user's yes. With server components doing the fetching, a client cache may not be needed.

## Checklist

**Server-state cache**
- Query keys include every parameter the request depends on (id, filters, page, locale).
- `staleTime` / revalidation is a deliberate choice per query, not the library default everywhere.
- Mutations invalidate or update the queries they change.
- Two components needing the same data share one query instead of fetching twice.

**Cancellation**
- Requests are cancelled on unmount and route change (`AbortController`, or the query library's `signal`).
- Search-as-you-type and other superseded requests are cancelled, so a slow old response can't overwrite a newer one.
- `AbortError` is not shown to the user as a failure.

**Token refresh and retry** (guardian A-25, C-94/95, E-119)
- All 401s share one in-flight refresh (single-flight). Ten parallel 401s must not send ten refresh calls.
- After a successful refresh, the original request is retried once. A failed refresh logs the user out.
- Automatic retries only for idempotent requests (GET, or writes with an idempotency key), bounded, with backoff and jitter.
- Prefer httpOnly cookies over tokens in `localStorage`.

**Typed API layer** (guardian E-128)
- Request/response types come from one source: generated from OpenAPI, or shared (tRPC, zod schemas). Not hand-copied.
- Components call the API layer, not raw URLs.

**Real-time**
- Pick by need: WebSockets for frequent, two-way or latency-sensitive updates; SSE for server → client streams;
  polling for slow-changing data, where it's the simplest correct answer.
- Reconnect with backoff, resync after reconnect (refetch or resume from the last event ID), authenticate on
  connect (guardian E-122/123).
- Pushed updates go into the same query cache, not a second copy of the state.

## Original prompt (verbatim)

> Connecting Backend APIs in Frontend : the advanced way
> → Use TanStack Query for caching & background refetch.
> → Implement abort controllers to cancel API calls on route change.
> → Add Axios interceptors for token refresh & retry logic.
> → Maintain a typed API layer for clean FE-BE contracts.
> → Use WebSockets for real-time updates over polling.
> Smart API handling and orchestration is important
