# The State-Changing Tool

---

> *"A tool that can change the world should know exactly which part of the world it's allowed to change."*

---

## Context

An agent needs to take action in an external system — create a record, send a message, modify a configuration, initiate a transaction. The action changes state. Once executed, it may be difficult or impossible to reverse.

---

## Problem

State-changing tools are the mechanism by which agents affect the real world. A misconfigured, over-scoped, or improperly authorized state-changing tool turns the agent into an uncontrolled actor. The consequences compound: an agent that can "helpfully" create records it shouldn't, send messages it wasn't asked to, or modify configurations outside its scope produces harm that scales with execution speed.

---

## Forces

- **Action capability vs. action authorization.** The tool is technically capable of broad state changes. The spec authorizes only a subset of those changes. The tool must enforce the narrower scope.
- **Pre-authorization vs. per-call approval.** Requiring human approval for every write operation defeats the purpose of automation. But some writes are consequential enough to require it.
- **Specificity vs. flexibility.** A tool that only does one specific operation (create a refund for this order) is safe but inflexible. A tool that does many operations (manage all financial transactions) is flexible but dangerous.
- **Reversibility vs. permanence.** Some state changes can be undone (soft delete, draft creation). Others cannot (sending an email, processing a payment). The authorization model must distinguish these.

---

## The Solution

Design state-changing tools with **explicit scope, declared effect, and authorization constraints** that match the spec's requirements.

**Design requirements:**

1. **Single responsibility.** Each tool does one kind of state change. `refund.initiate` and `order.cancel` are separate tools, not options on a "manage_order" tool.
2. **Declared effect.** The tool description states exactly what state it changes, in what system, with what permanence. Agents and reviewers know the consequence before the call is made.
3. **Input validation at the tool boundary.** The tool validates its inputs against its own schema before executing. Invalid inputs are rejected with structured errors, not silently accepted.
4. **Authorization from the spec.** The tool checks that the calling agent is authorized to use it (via the tool manifest) and that the specific parameters are within the spec's constraints (e.g., refund amount ≤ $100).
5. **Confirmation for irreversible actions.** State changes classified as irreversible require explicit confirmation — either from a human (via a Human-in-the-Loop Gate) or from a Guardian agent that validates the action against constraints.

**Effect class hierarchy:**
- **Create** — adds new state. Generally reversible if deletion is available.
- **Update** — modifies existing state. Reversibility depends on whether the old state is preserved (audit log, soft update).
- **Delete** — removes state. Irreversible unless soft-delete is implemented.
- **Transmit** — sends data outside the system boundary (email, API call, webhook). Irreversible once transmitted.

---

## Resulting Context

- **Agents take consequential actions safely.** State changes are authorized, scoped, and validated before execution.
- **Incident response knows what happened.** Each state-changing call is logged with inputs, outputs, and the spec_id that authorized it.
- **Authorization granularity matches risk.** Low-risk creates are automated freely. High-risk deletes and transmissions require confirmation.

---

## Therefore

> **Design state-changing tools with single responsibility, declared effects, and authorization constraints that trace back to the spec. Separate create, update, delete, and transmit operations. Require confirmation for irreversible actions.**

---

## Connections

- [The Read-Only Tool](read-only-tool.md) — read operations separated to prevent accidental state changes
- [The Idempotent Tool](idempotent-tool.md) — state-changing tools should be idempotent to handle retries safely
- [The Tool Manifest](../capability/tool-manifest.md) — state-changing tools require explicit authorization in the manifest
- [Human-in-the-Loop Gate](../coordination/human-gate.md) — irreversible state changes may require human confirmation
- [Audit Trail](../observability/audit-trail.md) — every state change is logged as an auditable event
- [Design for Reversibility](../../theory/04-reversibility-as-design-dimension.md) — the reversibility of each tool determines its oversight tier
