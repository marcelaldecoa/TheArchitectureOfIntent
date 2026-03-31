# Rollback on Failure

---

> *"When the new spec breaks production, revert first and diagnose second."*

---

## Context

An agent system runs in production with real traffic. Spec changes are deployed regularly — tightened constraints, new capabilities, adjusted scope. Despite pre-deployment testing and canary validation, some regressions only manifest under full production load, with specific user segments, or after a time delay. When a regression is detected, the priority is restoring correct behavior in minutes, not diagnosing the root cause.

---

## Problem

A customer service agent has spec v2.1 deployed. The new version reduces the refund authorization limit from $500 to $100 based on a policy change. In production, within 30 minutes, 200 legitimate refund requests fail because the new constraint is too tight for the actual refund distribution. The team doesn't immediately know whether the constraint is wrong or whether the policy should never have been changed. Every minute the wrong spec is live costs customer satisfaction and revenue. Editing the spec in production is tempting but dangerous — it bypasses review, creates an unversioned state, and may introduce new problems.

---

## Forces

- **Immediate recovery vs. root cause understanding.** Users and revenue are affected now; understanding why can wait. But reverting without understanding risks reverting a correct change.
- **Immutable versions vs. in-place fixes.** Immutable specs make rollback safe (you know exactly what v2.0 does). In-place edits are faster but create unversioned, unreviewed states.
- **In-flight execution vs. clean cutover.** Some requests started under v2.1 and are mid-execution when rollback occurs. Cancelling them has user impact; completing them under the failing spec has quality impact.
- **Rollback frequency vs. deployment confidence.** Frequent rollbacks signal spec review problems. Zero rollbacks may signal insufficient canary scrutiny. The rollback mechanism should exist and rarely be needed.

---

## The Solution

Maintain the **previous spec version as a deployable artifact** and revert to it when the current version causes regression.

1. **Spec versions are immutable.** Old versions are never modified. v2.0.3 is archived and remains deployable indefinitely. When you revert, you know exactly what behavior you're restoring.
2. **Rollback is a deployment operation, not a code change.** Switch the active spec version from v2.1.0 back to v2.0.3. This is a routing/configuration change — no editing, no emergency patches, no unreviewed modifications.
3. **Define in-flight execution policy ahead of time.** Before deploying any spec change, decide: when rollback triggers, do in-flight executions (a) complete under the old constraints, (b) complete under the new constraints, or (c) get cancelled with a retry signal? The policy depends on reversibility of the agent's actions.
4. **Rollback triggers a mandatory post-mortem.** Every rollback generates an investigation record: Why did the canary not catch this? Why did conformance tests pass? Was the spec change correct but poorly communicated, or was it a spec error? The rollback is immediate; the investigation is thorough and asynchronous.

**Example:** At 2:15 PM, monitoring alerts fire: refund success rate dropped from 98% to 71% after v2.1 deployment at 2:00 PM. At 2:18 PM, on-call engineer issues: `deploy spec customer-service:2.0.3`. At 2:20 PM, version switch completes. The 200 queued refund requests retry under v2.0.3 and succeed. At 2:25 PM, the service returns to normal. Post-mortem investigation (next day) finds: the $100 limit was correct policy, but the spec needed an exception path for orders with pre-approved refund amounts. Fix: v2.2 adds the exception path, goes through full review and canary before deployment.

---

## Resulting Context

- **Recovery is operationalized.** Rollback is a single deployment step, not an emergency patch cycle. Any on-call engineer can execute it.
- **Immutability enables confidence.** Because old specs are never modified, you know exactly what v2.0.3 does — no hidden changes, no "I think I fixed it in place."
- **Governance accountability is strengthened.** Every rollback generates investigation. You cannot silently deploy a broken spec and hope no one notices.
- **Deployment confidence increases over time.** Teams that know rollback is fast and safe deploy more frequently and with smaller changes — reducing risk per deployment.

---

## Therefore

> **Keep previous spec versions deployable and immutable. Rollback is a version switch, not an edit. Revert immediately when production regresses, then diagnose. Never modify a failing spec in production — revert to the last known good version.**

---

## Connections

- [Spec Versioning](spec-versioning.md) — immutable versions make rollback possible
- [Canary Deployment](canary.md) — canary catches most issues before full deployment; rollback handles the rest
- [Checkpoint and Resume](../state/checkpoint-resume.md) — in-flight pipeline executions may need to resume under the rolled-back spec
- [Six Failure Categories](../../agents/07-failure-modes.md) — the rollback trigger signals either a spec failure or a model-level failure
