# Escalation Chain

---

> *"When the agent reaches its limit, the request should move up — not out."*

---

## Context

An agent is executing a task and encounters a situation it cannot handle within its authorized scope: a request outside its archetype's authority, an input it doesn't have skills for, a decision it lacks the authorization to make. The task cannot be completed by this agent, but it can be completed by a more capable agent or a human with broader authority.

---

## Problem

Without a defined escalation path, agents either refuse the request (frustrating the user) or attempt to handle it anyway (overstepping their scope). When escalation exists but is unstructured, the escalation target receives a request without context — they must reconstruct what was tried, what failed, and what's needed from scratch.

---

## Forces

- **Scope constraint vs. user frustration**: Keeping agents tightly scoped prevents overreach but frustrates users when requests fall outside scope. Loosening scope increases capability but risks overreach.
- **Escalation latency**: Escalation adds a handoff — from agent to escalation target. Each handoff introduces latency. Real-time systems cannot afford 10-minute escalation delays.
- **Context preservation**: Passing full context preserves information but increases payload size and privacy risk. Dropping context is fast but makes escalation targets start from scratch.
- **Authority chain clarity**: In a multi-tier escalation, who has authority to decide what? If tier 1 escalates to tier 2, and tier 2 escalates to tier 3, is tier 3's decision final or can they escalate further?

---

## The Solution

Declare escalation tiers in the spec. Each tier names the handler, their authority, and what context is passed.

**Escalation structure:**

1. **Each agent's spec declares its escalation path.** When the agent cannot handle a request, it doesn't choose where to escalate — the spec tells it.
2. **Context carries forward.** The escalation package includes: what was requested, what the agent attempted, why it couldn't complete the task, and what decision is needed.
3. **The escalated handler inherits all constraints** from the original spec, unless the handler's own spec explicitly overrides them. Escalation does not mean unconstrained authority.
4. **Escalation is logged** as a named event with the reason and the destination tier.

**Typical escalation tiers:**
- Tier 1: Specialized agent with broader scope
- Tier 2: Human specialist with domain authority
- Tier 3: Manager or policy owner with exception authority

**Example:** A refund processing agent handles standard refunds up to $100. Request: "Customer wants $500 refund due to service failure."

Agent executes:
- Refund amount: $500
- Check: "$500 > maximum authorized ($100)" → Cannot handle
- Escalation trigger: "refund_amount_exceeds_limit"

Escalation context package:
```json
{
  "original_request": "Refund for service failure",
  "customer_id": "CUST_4721",
  "amount_requested": 500,
  "agent_attempted": "Standard refund process",
  "failure_reason": "Exceeds authorization limit of $100",
  "escalation_tier": 1,
  "decision_needed": "Approve exception refund"
}
```

Tier 1: AI refund specialist agent that handles exceptions up to $1000.
- Tier 1 agent checks: "Service failure documented?" → Yes. "Amount <= $1000?" → Yes. → Approves $500 refund.

If Tier 1 had checked "Amount <= $300?", it would escalate to Tier 2: Human specialist (authority up to $5000).

---

## Resulting Context

- **Requests are resolved by the right authority.** Complex cases reach someone who can handle them rather than bouncing or being refused.
- **Context is preserved.** The escalation target doesn't start from scratch.
- **Escalation frequency is measurable.** High escalation rates signal that the agent's scope or skills need expansion.

---

## Therefore

> **Declare escalation tiers in the spec with named handlers and context carry-forward. When the agent cannot complete a task within its authorized scope, it escalates upward with full context — not outward into a void.**

---

## Connections

- [Conditional Routing](conditional-routing.md) — routing directs requests to the right agent initially; escalation handles cases where the initial agent was insufficient
- [Human-in-the-Loop Gate](human-gate.md) — escalation to a human follows the same structured handoff pattern
- [Proportional Oversight](../../agents/06-human-oversight-models.md) — escalation is the oversight mechanism for exception cases
- [Six Failure Categories](../../agents/07-failure-modes.md) — escalation is the appropriate response when the failure exceeds the agent's correction capability