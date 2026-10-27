<!-- Source: sources/code-prompt/prompt-2.md (verbatim slice, lines 248-268). -->

### G. Capacity, performance, and observability (162–179)

- [ ] **162. Horizontal vs Vertical Scaling** — Choose based on bottlenecks, statefulness, cost, and availability requirements.
- [ ] **163. Cold Starts** — Measure startup impact and mitigate only where it matters to user experience or SLOs.
- [ ] **164. Capacity Planning** — Forecast demand and growth; include headroom, quotas, failover capacity, and cost.
- [ ] **165. Load Testing** — Test representative workloads, concurrency, spikes, and saturation in a controlled environment.
- [ ] **166. Memory Leaks** — Track memory over time and investigate retained objects, subscriptions, handles, and caches.
- [ ] **167. OOM Killer** — Set realistic memory limits and diagnose resource pressure instead of treating restarts as a fix.
- [ ] **168. Structured Logging** — Use queryable structured events and redact secrets and personal data.
- [ ] **169. Log Levels** — Use levels consistently; avoid logging expected control flow as errors.
- [ ] **170. Log Rotation** — Bound disk use and retention, and confirm logs remain available for incident investigation.
- [ ] **171. Distributed Tracing** — Trace cross-service paths with appropriate sampling, context propagation, and privacy controls.
- [ ] **172. OpenTelemetry** — Instrument consistently and manage exporters, sampling, cardinality, and data sensitivity.
- [ ] **173. Correlation IDs** — Propagate trusted trace/request IDs across boundaries without treating them as authentication.
- [ ] **174. Metrics Cardinality** — Avoid unbounded labels such as raw user IDs, request paths, or arbitrary inputs.
- [ ] **175. p99 Latency** — Monitor tail latency by critical operation and correlate it with saturation and errors.
- [ ] **176. Alert Fatigue** — Alert on actionable symptoms and user impact; tune duplicates and non-actionable notifications.
- [ ] **177. Error Tracking** — Capture useful context safely and group actionable errors without exposing secrets.
- [ ] **178. Profiling** — Profile realistic workloads before optimizing and assess the overhead of profilers.
- [ ] **179. Flame Graphs** — Use flame graphs to identify measured CPU or stack hotspots, not as proof without context.

