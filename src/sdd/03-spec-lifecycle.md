# Pattern 4.3 — The Spec Lifecycle: From Intent to Validation

**Part IV: Spec-Driven Development** · *3 of 7*

---

> *"You do not understand a thing until you can write it. You do not know you have written it correctly until someone can build from it."*

---

## Context

You know that specs must precede execution and that they function as control surfaces. Now you need the process: how does a task become a spec, and how does a spec become a validated outcome?

This is the procedural backbone of Spec-Driven Development. It is deliberately not a software development methodology in the project-management sense — it has no sprints, no ceremonies, no artifacts beyond the spec itself. It is a discipline applied to individual tasks delegated to agents.

This pattern assumes [What Spec-Driven Development Really Means](01-what-sdd-means.md) and [Specs as Control Surfaces](02-specs-as-control-surfaces.md).

---

## The Problem

Without a named lifecycle, the "spec-first" principle collapses into ad-hoc practice. Different engineers apply the discipline differently. Some write rich specs; others write prompts they call specs. Some validate rigorously; others skim. The feedback loop — the mechanism by which failures become spec improvements — is not practiced because it was never made explicit.

A lifecycle gives the discipline repeatability. It makes the required activities visible, so they can be audited, measured, and improved. It also makes handoffs possible: you can hand a spec to an agent you've never worked with before, and both you and the agent have a shared understanding of what exists at each stage.

---

## Forces

- **Discipline vs. freedom.** A named lifecycle constrains how teams work. Not having one avoids that constraint but makes practices inconsistent.
- **Efficiency vs. completeness.** Phase 1 (intent capture) can seem excessive. Yet skipping it produces specs that answer 'how' before establishing 'what.'
- **Heavyweight vs. visible.** Making the lifecycle explicit creates pressure. But visibility also enables noticing when it is being skipped.
- **Reusability vs. context-binding.** Each phase produces reusable artifacts. Yet each task is unique. The lifecycle must help without being so prescriptive it prevents legitimate variation.

---

## The Solution

### The Five Phases

The SDD lifecycle has five phases. Each phase has a defined input, a defined output, and a defined responsibility assignment.

---

**Phase 1: Intent Capture**

*Input:* A task, goal, or problem statement — in any form.  
*Output:* A written problem statement (one paragraph max) that answers: What problem is being solved? Who is affected? Why now? What breaks if this is not done?  
*Responsibility:* Human (author/requester)

This is the "WHY" phase. Its product is not the spec — it is the raw material the spec will be built from.

The problem statement is deliberately narrow: one paragraph, no implementation. Its only job is to establish that the problem is real, bounded, and understood. If you cannot write a one-paragraph problem statement that survives five minutes of scrutiny, you do not understand the problem well enough to spec it. Stop here and think.

Common failure: skipping Phase 1 entirely and writing a solution first. The output of a Phase 1 skip is a spec that answers "how" before it has established "what" — which reliably produces systems that are built correctly for the wrong purpose.

---

**Phase 2: Specification**

*Input:* Problem statement (Phase 1)  
*Output:* The complete spec, following the canonical template  
*Responsibility:* Human (author, with archetype review if applicable)

This is the "WHAT" phase. The spec captures:
- Desired outcomes (primary and secondary)
- Scope boundaries (in/out)
- Functional intent (what the system must do)
- Non-functional constraints (what it must never violate)
- Invariants (what must always be true)
- Acceptance criteria (how to verify success)
- Assumptions and open questions
- Agent execution instructions
- Archetype declaration (for agent systems)

The spec must be complete enough that a person not involved in writing it can validate an output against it without asking questions. This is the completeness test: Can validation happen independently?

If the spec requires the author to explain it before it can be used, it is not done. Write the explanation into the spec.

Agent-assisted drafting is appropriate here. An agent can generate a first-draft spec from the problem statement. The human reviews and approves it. The approved version is what governs execution — not the draft, not the conversation that produced the draft.

---

**Phase 3: Clarification**

*Input:* Draft spec (Phase 2)  
*Output:* Resolved open questions, refined spec  
*Responsibility:* Human (author) + agent (for clarifying questions); reviewer (for spec approval)

Before execution, the spec is reviewed for gaps:
- Are any assumptions unverified?
- Are any scope boundaries ambiguous?
- Are invariants contradictory or incomplete?
- Can every acceptance criterion be tested?

This phase uses agents effectively: a clarification pass where the agent asks what's missing is one of the highest-value uses of agent capability. *"Given this spec, what would you need clarified before you could proceed without asking questions?"* The agent's uncertainties are a diagnostic of spec quality.

Phase 3 ends with a formal approval — the spec is marked *Approved* and the version is locked for the next execution. An approved spec can be changed; the change requires a new version and a new approval. Execution against an unapproved spec is a process violation.

---

**Phase 4: Execution**

*Input:* Approved spec (Phase 3)  
*Output:* Implementation artifacts (code, tests, documents, configuration)  
*Responsibility:* Agent (constrained by spec)

The agent executes against the approved spec. The rules:
- Agents do not make product decisions
- Agents do not override constraints
- Agents surface uncertainty instead of inventing answers
- Agents do not expand scope

If the agent encounters a situation the spec does not cover, it halts and surfaces the gap — it does not resolve the gap autonomously. The gap is a spec deficiency. It becomes an open question that flows back to Phase 3.

During execution, the spec is the agent's primary reference. Not the conversation history. Not the examples in the training data. Not what seems sensible. The spec.

---

**Phase 5: Validation & Learning**

*Input:* Implementation artifacts (Phase 4)  
*Output:* Approved outcomes or identified spec gaps; updated spec  
*Responsibility:* Human (validator)

Validation is performed by a human against the spec, not against personal preference. The validation questions are:

- Does the output satisfy the acceptance criteria in section 7?
- Were the invariants in section 6 respected?
- Were any out-of-scope behaviors produced (violating section 3)?
- What assumptions from section 8 were revealed to be wrong?

After validation, one of three outcomes:

**A — Output accepted.** The spec was correct, the execution was correct. Log to the spec evolution section: what was learned, any invariants that were confirmed, any assumptions that were validated. The spec is now slightly richer.

**B — Output rejected, spec gap.** The output was wrong because the spec was incomplete or ambiguous. Fix the spec first. Re-execute. Do not patch the output directly — the patch is local and will not influence future executions. The spec fix is permanent.

**C — Output rejected, implementation failure.** The spec was correct; the output violated it. This is an implementation-level issue. Fix the output. Also document the failure in the spec evolution log, noting which clause was violated and the failure type. This documentation may eventually suggest that the spec clause needs to be more explicit.

---

### The Lifecycle at a Glance

```
┌──────────────────────────────────────────────────────────────────┐
│  PHASE 1: Intent Capture                                          │
│  Human writes problem statement (one paragraph)                   │
│  Output: Why we're doing this                                     │
└──────────────────────────────────┬───────────────────────────────┘
                                   ↓
┌──────────────────────────────────────────────────────────────────┐
│  PHASE 2: Specification                                           │
│  Human (± agent draft) writes complete spec                      │
│  Output: Full spec, status = Draft                               │
└──────────────────────────────────┬───────────────────────────────┘
                                   ↓
┌──────────────────────────────────────────────────────────────────┐
│  PHASE 3: Clarification                                           │
│  Agent surfaces gaps; human resolves; reviewer approves          │
│  Output: Spec, status = Approved, version locked                 │
└──────────────────────────────────┬───────────────────────────────┘
                                   ↓
┌──────────────────────────────────────────────────────────────────┐
│  PHASE 4: Execution                                               │
│  Agent executes against approved spec                            │
│  Output: Implementation artifacts                                │
└──────────────────────────────────┬───────────────────────────────┘
                                   ↓
┌──────────────────────────────────────────────────────────────────┐
│  PHASE 5: Validation & Learning                                   │
│  Human validates against spec; categorizes gaps                  │
│  Output A: Accepted + spec evolution log updated                 │
│  Output B: Spec gap → back to Phase 3 with fix                   │
│  Output C: Implementation failure → output fix + log             │
└──────────────────────────────────────────────────────────────────┘
```

### What the Lifecycle Is Not

The lifecycle is not a Waterfall process. Each phase is short — for a well-understood task, Phases 1–3 can be completed in under an hour. The lifecycle applies to an individual task, not a project. A project may have dozens of spec cycles running in parallel.

The lifecycle is not a gate-heavy process. Its approvals are lightweight: *"Does this spec answer the completeness test?"* The weight is in the thinking, not the ceremony.

The lifecycle is not final on completion. Phase 5 feeds back into Phase 2. Specs accumulate evolution entries. Over time, a reused spec becomes a rich document of what was learned — a form of organizational memory that is directly executable by the next agent that needs it.

---

## Resulting Context

After applying this pattern:

- **Handoff becomes possible.** With a named lifecycle, a task can be handed off at any phase. The phases make handoff explicit.
- **Failure categories are visible.** When an outcome is rejected, the reason is clear: spec gap or implementation failure.
- **Learning is systematic.** Each phase produces a formally validated artifact that becomes organizational history.
- **Gatekeeping becomes strategic.** Gates are at phase transitions: spec approved before execution, outcomes validated against spec. Few gates, but loadbearing.

---

## Therefore

> **The SDD lifecycle has five phases: intent capture, specification, clarification, execution, and validation. Each phase has a defined input, output, and responsibility. The feedback from validation flows back into the spec — not into the output — so that every failure makes the next execution better. The lifecycle is not a project methodology; it is a discipline applied to every individual task delegated to an agent.**

---

## Connections

**This pattern assumes:**
- [What Spec-Driven Development Really Means](01-what-sdd-means.md)
- [Specs as Control Surfaces](02-specs-as-control-surfaces.md)

**This pattern enables:**
- [SpecKit in the Architecture of Intent](04-speckit.md)
- [Writing Specs for Agents, Not Humans](05-writing-specs-for-agents.md)
- [Living Specs and Feedback Loops](06-living-specs.md)
- [The Canonical Spec Template](07-canonical-spec-template.md)

---

*Next: [SpecKit in the Architecture of Intent](04-speckit.md)*


