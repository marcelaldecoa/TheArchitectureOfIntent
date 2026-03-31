# Spec-Driven Development

**Specification**

---

> *"We don't scale by writing more code. We scale by expressing intent clearly enough that systems can build correctly on our behalf."*

---

## Context

You have an agent that can write code, call APIs, modify databases, compose documents, and coordinate other agents. You have been using it. Some of its outputs are excellent. Others require significant correction. You are not sure whether the corrections are the agent's fault, your instructions' fault, or simply the nature of the work.

You are about to discover that most of the corrections are the spec's fault — and that you didn't know you were writing a spec in the first place.

This pattern opens Part IV and assumes the conceptual vocabulary of Parts I–III: intent vs. implementation, agency levels, failure categories, and the archetype framework.

---

## The Problem

When organizations first deploy AI agents seriously, they observe a pattern: the first few uses are impressive. The agent produces results rapidly — work that might have taken a developer hours is drafted in minutes. Then, as tasks become more complex, the rework begins. The agent's output needs correction — sometimes small, sometimes large. The team concludes, usually too quickly, that the agent "isn't good enough yet" or that "AI still needs a lot of human oversight."

Both conclusions miss the important point. The agent may well be capable. The more common problem is that the human didn't specify what they wanted precisely enough to tell the difference between a good output and a bad one before seeing it. The specification — whether it was a five-line prompt, a Jira ticket, or a verbal briefing — was insufficient to produce the correct output, and also insufficient to validate it. The human is doing both production and quality control in their head.

This is primarily a clarity problem, though not exclusively. Some failures are genuinely model-level — hallucination, confidence miscalibration, distribution mismatch. But clarity failures are the most common and the most fixable. The clarity gap has always existed in software — it was previously hidden because human developers could read between the lines, ask questions, interpret intent, and apply professional judgment. Agents do not do that. They execute what they are told. The gap between what you intended and what you expressed is now fully visible.

Spec-Driven Development (SDD) is the discipline that closes that gap — not by making agents smarter, but by making humans more precise about what they want before they ask for it.

---

## Forces

- **Human comprehension vs. agent execution.** Humans tolerate ambiguity and resolve it implicitly; agents execute literal text, making human imprecision immediately visible as incorrect outputs.
- **Implicit judgment vs. explicit specification.** Human developers applied professional judgment silently; agents have no embedded judgment. Either the judgment goes into the spec, or the agent fills the gap with probability.
- **Feedback speed vs. feedback quality.** With human developers, feedback was immediate and conversational. Agent-mediated work is slower but buys precision: outputs can be validated against explicit criteria.
- **Completeness vs. pragmatism.** A complete spec seems heavy. Yet incomplete specs produce more rework. The actual time cost of precision is often less than the perceived cost.

---

## The Solution

### What SDD Is

Spec-Driven Development is a development discipline in which **a complete, validated specification precedes all agent execution**. The spec is:

- Written before any code, test, or implementation artifact is produced
- Detailed enough that a knowledgeable person could verify the output against it without seeing the work in progress
- Structured to be directly consumed by an agent as its primary input
- Treated as the authoritative source of truth — not the code, not the conversation history, not "what we talked about in the standup"

The spec is not documentation. Documentation is produced after the work and describes what was done. A spec is produced before the work and describes what must be done. Documentation explains. Specs constrain.

The spec is not a requirements document in the traditional sense. Traditional requirements documents are written for humans — they use natural language, allow ambiguity, and rely on the reader's judgment to resolve gaps. A spec in SDD is written so that the primary reader is an agent executing the work, and the secondary reader is a human validating the output. Both readers need the same unambiguous interpretation.

The spec is not a conversation. The most common substitute for a spec is a prompt — a sentence or paragraph that gets refined in a conversation with an agent. Conversations are excellent for exploration. They are terrible for execution at scale, because they cannot be reviewed independently, cannot be reused, and cannot be enforced. A spec is not a conversation that got long enough.

### What SDD Is Not

SDD is not a return to heavyweight upfront design. The spec is intended to be minimal, not comprehensive — it captures what must be true, not everything that might be relevant. A good spec is shorter than the code it produces.

SDD is not a way to remove human judgment. The human who writes the spec is the person exercising judgment about what matters. Agents execute against that judgment; they do not replace it. SDD concentrates judgment at the front of the process rather than distributing it across a conversation.

SDD is not a way to make agents infallible. Even a perfect spec will occasionally produce an imperfect output. SDD exists to make failure diagnostic — when the output is wrong, you can ask: was the spec right? If yes, it is an implementation failure. If no, fix the spec first.

### The Foundational Rules of SDD

Four rules are non-negotiable:

**Rule 1: No agent execution without a spec.**  
Every task delegated to an agent must have a spec that precedes it. The spec may be short. It must exist. A prompt is not a spec unless it contains a complete specification. The test: could a new team member validate the output without talking to you?

**Rule 2: Fix the spec, not just the code.**  
When agent output is wrong, the reflex is to correct the output. The discipline is to ask first: is the spec correct? If the output was wrong because the spec was ambiguous or incomplete, fix the spec and re-execute. Only fix the output directly if the spec was correct and the output violated it.

**Rule 3: Review outcomes against the spec, not personal preference.**  
"I don't like how this is structured" is not a spec violation unless it contradicts something the spec required. Validation questions are: *Does this match the spec?* If yes, the output is valid independent of preference. If no, the spec governs, not the preference.

**Rule 4: The spec is the source of truth.**  
If the spec and the code disagree, the spec is right. The code is wrong. This is not bureaucratic pedantry — it is the mechanism by which the agent's work remains governable. A spec that is silently overridden by code changes is not a spec anymore; it is a historical document.

### The Discipline Shift

SDD requires a genuine shift in where engineering effort is applied. In a pre-agent workflow, engineers spend most of their time producing code and iteratively correcting it via tests and review. In an SDD workflow, engineers spend significant effort producing clear specifications before any production work starts — then validate the output, update the spec based on findings, and re-execute.

| Activity | Pre-Agent | SDD |
|---|---|---|
| Problem definition | Informal, often implicit | Written problem statement, owner-signed |
| Success criteria | Defined after code | Defined before code, testable |
| Constraint declaration | Informal | Explicit invariants and non-negotiables |
| Code production | Engineer writes | Agent executes against spec |
| Validation | Code review against unstated expectations | Output validation against spec |
| Failure response | Debug the code | Diagnose: spec gap or implementation failure |
| Learning capture | Institutional memory | Spec evolution log |

The column on the right is not slower. It requires more discipline at the front. But the rework rate is dramatically lower, and the organizational learning is durable — captured in specs that can be reused, reviewed, and evolved — rather than locked in the heads of individuals who were in the room.

### Why "Development"

The word "development" in Spec-Driven Development is deliberate. SDD is not spec-driven *documentation* or spec-driven *process*. It is a development discipline — it governs how software is built, not just how it is described.

This means SDD applies everywhere a developer would have previously applied their own judgment without writing it down: choosing an architecture, handling an edge case, deciding how an error should be surfaced. In SDD, those judgments belong in the spec. Not because the agent can't make them — but because when it does, they are invisible. When they are in the spec, they can be reviewed, challenged, and revised.

---

## Resulting Context

After applying this pattern:

- **Rework rate drops dramatically.** When output is validated against explicit criteria, agents produce correct results more often.
- **Judgment is concentrated but visible.** Rather than judgment being distributed across conversations, it is concentrated in the spec and reviewable before execution.
- **Agents become reliable.** An agent executing against a clear spec produces consistent, auditable results.
- **Organizational memory is durable.** The spec captures decision rationale and constraints that transfer when people leave.

---

## Therefore

> **Spec-Driven Development is the discipline of writing a complete, validated specification before any agent executes work. The spec precedes code; it is the source of truth; and when output is wrong, the first question is whether the spec is wrong. SDD does not make agents smarter — it makes human intent precise enough that execution and validation both become possible.**

---

## Connections

**This pattern assumes:**
- [The Intent-Implementation Boundary](../theory/02-intent-vs-implementation.md)
- [Failure as Diagnostic Signal](../theory/05-failure-as-design-signal.md)
- [The Moral Weight of Specification](../theory/06-why-specs-are-moral-artifacts.md)

**This pattern enables:**
- [The Spec as Control Surface](02-specs-as-control-surfaces.md)
- [The Spec Lifecycle](03-spec-lifecycle.md)
- [The Canonical Spec Template](07-canonical-spec-template.md)

---
