# Validate in practice — Customer-support agent

**Part 4 · VALIDATE · Scenario 1 of 3**

---

> **v2.0.0-rc1 stub.** Structural placeholder. Prose lands in PR-C. v1.x source: [examples/01-ai-customer-support/validation.md](../../examples/01-ai-customer-support/validation.md), [examples/01-ai-customer-support/postmortem.md](../../examples/01-ai-customer-support/postmortem.md).

---

## What this chapter will cover

The chapter walks the validation phase for the customer-support agent: pre-launch evals, the launch readiness gate, the four signal metrics in production, and the first month's failure-categorization discipline.

Specifically:

- **Pre-launch eval suite.** ~150 known-good question-resolution pairs from prior support transcripts. Pass threshold ≥ 88% first-pass acceptance. Held-out 30 adversarial cases (politeness-attack, scope-bait, sensitive-PII probes) for a separate red-team scoreline.
- **Red-team protocol.** Two-week structured exercise: prompt-injection through ticket bodies, scope-creep prompts ("can you also reset my password"), adversarial refund requests around the cap. The chapter shows the categorized findings.
- **The four signal metrics, instrumented.** Spec-gap rate (per 1000 conversations, how many produced a Cat 1 amendment). First-pass validation (% accepted by the support manager without rework). Cost per correct outcome (tokens + escalation cost / conversations resolved). Oversight load (manager-minutes per 1000 conversations). The chapter shows the dashboard.
- **The first month's Cat 1–7 categorization.** Worked through eight real failures, traced to the fix-locus: where the spec needed amending vs. where the manifest needed tightening vs. where the model failed despite a correct spec. Specifically Cat 7 *does not* apply to this scenario — the agent is text-only.
- **The launch gate decision.** What "ready to ship" looks like, who signs off, what the 30-day reassessment trigger is for relaxing the Output Gate to Periodic.

## Reading path through this scenario

| Phase | Chapter |
|---|---|
| 1. Frame | [Frame in practice — Customer-support agent](../../frame/scenarios/customer-support.md) |
| 2. Specify | [Specify in practice — Customer-support agent](../../specify/scenarios/customer-support.md) |
| 3. Delegate | [Delegate in practice — Customer-support agent](../../delegate/scenarios/customer-support.md) |
| 4. **Validate** | *(this chapter)* |
| 5. Evolve | [Evolve in practice — Customer-support agent](../../evolve/scenarios/customer-support.md) |

## Conceptual chapters this scenario binds to

- [Failure Modes and How to Diagnose Them](../../theory/05-failure-as-design-signal.md)
- [Four Signal Metrics](../../operating/06-metrics.md)
- [Evals and Benchmarks](../../operating/07-evals-and-benchmarks.md)
- [Red-Team Protocol](../../operating/08-red-team-protocol.md)

## Source material

v1.x validation: [examples/01-ai-customer-support/validation.md](../../examples/01-ai-customer-support/validation.md). v1.x postmortem (which becomes Evolve material): [examples/01-ai-customer-support/postmortem.md](../../examples/01-ai-customer-support/postmortem.md).
