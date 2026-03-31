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

## The Solution

Declare the **maximum scope of effect** in the spec. If the agent fails in the worst possible way, the damage is bounded by these declarations.

1. **Bounded data access.** The agent can only read/write declared data scopes. A failure cannot affect databases or tables outside the scope.
2. **Bounded user impact.** "This agent serves requests from users in [segment]. It cannot access data or take actions affecting users outside this segment."
3. **Bounded action scope.** "Maximum refund amount: $100. Maximum messages sent per execution: 1. Maximum records modified per execution: 10."
4. **Bounded temporal scope.** Rate limits and execution timeouts prevent a runaway agent from operating indefinitely.
5. **Kill switch.** A mechanism to immediately halt the agent — not graceful shutdown, but immediate cessation of all tool calls and output.

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
