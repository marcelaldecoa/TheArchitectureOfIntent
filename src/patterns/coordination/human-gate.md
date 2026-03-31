# Human-in-the-Loop Gate

---

> *"Pause here. A human needs to decide before the system proceeds."*

---

## Context

An agent pipeline reaches a point where the next action is consequential, ambiguous, or policy-sensitive. The agent has gathered information and may have a recommendation, but the decision authority belongs to a human.

---

## Problem

Without an explicit gate, agents either proceed autonomously past decision points (overstepping authority) or stop entirely and wait for unstructured human input (blocking progress). The human receives no context about what was attempted, what was found, or what decision is needed — they are asked to "review" without knowing what to review.

---

## Forces

- **Autonomy speed vs. decision quality.** Autonomous execution is fast. But consequential decisions made autonomously lack the judgment that only humans provide.
- **Structured handoff vs. open-ended review.** A structured decision package is actionable. An open-ended "please review" invitation is a time sink.
- **Gate frequency vs. operational throughput.** Every gate adds latency. Too many gates eliminate the productivity benefit of agents. Too few gates let consequential actions pass without review.

---

## The Solution

Design the gate as a **named checkpoint** where the agent produces a **structured decision package** and the human provides a **routing decision**.

**Gate structure:**

1. **The agent pauses.** Execution halts at the declared checkpoint. No downstream actions occur until the human responds.
2. **The agent presents a decision package:**
   - What was done so far (summary of prior stages)
   - What was found (data, analysis, relevant context)
   - What decision is needed (a specific question, not "what do you think?")
   - Available options (with consequences of each)
   - Agent's recommendation (if authorized to recommend)
3. **The human responds with a routing decision.** "Proceed with option A." "Reject — revise the constraint to X." "Escalate to [person]." The response is structured, not free-text conversation.
4. **The agent continues** with the human's decision as authoritative input. The decision is logged as part of the execution record.

**Placement criteria:** Gates are placed at points where:
- The action is irreversible (payment, external communication, production deployment)
- The decision involves policy judgment (approve exception, override constraint)
- The spec explicitly requires human approval for this class of action

---

## Resulting Context

- **Consequential decisions have human judgment.** The gate ensures that high-stakes actions receive human review without requiring human involvement in every step.
- **The human is informed, not overwhelmed.** A structured decision package takes seconds to review rather than minutes to understand.
- **Decision authority is traceable.** The human's routing decision is logged with identity, timestamp, and the decision package they reviewed.

---

## Therefore

> **At consequential decision points, halt the pipeline and present the human with a structured decision package — what was found, what decision is needed, and what options exist. The human's response becomes authoritative input for the next stage.**

---

## Connections

- [Sequential Pipeline](sequential-pipeline.md) — the gate is a named stage in the pipeline
- [Proportional Oversight](../../agents/06-human-oversight-models.md) — gates are placed proportionally to consequence, not uniformly
- [Escalation Chain](escalation-chain.md) — one of the human's options at a gate is to escalate to a higher authority
- [Audit Trail](../observability/audit-trail.md) — human decisions at gates are logged as auditable events
- [Design for Reversibility](../../theory/04-reversibility-as-design-dimension.md) — gates are mandatory before irreversible actions
