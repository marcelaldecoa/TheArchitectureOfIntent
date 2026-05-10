# Evolve in practice — Customer-support agent (90 days post-launch)

**Part 5 · EVOLVE · Scenario 1 of 3**

---

> **v2.0.0-rc1 stub.** Structural placeholder. Prose lands in PR-C. v1.x source: [examples/01-ai-customer-support/postmortem.md](../../examples/01-ai-customer-support/postmortem.md).

---

## What this chapter will cover

The chapter walks the customer-support agent 90 days post-launch — the period where the closed-loop discipline either compounds or quietly degrades. It is a worked example of [The Closed Loop: From Failures to Spec Amendments](../01-closed-loop.md) in operation.

Specifically:

- **The spec evolution log.** Eleven amendments in 90 days: which §, which Cat triggered the amendment, what the amendment looked like. The chapter argues that an empty spec evolution log is itself a signal — usually that Cat 1s are being patched in prompts instead of in the spec.
- **The transition from Output Gate to Periodic oversight.** The team committed in §10 that this transition would happen at 30 days conditional on first-pass-validation ≥ 92%. They hit 89% at day 30 and held the Output Gate for another 14 days; the chapter shows the post-30-day diagnostic that found two Cat 1s and one Cat 4 producing the gap.
- **Cost Posture incident.** Day 47, a model-tier upgrade in the response composition step doubled per-call cost. The Cost Posture sub-block's "breach behavior" fired — the agent fell back to the prior tier; the team filed a §4 amendment naming the new ceiling and the amortization plan.
- **Discipline-Health Audit.** The chapter walks the [11-anti-pattern audit](../../operating/15-anti-patterns.md) at the 90-day mark. The team scored "concerning" on two anti-patterns; the chapter shows the corrective action plan.
- **What graduated from MVP to full framework.** The agent didn't start at MVP-AoI — it started at the full discipline because of the consequence profile. The chapter contrasts what would have been different if it had launched at MVP and grown into the full framework instead.
- **The post-90 disposition.** Continue, deprecate, or refactor. The chapter shows the decision and its evidence.

## Reading path through this scenario

| Phase | Chapter |
|---|---|
| 1. Frame | [Frame in practice — Customer-support agent](../../frame/scenarios/customer-support.md) |
| 2. Specify | [Specify in practice — Customer-support agent](../../specify/scenarios/customer-support.md) |
| 3. Delegate | [Delegate in practice — Customer-support agent](../../delegate/scenarios/customer-support.md) |
| 4. Validate | [Validate in practice — Customer-support agent](../../validate/scenarios/customer-support.md) |
| 5. **Evolve** | *(this chapter)* |

## Conceptual chapters this scenario binds to

- [The Closed Loop: From Failures to Spec Amendments](../01-closed-loop.md)
- [Signs Your Architecture of Intent Is Degrading](../../operating/15-anti-patterns.md)
- [Cost and Latency Engineering](../../operating/09-cost-and-latency.md)
- [Adoption Playbook](../../operating/11-adoption-playbook.md)

## Source material

v1.x postmortem: [examples/01-ai-customer-support/postmortem.md](../../examples/01-ai-customer-support/postmortem.md).
