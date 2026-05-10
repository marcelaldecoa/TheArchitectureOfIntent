# Frame in practice — Customer-support agent

**Part 1 · FRAME · Scenario 1 of 3**

---

> **v2.0.0-rc1 stub.** This chapter is the structural placeholder for Scenario 1's *Frame* walkthrough in v2.0.0. The full prose lands in PR-C of the v2.0.0 rollout (see [`CHANGELOG.md`](https://github.com/marcelaldecoa/TheArchitectureOfIntent/blob/main/CHANGELOG.md)). The existing worked pilot in [Designing an AI Customer Support System](../../examples/01-ai-customer-support/README.md) is the v1.x source material this chapter will rework into the phase-by-phase form.

---

## What this chapter will cover

The chapter walks a working team through the *Frame* activity for an AI customer-support agent that handles inbound chat. It is the first of five chapters that follow the same scenario across the five activities of the Architecture of Intent.

Specifically, the chapter will name:

- **The archetype call.** The team picks **Executor** (acts within bounded scope), with **Orchestrator** as a risk-override candidate if the support flow turns out to span systems the agent must coordinate. The decision is made on the [archetype selection tree](../../architecture/04-decision-tree.md), not by intuition.
- **The four-dimension calibration.** Agency: low — the agent acts only within a documented response repertoire. Autonomy: low-to-medium — chained actions are pre-authorized, novel actions escalate. Responsibility: shared — the agent is operationally responsible, the support manager is authorially responsible. Reversibility: high for messages, low for refunds — the spec will treat these classes asymmetrically.
- **Composition Declaration.** The agent embeds an **Advisor** when surfacing knowledge-base articles to the human supervisor, and a **Guardian** mode for the refund-cap invariant.
- **The pre-spec hand-off.** What Frame produces — archetype, dimensions, composition declaration — flows into [Specify in practice — Customer-support agent](../../specify/scenarios/customer-support.md) as the input to the canonical spec.

## Reading path through this scenario

| Phase | Chapter |
|---|---|
| 1. **Frame** | *(this chapter)* |
| 2. Specify | [Specify in practice — Customer-support agent](../../specify/scenarios/customer-support.md) |
| 3. Delegate | [Delegate in practice — Customer-support agent](../../delegate/scenarios/customer-support.md) |
| 4. Validate | [Validate in practice — Customer-support agent](../../validate/scenarios/customer-support.md) |
| 5. Evolve | [Evolve in practice — Customer-support agent (90 days post-launch)](../../evolve/scenarios/customer-support.md) |

## Conceptual chapters this scenario binds to

- [Pick an Archetype](../../architecture/02-canonical-intent-archetypes.md)
- [Calibrate Agency, Autonomy, Responsibility, Reversibility](../../theory/03-agency-autonomy-responsibility.md)
- [Composing Archetypes](../../architecture/05-composing-archetypes.md)

## Source material

The existing worked pilot for this scenario is in [Part 6 — Reference, Worked Pilots: Customer Support](../../examples/01-ai-customer-support/README.md), which v2.0.0 keeps as legacy reference while the phase-by-phase scenario chapters supersede it.
