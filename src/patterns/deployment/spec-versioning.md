# Spec Versioning

---

> *"Version the spec like you version the code. Breaking changes demand coordination."*

---

## Context

Specs evolve — constraints are tightened, scope is adjusted, success criteria are refined. Multiple consumers depend on the spec: agents executing against it, tests validating against it, dashboards reporting against it. Changes must be tracked and coordinated.

---

## Problem

Unversioned specs create ambiguity: which version of the constraint is currently enforced? When a spec changes, do all downstream consumers get updated automatically or must they explicitly migrate? If a spec is rolled back, which version do systems revert to? Without explicit versioning, teams either over-communicate every change (noise) or under-communicate (silent breakage).

---

## Forces

- **Backward compatibility vs. improvement.** Tightening constraints improves reliability but breaks systems built on the loosely constrained version. Complete backward compatibility prevents improvement. Some level of breaking change is inevitable; versioning makes it explicit and negotiable.
- **Granularity of versions.** Should every rewording of a constraint trigger a version bump? Every new tool authorization? Only structural changes? Overly granular versions obscure meaningful changes; overly coarse versions hide significant shifts.
- **Downstream coordination cost.** Each version bump potentially requires consumers to review and acknowledge the change. Too many buckets create overhead; too few hide migration paths.

---

## The Solution

Version specs with **semantic versioning** tied to behavioral impact.

1. **Major version** — breaking changes. Constraint tightening, scope reduction, archetype reclassification, removed authorization. All downstream consumers must review and potentially update.
2. **Minor version** — additive changes. New capabilities within existing scope, additional success criteria, new tool authorization. Backward-compatible with existing consumers.
3. **Patch version** — behavior preservation fixes. Clarifying ambiguous language, fixing typos, adding examples. No behavioral change.
4. **The spec evolution log** records every version transition with: what changed, why, who approved, and what downstream impact was assessed.

**Example:** Spec `claims-validator` is at v2.3.1. A new requirement emerges: "Validate that claim doesn't duplicate within 30 days." This is a new rule within existing scope (validation). Minor version bump to v2.4.0. Six weeks later, a business rule tightens: claim limits drop from $5K to $3K. This is a constraint tightening. Major version bump to v3.0.0. All systems consuming this spec receive notification. Those set to auto-upgrade minor versions are automatically moved to v2.4.0 but must acknowledge before upgrading to v3.0.0.

---

## Resulting Context

- **Downstream systems know when to react.** Major version changes demand review; minor and patch changes are safe to consume.
- **A/B testing is possible.** Two agents can run under different spec versions simultaneously to measure impact before rolling out major versions.
- **Rollback is explicit.** When a spec version causes problems, rolling back to the previous version is a named, auditable action.
- **Evolution is recorded.** The spec evolution log documents the business reasoning behind each change, not just the technical diff.

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