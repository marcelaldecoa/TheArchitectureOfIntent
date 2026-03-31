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

## Forces

- **Speed vs. quality gate latency**: Adding validation delays output. For latency-critical tasks, expensive semantic validation may be unacceptable. The tradeoff must be chosen per task.
- **False positives in validation**: A Guardian agent might reject correct output that deviates from expected patterns. Conversely, a programmatic validator might miss subtle semantic errors. No gate is perfect.
- **Consequence of rejection**: If validation rejects output, what happens? Retry with feedback? Escalate to human? Fail the task? The cost of rejection varies by task and affects gate threshold.
- **Determining success criteria**: What does "correct" mean? The spec must define success criteria precisely. Ambiguous specs produce ambiguous validation.

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

**Example:** A code generation agent produces pull requests.
- **Low-risk fixes** (tests, minor refactors): Tier 1 — Python AST validation (code is syntactically valid), no constraint check needed.
- **Medium-risk changes** (API modifications, doc updates): Tier 1+2 — AST validation + constraint check ("does PR reference the issue number?" and "does it not modify database schema without approval?").
- **High-risk changes** (permission system, payment logic): Tier 1+2+3 — AST validation + constraint check + Guardian agent that reviews architecture consistency and SQL query safety + human code review.

---

## Resulting Context

- **Structural errors are caught immediately.** Tier 1 validation prevents malformed output from reaching downstream systems.
- **Policy violations are caught before delivery.** Tier 2 constraint checking ensures spec compliance.
- **Semantic quality is validated without human bottleneck.** Guardian validation (tier 3) provides semantic checking at machine speed.
- **High-consequence output receives appropriate scrutiny.** The validation gate matches consequence: low-risk tasks are fast, high-risk tasks are slower but more reliable.

---

## Therefore

> **Validate agent output against the spec's success criteria before delivery. Use programmatic checks for structure, constraint conformance for authorization, and Guardian agents or human review for semantic quality. Place the gate proportionally to consequence.**

---

## Connections

- [Retry with Structured Feedback](../coordination/retry-feedback.md) — validation failures feed the retry mechanism
- [Spec Conformance Test](../testing/spec-conformance.md) — conformance tests are the test-time version of validation gates
- [The Guardian Archetype](../../architecture/archetypes/guardian.md) — the Guardian is the agent-based semantic validator
- [Proportional Oversight](../../agents/06-human-oversight-models.md) — the oversight model determines which validation tier is required