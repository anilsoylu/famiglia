<!-- Source: sources/code-prompt/prompt-1.md (verbatim slice, lines 253-268). -->

# Phase 3 — Cross-cutting engineering review

After the checklist, assess whether the code and proposed fixes follow these principles **where relevant and proportional to the project**:

- **SOLID / SRP / separation of concerns:** responsibilities and boundaries are clear; modules do not take on unrelated work; dependencies point in manageable directions.
- **DRY:** repeated business rules are centralized when duplication creates a real risk of drift, not merely because two snippets look similar.
- **KISS / YAGNI:** choose the least complex correct solution; avoid speculative abstractions, premature frameworks, and features without demonstrated requirements.
- **Open/Closed and Dependency Inversion:** use extension points and abstractions where real variation or testability justifies them; do not introduce them by default.
- **Composition:** prefer composable, small units when that makes behavior easier to test and change; avoid layers that only forward calls.
- **Fail fast:** reject invalid state and configuration early with actionable, non-sensitive errors.
- **Measure first:** base performance claims on profiling, query plans, telemetry, or reproducible benchmarks. Look for N+1 queries, repeated work, avoidable network round trips, excessive rendering, unbounded loops, and memory-heavy processing where evidence points there.
- **Optimization with parity:** shorten or streamline hot paths only when correctness and benefit can be shown. Consider batching/vectorization/JIT compilation only when supported and measurably useful. Keep the same outputs, side effects, errors, ordering, precision, and edge-case semantics unless a behavior change is approved.
- **Maintainability:** code should be readable to the next engineer; do not sacrifice clarity for micro-optimizations without measured benefit.

Do not turn each principle into a demand for refactoring. Mention only concrete issues with evidence and a clear expected benefit.

