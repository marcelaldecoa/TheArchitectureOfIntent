# Shared Context Store

---

> *"One agent writes. Others read. The store is the single source of shared truth."*

---

## Context

Multiple agents in a pipeline need access to the same data — a parsed schema, a generated plan, a classification result. The data was produced by one agent and is needed by one or more downstream agents.

---

## Problem

Passing data through agent conversation chains is lossy — context is summarized, truncated, or reformatted at each handoff. Agents that need the same data get different versions of it. There is no single source of truth for shared pipeline state.

---

## The Solution

Declare an explicit **shared context store** — a structured data location where agents read and write pipeline state.

1. **Write-ownership is declared.** Each data element has exactly one writer. Only the Schema Parser writes `parsed_schema`. Only the Controller Generator writes `controller_files`. No concurrent writes to the same key.
2. **Read access is declared.** Each agent's spec declares which store keys it reads. Agents cannot access keys outside their manifest.
3. **The store is typed.** Each key has a declared schema. Writes are validated against the schema before storage.
4. **The store is ephemeral to the pipeline execution.** It is created when the pipeline starts and discarded when the pipeline completes (or persisted as an artifact if the spec declares it).
5. **The store is not agent memory.** It is pipeline state, not persistent knowledge. Long-term memory has its own pattern.

---

## Therefore

> **When agents in a pipeline need shared data, use an explicit shared context store with declared write-ownership, typed schemas, and read-access controls. The store is the single source of truth for pipeline state.**

---

## Connections

- [Session Isolation](session-isolation.md) — the store is shared within a pipeline, not across users
- [Sequential Pipeline](../coordination/sequential-pipeline.md) — the store holds intermediate results between pipeline stages
- [Agent-to-Agent Contract](../coordination/agent-contract.md) — the store schema IS the contract between agents
- [Checkpoint and Resume](checkpoint-resume.md) — the store is what gets checkpointed for resumption
