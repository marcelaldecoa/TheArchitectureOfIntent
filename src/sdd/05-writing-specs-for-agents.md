# Writing for Machine Execution

**Specification**

---

> *"If you can't specify it, you don't understand it well enough yet."*

---

## Context

You know what a spec needs to contain and how it functions as a control surface. Now you are sitting down to write one. The blank page presents the same challenge it always does — but with a new constraint: your primary reader is not a human colleague. It is an agent that will execute against your words without asking for clarification, without applying professional judgment, and without reading between the lines.

Writing for an agent requires different craft than writing for a human. This pattern describes the specific differences.

This pattern assumes all preceding SDD patterns and [Four Dimensions of Governance](../architecture/03-archetype-dimensions.md).

---

## The Problem

Most technical writers — including experienced engineers — have internalized that their audience is human. Human readers tolerate ambiguity, resolve contradictions using context, ask questions when confused, and apply tacit knowledge that was never written. Professional communication is full of compressed meaning that expert readers expand correctly.

Agents do not do any of this. They execute the literal text. Ambiguity produces arbitrary resolution. Contradiction produces unpredictable behavior. Missing context produces questions, hallucinations, or failures. Tacit knowledge that wasn't written doesn't exist.

This is not a limitation to be engineered around. It is a clarifying property: **writing for agents reveals what was actually imprecise in your thinking.** The places where you struggle to write a clause that an agent could follow without asking questions are exactly the places where a human colleague would have silently applied their own judgment — judgment that might not match yours.

The discipline of writing for agents closes the gap between what you intended and what you expressed. It makes implicit decisions explicit, which makes them reversible, auditable, and transferable.

---

## Forces

- **Natural language vs. formal specification.** Natural language is expressive but ambiguous. Agents need precision but teams want readability. The spec must bridge both.
- **Expert knowledge vs. explicit knowledge.** Domain experts have mental models of what should be done. Encoding that knowledge explicitly is work. Yet it is the only way the knowledge transfers to an agent.
- **Completeness vs. brevity.** Adding detail makes specs more correct but longer. The spec must be minimal yet complete enough for execution without questions.
- **Inspiration vs. direction.** Some teams use specs to inspire creativity. Agents cannot work from inspiration; they need direction.

---

## The Solution

### Principle 1: Specify WHAT and the constraints, never HOW

A spec specifies observable outcomes, not implementation paths.

**Weak (specifies how):**
> The system should use a caching layer to optimize performance. Use Redis with a 5-minute TTL on user profile lookups.

**Strong (specifies what and constraint):**
> User profile data must be returned in under 100ms at P95 for authenticated requests. The solution must not require a database hit on every request for data unchanged in the last hour.

The first version locks an implementation. It will be followed literally — the agent will use Redis with a 5-minute TTL even if caching is not the right solution, or if the TTL should be different for different use cases. The second version constrains what must be true while leaving the implementation open. The agent can choose the best approach; you can evaluate whether the constraint was met.

The forcing question: *Am I specifying what the system must do, or am I specifying how I would implement it?*

---

### Principle 2: Name every constraint explicitly

Agents do not infer constraints from adjacent context. A human reading "this system processes medical records" immediately applies their knowledge of HIPAA, data handling standards, and the general sensitivity of the domain. An agent applies what you wrote.

Write the constraints. All of them.

**Missing constraint:**
> The system processes patient medication schedules and sends reminders.

**Explicit constraints:**
> The system processes patient medication schedules and sends reminders.
> 
> **Constraints (non-negotiable):**
> - No patient data is stored beyond the active session; only medication schedule IDs are persisted
> - Reminder messages must not include medication names or dosage details — only appointment times
> - System errors visible to patients must never include technical detail or data references
> - All outbound messages require a confirmed opt-in on record before dispatch

Each of these would be obvious to a domain expert. An agent is not a domain expert unless you make it one — in the spec.

---

### Principle 3: Write success criteria that can be tested without you

Acceptance criteria in a spec are not a description of what good looks like. They are a set of verifiable conditions that, if all true, constitute success.

**Not testable:**
> The interface should be intuitive and responsive.

**Testable:**
> - All primary user actions (create, edit, delete, submit) complete within 2 seconds for datasets up to 1000 records
> - On any page, a user who has not seen the product before can identify the primary action within 30 seconds (validated via usability review with 3+ test users)
> - No action requires more than 3 steps from the main navigation

The test for a good acceptance criterion: *Could a person who has never spoken to me determine whether this criterion was met by examining the output?* If yes, it is a good criterion. If no, it needs to be rewritten.

---

### Principle 4: State the invariants separately from the behaviors

Invariants are constraints that are always true, under all conditions, regardless of other decisions an agent might make. They are different from non-functional requirements (which may have acceptable degradation) and different from acceptance criteria (which describe success on the primary path).

Invariants are non-negotiable, unconditional, and frequently the clauses that an agent will silently violate if they are only implied.

Write invariants as their own section. Use absolute language.

**Behavioral requirement (can be traded off):**
> The system should retry failed API calls up to 3 times.

**Invariant (cannot be traded off):**
> The system must never send a user-facing message that contains raw exception text, stack traces, or internal error codes.

The first requirement can be loosened under certain conditions. The second cannot. Agents make decisions about requirements; they must obey invariants. If you write them in the same section with the same tone, the agent will treat them with equal discretion.

---

### Principle 5: Write agent execution instructions as a direct address

The agent execution section of the spec is not documentation about what the agent will do. It is a direct instruction to the agent. Write it in second person, imperative.

**Documentation voice (not direct):**
> The agent will generate source code based on the functional intent above. It should avoid making product decisions and escalate when scope is unclear.

**Direct instruction (effective):**
> **Agent instructions:**
> - You are authorized to: generate source code, generate tests, generate inline documentation
> - You are NOT authorized to: make architectural decisions not specified here, expand scope beyond section 3, resolve open questions in section 8 without surfacing them
> - If you encounter a situation this spec does not cover: stop execution, list the specific gap, and present it for human resolution before continuing
> - If the spec appears to have a contradiction: do not resolve it by choosing one side; surface the contradiction

This distinction matters because agents read documents from the perspective of their role. A section labeled "Agent Instructions" in second-person imperative is read as instructions. A section describing what the agent will do is read as context — and context is lower-priority than instructions.

---

### The Three Anti-Patterns

**Anti-pattern 1: The Vision Document**

Signs: Lofty goals, no scope limits, no acceptance criteria.

*"Build a system that delights customers by providing instant, intelligent answers to their questions."*

An agent executing against a vision document is writing the spec itself — which means it is making all the decisions the spec should have made. The output will be coherent but wrong, because the implicit decisions the agent made are not the ones you would have made.

---

**Anti-pattern 2: The Implementation Prescription**

Signs: Specific technology choices, class names, function signatures, data structures not derived from constraints.

*"Create a class called `UserSessionManager` with a method `invalidateSession(userId: string)` that calls the Redis client to delete the key `session:{userId}`. Use LRU eviction with a max of 10,000 keys."*

An agent executing against an implementation prescription is a transcription service. It will follow the instructions, produce exactly what was specified, and miss any better approach the agent would have found if given the freedom to. More practically: the output is predetermined, so why involve an agent at all?

---

**Anti-pattern 3: The Conversation Transcript**

Signs: Context that builds over many paragraphs, references to "we discussed" or "as mentioned above," requirements that only make sense in context of preceding paragraphs.

A spec must stand alone. It will be read by an agent — and by future humans — who were not present for the conversation that produced it. Every decision in the spec should be self-evidently justified within the spec. If it requires context that isn't in the spec, put the context in the spec.

---

### The Quality Signals

A spec ready for agent execution shows these properties:

- [ ] Can be handed to someone who wasn't involved in writing it and used immediately
- [ ] Has no acceptance criteria that requires the author to explain it
- [ ] Has explicitly stated invariants distinct from requirements
- [ ] States scope out-of-bounds explicitly, not just what's in-scope
- [ ] Has agent execution instructions in direct, second-person imperative
- [ ] Has an archetype declaration (for agent systems)
- [ ] Contains no implementation choices not derived from stated constraints

A spec that passes this checklist is machine-executable. A spec that fails it will require conversation during execution — which collapses SDD back into prompt engineering.

---

## Resulting Context

After applying this pattern:

- **Imprecision becomes visible.** Writing for agents reveals where human communication relies on impression and judgment. Making this explicit allows deliberate decisions about what to specify vs. delegate.
- **Requirement clarity improves.** Specs written for agents often end up clearer for other humans too.
- **Validation becomes independent.** A spec written precisely enough for an agent can be validated by someone who was not involved in writing it.
- **Reuse becomes possible.** A clear, complete spec can be run again months later, by a different agent, and produce an equivalent outcome.

---

## Therefore

> **Writing for agents requires specifying WHAT and constraints, never HOW; naming every constraint explicitly that a human expert would know but an agent would not; writing acceptance criteria that can be tested without the author present; stating invariants as a separate unconditional section; and writing agent instructions as direct second-person imperatives. The anti-patterns — vision documents, implementation prescriptions, and conversation transcripts — all fail by either under-constraining or over-specifying, leaving the agent to make decisions the spec should have made.**

---

## Connections

**This pattern assumes:**
- [Spec-Driven Development](01-what-sdd-means.md)
- [The Spec as Control Surface](02-specs-as-control-surfaces.md)
- [The Intent-Implementation Boundary](../theory/02-intent-vs-implementation.md)

**This pattern enables:**
- [The Canonical Spec Template](07-canonical-spec-template.md) — every section in the template was designed for this reading audience
- [Spec Template Library](../repertoires/03-spec-template-library.md)

---
