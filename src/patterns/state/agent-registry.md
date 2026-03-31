# Agent Registry

---

> *"Before deploying a new agent, know what agents already exist."*

---

## Context

An organization has multiple agent deployments — customer support agents, code generation pipelines, monitoring agents, data analysis agents. Teams deploy new agents independently. There is no central view of what agents exist, what archetype each follows, what spec governs each, or who owns each.

---

## Problem

Without a registry, the organization cannot answer basic questions: How many agents do we have? Which ones have write access to production systems? Which ones were last reviewed more than six months ago? Duplicate agents are deployed for the same function. Governance reviews cannot enumerate the systems under governance.

---

## The Solution

Maintain a **discoverable agent registry** — a catalog of all deployed agent systems with their governance metadata.

**Registry entry structure:**
- Agent name and identifier
- Archetype classification
- Current spec version (link to spec document)
- Owner (team and individual)
- Deployment status (active, staging, deprecated)
- Last governance review date
- Tool manifest summary (effect classes in use)
- Escalation path

The registry is the organizational view of the agent fleet. It is maintained alongside the archetype catalog and updated when agents are deployed, modified, or retired.

---

## Therefore

> **Maintain a registry of all deployed agents with their archetype, spec version, owner, and governance status. The registry enables fleet-level governance, prevents duplication, and makes the organization's agent landscape visible.**

---

## Connections

- [Delegated Definition Authority](../../operating/03-who-defines-archetypes.md) — the registry records who authorized each agent's archetype
- [Four Signal Metrics](../../operating/06-metrics.md) — registry-level aggregation enables fleet-wide metrics
- [Agent Deprecation Path](../deployment/deprecation.md) — deprecated agents are marked in the registry with migration guidance
- [Audit Trail](../observability/audit-trail.md) — registry changes are auditable events
