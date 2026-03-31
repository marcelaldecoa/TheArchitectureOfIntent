# Constitutional Archetypes

**Governance & Architecture**

---

> *"A constitution does not tell you what to do in every situation. It tells you what kind of system you are — and what you are not permitted to become."*

---

## Context

Part II gave us a vocabulary: intent, implementation, agency, autonomy, responsibility, reversibility, failure signal, moral weight. We can now reason precisely about what a delegated system *is*.

The question Part III answers is: **how do we make those decisions durable?**

The problem is not that experienced practitioners don't know how to design good agent systems. Many do. The problem is that their knowledge is tacit, personal, and non-transferable at scale. When a team grows, when engineers are onboarded, when an agent generates code at 3am with no human in the loop — the accumulated judgment of experienced practitioners is not present.

Archetypes are the solution. They are the mechanism by which accumulated judgment becomes **encoded law**: persistent, transferable, and enforceable without requiring a senior practitioner to be in the room.

This chapter establishes why archetypes should be understood as **constitutional** structures — not stylistic suggestions, not best practices, not guidelines. Constitutional law.

**A note on enforcement.** The constitutional analogy is deliberate and useful, but it has a limit worth naming. Real constitutional law has enforcement mechanisms: courts, judicial review, separation of powers. Archetypes, as described here, are enforced through organizational discipline — spec review processes, governance cadences, authority matrices — not through technical mechanisms that prevent violations at runtime. An agent system can technically take actions outside its declared archetype; nothing in the runtime prevents it. The enforcement is procedural and social. This is not a weakness to be apologized for — it is the same model by which most organizational governance operates. But it means that archetypes are only as strong as the review and oversight practices that surround them. The governance calendar and spec approval processes in Part VII exist precisely to make this enforcement operational.

---

## The Problem

Every architecture decision starts with intent. But intent is ephemeral. It lives in the mind of the person who designed the system. It deteriorates through conversation, through documentation written once and forgotten, through team turnover, through the accumulation of small implementation decisions that individually seem harmless but collectively drift away from the original frame.

In human-paced development, this drift is visible. Code reviews catch it. Architects notice it. Senior engineers push back. The feedback loop, though slow, operated.

In agent-mediated development, drift happens faster and more quietly. An agent generates code that seems reasonable in isolation but violates an architectural principle that was decided eighteen months ago in a conversation no one documented. Another agent adds a new capability that crosses a boundary that "everyone knows" exists but that no one encoded. A system that started as an advisor gradually acquires executor behaviors through incremental feature additions — none of which individually seemed like a category change.

**Without constitutionalized architecture, agent systems drift away from their original frame at the speed of agent execution.**

---

## Forces

- **Preserving intent vs. enabling scale.** Individual judgment is reliable at small scale but does not distribute. Scaling requires encoding judgment as durable rules that operate independently of whether the original architects are in the room.
- **Stability vs. responsiveness.** Systems need to respond to new requirements, but every small locally-reasonable decision can compound into architectural drift. Pre-commitment constrains flexibility to protect coherence.
- **Tacit knowledge vs. transferable authority.** Expert practitioners carry mental models of why systems work; junior engineers and agents lack this context. Making judgment explicit through constitutionalized rules makes authority transferable.
- **Technical convenience vs. categorical integrity.** At any point, a locally optimal technical choice might cross an architectural boundary. Without constitutional constraint, these choices accumulate until the system has drifted into a different category than it was designed to be.

---

## The Solution

### What a Constitution Does

A constitutional system — whether political or software — does four things:

1. **It defines what kind of system this is.** Not what it does today, but what category of actor it is. This is the difference between "a system that sends notifications" (behavioral description) and "an advisor-class system that surfaces information without taking autonomous action" (constitutional description).

2. **It establishes what the system is not permitted to become**, regardless of what might be technically convenient or locally optimal. Constitutions exist precisely because individual decisions, each seemingly reasonable, can compound into something that violates the founding principles. The constraint exists ahead of the decision.

3. **It distributes authority.** A constitution says who is allowed to decide what. Not everything can be changed by anyone. Some decisions — the ones closest to the core principles — require a higher threshold: more authority, more deliberation, more consensus.

4. **It provides interpretive authority** for decisions not explicitly covered. A constitutional description of an archetype tells a practitioner (or an agent) how to reason about a novel situation that the original authors did not anticipate. "Given that this is a Guardian-class system, how should we handle this edge case?" is a question with a frame for an answer.

All four of these functions are exactly what archetypes provide for agent system design.

---

### Why "Best Practices" Fails

Before naming what archetypes are, it is worth naming what they are not — because the category confusion is common.

**Archetypes are not best practices.** Best practices are advisory: "here are patterns that work well." They can be followed or ignored based on context and judgment. They require a skilled practitioner to decide when they apply. They do not bind anyone.

**Archetypes are not patterns** in the classic Gang-of-Four sense. A design pattern describes a solution to a recurring implementation problem. It is applied at the level of code structure. An archetype describes a governance frame for an entire class of system. It is applied at the level of authorization, oversight, and accountability.

**Archetypes are not templates.** A template is a starting structure that is adapted. An archetype is a constraint set that is respected. You fill in a template. You operate within an archetype.

The distinction matters because the difference between advisory and binding determines whether the protection works. A best practice that can be ignored when a deadline is tight offers no protection when the stakes are highest — precisely the moment when the protection matters most.

---

### The Anatomy of an Archetype

An archetype formally defines five things:

**1. Identity**
What kind of system this is at the categorical level. The identity is a name that carries meaning — Advisor, Executor, Guardian, Synthesizer, Orchestrator — and a precise description of what that identity entails.

**2. Agency Level**
The range of discretion the system is authorized to exercise. Expressed as: what classes of decision can the system make autonomously?

**3. Oversight Model**
How human oversight is required to function for this class of system. Not "some oversight" but: what kind, at what frequency, triggered by what conditions, performed by whom?

**4. Reversibility Posture**
What is the reversibility profile of this system's actions, and what design requirements follow from that? A system with irreversible action potential has a different minimum design standard than one without.

**5. Invariants**
The constraints that cannot be violated under any implementation of this archetype. These are the constitutional clauses — the things that define the boundary between "still this kind of system" and "something that has crossed into a different category."

---

### Pre-commitment as the Core Mechanism

The reason archetypes work as constitutional law is that they are **pre-commitments** — decisions made before the pressure to compromise them exists.

This is a well-studied principle. Humans are better at making ethical decisions in the abstract (when stakes are low and the decision is hypothetical) than in the moment (when there is time pressure, cost pressure, and a specific face asking for an exception). The same applies to organizations.

When an archetype is defined — when a governance body says "all customer-facing AI systems in this organization are constrained to Advisor or limited-Executor behavior" — that decision is made in a deliberate setting by the right people. When a product manager subsequently asks to give the system more autonomy over a specific decision "just for this release," the answer is already known. Not because someone is being rigid, but because the principle was expressed, reasoned about, and pre-committed.

Pre-commitment does not eliminate the ability to change the rules. It requires that changes go through the same deliberate process that created them. This is not bureaucracy — it is the mechanism that prevents drift.

---

### The Relationship Between Archetypes and Specs

Archetypes and specs are different artifacts with different owners and different lifetimes:

| | Archetype | Spec |
|---|---|---|
| **Defines** | The category of system | The behavior of this system |
| **Owner** | Principals / Architects | Engineers / Product teams |
| **Lifetime** | Stable; changes rarely, deliberately | Living; evolves with the system |
| **Scope** | Applies to all systems of this class | Applies to one system |
| **Authority** | Constitutional — cannot be overridden by individual spec | Operational — expresses intent within archetype bounds |

A spec that attempts to authorize behavior that violates the governing archetype is constitutionally invalid. This is not a technical constraint — it is an organizational one. The archetype represents decisions made by those with the authority to make them. The spec operates within that frame.

In practice, this relationship means that the archetype selection is the first decision in any spec development process — before any behavioral specification is written. Getting the category right is more important than getting any specific behavior right, because all specific behaviors must remain consistent with the category.

---

## Resulting Context

After applying this pattern:

- **Durable intent at agent speed.** The original frame of a system persists through agent-mediated execution. Individual decisions that would otherwise drift the system are bound by pre-committed category constraints.
- **Authority distributes without ambiguity.** Different people can make different system decisions without requiring consensus or architectural review, because the constitutional boundaries establish what kinds of decisions each person is authorized to make.
- **Evolution becomes visible.** When a system must evolve beyond its original archetype, the change is deliberate — it goes through the same governance process that created the original classification, rather than accumulating silently.
- **Judgment becomes code.** The accumulated judgment of experienced architects that was previously tacit and lost to team turnover is now encoded in archetype specifications — persistent, teachable, and enforceable.

---

## Therefore

> **Archetypes function as constitutional law for agent systems: they pre-commit the category of system, the scope of authorized agency, the required oversight model, and the invariants that cannot be violated — before any individual system is designed. They make accumulated judgment durable, protect against drift at agent execution speed, and provide interpretive authority for cases the original authors did not anticipate. Understanding this is prerequisite to using them well.**

---

## Connections

**This pattern assumes:**
- [Why Architecture Must Become Law](../foundations/06-why-architecture-must-become-law.md)
- [The Moral Weight of Specification](../theory/06-why-specs-are-moral-artifacts.md)
- [Three Dimensions of Delegation](../theory/03-agency-autonomy-responsibility.md)

**This pattern enables:**
- [The Five Archetypes](02-canonical-intent-archetypes.md) — the five archetypes defined
- [Four Dimensions of Governance](03-archetype-dimensions.md) — the formal axes of variation
- [Delegated Definition Authority](../operating/03-who-defines-archetypes.md) — the governance structure
- [The Intent Archetype Catalog](../repertoires/02-archetype-catalog.md) — the reference library

---
