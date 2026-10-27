<!-- Source: sources/code-prompt/prompt-2.md (verbatim slice, lines 269-290). -->

### H. Delivery, containers, infrastructure as code, and release safety (180–198)

- [ ] **180. Infrastructure as Code** — Version, review, validate, and safely apply infrastructure changes.
- [ ] **181. Terraform State** — Protect state confidentiality and integrity; use appropriate remote storage, locking, and access controls.
- [ ] **182. GitOps** — Control deployment permissions and reconcile declared state without leaking secrets into repositories.
- [ ] **183. Blue-Green Deployments** — Verify compatibility, health, traffic switching, and rollback constraints.
- [ ] **184. Canary Releases** — Define progressive rollout gates and monitor the right health and business signals.
- [ ] **185. Rollbacks** — Ensure rollback is operationally possible and compatible with data/schema changes.
- [ ] **186. Feature Flags** — Secure flag access, plan cleanup, and avoid using flags as a substitute for authorization.
- [ ] **187. Environment Parity** — Keep development, staging, and production behavior meaningfully consistent while isolating secrets and data.
- [ ] **188. Staging Environments** — Validate production-like flows with safe test data, controlled access, and realistic dependencies.
- [ ] **189. 12-Factor Apps** — Apply relevant principles for config, disposability, logs, processes, and environment separation.
- [ ] **190. Multi-Stage Builds** — Keep build tools out of runtime images where possible and minimize the final image.
- [ ] **191. Non-Root Containers** — Run as non-root with only required capabilities and filesystem permissions.
- [ ] **192. Image Scanning** — Scan container images, prioritize actionable findings, and rebuild on patched base images.
- [ ] **193. Resource Requests & Limits** — Set suitable CPU and memory requests/limits based on workload and platform behavior.
- [ ] **194. Pod Disruption Budgets** — Configure disruption tolerance to match availability goals without blocking necessary maintenance indefinitely.
- [ ] **195. Semantic Versioning** — Communicate compatibility changes accurately and do not use version numbers as a substitute for tested compatibility.
- [ ] **196. Lockfiles** — Commit and respect lockfiles where appropriate for reproducible dependency resolution.
- [ ] **197. Reproducible Builds** — Pin inputs and reduce uncontrolled build-time differences; verify artifacts when practical.
- [ ] **198. Branch Protection** — Require appropriate reviews and automated checks; restrict bypass permissions.

