# Shared Context Store

---

> *"One agent writes. Others read. The store is the single source of shared truth."*

---

## Context

Multiple agents in a pipeline need access to the same data — a parsed schema, a generated plan, a classification result. The data was produced by one agent and is needed by one or more downstream agents.

---

## Problem

Passing data through agent conversation chains is lossy — context is summarized, truncated, or reformatted at each handoff. Agents that need the same data get different versions of it. There is no single source of truth for shared pipeline state.

**Concrete scenario:** A code-generation pipeline: Agent 1 (Parser) reads an OpenAPI spec and generates a structured schema object. Agent 2 (Controller Generator) needs that schema to generate controller code. Agent 3 (Test Generator) also needs it. Data passes: Parser → context history → Controller (quotes key parts of schema in its input prompt) → Controller → context history → Test Generator. The Test Generator's view of the schema is a summary of a summary, missing optional fields and nested object details. Test Generator generates tests for an incomplete schema, missing edge cases.

---

## Forces

- **Need shared data for coordination** vs. **risk of shared data becoming a bottleneck** (write conflicts, synchronization)
- **Need to trust the shared data** ("Is this the current version?") vs. **complexity of schema versioning** (which version are you reading?)
- **Need fast writes** (one agent completes, immediately passes data) vs. **need data validation** (wrong data causes downstream failure)
- **Need the store to enable agent independence** vs. **need tight coupling for data contracts** (agents must know what format to expect)

---

## The Solution

Declare an explicit **shared context store** — a structured data location where agents read and write pipeline state.

1. **Write-ownership is declared.** Each data element has exactly one writer. Only the Schema Parser writes `parsed_schema`. Only the Controller Generator writes `controller_files`. No concurrent writes to the same key.
2. **Read access is declared.** Each agent's spec declares which store keys it reads. Agents cannot access keys outside their manifest.
3. **The store is typed.** Each key has a declared schema. Writes are validated against the schema before storage.
4. **The store is ephemeral to the pipeline execution.** It is created when the pipeline starts and discarded when the pipeline completes (or persisted as an artifact if the spec declares it).
5. **The store is not agent memory.** It is pipeline state, not persistent knowledge. Long-term memory has its own pattern.

**Example:** The code-generation pipeline. The spec declares the shared context store:
```
shared_context:
  store_type: "in_memory_map"
  schema:
    parsed_schema:
      writer: "agent_parser"
      readers: ["agent_controller", "agent_test"]
      type: "OpenAPISchema"
      required_fields: ["paths", "components", "info"]
    controller_files:
      writer: "agent_controller"
      readers: []
      type: "FileCollection"
    test_files:
      writer: "agent_test"
      readers: []
      type: "FileCollection"
```
Agent 1 (Parser) reads the OpenAPI spec, validates it against the schema, writes `parsed_schema` with all fields: `{"paths": {...}, "components": {...}, "info": {...}, "servers": [...], "security": [...]}`. The write is validated.

Agent 2 (Controller) reads `parsed_schema`, generates `controller_files`, writes them. Agent 3 (Test) reads `parsed_schema` (same complete object, not a summary), generates tests that cover all the edge cases because the schema is intact.

---

## Resulting Context

- **Agents coordinate with complete, current data**, not summaries or stale copies
- **Data contracts are explicit** (typed schemas, write-ownership, read access), so agents know exactly what they're getting
- **One source of truth** prevents version confusion across the pipeline
- **Write-conflicts are prevented** by declaring single writers per key

---

## Therefore

> **When agents in a pipeline need shared data, use an explicit shared context store with declared write-ownership, typed schemas, and read-access controls. The store is the single source of truth for pipeline state.**

---

## Connections

- [Session Isolation](session-isolation.md) — the store is shared within a pipeline, not across users
- [Sequential Pipeline](../coordination/sequential-pipeline.md) — the store holds intermediate results between pipeline stages
- [Agent-to-Agent Contract](../coordination/agent-contract.md) — the store schema IS the contract between agents
- [Checkpoint and Resume](checkpoint-resume.md) — the store is what gets checkpointed for resumption