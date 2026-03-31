# Rollback on Failure

---

> *"When the new spec breaks production, revert first and diagnose second."*

---

## Context

A spec change was deployed and is causing regressions — increased error rates, validation failures, user complaints. The new spec version is worse than the old one. You need to restore correct behavior immediately.

---

## The Solution

Maintain the **previous spec version as a deployable artifact** and revert to it when the current version fails.

1. **Spec versions are immutable.** Old versions are never modified. They are archived and remain deployable.
2. **Rollback is a deployment operation, not a code change.** Switch the active spec version from v2.1.0 back to v2.0.3. No editing, no emergency patches.
3. **Rollback triggers a post-mortem.** Why did the canary not catch this? Why did regression tests pass? The rollback is immediate; the diagnosis follows.
4. **Agents executing at rollback time complete under the old spec or are cancelled.** In-flight executions under the failing spec are handled according to the pipeline's failure policy.

---

## Therefore

> **Keep previous spec versions deployable. Rollback is a version switch, not an edit. Revert immediately when production regresses, then diagnose. Never modify a failing spec in production — revert to the last known good version.**

---

## Connections

- [Spec Versioning](spec-versioning.md) — immutable versions make rollback possible
- [Canary Deployment](canary.md) — canary catches most issues before full deployment; rollback handles the rest
- [Checkpoint and Resume](../state/checkpoint-resume.md) — in-flight pipeline executions may need to resume under the rolled-back spec
- [Six Failure Categories](../../agents/07-failure-modes.md) — the rollback trigger signals either a spec failure or a model-level failure
