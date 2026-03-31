# Canary Deployment

---

> *"Let a few requests test the new spec before all requests trust it."*

---

## Context

You have an updated spec for a production agent system. The new spec may improve quality, tighten constraints, or add capability. But deploying it to all traffic at once risks a regression affecting every user simultaneously. Pre-deployment testing covers known scenarios; production traffic includes edge cases no test suite anticipates.

---

## Problem

A content moderation agent running spec v1.2 operates correctly. The team ships v1.3 to reduce false positives with more nuanced policies. All regression tests pass. They deploy to 100% of traffic at 6 PM. Within 30 minutes, support tickets triple — the new spec is too permissive, and harmful content slips through. Reverting requires another deployment cycle and an incident report. If v1.3 had been deployed to 5% of traffic first, the permissiveness would have been caught within an hour, affecting 50 users instead of 1,000.

---

## Forces

- **Pre-deployment testing cannot capture production diversity.** Test suites cover happy paths and known failure modes; production has edge cases you didn't anticipate.
- **Spec failures affect all traffic simultaneously.** Unlike feature flags on code paths, a spec change is an instant switch that affects every agent execution using it.
- **Metrics comparison requires time and volume.** A 5% canary for 24 hours captures patterns that a 1-hour full deployment cannot — different user segments, time-of-day effects, interaction patterns.
- **Binary decisions reduce ambiguity.** Either promote the canary to 100% or revert to 0%. Half-rollback creates confusion about which users are experiencing which behavior.

---

## The Solution

Route a **percentage of traffic to the new spec version** while the majority continues under the old spec. Compare metrics between old and new, then make a binary promote-or-revert decision.

1. **Declare the canary percentage and duration before deploying.** Begin with 5-10% of traffic. The typical canary period is 24-48 hours — long enough to capture time-of-day patterns and user segment diversity. The percentage and duration are declared in the deployment plan, not improvised.
2. **Define comparison metrics before deploying.** Before the canary starts, declare what you will measure: validation pass rate, error rate, cost per correct output, escalation frequency, latency. These metrics are your decision criteria — not gut feeling after the fact.
3. **Compare old and new on the same time window.** Both spec versions run side by side. Compare their metrics over the same period. If v1.3 has a 98.5% pass rate while v1.2 has 99.2% over the same 24 hours, the regression is visible and quantified.
4. **Promote or revert — no middle ground.** If the new spec matches or exceeds the old spec on all declared metrics, promote to 100%. If it degrades on any critical metric, revert to 0% on the new spec. No "let's try 15% and see" — that delays the decision and extends risk exposure.

**Example:** A payment processing agent deploys spec v2.5 to 10% canary. Over 48 hours, v2.4 (old) runs at 90% traffic; v2.5 (new) runs at 10%. Metrics: old has 99.2% pass rate, $0.08 cost/transaction, 0.3% escalation rate. New has 99.4% pass rate, $0.07 cost/transaction, 0.2% escalation rate. New is better on all metrics. Promote v2.5 to 100%.

---

## Resulting Context

- **Risk is graduated and observable.** The majority of production traffic is protected while the new spec proves itself against real requests.
- **Rollback is a routine operation.** If the canary fails, the revert is pre-planned and operationally simple — not an emergency.
- **Spec changes are validated under real conditions.** Pre-deployment testing is necessary but insufficient; canary deployment provides the confidence that testing alone cannot.
- **Metrics-driven decisions replace intuition.** The promote/revert decision is based on quantitative comparison, not on someone's opinion of the new spec.

---

## Therefore

> **Deploy spec changes to a traffic percentage first. Compare metrics between old and new over a declared period. Promote when the canary validates. Revert immediately when it regresses. The canary protects the majority from untested changes.**

---

## Connections

- [Spec Versioning](spec-versioning.md) — canary deploys compare two spec versions in production
- [Spec Conformance Testing](../testing/spec-conformance.md) — pre-deployment testing catches many issues; canary catches the rest
- [Rollback on Failure](rollback.md) — canary revert is a specific case of rollback
- [Four Signal Metrics](../../operating/06-metrics.md) — signal metrics are the comparison criteria
