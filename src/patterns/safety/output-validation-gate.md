# Output Validation Gate

---

> *"The agent produced something. Before it goes anywhere, check it."*

---

## Context

An agent has produced output — generated code, a customer response, a report, a transaction. The output is about to be delivered to a user, stored in a system, or passed to the next agent in a pipeline.

---

## Problem

Agent output looks correct more often than it is correct. Without validation, incorrect output reaches consumers at machine speed. The faster the agent executes, the faster incorrect output accumulates. Catching errors after delivery is more expensive than catching them before.

---

## The Solution

Validate agent output **against the spec's success criteria before delivery**. Use the appropriate validation mechanism for the output type.

**Validation tiers:**

1. **Programmatic validation.** Schema checks, range validation, format compliance, required field presence. Fast, deterministic, catches structural errors.
2. **Constraint conformance.** Check output against each constraint in the spec. Did the agent violate any invariant? Did it take an unauthorized action?
3. **Semantic validation.** Use a second agent (Guardian archetype) to evaluate output quality against the spec's success criteria. The Guardian follows its own spec. It checks; it does not modify.
4. **Human review.** For irreversible or high-consequence output, a human reviews against the spec. Human review answers "does this match the spec?" not "do I like this?"

**Place the gate based on consequence:**
- Low consequence, high volume → tier 1 (programmatic) is sufficient
- Medium consequence → tiers 1+2 (programmatic + constraint check)
- High consequence, irreversible → tiers 1+2+3 (add Guardian) or 1+2+4 (add human)

---

## Therefore

> **Validate agent output against the spec's success criteria before delivery. Use programmatic checks for structure, constraint conformance for authorization, and Guardian agents or human review for semantic quality. Place the gate proportionally to consequence.**

---

## Connections

- [Retry with Structured Feedback](../coordination/retry-feedback.md) — validation failures feed the retry mechanism
- [Spec Conformance Test](../testing/spec-conformance.md) — conformance tests are the test-time version of validation gates
- [The Guardian Archetype](../../architecture/archetypes/guardian.md) — the Guardian is the agent-based semantic validator
- [Proportional Oversight](../../agents/06-human-oversight-models.md) — the oversight model determines which validation tier is required
