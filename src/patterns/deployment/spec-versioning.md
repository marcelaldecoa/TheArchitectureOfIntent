# Spec Versioning

---

> *"Version the spec like you version the code. Breaking changes demand coordination."*

---

## Context

Specs evolve — constraints are tightened, scope is adjusted, success criteria are refined. Multiple consumers depend on the spec: agents executing against it, tests validating against it, dashboards reporting against it. Changes must be tracked and coordinated.

---

## The Solution

Version specs with **semantic versioning** tied to behavioral impact.

1. **Major version** — breaking changes. Constraint tightening, scope reduction, archetype reclassification, removed authorization. All downstream consumers must review and potentially update.
2. **Minor version** — additive changes. New capabilities within existing scope, additional success criteria, new tool authorization. Backward-compatible with existing consumers.
3. **Patch version** — behavior preservation fixes. Clarifying ambiguous language, fixing typos, adding examples. No behavioral change.
4. **The spec evolution log** records every version transition with: what changed, why, who approved, and what downstream impact was assessed.

---

## Therefore

> **Version specs semantically: major for breaking changes, minor for additions, patch for fixes. Record every version with change rationale and downstream impact. Spec versions are the coordination mechanism for managing change across agents, tests, and governance.**

---

## Connections

- [The Living Spec](../../sdd/06-living-specs.md) — the living spec practice produces version changes through the feedback loop
- [Regression on Spec Change](../testing/regression-spec-change.md) — version changes trigger regression testing
- [Canary Deployment](canary.md) — new versions can be canary-deployed
- [Agent-to-Agent Contract](../coordination/agent-contract.md) — contract versions align with spec versions
- [Artifact Store](../state/artifact-store.md) — artifacts are linked to the spec version that produced them
