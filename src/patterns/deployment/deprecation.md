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

## Forces

- **Breaking consumers vs. clean deletion.** Immediately removing the agent prevents technical debt and confusion about which version is current. But it breaks all systems that depend on it. A transition period prevents breakage but delays cleanup.
- **Notification reach vs. notification noise.** Reaching every consumer requires comprehensive discovery (who depends on this agent?). But over-notifying creates alarm fatigue. The deprecation announcement must be loud enough to reach everyone but specific enough to prioritize action.
- **Migration support vs. autonomy.** Providing detailed migration guides helps teams move faster. But writing and maintaining those guides is expensive. Teams would prefer autonomy to figure out migration themselves — until they can't.

---

## The Solution

Retire agents through a **declared deprecation path** with communication, migration, and archival.

1. **Announce deprecation.** Notify all known consumers (teams, pipeline specs, integration owners) with: the deprecation date, the reason, and the replacement (if any).
2. **Provide migration guidance.** If a replacement exists, document how to migrate: spec changes needed, capability differences, timeline.
3. **Deprecation period.** The agent continues to operate for a declared transition period (typically 30-90 days) with a deprecation warning in its responses.
4. **Archive, don't delete.** The agent's spec, governance history, and registry entry are archived — not destroyed. They remain available for audit and reference.
5. **Update the registry.** The agent's status moves to "deprecated" with the deprecation date and replacement link.

**Example:** The `email-drafter` agent is being deprecated in favor of the new `message-composer` agent, which handles email, SMS, and push notifications. Announcement issued. Email-drafter responses now include: "This agent is deprecated as of [date]. Use message-composer instead. See migration guide at [link]." Thirty days to migration. After 90 days total, email-drafter returns 410 Gone, with a contact for questions. The spec and full governance chain are preserved in the archive under `deprecated/email-drafter/`.

---

## Resulting Context

- **Dependent systems have time to adapt.** The transition period and clear timeline give teams runway to plan migration rather than scrambling after sudden removal.
- **Governance is auditable.** Why was this agent deprecated? When? What was the replacement? This history is preserved, not erased.
- **Learning is captured.** If the deprecated agent solved a hard problem that the replacement solves differently, the old spec remains as reference documentation.
- **No silent failures.** Consumers discover deprecation through explicit messaging, not through error logs weeks later.

---

## Therefore

> **Retire agents through a declared deprecation path: announce, provide migration guidance, maintain a transition period, archive governance history, and update the registry. Deprecation is a governed event with accountability, not a silent removal.**

---

## Connections

- [Agent Registry](../state/agent-registry.md) — the registry tracks deprecation status
- [Spec Versioning](spec-versioning.md) — the deprecated agent's last spec version is archived
- [Audit Trail](../observability/audit-trail.md) — the deprecation decision is an auditable governance event
- [Governed Archetype Evolution](../../architecture/06-evolving-archetypes.md) — deprecation is one outcome of archetype evolution