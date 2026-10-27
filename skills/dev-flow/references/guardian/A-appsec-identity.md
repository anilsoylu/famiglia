<!-- Source: sources/code-prompt/prompt-2.md (verbatim slice, lines 69-111). -->

### A. Application security and identity (1–40)

- [ ] **1. SQL Injection** — Use parameterized queries or safe query builders; avoid unsafe string concatenation.
- [ ] **2. XSS** — Escape output for its context; sanitize deliberately supported HTML; avoid unsafe DOM APIs.
- [ ] **3. CSRF** — Protect cookie-authenticated state-changing actions with appropriate CSRF controls and cookie settings.
- [ ] **4. CORS** — Allow only intended origins, methods, and headers; never use CORS as authorization.
- [ ] **5. SSRF** — Restrict outbound destinations, validate URLs, and guard against private-network and metadata-service access.
- [ ] **6. IDOR** — Verify object-level authorization for every requested resource.
- [ ] **7. Path Traversal** — Canonicalize and constrain file paths to approved directories.
- [ ] **8. Mass Assignment** — Explicitly allow writable fields; do not bind arbitrary request fields to privileged models.
- [ ] **9. Clickjacking** — Use appropriate framing restrictions such as CSP `frame-ancestors` or `X-Frame-Options` where applicable.
- [ ] **10. Content Security Policy** — Define a practical CSP and avoid unsafe allowances where possible.
- [ ] **11. Security Headers** — Review headers suitable for the app, framework, and deployment topology.
- [ ] **12. Input Validation** — Validate type, shape, length, range, and business rules at trust boundaries.
- [ ] **13. Server-Side Authorization** — Enforce permissions on every protected operation at the server or trusted service.
- [ ] **14. Row-Level Security** — Use database-enforced row policies when appropriate and verify policy coverage and service-role behavior.
- [ ] **15. Least Privilege** — Give users, services, jobs, and database roles only the permissions they need.
- [ ] **16. RBAC** — Keep role and permission rules explicit, reviewable, and tested.
- [ ] **17. Secrets Management** — Use an appropriate secret store or runtime injection; restrict access and exposure.
- [ ] **18. `.env` in `.gitignore`** — Exclude local secret files and ensure real secrets are not committed or built into images.
- [ ] **19. API Key Rotation** — Have a workable process to rotate and revoke keys without unnecessary downtime.
- [ ] **20. Secret Scanning** — Scan history and changes for credentials; respond to exposure by revoking or rotating them.
- [ ] **21. Hashing vs Encryption** — Hash one-way verification data; encrypt data that must later be recovered.
- [ ] **22. Password Salting** — Use a unique salt through a modern password-hashing library.
- [ ] **23. bcrypt & Argon2** — Use a suitable adaptive password hash with parameters appropriate to the environment.
- [ ] **24. JWT Expiry** — Set suitable expiry, issuer, audience, and algorithm validation; plan revocation behavior.
- [ ] **25. Refresh Tokens** — Protect, rotate, expire, and revoke refresh tokens; detect reuse where supported.
- [ ] **26. OAuth 2.0** — Use suitable flows, PKCE where appropriate, strict redirect URI validation, and correct state handling.
- [ ] **27. OpenID Connect** — Validate identity tokens and issuer, audience, nonce, signature, and discovery configuration as applicable.
- [ ] **28. Session Fixation** — Rotate session identifiers at authentication and privilege changes.
- [ ] **29. MFA** — Offer or require multi-factor authentication according to the threat model and sensitivity.
- [ ] **30. Brute Force Protection** — Apply rate limits, progressive delays, and abuse monitoring without enabling trivial denial of service.
- [ ] **31. Account Enumeration** — Avoid unnecessary differences in responses, timing, and recovery flows that reveal account existence.
- [ ] **32. Timing Attacks** — Use appropriate constant-time comparisons for secret values and avoid avoidable timing leaks.
- [ ] **33. File Upload Validation** — Check size, type, content, storage location, names, and processing risks; do not trust filenames or MIME headers alone.
- [ ] **34. Webhook Signature Verification** — Verify signatures over the exact raw payload with a trusted secret and enforce replay protection where supported.
- [ ] **35. TLS Certificate Expiry** — Monitor certificate expiration and renewal failures.
- [ ] **36. HSTS** — Enable HSTS when HTTPS deployment and subdomain implications are understood.
- [ ] **37. Encryption at Rest** — Protect stored sensitive data using appropriate storage and key-management controls.
- [ ] **38. Dependency Vulnerabilities** — Assess direct and transitive dependencies and prioritize exploitable, relevant vulnerabilities.
- [ ] **39. Supply Chain Attacks** — Pin and verify dependencies and build inputs; restrict CI permissions and review provenance where practical.
- [ ] **40. Threat Modeling** — Identify assets, trust boundaries, actors, abuse cases, mitigations, and residual risk.

