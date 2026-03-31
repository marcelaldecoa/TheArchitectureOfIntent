# Pattern 4.2 — The Spec as Control Surface

**Part IV: Spec-Driven Development** · *2 of 7*

---

> *"A constitution is not a description of government. It is the mechanism that constrains government. The description is history. The constraint is law."*

---

## Context

You have adopted the discipline of writing specs before agent execution. Specs exist. Agents use them. But the team still experiences drift — the spec was followed in letter but not in spirit, or the scope widened incrementally without the spec catching it, or a new version of the agent behaved differently against the same spec.

Something is missing. The specs exist as documents, but they are not functioning as control mechanisms. They are being read, not enforced.

This pattern assumes [Spec-Driven Development](01-what-sdd-means.md) and [Constitutional Archetypes](../architecture/01-archetypes-as-constitutional-law.md).

---

## The Problem

The most common failure in SDD adoption is treating specs as documentation rather than as control surfaces.

A control surface is something you can act on to change the behavior of a system. A cockpit's controls are not a description of where the plane should go — they are the mechanisms by which the pilot's intent becomes the plane's behavior. Remove a control surface and the intent still exists; it just has no effect.

A spec functions as a control surface when:
- It is consulted before execution begins
- Its clauses are evaluated during validation
- Violations of it trigger a response (either fixing the output or fixing the spec)
- It changes when the intent changes — not after the implementation changes

A spec ceases to function as a control surface when:
- It is written and then not consulted during execution
- Validation consists of human aesthetic judgment rather than spec-conformance checking
- Violations of it are corrected directly in the output without updating the spec
- The implementation evolves and the spec is updated afterward to match

The second pattern looks like SDD. It produces documents that resemble specs. But the spec is not controlling anything — the human is, using the spec as a post-hoc rationalization. The agent is not being constrained by the spec; it is being directed by prompts and corrected by inspection. This is prompt engineering with a document attached.

The distinction matters because the benefits of SDD come specifically from the spec functioning as a control surface. Reusability requires a stable spec that can be run again. Audibility requires a spec that was actually enforced. Organizational learning requires that failures get encoded into the spec, not just corrected in the output.

---

## Forces

- **Documentation vs. mechanism.** A spec can describe what a system should do or control what it does. The distinction is clear in principle but easy to slip on in practice.
- **Constraint vs. preference.** Specs must constrain behavior that matters while teams tend to enforce preference. The spec's authority gets divided between non-negotiable and negotiable, weakening both.
- **Precision vs. readability.** A control surface requires precise, testable language. Making specs precise enough to control agent behavior makes them harder for casual readers.
- **Enforcement vs. trust.** Making a spec a control surface requires that violations be actioned. Without enforcement, the spec documents what should have happened, not what does happen.

---

## The Solution

### What a Control Surface Is

A control surface has three properties:

**1. It is consulted at decision points.**  
The spec is read by the agent at the moment it is executing, not as background context from a conversation. The agent's behavior is directly shaped by the spec's clauses: what it is authorized to do, what it must not do, what it should produce, and what constitutes success. This requires that the spec be structured so relevant sections are accessible when the agent needs them — not buried in prose that requires interpretation.

**2. It is checked at validation points.**  
A human (or a validation agent) explicitly checks the output against the spec. Not "does this look right?" but "does this satisfy clause 6.2? Does it violate invariant 3?" The spec has sections that map to checkable questions. If the spec is so general that you cannot check a specific violation of it, it is not functioning as a control surface — it is providing cover.

**3. Changes to it change behavior.**  
When a spec clause is tightened, the next execution should produce different output. When a scope boundary is clarified, the next execution should respect that boundary. If you can change the spec and the output doesn't change, the agent isn't reading the spec — it's reading the conversation history, the examples, or making up what seems reasonable.

### The Hierarchy of Control

Specs are not the only control surface in an intent-engineered system, but they are the primary one. The control hierarchy:

```
Constitutional layer    — Archetype definitions (what kinds of systems 
                          we're allowed to build and under what terms)
                                ↓
Spec layer              — Intent specification (what this system must do,
                          must not do, and what success looks like)
                                ↓
Invariant layer         — Non-negotiable constraints (clauses that cannot
                          be overridden by any execution)
                                ↓
Execution layer         — Agent action (operates within all layers above)
                                ↓
Validation layer        — Human verification (checks output against spec;
                          feeds back into spec layer)
```

Each layer constrains the one below it. Constitutional law constrains what kinds of specs can be written. The spec constrains what the agent can do. Invariants within the spec constrain even specification updates. Validation checks that execution respected the spec.

When feedback from the validation layer reveals a problem, the fix propagates upward: if the output was wrong because the spec was wrong, the spec changes. If the spec was wrong because the archetype classification was wrong, the classification changes. If the invariant was too restrictive, the invariant changes — but only through the governance process established for that layer.

### Spec Clauses as Control Mechanisms

A spec functions as a control surface through its specific clauses, not its general description. The difference:

**Descriptive (not a control surface):**
> The system should handle errors gracefully and provide useful feedback to users.

**Control surface:**
> **Invariant:** If any external API call returns a non-2xx status, the system must:
> 1. Log the failure with: timestamp, endpoint, status code, correlation ID
> 2. Return a structured error response — not a raw exception
> 3. Not retry more than once
> 4. Never surface raw stack traces to the user interface

The descriptive version is not checkable. The control surface version produces a specific set of tests and a specific set of agent behaviors. You can look at an output and determine, clause by clause, whether it was followed.

The key forcing question when writing a spec clause: *Could I write a test for this?* If you cannot write a test, the clause is not a control surface. It is a preference.

### The Spec Is Not the Only Check

Control surfaces require active use. A spec that exists in a repository but is never consulted during execution or validation has no control effect. The organizational practice around specs matters as much as the spec's content:

- Was the spec consulted at the start of execution? (Input control)
- Was the output validated against the spec, not just reviewed generally? (Output control)
- Did a spec violation trigger a spec update, not just an output patch? (Feedback control)
- Was the spec version known at validation time? (Traceability)

These practices are the organizational infrastructure that makes the control surface work. A spec without these practices is a document. A spec with them is a mechanism.

### The Temporal Contract

A spec establishes a temporal contract: it describes what must be true *at the moment of execution* and *at the moment of validation*. This is different from a living document that logs what happened.

The spec says: "Before this agent runs, these things must be true. After it runs, these things must be verified."

This temporal structure is what makes specs reusable. The same spec can be run again tomorrow, next month, by a different agent, and produce an equivalent outcome because the spec's clauses still describe what must be true. If the clauses are no longer valid — the system changed, the intent changed, the constraints changed — the spec must be updated before the next execution. Not after.

---

## Resulting Context

After applying this pattern:

- **Compliance becomes checkable.** A spec that is a control surface produces outputs that conform or don't. Conformance can be checked against spec clauses.
- **Intent persists through iteration.** When the spec is the source of truth, the intent remains stable even as implementation details change.
- **Drift becomes costly.** When violations must be addressed, there is no incentive to ignore the spec.
- **Feedback loops function.** Violations feed back into the spec, improving it. The spec becomes richer with use, not stale.

---

## Therefore

> **A spec functions as a control surface when it is consulted before execution, checked during validation, and updated when intent changes — not after implementation changes. Specs that describe rather than constrain are documentation, not control. The transition from documentation to control requires testable clauses, active use at decision and validation points, and feedback that flows upward into the spec, not sideways into the output.**

---

## Connections

**This pattern assumes:**
- [Spec-Driven Development](01-what-sdd-means.md)
- [Constitutional Archetypes](../architecture/01-archetypes-as-constitutional-law.md)
- [The Intent-Implementation Boundary](../theory/02-intent-vs-implementation.md)

**This pattern enables:**
- [The Spec Lifecycle](03-spec-lifecycle.md)
- [Writing for Machine Execution](05-writing-specs-for-agents.md)
- [The Living Spec](06-living-specs.md)

---

*Next: [Five Phases of the Spec](03-spec-lifecycle.md)*


