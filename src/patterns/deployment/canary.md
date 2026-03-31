# Canary Deployment

---

> *"Let a few requests test the new spec before all requests trust it."*

---

## Context

You have an updated spec for a production agent system. The new spec may improve quality, tighten constraints, or change behavior. But deploying it to all traffic at once risks a regression affecting every user simultaneously.

---

## The Solution

Route a **percentage of traffic to the new spec version** while the majority continues under the old spec.

1. **Declare the canary percentage** — typically 5-10% to start, increasing as confidence grows.
2. **Compare metrics between old and new.** Validation pass rate, error rate, cost per correct output, escalation frequency. If the new spec matches or exceeds the old spec's metrics, promote. If it degrades, roll back.
3. **Canary duration is declared.** The new spec runs for a declared period (hours or days) before promotion. The period must be long enough to capture typical request variety.
4. **Rollback is immediate.** If the canary shows regression, route 100% back to the old spec. No partial rollback — canary is binary: promote or revert.

---

## Therefore

> **Deploy spec changes to a traffic percentage first. Compare metrics between old and new. Promote when the canary validates. Revert immediately when it regresses. The canary protects the majority from untested changes.**

---

## Connections

- [Spec Versioning](spec-versioning.md) — canary deploys compare two spec versions in production
- [Regression on Spec Change](../testing/regression-spec-change.md) — pre-deployment testing catches many issues; canary catches the rest
- [Rollback on Failure](rollback.md) — canary revert is a specific case of rollback
- [Four Signal Metrics](../../operating/06-metrics.md) — signal metrics are the comparison criteria
