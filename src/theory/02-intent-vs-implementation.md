# Pattern 2.2 — The Intent-Implementation Boundary

**Part II: Theory of Intent Engineering** · *2 of 6*

---

> *"If you fix the code when something goes wrong, you are an implementer. If you fix the spec, you are an intent engineer."*

---

## Context

You are working in a spec-driven system and something has gone wrong. An agent produced incorrect behavior. A system does not satisfy its users. A test passes but the outcome is wrong. Before you can fix it, you need to diagnose it — and the most important diagnostic question is: **was the problem in the intent or in the implementation?**

This pattern introduces the most fundamental distinction in intent engineering: the difference between *what a system is trying to do* and *how it does it*. This distinction sounds obvious. It is not. Teams collapse it constantly — and the collapse is the source of most of the chronic dysfunction that SDD is designed to cure.

This pattern assumes [Intent Engineering as a Discipline](01-what-is-intent-engineering.md).

---

## The Problem

In traditional software development, intent and implementation were tightly coupled. The specification was informal, the code was the real artifact, and the developer's judgment was the bridge between them. When something went wrong, the developer held both sides of the problem simultaneously. They could tell, through experience and institutional knowledge, whether the problem was a mistake in the code or a mistake in the understanding of what the code should do.

In agent-mediated development, this coupling breaks. The agent holds the implementation. The human holds the intent. When the output is wrong, the question of *which side is broken* is now an explicit decision that must be made deliberately.

If you cannot tell the difference between an intent failure and an implementation failure, you will fix the wrong thing almost every time:
- **Fixing the code when the spec is wrong** produces correct implementation of wrong intent, which will fail again in a different way
- **Fixing the spec when the code is wrong** produces a more elaborate description of the same failure, which the agent will faithfully implement
- **Both together, without distinguishing them**, produces confusion that compounds across iterations

The inability to systematically distinguish intent from implementation is the hidden cause of most "the agent keeps getting it wrong" complaints.

---

## Forces

- **Coupled history vs. decoupled reality.** Traditional development integrated intent and implementation in one person's judgment; agent systems split these across humans and machines, demanding the ability to diagnose failure origins.
- **Transient code vs. persistent spec.** Code execution is temporary and repeatable; specs are the persistent artifacts governing repeated executions, yet traditional debugging focuses on implementation rather than specification.
- **Speed of fixing code vs. difficulty of fixing intent.** It is faster and more satisfying to patch implementation; acknowledging and fixing spec gaps requires confronting incomplete thinking.

---

## The Solution

### The Definition

**Intent** is *what a system is meant to achieve* — the purpose it serves, the outcomes it must produce, the constraints it must respect, and the criteria by which its behavior will be judged correct or incorrect.

Intent lives in the specification. It is owned by humans. It changes when the understanding of the problem changes, when business requirements evolve, or when validation reveals that what was specified does not match what was actually needed.

**Implementation** is *how a system achieves its intent* — the code, configuration, infrastructure, agent instructions, tool calls, and runtime decisions that produce concrete outputs.

Implementation lives in the code and agent outputs. It is produced (increasingly) by machines. It changes when better techniques are discovered, when performance requirements shift, or when the implementation was simply wrong.

---

### The Diagnostic Test

When something goes wrong in a system involving agents, apply this test before acting:

> **If a perfectly competent agent had executed this spec exactly as written, would the outcome have been correct?**

- If **yes**: the problem is in the implementation. The agent failed to execute the spec correctly. Diagnose and fix the execution, not the spec.
- If **no**: the problem is in the intent. The spec was incomplete, ambiguous, or wrong. Fix the spec first. Then let the agent re-execute.
- If **you can't answer this question**: the spec is too ambiguous to reason about. That is itself an intent failure — a spec that cannot be evaluated against an outcome has not specified anything.

This test is simple. Applying it rigorously is not. It requires being willing to locate the problem in your own specification — in the thing you wrote — rather than in the tool that executed it.

---

### Three Failure Modes That Blur This Distinction

**Over-specified intent**

A spec that describes *how* to implement something has collapsed intent into implementation. It is no longer specifying what to achieve — it is specifying how to achieve it. This is dangerous because it prevents agents from applying better approaches, locks in decisions at the wrong level, and makes the spec brittle: any change in implementation requires rework of the spec.

Signs of over-specification: the spec contains specific library names, class structures, algorithm choices, or file organization. The spec uses the word "use" when it should use the word "ensure."

*Anti-pattern:* "Use a Redis cache with a 5-minute TTL."  
*Correct form:* "Response time for authenticated requests must be under 200ms at p99. Implement caching as appropriate."

**Under-specified intent**

A spec that does not constrain behavior enough to distinguish correct from incorrect implementations. The agent fills the gaps with probability — often producing something that looks plausible and is wrong in subtle ways.

Signs of under-specification: the spec contains words like "appropriate," "as needed," "handle edge cases," or "follow best practices" without defining what those mean in this context. The spec has no success criteria. The scope section is empty.

*Anti-pattern:* "Build a user authentication system following security best practices."  
*Correct form:* "Users must authenticate via OAuth 2.0. Sessions must expire after 30 minutes of inactivity. Failed login attempts must be rate-limited to 5 per minute per IP. Do not implement username/password authentication."

**Intent drift**

A spec that was correct at time of writing but has not been updated when the problem changed. The implementation may be a faithful execution of the original intent — but the original intent is no longer what is wanted.

Intent drift is the most insidious failure mode because the system is behaving as specified, which makes it hard to identify as a spec problem. The diagnostic: if the system does exactly what it was told to do, and that is still wrong, the spec needs to change.

---

### The Hierarchy of Fixes

This distinction establishes a strict hierarchy for how to respond to failures:

```
Something is wrong
│
├─ Is the spec ambiguous or incorrect?
│   └─ YES → Fix the spec first. Always. Then re-delegate.
│
└─ Is the spec correct but the agent failed to execute it?
    └─ YES → Debug the execution.
              Is this a systematic agent failure?
              ├─ YES → Improve context, constraints, or archetype selection
              └─ NO  → Isolated failure; correct the output, document the case
```

The rule at the top of this hierarchy is sometimes called the **spec-first discipline**: when something is wrong, the spec is the first thing you look at — not the code. This rule feels counterintuitive to engineers trained in implementation-first thinking. It requires rewiring.

---

### Why This Matters for Agent Systems Specifically

In human development teams, collapsing intent and implementation had a natural corrective mechanism: the developer who understood both could bridge the gap. The "implementation" always contained implicit intent — the developer's tacit judgment about what was really needed.

Agents do not carry tacit judgment. They execute the spec with high fidelity and without the compensatory reasoning that human developers applied. This means that **the quality of the intent is now directly proportional to the quality of the implementation** — far more directly than it ever was with human developers.

This is the reason for the rule "fix the spec, not the code." Fixing the code without fixing the spec means the next execution will repeat the mistake. The spec is the persistent artifact. The implementation is transient.

---

### A Note on Shared Understanding

One underappreciated dimension of this distinction is its role in team communication.

When an implementation team and a product team disagree about whether a system is working correctly, they are almost always in an implicit argument about intent vs. implementation — they just do not have the vocabulary to name it.

"The agent is doing it wrong" (implementation claim) and "no it isn't, that's not what we asked for" (intent claim) are not the same disagreement. Confusing them produces conversations where everyone is right from their own frame and nothing gets resolved.

Having explicit vocabulary for this distinction — and a shared diagnostic process — turns ambiguous conflict into solvable problems.

---

## Resulting Context

After applying this pattern:

- **Intent failures become explicitly recognizable.** A diagnostic test reveals whether a failure originated in the specification or execution, enabling targeted fixes that address root cause rather than symptoms.
- **Specs stabilize while implementations iterate.** The spec becomes the control artifact governing multiple implementation attempts; implementing agents can be corrected, replaced, or improved without touching the persistent intent layer.
- **Teams gain shared diagnostic language.** Disputes about system correctness shift from blame attribution ("the agent is wrong") to shared problem-solving ("the spec needs to be clarified").

---

## Therefore

> **Intent and implementation are distinct artifacts with distinct owners, distinct failure modes, and distinct fixes. When something goes wrong, the first diagnostic question is always: was the spec correct? If yes, fix the execution. If no — or if you cannot answer the question — fix the spec first. The spec is the persistent artifact. The implementation is its shadow.**

---

## Connections

**This pattern assumes:**
- [Intent Engineering as a Discipline](01-what-is-intent-engineering.md)

**This pattern enables:**
- [Three Dimensions of Delegation](03-agency-autonomy-responsibility.md) — who decides what in each layer
- [The Spec as Control Surface](../sdd/02-specs-as-control-surfaces.md) — the mechanism by which intent controls implementation
- [The Spec Lifecycle](../sdd/03-spec-lifecycle.md) — how intent and implementation evolve together
- [The Living Spec](../sdd/06-living-specs.md) — the fix-the-spec discipline in practice
- [Intent Review Before Output Review](../operating/05-reviewing-intent.md) — applying this distinction in review processes

---

*Next: [Three Dimensions of Delegation](03-agency-autonomy-responsibility.md)*

