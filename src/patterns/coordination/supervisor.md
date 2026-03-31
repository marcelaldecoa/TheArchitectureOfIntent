# Supervisor Agent

---

> *"Workers execute. The supervisor watches for the problems that no individual worker can see."*

---

## Context

Multiple agents are executing in parallel or in sequence. Each agent produces valid output by its own criteria. But the combination of outputs may be inconsistent, contradictory, or violate system-level constraints that no individual agent is aware of.

---

## Problem

Individual agents validate their own output against their own spec. But cross-agent consistency — naming conventions applied the same way across generated files, no conflicting API contracts, no duplicate work — is invisible to each agent in isolation. Without supervision, multi-agent systems produce individually correct but collectively incoherent results.

---

## The Solution

Deploy a **supervisor agent** (Orchestrator archetype) that monitors worker agents' outputs for cross-agent consistency and coordination failures.

**Supervisor responsibilities:**

1. **Cross-output consistency checking.** After workers complete, the supervisor validates that outputs are mutually consistent: shared references resolve, naming conventions align, no contradictions.
2. **Intervention on coordination failure.** When the supervisor detects inconsistency, it can: request correction from specific workers (with the inconsistency report as feedback), halt the pipeline, or escalate.
3. **System-level constraint enforcement.** Constraints that span multiple agents — total cost budget, aggregate output size limits, cross-module API consistency — are the supervisor's responsibility.
4. **The supervisor does not do the work.** It monitors and coordinates. If it starts producing content, it has drifted from Orchestrator into Executor and needs archetype re-evaluation.

---

## Resulting Context

- **Multi-agent coherence is maintained.** System-level consistency is checked by a dedicated agent rather than assumed.
- **Coordination failures are caught before delivery.** The supervisor is the last quality gate before the combined output is released.
- **Individual agents remain focused.** Workers don't need to know about each other — the supervisor handles inter-agent concerns.

---

## Therefore

> **When multiple agents produce outputs that must be consistent, deploy a supervisor agent to check cross-agent coherence, enforce system-level constraints, and intervene when coordination fails. The supervisor monitors; it does not produce.**

---

## Connections

- [Parallel Fan-Out](parallel-fan-out.md) — the supervisor monitors parallel workers
- [Agent-to-Agent Contract](agent-contract.md) — the supervisor verifies that inter-agent contracts are honored
- [Sequential Pipeline](sequential-pipeline.md) — the supervisor can be a validation stage between pipeline phases
- [Archetype Composition](../../architecture/05-composing-archetypes.md) — the supervisor is an Orchestrator archetype composed with worker archetypes
