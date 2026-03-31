# Agent-to-Agent Contract

---

> *"What Agent A sends must be what Agent B expects. Write it down."*

---

## Context

Two agents in a pipeline or multi-agent system need to exchange data. Agent A produces output that Agent B consumes as input. The agents may be written by different people, run on different platforms, or be modified independently.

---

## Problem

Without a declared contract, Agent A's output shape drifts over time, and Agent B fails silently on unexpected input. The failure manifests far downstream — not at the handoff where it originated. Debugging requires tracing backward through multiple agents to find where the mismatch occurred.

---

## Forces

- **Evolution creates drift**: As requirements change, agents are updated. Without a contract, Agent A's output shape drifts without Agent B's knowledge.
- **Silent failures hide the mismatch**: Agent B might accept unexpected input gracefully (ignoring unknown fields) or crash. Silent acceptance is worse — B processes incorrect data without knowing it.
- **Contract enforcement has overhead**: Validating every handoff adds latency. For high-throughput pipelines, validation cost is significant.
- **Versioning and backward compatibility**: When the contract changes, should Agent B still accept old versions of Agent A's output? How many versions back? The versioning strategy must be clear.

---

## The Solution

Declare an **explicit contract** between agents — a versioned schema that specifies what one agent produces and what the next agent expects.

**Contract structure:**

1. **Output schema for Agent A.** The exact shape of the data: fields, types, required vs. optional, nested structures. JSON Schema or equivalent.
2. **Input schema for Agent B.** What Agent B requires: which fields it reads, which are mandatory, acceptable value ranges.
3. **Contract validation at handoff.** The pipeline validates Agent A's output against the contract before passing it to Agent B. Contract violations halt the pipeline with a structured error, not a downstream crash.
4. **Contract versioning.** When the contract changes, both agents must be updated. Breaking changes require coordination. The contract version is logged with every handoff.
5. **Example payloads.** At least one example of valid contract data, used for testing and documentation.

**Example:** Agent A generates a feature specification; Agent B implements the feature.

**Contract v1.0:**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["feature_name", "acceptance_criteria", "priority"],
  "properties": {
    "feature_name": {"type": "string"},
    "description": {"type": "string"},
    "acceptance_criteria": {"type": "array", "items": {"type": "string"}},
    "priority": {"enum": ["low", "medium", "high"]},
    "estimated_hours": {"type": "number"}
  }
}
```

Agent A produces:
```json
{
  "feature_name": "User login with OAuth",
  "description": "Support OAuth login flow",
  "acceptance_criteria": ["User can login with GitHub", "Session persists"],
  "priority": "high",
  "estimated_hours": 8,
  "contract_version": "1.0"
}
```

Agent B validates against contract v1.0 before consuming. If Agent A produces missing `priority` field, validation fails immediately with "Missing required field: priority". The error is caught at the handoff, not three agents downstream.

---

## Resulting Context

- **Handoff failures are caught immediately.** Contract validation at the boundary produces clear errors at the point of mismatch.
- **Agents evolve independently.** As long as the contract is honored, Agent A can be replaced, upgraded, or modified without affecting Agent B.
- **Integration testing has a defined surface.** Test the contract — not the internal implementation — and integration is verified.

---

## Therefore

> **Declare an explicit, versioned contract between any two agents that exchange data. Validate output against the contract at every handoff. When the contract breaks, the pipeline halts at the boundary — not downstream where the debugging is harder.**

---

## Connections

- [Sequential Pipeline](sequential-pipeline.md) — contracts define the handoffs between pipeline stages
- [Parallel Fan-Out](parallel-fan-out.md) — fan-out merge requires that all subtask outputs conform to the merge contract
- [Supervisor Agent](supervisor.md) — the supervisor validates cross-agent contracts
- [Multi-Agent Integration Test](../testing/multi-agent-integration.md) — integration tests verify contracts under realistic conditions