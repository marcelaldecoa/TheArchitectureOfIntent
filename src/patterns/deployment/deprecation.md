# Agent Deprecation Path

---

> *"Retiring an agent is a governance event, not a silent deletion."*

---

## Context

An agent deployment is being retired — replaced by a better system, consolidated into another agent, or decommissioned because its function is no longer needed. Active consumers — users, other agents, pipelines, integrations — depend on it.

---

## Problem

Without a deprecation path, retired agents disappear without notice. Consumers discover the retirement through errors. Pipelines that depended on the agent fail. Users who relied on it receive no guidance about alternatives.

---

## The Solution

Retire agents through a **declared deprecation path** with communication, migration, and archival.

1. **Announce deprecation.** Notify all known consumers (teams, pipeline specs, integration owners) with: the deprecation date, the reason, and the replacement (if any).
2. **Provide migration guidance.** If a replacement exists, document how to migrate: spec changes needed, capability differences, timeline.
3. **Deprecation period.** The agent continues to operate for a declared transition period (typically 30-90 days) with a deprecation warning in its responses.
4. **Archive, don't delete.** The agent's spec, governance history, and registry entry are archived — not destroyed. They remain available for audit and reference.
5. **Update the registry.** The agent's status moves to "deprecated" with the deprecation date and replacement link.

---

## Therefore

> **Retire agents through a declared deprecation path: announce, provide migration guidance, maintain a transition period, archive governance history, and update the registry. Deprecation is a governed event with accountability, not a silent removal.**

---

## Connections

- [Agent Registry](../state/agent-registry.md) — the registry tracks deprecation status
- [Spec Versioning](spec-versioning.md) — the deprecated agent's last spec version is archived
- [Audit Trail](../observability/audit-trail.md) — the deprecation decision is an auditable governance event
- [Governed Archetype Evolution](../../architecture/06-evolving-archetypes.md) — deprecation is one outcome of archetype evolution
