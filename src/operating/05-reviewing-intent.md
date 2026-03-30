# Pattern 7.5 — Reviewing Intent, Not Code

**Part VII: Operating the System** · *5 of 6*

---

> *"Code review asks: is this implementation correct? Intent review asks: is this the right thing to implement? The second question is harder and worth more."*

---

## Context

Code review is one of the most established practices in software engineering. It evolved to catch implementation errors: logic bugs, style violations, security vulnerabilities, missing tests. It works because the reviewer can read the implementation and evaluate whether it is correct.

In an agent-augmented practice, the implementation is increasingly produced by an agent executing against a spec. The reviewer who reads the output code and checks it for correctness is still doing useful work — but they are reviewing the *output* of an already-executed decision. Every spec gap, every wrong archetype selection, every missing constraint has already been faithfully implemented by the time the code review is opened.

This chapter describes the shift to intent review as the primary lever for quality — and how to run it effectively alongside traditional code review rather than instead of it.

---

## The Problem

Code review is downstream of every consequential decision. By the time a PR is open:

- The archetype was selected (correctly or incorrectly)
- The scope was defined (completely or not)
- The constraints were written (with gaps or without)
- The success criteria were established (testable or aspirational)
- The agent executed (faithfully, against whatever spec it was given)

A code reviewer who finds a logic error can request a fix. A code reviewer who finds that the agent implemented the wrong abstraction, built to the wrong scope, or missed a security requirement faces a much heavier remediation — one that may require re-specifying and re-executing, not just a minor fix.

The structural problem is that code review, as traditionally practiced, cannot catch intent failures. It can catch implementation failures in the output of a wrong intent. These are different categories of failure and require different review practices.

The secondary problem is review automation confusion. Many teams assume that because agents produce code, automated review tools can replace human review. Automated tools check structure (linting, formatting, security scanners). They cannot check whether the implementation is appropriate for the context, complete against the spec, or free from the class of error that originates in a wrong objective.

---

## The Resolution

### Two Review Disciplines, Not One

An agent-augmented practice needs two review disciplines operating at different points in the workflow:

**Intent review** happens *before* execution — when the spec is submitted for approval. It examines the intent: is the right problem being solved, in the right scope, with the right constraints, under the right oversight model? Intent review catches errors before any agent work begins.

**Output review** happens *after* execution — when the agent's output is submitted for acceptance. It validates the output against the spec: does the output satisfy the success criteria? Does the implementation match the declared scope? Are there outputs that violate stated constraints?

These are not replacements for each other. Intent review without output review leaves implementations unvalidated. Output review without intent review is downstream of every intent error.

### How to Run Intent Review

Intent review is spec approval. It follows the five-question framework from Chapter 7.4, and the reviewer's job is explicitly to find failures before execution.

**The mindset shift for intent reviewers.** Traditional code reviewers are trained to evaluate what is there. Intent reviewers must also evaluate what is missing. A spec that is structurally complete but missing a critical constraint is worse than a spec with an obvious gap — because the obvious gap is caught; the missing constraint that seems implicit is not.

The technique: after reading the spec, write two lists before submitting your review:
1. "What would this agent do that the spec author would consider correct?"
2. "What would this agent do that the spec author would consider incorrect, based on what's in the spec?"

Items on the second list are the spec gaps. They may be genuinely out of scope (in which case they should be explicit NOT-authorized items). They may be accidental gaps. Either way, they need to be resolved before the spec is approved.

**Intent review duration.** A well-written spec for a bounded task should be reviewable in 10–20 minutes. A spec that requires 45 minutes to review is signaling something: either the spec is complex enough that the task is appropriately ambitious (and the review time is warranted), or the spec is poorly structured and the reviewer is doing reconstruction work that the author should have done.

**Intent review by someone who didn't write the spec.** This is the cardinal rule of intent review. A spec author cannot effectively review their own spec for gaps, because their assumptions fill the gaps automatically. The reviewer must have no implicit context about the task except what the spec provides.

### How to Run Output Review

Output review validates execution against the spec. The reviewer's primary reference is Section 6 of the spec (Success Criteria & Acceptance Tests), not the reviewer's personal judgment about quality.

**The single question output review asks:** Does this output satisfy the spec's success criteria?

Not: "Is this code good?" Not: "Is this how I would have done it?" Not: "Is this clean?" These are valid aesthetic concerns that may belong in a separate technical debt discussion — but they are not output review questions. Output review against a spec has an objective answer; preference questions do not.

**When output review finds a failure:** Diagnose the category before requesting a fix.

- If the output violates the spec (the spec was correct, the execution was wrong): re-execute against the same spec. The spec is not changed.
- If the output is correct against the spec but the output is wrong (the spec was wrong or incomplete): update the spec, log the gap, re-execute against the corrected spec.
- If both are correct but the outcome is not what was intended: the intent was not captured in the spec. Discuss and update before re-executing.

**The anti-pattern to eliminate:** "I know what was meant, let me just fix the code." This converts a spec gap into spec debt. The gap remains; the fix lives only in the code. The next execution of the same spec will produce the same gap.

### The Spec Review as a Team Ritual

The most powerful organizational implementation of intent review is the **spec review workshop** — a team ritual distinct from individual PR review. Once a month (or more frequently in teams with high agent throughput), the team reviews real specs together:

- Select 3–5 recent specs: some that produced excellent outputs, some that produced gaps
- For each: the author presents the objective and constraints; reviewers apply the five-question framework cold; the team discusses what was found
- For specs that produced gaps: trace the gap to the spec section, discuss what the spec should have said
- Update the constraint library or archetype catalog if the gap reveals a systemic pattern

The spec review workshop does several things simultaneously: it develops the spec review skill across the team (exposure to multiple spec styles and gap types); it improves the team's constraint libraries (gaps identified become catalog updates); and it creates shared vocabulary about what "a good spec" means in this team's specific domain.

### The Relationship Between Intent Review and Code Review

Intent review does not replace code review; it precedes it and changes its purpose.

In an agent-augmented practice:

**Intent review (pre-execution)** is the first defense. It has the highest leverage. A gap caught here costs 20 minutes. A gap caught at code review costs hours of re-execution. A gap caught in production costs significantly more.

**Code review (post-execution)** catches: implementation deviations from the spec (the agent didn't follow the spec exactly), emergent issues not capturable in spec (performance characteristics, subtle security implications), and constraint violations (the agent exceeded its authorized scope in ways that passed the agent's own validation).

**Automated checks** (linter, tests, security scanner) catch: structural violations, known anti-patterns, test failures. They operate independently and should be required gates before human review.

The ordering:
```
Spec written → Intent review → Spec approved → Agent executes →
Automated checks pass → Output review → Human code review → Merged
```

A gap caught at intent review stage costs one spec revision.  
The same gap caught at output review stage costs spec revision plus re-execution.  
The same gap caught at code review stage costs all of the above plus code investigation.  
The same gap caught in production costs all of the above plus incident response.

The value of intent review is not that it replaces other reviews. It is that it catches the class of failure that no other review can catch — intent failures — at the cheapest possible point.

---

## Therefore

> **Intent review and output review are separate disciplines that operate at different points in the spec-execute-validate loop: intent review before execution catches spec gaps before they are implemented; output review after execution validates that the implementation satisfies the spec. Neither replaces code review, but intent review is the highest-leverage activity in the agent-augmented practice — a gap caught before execution costs one spec revision; the same gap caught after production deployment costs a multiple of that. The spec review workshop is the team ritual that develops this discipline collectively.**

---

## Connections

**This pattern assumes:**
- [What Spec-Driven Development Really Means](../sdd/01-what-sdd-means.md)
- [Governance Without Bureaucracy](04-governance.md)
- [Failure Modes in Agent Systems](../agents/07-failure-modes.md)
- [Validation & Acceptance Templates](../repertoires/05-validation-templates.md)

**This pattern enables:**
- [Metrics That Actually Matter](06-metrics.md)
- Team spec quality development over time

---

*Next: [Metrics That Actually Matter](06-metrics.md)*


