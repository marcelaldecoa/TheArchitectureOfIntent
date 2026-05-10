# Validate in practice — Coding-agent pipeline

**Part 4 · VALIDATE · Scenario 2 of 3**

---

> **v2.0.0-rc1 stub.** Structural placeholder. Prose lands in PR-E. v1.x source: [examples/02-code-generation-pipeline/validation.md](../../examples/02-code-generation-pipeline/validation.md), [examples/03-coding-agent/evals.md](../../examples/03-coding-agent/evals.md), [examples/03-coding-agent/postmortem.md](../../examples/03-coding-agent/postmortem.md).

---

## What this chapter will cover

The chapter walks the validation phase for the coding-agent pipeline: spec-conformance test suite, the structural CI guards, the four signal metrics measured per session, and the canonical *deleted-tests* failure walked through Cat 1–7.

Specifically:

- **Pre-launch eval suite.** A graded set of session-task prompts from the team's own backlog, each with a known-good outcome (PR shape, tests passing, no test-skip-set growth). Pass thresholds for first-pass-validation, acceptable-with-review, and reject-and-amend-spec.
- **Structural CI guards.** Test-skip-set monotonicity check (the agent must not delete or skip existing tests). Tool-manifest scope check (no unrestricted shell escape). Branch-protection enforcement (no push to `main`). Spec-conformance tests gating PR merge. The chapter argues these are *load-bearing*: they're the form Cat 1 / Cat 3 hybrid fixes have to take to actually compound.
- **The four signal metrics per session.** Spec-gap rate per session-task. First-pass-validation = PR merged without spec amendment. Cost per correct outcome = tokens + reviewer-minutes / merged PRs. Oversight load = reviewer-minutes per session.
- **The deleted-tests failure, walked through Cat 1–7.** The canonical example. The chapter applies the diagnostic test ("If a competent agent had executed this spec as written, would the outcome have been correct?") and traces the fix to §4 NOT-authorized scope and CI guard — *not* to a prompt patch. Cat 7 *does not* apply (text-only agent).
- **Per-mode failure observability.** Because the agent uses Pattern E (mode-switching) composition, the validation surface includes per-mode failure rate so the team can see whether failures concentrate in Frame, Plan, Implement, or Review.

## Reading path through this scenario

| Phase | Chapter |
|---|---|
| 1. Frame | [Frame in practice — Coding-agent pipeline](../../frame/scenarios/coding-pipeline.md) |
| 2. Specify | [Specify in practice — Coding-agent pipeline](../../specify/scenarios/coding-pipeline.md) |
| 3. Delegate | [Delegate in practice — Coding-agent pipeline](../../delegate/scenarios/coding-pipeline.md) |
| 4. **Validate** | *(this chapter)* |
| 5. Evolve | [Evolve in practice — Coding-agent pipeline](../../evolve/scenarios/coding-pipeline.md) |

## Conceptual chapters this scenario binds to

- [Failure Modes and How to Diagnose Them](../../theory/05-failure-as-design-signal.md)
- [Spec Conformance Testing](../../patterns/testing/spec-conformance.md)
- [Coding Agents](../../agents/08-coding-agents.md)
- [Four Signal Metrics](../../operating/06-metrics.md)
