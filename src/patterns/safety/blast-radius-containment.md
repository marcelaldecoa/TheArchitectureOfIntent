# Blast Radius Containment

---

> *"If the agent fails catastrophically, how much damage can it do? That's the blast radius. Design it before deployment."*

---

## Context

An agent system is deployed in production with access to real systems, real data, and real users. Despite spec constraints and oversight, catastrophic failure is possible — a constraint bypassed, a tool misused, a cascading error.

---

## Problem

Without declared boundaries on maximum impact, a catastrophic agent failure affects everything the agent can reach — every database it can write to, every API it can call, every user it can message. The blast radius is the full extent of the agent's capability, not just the scope of the current task.

---

## Forces

- **Capability and blast radius are coupled**: The tools the agent needs for legitimate work are the same tools that could cause harm if misused. Restricting tools limits harm but may cripple the agent.
- **Failures are often cascading**: A single bug or constraint violation doesn't cause isolated damage; it triggers downstream failures that multiply the impact.
- **Detection lag**: By the time a catastrophic failure is detected (monitoring alert, user report, log review), damage may already be extensive. Recovery is harder than prevention.
- **Authorization creep**: Over time, agents gain access to additional tools and data scopes as new requirements arise. Without periodic blast radius review, the authorized scope grows unbounded.

---

## The Solution

Declare the **maximum scope of effect** in the spec. If the agent fails in the worst possible way, the damage is bounded by these declarations.

1. **Bounded data access.** The agent can only read/write declared data scopes. A failure cannot affect databases or tables outside the scope.
2. **Bounded user impact.** "This agent serves requests from users in [segment]. It cannot access data or take actions affecting users outside this segment."
3. **Bounded action scope.** "Maximum refund amount: $100. Maximum messages sent per execution: 1. Maximum records modified per execution: 10."
4. **Bounded temporal scope.** Rate limits and execution timeouts prevent a runaway agent from operating indefinitely.
5. **Kill switch.** A mechanism to immediately halt the agent — not graceful shutdown, but immediate cessation of all tool calls and output.

**Example:** A customer refund agent is deployed with:
- Data access: Only `customer_refunds` table, user segment: "North America"
- Action limits: Maximum $500 refund per execution, maximum 1 refund per task, maximum 60-second execution time
- Kill switch: An operator can invoke a "halt_agent()" command that stops all in-flight calls immediately

If the agent malfunctions and enters a retry loop, the blast radius is 1 incorrect $500 refund (not 100), affecting 1 user (not the entire customer base), with a hard stop at 60 seconds (not indefinite execution).

---

## Resulting Context

- **Maximum impact is bounded and measurable.** Even in catastrophic failure, the damage cannot exceed the declared limits.
- **Recovery is scoped.** The operations team knows exactly what needs to be remedied: affected user segment, transaction amount, time window.
- **Designer accountability is clear.** The spec author declares blast radius; they own the tradeoff between capability and safety.
- **Kill switch provides last-resort control.** When detection is too slow, manual intervention can halt the agent mid-execution.

---

## Therefore

> **Declare the maximum scope of effect before deployment: which data, which users, which actions, with what limits. Design the blast radius to be the smallest containment that still allows the agent to do its job. Include a kill switch.**

---

## Connections

- [The Tool Manifest](../capability/tool-manifest.md) — the manifest bounds tool access; blast radius bounds impact
- [Rate Limiting](rate-limiting.md) — rate limits are a temporal blast radius constraint
- [Session Isolation](../state/session-isolation.md) — isolation prevents cross-user blast radius
- [Code Execution Sandbox](../integration/code-sandbox.md) — the sandbox is a blast radius boundary for generated code
- [Design for Reversibility](../../theory/04-reversibility-as-design-dimension.md) — reversible actions have smaller effective blast radius