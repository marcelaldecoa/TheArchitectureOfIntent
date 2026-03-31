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

## Forces

- **Individual autonomy vs. system coherence**: Each agent must be autonomous to execute efficiently. But full autonomy means agents don't coordinate. Cross-agent consistency requires some form of coordination layer.
- **Supervisor bottleneck**: The supervisor reads all worker outputs and validates them. If workers run in parallel and produce large outputs, the supervisor becomes the bottleneck in the pipeline.
- **Feedback loop latency**: When the supervisor detects inconsistency, requesting correction from workers adds a round-trip delay. For latency-critical pipelines, this is expensive.
- **Authority ambiguity**: When the supervisor detects an inconsistency, who decides the resolution? If the supervisor corrects it, it has become a worker. If it escalates, latency increases. The decision rule must be clear.

---

## The Solution

Deploy a **supervisor agent** (Orchestrator archetype) that monitors worker agents' outputs for cross-agent consistency and coordination failures.

**Supervisor responsibilities:**

1. **Cross-output consistency checking.** After workers complete, the supervisor validates that outputs are mutually consistent: shared references resolve, naming conventions align, no contradictions.
2. **Intervention on coordination failure.** When the supervisor detects inconsistency, it can: request correction from specific workers (with the inconsistency report as feedback), halt the pipeline, or escalate.
3. **System-level constraint enforcement.** Constraints that span multiple agents — total cost budget, aggregate output size limits, cross-module API consistency — are the supervisor's responsibility.
4. **The supervisor does not do the work.** It monitors and coordinates. If it starts producing content, it has drifted from Orchestrator into Executor and needs archetype re-evaluation.

**Example:** A code generation system spawns three worker agents in parallel — AuthAgent (generates auth module), PaymentAgent (generates payment module), APIAgent (generates API definitions). Worker specs are independent; they don't know about each other.
Supervisor checks:
- All three agents use the same error code schema ("error_code": "AUTH_EXPIRED" vs. "expired_auth")?
- API definitions reference auth and payment endpoints correctly?
- No duplicate endpoints defined by multiple agents?
- Total generated files < 100 (cost constraint)?
If APIAgent and AuthAgent define conflicting user types, supervisor requests correction from APIAgent with the report: "User type in api.py conflicts with auth.py. Please reconcile."

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