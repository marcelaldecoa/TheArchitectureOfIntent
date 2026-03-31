# Agent Registry

---

> *"Before deploying a new agent, know what agents already exist."*

---

## Context

An organization has multiple agent deployments — customer support agents, code generation pipelines, monitoring agents, data analysis agents. Teams deploy new agents independently. There is no central view of what agents exist, what archetype each follows, what spec governs each, or who owns each.

---

## Problem

Without a registry, the organization cannot answer basic questions: How many agents do we have? Which ones have write access to production systems? Which ones were last reviewed more than six months ago? Duplicate agents are deployed for the same function. Governance reviews cannot enumerate the systems under governance.

**Concrete scenario:** A mid-size fintech company. Engineering deploys "MarketAnalysis-v1" (autonomy archetype, read-only). Two months later, the Data team deploys "MarketWatch" (autonomous archetype, write access to recommendations database) to run the same function. Neither team knows about the other. Six months goes by with both running in production. An audit finds two agents doing the same job with different governance oversight. The Data team's agent has never been reviewed. The Engineering team doesn't know MarketWatch exists. The company cannot answer: "How many agents have production write access?"

---

## Forces

- **Need visibility into agent fleet** vs. **overhead of registry maintenance** (who keeps it current?)
- **Need to prevent duplication** vs. **freedom for teams to deploy independently** (registry becomes a bottleneck)
- **Need to enforce governance compliance** vs. **ease of deployment** (registry becomes friction)
- **Need to track agent lineage** (owner, creation date) vs. **privacy/autonomy** (teams don't want to be audited constantly)

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

**Example:** The fintech company implements a registry at `governance.internal/agents/`:
```
{
  "agents": [
    {
      "id": "market-analysis-v1",
      "name": "Market Analysis (Engineering)",
      "archetype": "autonomy:read_only",
      "spec_version": "market-analysis/v2.3.1",
      "owner": {"team": "Engineering", "contact": "eng-leads@company.com"},
      "status": "active",
      "last_review": "2026-02-15",
      "tools_used": ["data:read", "api:market_data"],
      "escalation": "eng-sre@company.com"
    },
    {
      "id": "market-watch",
      "name": "Market Watch (Data Team)",
      "archetype": "autonomy:read_write",
      "spec_version": "market-watch/v1.0.0",
      "owner": {"team": "Data", "contact": "data-leads@company.com"},
      "status": "active",
      "last_review": null,
      "tools_used": ["data:read", "database:write", "api:market_data"],
      "escalation": "data-sre@company.com"
    }
  ]
}
```
Query: "Which agents have database write access?" → Returns market-watch. "Which agents haven't been reviewed in 6 months?" → Returns market-watch. Governance team schedules a review. When a new agent is proposed, the team checks registry first: "Market analysis already exists — propose consolidation or a different function."

---

## Resulting Context

- **Duplication is visible and preventable** — teams can see what already exists before deploying
- **Governance is fleet-wide** — compliance checks can query all agents systematically
- **Ownership is clear** — every agent has a designated owner and escalation path
- **Risk is quantified** — how many write-access agents? How many overdue for review?

---

## Therefore

> **Maintain a registry of all deployed agents with their archetype, spec version, owner, and governance status. The registry enables fleet-level governance, prevents duplication, and makes the organization's agent landscape visible.**

---

## Connections

- [Delegated Definition Authority](../../operating/03-who-defines-archetypes.md) — the registry records who authorized each agent's archetype
- [Four Signal Metrics](../../operating/06-metrics.md) — registry-level aggregation enables fleet-wide metrics
- [Agent Deprecation Path](../deployment/deprecation.md) — deprecated agents are marked in the registry with migration guidance
- [Audit Trail](../observability/audit-trail.md) — registry changes are auditable events