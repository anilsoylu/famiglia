<!-- Source: sources/code-prompt/prompt-2.md (verbatim slice, lines 196-216). -->

### E. Networking, HTTP, and API contracts (116–133)

- [ ] **116. DNS** — Understand record types, TTLs, caching, and failure behavior for service discovery and public endpoints.
- [ ] **117. DNS Propagation** — Plan for resolver caching and TTLs rather than assuming changes are immediate everywhere.
- [ ] **118. HTTP Status Codes** — Use status codes consistently and avoid leaking internal error details.
- [ ] **119. HTTP Method Semantics** — Respect safety and idempotency semantics, especially for retries and intermediaries.
- [ ] **120. Keep-Alive** — Configure persistent connections and idle timeouts to fit proxies and upstream services.
- [ ] **121. HTTP/2** — Understand multiplexing, connection-level failure effects, and deployment/proxy compatibility.
- [ ] **122. WebSockets** — Authenticate and authorize connections and messages; limit payloads, connections, and idle sessions.
- [ ] **123. Server-Sent Events** — Handle reconnects, event IDs, buffering, proxy timeouts, and authorization.
- [ ] **124. Long Polling** — Bound wait duration and resource use; support safe reconnect and cancellation.
- [ ] **125. gRPC** — Set deadlines, cancellation, authentication, message limits, and retry policy deliberately.
- [ ] **126. Protocol Buffers** — Evolve schemas compatibly; do not reuse field numbers and follow reserved-field conventions.
- [ ] **127. API Versioning** — Define a compatibility and deprecation policy for clients and consumers.
- [ ] **128. OpenAPI Specs** — Keep API definitions aligned with implementation, validation, and generated clients.
- [ ] **129. Backward Compatibility** — Roll out schema and API changes in a sequence safe for old and new versions running concurrently.
- [ ] **130. Request Size Limits** — Limit bodies, headers, uploads, and decompressed content to mitigate resource exhaustion.
- [ ] **131. Compression** — Balance bandwidth and CPU; consider compression side channels where secrets and attacker-controlled content mix.
- [ ] **132. Latency vs Throughput** — Measure both and make the service objective explicit; do not optimize one blindly.
- [ ] **133. Egress Fees** — Account for outbound data-transfer costs in architecture, logs, backups, and cross-region traffic.


<!-- Additions (not in prompt-2). -->
#### Additions

- [ ] **216. Reverse Proxies & Load Balancers** — Trust `X-Forwarded-For` and similar headers only from known proxies when deriving client IP for rate limits and logs; align timeouts and body limits along the chain; prefer stateless instances over sticky sessions; make health checks reflect real readiness.
- [ ] **217. API Gateways** — Only if one exists or is proposed. Gateway authentication does not replace authorization inside each service; set per-route limits and timeouts; avoid making the gateway a single point of failure; don't add one in front of a single service without a reason.
- [ ] **218. Rate Limiting & Throttling** — Keep counters in a shared store keyed by identity (user, API key, IP); return 429 with `Retry-After` and have clients honor it; decide deliberately whether excess traffic is rejected or delayed.
- [ ] **219. GraphQL** — Only if the repo uses GraphQL. Limit query depth, complexity, aliases, and batching; authorize at the field/resolver level; batch resolvers (DataLoader) to avoid N+1; decide on introspection and persisted queries for public APIs.
