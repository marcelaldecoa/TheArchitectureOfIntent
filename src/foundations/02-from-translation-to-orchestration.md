# Pattern 1.2 — From Translation to Orchestration

**Part I: Foundations** · *Pattern 2 of 6*

---

> *"You are no longer handing instructions to a junior developer. You are briefing a tireless, literal, fast collaborator who will execute exactly what you describe — and nothing more."*

---

## Context

You have accepted that the human compiler role has shifted (see [Pattern 1.1](01-end-of-human-compiler.md)). Now the question is: what has replaced it? What is the actual work that a skilled engineer, architect, or technical leader does in an agent-enabled world?

The temptation is to think of the change as acceleration — the same work, done faster. This is the mistake that causes teams to get inconsistent results, lose architectural coherence, and blame tools rather than framing.

---

## The Problem

If code is no longer the bottleneck, and agents are producing the code, what exactly is the new work?

The answer requires a precise term: **orchestration**.

Translation was the old work: taking a human specification and converting it into machine instructions. This was a one-way, sequential activity. Intent went in; code came out. The human was the bridge.

Orchestration is different in three ways:

1. **It is multi-party.** The engineer, the agent, the system, and the user are all actors. Orchestration means arranging these actors so that each does what they are best suited for.

2. **It operates at the level of goals, not instructions.** A translator specifies *how* to do something. An orchestrator specifies *what* to achieve, *under what constraints*, and *how success will be measured*. The implementation is delegated.

3. **It includes oversight as a first-class responsibility.** Translation is done when the code is written. Orchestration includes the feedback loop: reviewing outcomes, correcting intent, refining constraints when the system diverges from what was meant.

---

## The Resolution

The new model looks like this:

```
Business Intent
      ↓
Explicit Specification + Context
      ↓
Agent Execution (code, tests, docs, infra)
      ↓
Human Oversight & Correction
      ↓
Refined Specification (living artifact)
```

Notice what the human owns in this model: **the top and the bottom of the loop**. Intent origination and outcome validation are irreducibly human functions. Everything in the middle — the mechanical execution of well-specified work — is what agents are for.

This is not a demotion. It is a clarification.

The engineer's new primary skills are:

**Problem framing** — The ability to decompose a vague business need into a precise, solvable statement. *What are we actually building? What is the real problem? What would wrong look like?*

**Constraint design** — The ability to identify and articulate the non-negotiables: the things that must never happen, the boundaries that may not be crossed, the invariants that must hold. Constraints are not limitations — they are the expression of judgment encoded in advance.

**Context provision** — Agents do not carry institutional memory. The engineer's job includes ensuring that relevant context — architectural decisions, past failures, business rules, regulatory requirements — is made explicit in the specification rather than assumed.

**Outcome validation** — When an agent produces a result, the human must evaluate it not against the code, but against the intent. Does this satisfy the goal? Does it respect the constraints? Is there something the spec failed to anticipate?

These are not new skills. They are old skills, applied at a new level of importance.

---

## From "How" to "What" and "Why"

The practical shift in daily work:

**Old question:** "How do I implement this?"

**New questions:**
- "What outcome am I actually trying to produce?"
- "What context must always be present for this to be correct?"
- "What constraints prevent the known failure modes?"
- "What feedback loop keeps this on track?"
- "What does done mean, verifiably?"

A helpful frame: you are not writing a program. You are **briefing a collaborator**. The brief must be:
- Complete enough that the collaborator can act without guessing
- Constrained enough that they cannot accidentally exceed their authority
- Specific enough that you can tell when the outcome is correct

This is a different skill from implementation, and it requires deliberate practice to develop.

---

## The Failure Mode: Treating Agents as Fast Interns

The most common failure of teams in this transition is treating agents as "faster interns" — giving them informal prompts, correcting output manually, iterating at the level of code rather than spec.

This pattern is seductive because it produces visible progress quickly. But it is not orchestration. It is manual correction of under-specified delegation. The agent is not the problem; the spec is.

Teams operating this way will find that:
- Results are inconsistent across runs
- Architectural coherence degrades over time
- "Correcting" the agent creates debt that compounds
- Senior engineers are spending time on mechanical corrections rather than judgment

The fix is always more upstream: fix the spec, not the output.

---

## Therefore

> **The engineer's role has shifted from translator to orchestrator. The work is now: frame the problem precisely, design the constraints that make delegation safe, provide the context that makes execution reliable, and validate outcomes against intent. Implementation is delegated. Judgment is not.**

---

## Connections

**This pattern assumes:**
- [The End of the Human Compiler](01-end-of-human-compiler.md)

**This pattern enables:**
- [Authorship in Software](03-authorship-in-software.md) — who is responsible when machines act on your orchestration
- [What Spec-Driven Development Really Means](../sdd/01-what-sdd-means.md) — the method that makes orchestration systematic
- [Agents as Executors of Intent](../agents/03-agents-as-executors.md) — how agents fit in the orchestration model
- [Writing Specs for Agents, Not Humans](../sdd/05-writing-specs-for-agents.md) — the practice of writing briefs for machine collaborators

---

*Next: [Authorship in Software](03-authorship-in-software.md)*
