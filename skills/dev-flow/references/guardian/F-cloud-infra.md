<!-- Source: sources/code-prompt/prompt-2.md (verbatim slice, lines 217-247). -->

### F. Cloud, infrastructure, availability, and recovery (134–161)

- [ ] **134. VPCs** — Isolate workloads and define intentional network boundaries.
- [ ] **135. Subnets** — Separate public and private resources appropriately and plan routing and address capacity.
- [ ] **136. NAT Gateways** — Understand cost, throughput, availability, and outbound access implications.
- [ ] **137. Firewalls** — Default-deny where practical and manage rules as reviewed, auditable configuration.
- [ ] **138. Security Groups** — Restrict ingress and egress to required sources, destinations, and ports.
- [ ] **139. Service Mesh** — Adopt only when its traffic, identity, policy, or telemetry benefits justify operational complexity.
- [ ] **140. Ingress Controllers** — Secure routing, TLS termination, timeouts, body sizes, and exposed admin endpoints.
- [ ] **141. Health Checks** — Make checks meaningful without causing overload or revealing sensitive information.
- [ ] **142. Liveness vs Readiness Probes** — Use liveness for restart-worthy failure and readiness for traffic eligibility; avoid probe restart loops.
- [ ] **143. Graceful Shutdown** — Stop accepting work, drain in-flight requests, and close resources within the platform deadline.
- [ ] **144. Connection Draining** — Ensure load balancers and workers stop routing to instances that are shutting down.
- [ ] **145. Stateless Services** — Keep durable state in suitable backing systems or deliberately manage local state and affinity.
- [ ] **146. Failover** — Test detection, promotion, reconnection, data integrity, and failback procedures.
- [ ] **147. Multi-Region** — Define data residency, consistency, routing, failover, and operational trade-offs before deploying broadly.
- [ ] **148. Availability Zones** — Avoid accidental single-zone dependencies when resilience requirements demand zone-level redundancy.
- [ ] **149. Single Points of Failure** — Identify and mitigate components whose failure disables a critical path.
- [ ] **150. Disaster Recovery** — Maintain a practical, documented recovery strategy and validate dependencies and access.
- [ ] **151. RTO & RPO** — Define recovery time and recovery point objectives in measurable, business-aligned terms.
- [ ] **152. SLAs** — Understand contractual availability and support commitments and the consequences of missing them.
- [ ] **153. SLOs** — Define measurable service-level objectives and suitable SLIs.
- [ ] **154. Error Budgets** — Use reliability budgets to guide release and risk decisions rather than as a vanity metric.
- [ ] **155. Incident Response** — Define severity, ownership, communication, containment, and escalation procedures.
- [ ] **156. On-Call** — Make alert ownership, escalation, handover, and support load sustainable.
- [ ] **157. Runbooks** — Document actionable diagnosis and recovery steps, including safe commands and decision points.
- [ ] **158. Postmortems** — Focus on contributing system factors, learning, and trackable corrective actions rather than blame.
- [ ] **159. Chaos Engineering** — Run scoped, authorized experiments with hypotheses, guardrails, abort criteria, and rollback.
- [ ] **160. Graceful Degradation** — Preserve core functions when optional dependencies or noncritical features fail.
- [ ] **161. Autoscaling** — Set appropriate signals, bounds, cooldowns, and capacity limits; account for startup delay and cost.


<!-- Additions (not in prompt-2). -->
#### Additions

- [ ] **220. mTLS / Service-to-Service Identity** — Only if there is more than one internal service. Authenticate service calls instead of trusting the internal network; rotate and monitor certificates (35); use the service mesh's mTLS where one exists (139).
