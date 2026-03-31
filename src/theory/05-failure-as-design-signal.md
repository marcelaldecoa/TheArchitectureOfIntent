# Pattern 2.5 — Failure as Diagnostic Signal

**Part II: Theory of Intent Engineering** · *5 of 6*

---

> *"In a system you designed with clear intent, failure is not an accident. It is a message. The question is whether you built the structures to receive it."*

---

## Context

Your system has produced an incorrect outcome. An agent did something wrong, or produced something harmful, or failed to achieve the goal. The instinct is to fix the immediate problem and move on. But every failure in an agent-mediated system carries diagnostic information that, if read correctly, prevents a class of future failures.

This pattern teaches how to read failures as signals rather than noise — a practice that is central to the maintenance of living specs and the long-term health of agent-driven systems.

This pattern assumes [Design for Reversibility](04-reversibility-as-design-dimension.md) and pairs with [The Moral Weight of Specification](06-why-specs-are-moral-artifacts.md).

---

## The Problem

The default response to failure in software engineering is **correction**: find the bug, fix it, test it, deploy the fix. This is appropriate when the failure was an implementation error — a mistake in the how.

But in intent-engineered systems, many failures are not implementation errors. They are **intent errors** or **constraint omissions** — failures in the what. And intent errors cannot be fixed by correcting the implementation. They require going upstream to the specification.

The problem is that intent errors and implementation errors look identical from the outside: both produce wrong outputs. Without a discipline for distinguishing them, the "fix" will always be applied to the implementation — which is faster, easier, and satisfying in the short term. And the failure will recur, in a slightly different form, until the underlying intent problem is addressed.

Worse: in systems where agents execute continuously, an undiagnosed intent error will accumulate wrong outputs at machine speed. The longer it takes to recognize the failure as a signal about the spec, the larger the accumulated consequence.

---

## Forces

- **Quick fixing vs. diagnostic depth.** The immediate response to failure is correction — patch the code and move on; but intent failures require upstream spec analysis, which is slower and demands admitting incomplete thinking.
- **Probabilistic assumption vs. deterministic execution.** In traditional development, many failures were implementation errors; in agent-mediated systems, many failures are intent gaps that the agent faithfully executes.
- **Machine speed vs. human diagnosis cadence.** Agents execute continuously; if failures are not diagnosed at the right level, they compound at machine scale before anyone detects a pattern.

---

## The Solution

### The Four Categories of Agent System Failure

Failures in agent-mediated systems fall into four categories. Correctly categorizing a failure determines how to fix it — and more importantly, what it reveals about the system design.

---

**Category 1: Intent Failure**
*The spec described something incorrect, incomplete, or ambiguous, and the agent faithfully executed what was described.*

Signs:
- The agent did exactly what the spec said, but the outcome is wrong
- The failure reproduces reliably across different agent executions
- Different agents or models produce the same wrong output from the same spec

What it reveals: The spec has a gap. Either a constraint was missing, a scope boundary was undefined, a success criterion was wrong, or the framing of the problem was incorrect.

Fix: Correct the spec. Document what the gap was and why it was missed. Then re-execute.

---

**Category 2: Context Failure**
*The agent lacked the information it needed to act correctly, and filled the gap with probabilistic reasoning that was wrong.*

Signs:
- The agent's output shows it made an assumption that was incorrect
- With more information provided, the agent would have acted differently
- The failure varies across executions of the same spec (the agent "guesses" differently each time)

What it reveals: The spec or system context is missing information that the agent needs: architectural decisions, domain rules, regulatory constraints, business definitions, historical context.

Fix: Add the missing context to the spec — either directly or by linking to a document that expresses it. Context failures are a signal that the institutional knowledge required for this task has not been made explicit.

---

**Category 3: Constraint Violation Failure**
*The agent produced an output that violated a boundary that was not adequately expressed in the spec.*

Signs:
- The output achieves the stated goal but violates something that should have been treated as non-negotiable
- The constraint that was violated was assumed rather than written
- The failure would be described as "the agent went too far"

What it reveals: A constraint was implicit in the designer's mind but not encoded in the spec. This is among the most important failure categories because it reveals where professional judgment was tacitly assumed rather than explicitly expressed.

Fix: Add the violated boundary as an explicit constraint in the spec. Ask: "What else was I assuming that is not written down?" Treat this as an audit trigger for the entire constraint section.

---

**Category 4: Implementation Failure**
*The spec was correct and complete, but the agent failed to execute it correctly in this instance.*

Signs:
- The spec clearly prohibits or requires the behavior that failed
- The failure does not reproduce consistently across executions
- Providing the same spec to a different agent or context produces correct output

What it reveals: An execution reliability issue — in the model, the tooling, the prompt construction, or the runtime environment.

Fix: Debug the execution layer. This is the correct category for the "fix the implementation" response. But confirm it is Category 4 before applying a code-level fix.

---

### The Failure Diagnostic Protocol

When a failure occurs, resist the impulse to fix immediately. Apply this diagnostic first:

```
1. Reproduce the failure deliberately
   (If it can't be reproduced, treat as Category 4)

2. Ask: would the spec, as written, have predicted this failure as a valid output?
   YES → Category 1 (Intent Failure) — fix the spec
   NO  → continue

3. Ask: does the agent's output reflect an assumption that contradicts
         what we know to be true about this domain?
   YES → Category 2 (Context Failure) — add context to spec
   NO  → continue

4. Ask: did the output achieve the stated goal but violate something
         that "should go without saying"?
   YES → Category 3 (Constraint Violation) — add the constraint
   NO  → Category 4 (Implementation Failure) — fix execution
```

---

### Failure Archaeology

One of the most valuable practices in a mature intent engineering culture is **failure archaeology**: the systematic review of past failures to extract spec improvements.

Every deployment of an agent system should maintain a failure log. Not a bug tracker (which tracks implementation errors) — a **spec gap log**: a record of every time a failure pointed to something that should have been in the spec but wasn't.

Over time, this log becomes:
- A source of constraint additions that make future specs more complete
- A record of the tacit knowledge that was made explicit
- Training data for the team's calibration of "what needs to be in a spec"
- Evidence for governance conversations about where oversight should be increased

This is what it means to say failure is a design signal: each failure, properly diagnosed, makes the system of specs stronger. The goal is not zero failures — it is zero unlearned-from failures.

---

### Failure Modes Are Patterns Too

In the spirit of Alexander's pattern language, failure modes are patterns that can be named, cataloged, and used to guide design before failure occurs. [Six Failure Categories](../agents/07-failure-modes.md) provides a catalog of common failure patterns in agent execution. But the more fundamental catalog — the one that matters for intent engineering — is the catalog of **spec failure modes**: the recurring ways in which intent, expressed in language, fails to constrain agent behavior as intended.

The most common spec failure modes:

- **The Missing Invariant** — An assumption so obvious to the author that it was never written; the agent violated it
- **The Scope Ambiguity** — The spec didn't define what was out of scope; the agent built too much
- **The Implicit Audience** — The spec was written assuming the agent shared the author's cultural and institutional context; it did not
- **The Success Vacuum** — The spec had no measurable success criteria; the agent optimized for something that wasn't what was meant
- **The Frozen Context** — A constraint in the spec was true at time of writing but is no longer true; the system continues to enforce a rule that no longer applies

Each of these is a recurring design problem with a predictable resolution — which is exactly what a pattern is.

---

## Resulting Context

After applying this pattern:

- **Failures become diagnostic data, not just corrective events.** A categorization protocol reveals whether each failure originated in intent, context, constraints, or execution; this diagnosis determines where to fix.
- **Institutional knowledge accumulates in spec gap logs.** Each failure reveals something the specification assumed but did not express; a failure archaeology practice captures these gaps, making tacit knowledge explicit.
- **Specs improve systematically through failure-driven evolution.** Rather than accumulating legacy debt, each failure contributes a constraint addition or clarification — the living spec becomes stronger over time.

---

## Therefore

> **Failure in an agent-mediated system is a diagnostic event, not just a corrective one. Before fixing, categorize: is this an intent failure, a context failure, a constraint omission, or an implementation error? Fix at the correct level. Accumulate the signal in a spec gap log. Treat each failure as a message about what the specification assumed but did not say — and make it more explicit.**

---

## Connections

**This pattern assumes:**
- [Design for Reversibility](04-reversibility-as-design-dimension.md)
- [The Intent-Implementation Boundary](02-intent-vs-implementation.md)

**This pattern enables:**
- [The Moral Weight of Specification](06-why-specs-are-moral-artifacts.md) — the ethical dimension of letting failures propagate
- [The Living Spec](../sdd/06-living-specs.md) — the practice structure for failure-driven spec evolution
- [Six Failure Categories](../agents/07-failure-modes.md) — the execution-level failure catalog
- [Four Signal Metrics](../operating/06-metrics.md) — measuring spec quality through failure signal

---

*Next: [The Moral Weight of Specification](06-why-specs-are-moral-artifacts.md)*

