# Specify in practice — Customer-support agent

**Part 2 · SPECIFY · Scenario 1 of 3**

---

> **v2.0.0-rc1 stub.** Structural placeholder. Prose lands in PR-C. v1.x source: [examples/01-ai-customer-support/spec.md](../../examples/01-ai-customer-support/spec.md).

---

## What this chapter will cover

The chapter writes the [canonical 12-section spec](../../sdd/07-canonical-spec-template.md) for the customer-support agent framed in [Part 1's customer-support scenario](../../frame/scenarios/customer-support.md). Each spec section gets a worked entry — not a one-line gloss — so the reader sees the discipline, not just the template.

Highlights the chapter will pay specific attention to:

- **§3 Authorized scope** — what the agent can do (look up account, surface KB articles, draft responses, escalate to human, issue refund within cap).
- **§4 NOT-authorized scope** — what the agent must never do (refund above cap, change account ownership, communicate outside the support channel). Cat 3 (Scope Creep) lives here.
- **§4 Composition Declaration sub-block** — Executor (governing) + Advisor (embedded for KB suggestion) + Guardian (refund-cap invariant). Mode transitions named explicitly.
- **§4 Cost Posture sub-block** — model tier per step (Haiku for triage, Sonnet for response composition), p95 latency budget (3s), per-call ceiling, breach behavior.
- **§6 Invariants** — the refund cap and the "no PII to external systems" rule are the two non-negotiables.
- **§11 Agent execution instructions** — when to escalate, what to escalate with, how to hand off without losing context.

## Reading path through this scenario

| Phase | Chapter |
|---|---|
| 1. Frame | [Frame in practice — Customer-support agent](../../frame/scenarios/customer-support.md) |
| 2. **Specify** | *(this chapter)* |
| 3. Delegate | [Delegate in practice — Customer-support agent](../../delegate/scenarios/customer-support.md) |
| 4. Validate | [Validate in practice — Customer-support agent](../../validate/scenarios/customer-support.md) |
| 5. Evolve | [Evolve in practice — Customer-support agent](../../evolve/scenarios/customer-support.md) |

## Conceptual chapters this scenario binds to

- [The Canonical Spec Template](../../sdd/07-canonical-spec-template.md)
- [Writing for Machine Execution](../../sdd/05-writing-specs-for-agents.md)
- [The Spec as Control Surface](../../sdd/02-specs-as-control-surfaces.md)

## Source material

The v1.x worked spec is at [examples/01-ai-customer-support/spec.md](../../examples/01-ai-customer-support/spec.md). v2.0.0 reworks it into the 12-section canonical template with the new Composition Declaration and Cost Posture sub-blocks made explicit.
