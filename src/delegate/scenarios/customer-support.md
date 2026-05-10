# Delegate in practice — Customer-support agent

**Part 3 · DELEGATE · Scenario 1 of 3**

---

> **v2.0.0-rc1 stub.** Structural placeholder. Prose lands in PR-C. v1.x source: [examples/01-ai-customer-support/agent-instructions.md](../../examples/01-ai-customer-support/agent-instructions.md).

---

## What this chapter will cover

The chapter binds patterns to the customer-support spec written in [Specify in practice — Customer-support agent](../../specify/scenarios/customer-support.md), names the oversight model, and walks through the agent build itself.

Specifically:

- **System prompt and skill files.** What the agent's identity prompt looks like for the Executor governing archetype. How the embedded Advisor and Guardian modes are surfaced to the model (declarative tags vs. tool-shaped boundaries). Skill files for *escalation*, *refund within cap*, *KB lookup*.
- **Tool manifest and capability boundary.** The agent gets `lookup_account` (read-only), `lookup_kb` (read-only), `draft_response` (composition only), `issue_refund_within_cap` (parametric, Guardian-checked), `escalate_to_human` (handoff). It does **not** get a generic shell, file-system access, or write-access to the account record.
- **Patterns bound from Part 4.** Output Validation Gate on every customer-facing message. Sensitive Data Boundary at the response composition step. Rate limiting on the issue_refund tool. Distributed trace spanning the user turn, KB lookup, response composition, and (when present) the escalation hand-off.
- **Oversight model.** **Output Gate** for the first 30 days post-launch, transitioning to **Periodic** review at 30 days conditional on first-pass-validation ≥ 92%. The transition is documented in the spec, not in a side document.
- **The launch readiness check.** The chapter ends with the "is this ready to ship" checklist: spec is written and reviewed, tool manifest matches §3 / §4, oversight model is wired up, the four signal metrics are emitting, the rollback plan is documented.

## Reading path through this scenario

| Phase | Chapter |
|---|---|
| 1. Frame | [Frame in practice — Customer-support agent](../../frame/scenarios/customer-support.md) |
| 2. Specify | [Specify in practice — Customer-support agent](../../specify/scenarios/customer-support.md) |
| 3. **Delegate** | *(this chapter)* |
| 4. Validate | [Validate in practice — Customer-support agent](../../validate/scenarios/customer-support.md) |
| 5. Evolve | [Evolve in practice — Customer-support agent](../../evolve/scenarios/customer-support.md) |

## Conceptual chapters this scenario binds to

- [Proportional Oversight](../../agents/06-human-oversight-models.md)
- [Least Capability](../../agents/04-tools-mcp-capability-boundaries.md)
- [Output Validation Gate](../../patterns/safety/output-validation-gate.md)
- [Sensitive Data Boundary](../../patterns/safety/sensitive-data-boundary.md)

## Source material

v1.x agent instructions: [examples/01-ai-customer-support/agent-instructions.md](../../examples/01-ai-customer-support/agent-instructions.md).
