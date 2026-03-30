# Pattern 4.6 — Living Specs and Feedback Loops

**Part IV: Spec-Driven Development** · *6 of 7*

---

> *"A spec that is never wrong has never been used."*

---

## Context

You have been practicing SDD. Specs are written before execution. Agents execute against them. Outputs are validated. Some validations reveal problems.

Now you need to decide what to do when the spec was wrong. How should the spec change? When should you fix the spec versus fix the output? How do you make sure the learning from a failure is encoded so the next execution benefits from it?

This pattern assumes all preceding SDD patterns.

---

## The Problem

Two failure modes appear in teams that practice SDD but haven't closed the feedback loop:

**Failure Mode 1: Output patching.** The validation in Phase 5 reveals a problem. The engineer fixes the output directly. The spec remains unchanged. The next time a similar spec is written, or the same spec is run, the same problem reappears. The engineer patches it again. The spec is a fossil — it preserves the original intent at the moment of writing, not the current understanding.

**Failure Mode 2: Spec churn.** Every validation triggers a spec update. The spec is modified constantly, often in response to preference changes rather than genuine spec deficiencies. The spec version history is noise rather than signal. No one knows which version of the spec represents current practice. The spec has become a conversation transcript in markdown format.

Both failures share a diagnosis: the feedback loop from execution to spec is not governed. Either nothing flows back, or everything does. A living spec requires a governed feedback loop — specific conditions that trigger spec updates, and a version history that records why the spec changed, not just what changed.

---

## Forces

- **Learning vs. stability.** Specs must change as understanding deepens, but continuous change makes the spec unstable. The feedback loop must allow learning without allowing constant thrashing.
- **Spec gaps vs. implementation failures.** When output is wrong, there are two possible explanations. The response is dramatically different. Yet being certain which applies requires judgment.
- **Organizational memory vs. noise.** The spec evolution log should record what was learned. But if every preference change gets logged, the log becomes noise.
- **Experimentation vs. governance.** Some changes are worth trying as experiments. Other changes are constitutional. The feedback loop must allow experimentation while protecting constitutional constraints.

---

## The Solution

### What Makes a Spec "Living"

A living spec is not a spec that changes all the time. It is a spec that:

1. **Evolves as understanding deepens** — when a failure reveals that the spec was wrong, the spec is updated to correct the understanding
2. **Has a traceable history** — every version carries the reason for the change, who made it, and what triggered it
3. **Can be run at any version** — any historical version of the spec represents a complete, valid specification that could be executed, even if it is no longer the current version
4. **Accumulates validation evidence** — over time, the spec records which assumptions were confirmed, which invariants were tested, and what was learned from failures

A living spec is an organizational memory artifact. It records not just what was intended, but the process of learning what the right intention is.

### The Feedback Trigger Taxonomy

Not every validation finding should trigger a spec update. The taxonomy:

**Spec gap (always triggers spec update):**  
The output was wrong because the spec didn't say what was needed. The spec was silent on an important behavior, the scope boundary was ambiguous, or an invariant that should have been stated wasn't. Fix the spec. Re-run.

*Example: The spec said "process all incoming orders." An agent processed cancelled orders. The spec needed to say "process all orders with status = active."*

**Spec ambiguity (always triggers spec update):**  
The spec said something that could be interpreted two reasonable ways, and the agent chose the wrong interpretation. This is also a spec failure — not because the intent was wrong, but because the expression was imprecise. Rewrite the clause to be unambiguous.

*Example: The spec said "log all errors." The agent logged errors to stdout. The spec needed to say "log all errors to the structured error log at [path], with schema [defined schema]."*

**Spec over-constraint (may trigger spec update, requires judgment):**  
The spec stated an invariant or requirement that turned out to be incorrect given the actual system behavior. A Guardian's rejection rate is too high because the constraint was miscalibrated. Consider carefully before relaxing — the constraint may have been too tight, or the system may need to change.

*Example: An invariant said "never delete records." The system needs soft deletes for compliance. The invariant should say "never permanently delete records without archival."*

**Implementation failure (does NOT trigger spec update, may trigger spec clarification):**  
The spec was correct; the agent violated it. Fix the output. If the failure suggests the spec clause could be more explicit to prevent recurrence, add an explanatory note or example to the spec — but do not change the clause itself.

**Preference change (does NOT trigger spec update):**  
The spec was correct, the output matched the spec, but the engineer prefers a different approach. This is not a spec failure. If the preference represents a genuine requirement, it should be added to the spec for future executions — explicitly, as a requirement, not retroactively applied to the current output.

### The Spec Evolution Log

Every spec should have a version history section — the spec evolution log. It is not optional.

Structure:

```markdown
## Spec Evolution Log

| Version | Date | Change | Trigger | Author |
|---------|------|--------|---------|--------|
| 1.0 | 2025-01-10 | Initial specification | New work | J. Smith |
| 1.1 | 2025-01-18 | Added invariant: no-delete | Validation gap (v1.0 execution produced hard deletes) | J. Smith |
| 1.2 | 2025-02-03 | Clarified scope: active orders only | Spec ambiguity (agent processed cancelled orders) | A. Chen |
| 1.3 | 2025-02-28 | Updated acceptance criteria: P95 latency to 150ms | System changed (new downstream latency budget) | J. Smith |
```

The evolution log has three functions:

**Diagnostic:** When something goes wrong, the evolution log tells you whether this kind of problem has occurred before — and whether it was fixed at the spec level or just patched in the output.

**Educational:** A new team member reading the spec evolution log understands the history of decisions: what was tried, what failed, and what was learned. This is organizational memory that would otherwise exist only in the minds of the people who were present.

**Governance:** The evolution log makes it possible to audit whether the "fix the spec" rule was followed. If the log is sparse while the issue tracker is full of bugs that appeared in repeated executions of the same spec, the feedback loop is broken.

### The Spec Gap Log

Related to the evolution log, but distinct: the spec gap log is a running record of situations that fell outside what any existing spec covers. It is the place where "this came up and we didn't have a spec for it" goes.

The spec gap log is input to new spec creation, not to existing spec updates. Its entries look like:

```
- 2025-02-14: Agent asked about handling cases where an order has 
  no items. No coverage in current spec. Resolved ad hoc (skip). 
  Needs a spec clause or separate spec for empty-order handling.
  
- 2025-03-01: Two engineers made different decisions about whether 
  validation errors should abort the full batch or skip individual 
  records. Needs a declared invariant.
```

Spec gaps are not failures. They are opportunities. A team that maintains a spec gap log is systematically discovering the boundaries of their current understanding and scheduling the work to fix them.

### The Rule: Fix the Spec, Not the Code

The central discipline of the living spec is this: **when the output is wrong because the spec is wrong, fix the spec first.**

This rule is harder to follow than it sounds. The direct path is to fix the output — it is visible, immediate, and satisfying. The spec fix is invisible; no one sees the evolution log entry; the benefit is deferred to future executions.

The organizational cost of not following this rule is the gradual loss of the spec as a control surface. A spec that is routinely overridden by output patches is a spec where the agents are not actually constrained by the document — they are constrained by whatever the last human correction was. The spec describes an intent that no longer governs anything.

The way to make this rule stick: make the spec update part of the same change as the output fix. If you are fixing output and the fix represents a genuine spec gap, update the spec in the same PR. The habit is "spec update + output fix together," never "output fix alone when the spec was wrong."

### When a Spec Becomes a Repository Asset

Over time, a well-maintained living spec becomes something more valuable than a task description: it becomes a repository of decisions.

A spec that has been run five times, validated five times, and evolved through three rounds of feedback carries:
- The original problem statement
- The decisions made about scope
- The constraints discovered through operation
- The invariants that were tested and confirmed
- The failure modes that were encountered and addressed

This is the spec as organizational learning. It is the documentation that actually gets read, because it contains the map of what went wrong and why. It is the onboarding artifact for a new engineer or agent. It is the audit trail for a compliance review.

The teams that create this kind of asset are not more disciplined than others. They are teams that closed the feedback loop: they made spec updates the response to spec failures, consistently, over time.

---

## Resulting Context

After applying this pattern:

- **Failure drives improvement.** When a failure triggers a spec update instead of an output patch, the next execution learns from the failure. The spec gets richer.
- **Organizational learning is durable.** The spec evolution log records what was learned, when, and why. This becomes institutional memory.
- **Spec authority is preserved.** A spec that is consistently updated on failure remains the source of truth.
- **The feedback loop closes.** Validation flows back into the spec, making the system self-improving.

---

## Therefore

> **A living spec is not a spec that changes constantly — it is a spec that evolves when failures reveal that the spec was wrong, with a traceable history of why each change was made. The feedback loop from validation to spec must be governed: spec gaps and ambiguities always trigger spec updates; preference changes and implementation failures do not. The rule "fix the spec, not the code" protects the spec's function as a control surface. Over time, a well-maintained living spec becomes an organizational memory artifact: the full map of what was intended, what was learned, and what was decided.**

---

## Connections

**This pattern assumes:**
- [Specs as Control Surfaces](02-specs-as-control-surfaces.md)
- [The Spec Lifecycle](03-spec-lifecycle.md)
- [Failure as a Design Signal](../theory/05-failure-as-design-signal.md)

**This pattern enables:**
- [The Canonical Spec Template](07-canonical-spec-template.md) — the spec evolution log section
- [Evolving Archetypes Without Dogma](../architecture/06-evolving-archetypes.md) — the same feedback principle applied to archetype classification

---

*Next: [The Canonical Spec Template](07-canonical-spec-template.md)*


