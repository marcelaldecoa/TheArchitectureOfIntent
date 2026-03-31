# The Read-Only Tool

---

> *"A tool that only reads is a tool that cannot break anything."*

---

## Context

An agent needs information from an external system — a database, an API, a file system, a knowledge base. The agent needs to look things up, not change anything.

---

## Problem

Many tools bundle read and write operations together. An agent given access to a "customer management" tool can both look up customer records and modify them. The agent may exercise write capability even when the task only requires reading. Separating read from write at the tool level prevents authorization creep.

---

## Forces

- **Convenience vs. safety.** A single tool with full CRUD capability is easier to build and provision. But it cannot be authorized for read without also authorizing write.
- **Tool count vs. precision.** Separating read and write doubles the number of tools. But it permits the agent to look things up without any risk of state change.
- **Trust vs. verification.** Even a read-only tool can leak information if it reads data the agent shouldn't see. Read authorization is not the same as "safe."

---

## The Solution

Design tools with **read operations separated from write operations**. A read-only tool returns data without modifying any external state. It is the lowest-risk effect class and can be authorized broadly.

**Design requirements:**
- The tool is truly read-only — no side effects, no logging that changes state, no cache invalidation that affects other systems.
- The tool's scope is declared — which data sets it can access, which fields it returns.
- Data classification is respected — if a field is classified (PII, credentials), the tool either excludes it or marks it.
- Results are structured — the output follows a schema the agent can parse reliably.

**Authorization:** Read-only tools can be authorized at the lowest oversight tier. They do not require per-call human review unless the data itself is sensitive.

---

## Resulting Context

- **Agents can explore and gather information safely.** Read-only tools let agents look things up without risk of unintended state changes.
- **Authorization can be granular.** The spec can authorize lookups without authorizing modifications, giving the agent information access without action authority.
- **Audit is simplified.** Read-only operations are logged for completeness but do not require the same review rigor as state-changing operations.

---

## Therefore

> **Separate read from write at the tool level. A read-only tool returns data without side effects. It is the lowest-risk tool class, can be authorized broadly, and enables agents to gather information without the ability to change anything.**

---

## Connections

- [The State-Changing Tool](state-changing-tool.md) — write operations that require higher authorization
- [The Tool Manifest](../capability/tool-manifest.md) — read-only tools are classified as the lowest effect class in the manifest
- [The Idempotent Tool](idempotent-tool.md) — idempotency matters most for state-changing tools, not read-only ones
- [Sensitive Data Boundary](../safety/sensitive-data-boundary.md) — even read-only access to classified data requires authorization
