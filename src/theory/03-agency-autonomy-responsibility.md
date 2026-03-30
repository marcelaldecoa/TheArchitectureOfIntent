# Pattern 2.3 — Agency, Autonomy, and Responsibility

**Part II: Theory of Intent Engineering** · *3 of 6*

---

> *"Autonomy without authority is just a faster way of doing what you were told. Agency without accountability is just a faster way of causing harm."*

---

## Context

The vocabulary around agent systems is unstable. "Autonomous," "agentic," "semi-autonomous," "goal-directed" — these terms are used interchangeably in most of the industry, collapsing important distinctions that affect how systems should be designed. This pattern establishes precise definitions for three concepts that must be clearly separated: **agency**, **autonomy**, and **responsibility**.

These definitions form the conceptual backbone of the [Archetype Dimensions](../architecture/03-archetype-dimensions.md) chapter and directly inform every oversight model in this book.

This pattern assumes [Intent vs. Implementation](02-intent-vs-implementation.md) and builds toward [Reversibility as a Design Dimension](04-reversibility-as-design-dimension.md).

---

## The Problem

When engineers say a system is "autonomous," they might mean any of several different things:
- It runs without a human clicking a button each time
- It makes decisions that were not explicitly pre-specified
- It can modify its own behavior based on feedback
- It can initiate new goals rather than just executing given ones
- It has the ability to act in ways that were not foreseen by its designers

These are dramatically different claims — with dramatically different design implications. A deployment pipeline that runs on commit is "autonomous" in the first sense. An agent that decides to delete files it considers redundant is something closer to the last sense. Treating them with the same design patterns is a category error.

Similarly, "responsibility" in AI systems discussions is often vague: sometimes it means legal liability, sometimes ethical answerability, sometimes operational accountability, sometimes the technical responsibility of catching errors. Without distinguishing these, accountability conversations produce more confusion than clarity.

---

## The Resolution

### Autonomy: The Operational Dimension

**Autonomy** is the degree to which a system executes a process without requiring human intervention at each step.

Autonomy is a spectrum, not a binary. A fully manual process (human decides and acts every step) sits at one end. A fully automated process (system runs a predetermined sequence with no human involvement) sits at the other. Most real systems sit somewhere in between — some steps automated, some requiring human input or approval.

Autonomy is primarily an **operational** concept. It says: how much human labor is needed to run this system?

Autonomy does not, by itself, tell you how much discretion the system exercises. A fully autonomous script that runs `git push` every night exercises no meaningful discretion. A human who makes one decision a day about whether to deploy exercises more discretion than the script despite being "less autonomous."

**Key insight:** Raising autonomy reduces human labor. It does not necessarily raise risk — unless it also raises the discretion (agency) the system exercises or the irreversibility of its actions.

---

### Agency: The Discretion Dimension

**Agency** is the capacity to make decisions that were not explicitly pre-specified — decisions that require interpreting goals, weighing options, resolving ambiguity, or acting in situations the original instructors did not fully anticipate.

Agency is about **discretion**. An agent exercising genuine agency is doing something qualitatively different from an automated script executing a deterministic sequence. It is filling gaps in its instructions with its own judgment (probabilistic reasoning, in the case of language models).

Agency has a direction: it operates in service of a goal. To exercise agency is to take actions that the agent believes advance the goal, within constraints that were given. An agent with broad agency has wide latitude to decide *how* to pursue the goal. An agent with narrow agency has a very constrained solution space — it can still act without human intervention (autonomy) but its options are tightly defined.

**Key insight:** Agency determines exposure. The more discretion a system exercises, the more important it is that the goals, constraints, and escalation paths were specified correctly. Every gap in the spec becomes a decision the agent will fill with probability.

---

### Responsibility: The Accountability Dimension

**Responsibility** in intent engineered systems is distributed across multiple parties, each bearing a distinct kind of accountability:

**Authorial responsibility** — The humans who wrote the spec bear responsibility for the adequacy of the intent as expressed. If the spec authorized something harmful, or failed to constrain something that should have been constrained, the authors are accountable. This is the deepest form of responsibility. It cannot be transferred to the agent.

**Operational responsibility** — The humans who deployed and operate the system bear responsibility for ensuring it functions within its designed parameters, that monitoring is adequate, and that failures are caught and corrected. This is ongoing accountability, not a once-at-design-time judgment.

**Validation responsibility** — The humans who reviewed outputs and decided to act on them bear responsibility for that decision. If an agent produced a recommendation and a human implemented it without review, the accountable party for the outcome is the human who chose to act — not the system that generated the recommendation.

**Platform responsibility** — The builders of the agent infrastructure (the model, the orchestration layer, the MCP tools) bear responsibility for the reliability and safety of the platform within its stated operating parameters.

These responsibilities are **concurrent and non-exclusive**. A failed outcome often involves accountability at multiple levels: a spec that under-constrained, an operator who didn't monitor, a reviewer who did not catch a failure, a platform that behaved unexpectedly. Understanding which responsibility layer failed is prerequisite to preventing recurrence.

---

### The Danger Zone: High Agency + Low Responsibility Clarity

The most dangerous design configuration in agent systems is high agency (the system exercises significant discretion) combined with low responsibility clarity (nobody knows who is accountable for outcomes).

This combination emerges in three common patterns:

**The "AI decided" deflection** — When something goes wrong, the response is "the AI did it." This is not a meaningful answer. An AI system acts within a spec, authorized by humans, deployed by humans, running on infrastructure operated by humans. "The AI decided" is always a shorthand for a chain of human decisions that allocated agency.

**The empty oversight seat** — A system with significant agency but no designated human reviewer of its outputs. The system acts; nobody checks. When the system's discretionary judgment is wrong, nobody catches it until the consequences have compounded.

**The responsibility gap** — A system where authorial responsibility (who wrote the spec), operational responsibility (who runs it), and validation responsibility (who reviews outputs) belong to different teams who never coordinated on what "accountable" actually means in practice.

---

### The Calibration Framework

Given these definitions, the primary design question for any agent delegation is:

> For this system, at what level of discretion (agency), at what execution speed (autonomy), and with what distribution of accountability (responsibility) are we operating?

| Question | Design Response |
|---|---|
| High agency over irreversible actions | Requires maximum constraint specification + mandatory human review |
| High autonomy over repetitive, reversible tasks | Can run with light oversight; monitoring for drift is sufficient |
| Unclear responsibility distribution | Must be resolved before any system is deployed — not assumed to sort itself out |
| High agency + unclear responsibility | Do not deploy. Design the responsibility structure first. |

---

## Therefore

> **Autonomy (how independently it runs), agency (how much discretion it exercises), and responsibility (who is accountable for outcomes) are three distinct dimensions of agent system design. Conflating them produces unsafe systems. Calibrating them deliberately — specifying agency boundaries in the spec, matching autonomy to the oversight capacity of the team, and assigning responsibility explicitly before deployment — is a primary function of intent engineering.**

---

## Connections

**This pattern assumes:**
- [Intent vs. Implementation](02-intent-vs-implementation.md)
- [Where Agency Resides](../foundations/04-where-agency-resides.md)

**This pattern enables:**
- [Reversibility as a Design Dimension](04-reversibility-as-design-dimension.md) — the fourth key variable in this calibration
- [Archetype Dimensions](../architecture/03-archetype-dimensions.md) — formal encoding of agency levels in archetypes
- [Human Oversight Models](../agents/06-human-oversight-models.md) — designing oversight to match agency level
- [Who Is Allowed to Define Archetypes](../operating/03-who-defines-archetypes.md) — responsibility structures in governance

---

*Next: [Reversibility as a Design Dimension](04-reversibility-as-design-dimension.md)*

