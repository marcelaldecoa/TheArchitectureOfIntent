# Pattern 2.1 — What Is Intent Engineering

**Part II: Theory of Intent Engineering** · *1 of 6*

---

> *"A discipline exists when it has a name, a vocabulary, a set of distinguishing problems, and a body of knowledge about how to solve them. We have arrived at that moment for intent engineering."*

---

## Context

Part I established *why* the role of the software professional has shifted: the bottleneck moved from code production to intent specification. This part names and formalizes the discipline that has emerged in response.

Before something can be practiced reliably, it must be named. Before it can be taught, its concepts must be defined. Before it can be improved, its failure modes must be catalogued. This is what Part II does — it builds the vocabulary that the rest of the book depends on.

This pattern assumes the full argument of [Part I: Foundations](../foundations/01-end-of-human-compiler.md). It prepares the ground for everything that follows.

---

## The Problem

A new kind of work has emerged, practiced widely but not yet named clearly.

Teams are writing specifications meant to be executed by agents. Architects are designing systems where the most important decisions are not code structures but behavioral constraints. Some engineers have developed deep intuitions about how to describe goals so machines reliably achieve them. Others produce ambiguous, over-specified, or contradictory instructions and blame the tool for the poor result.

The gap between these practitioners is not a difference in AI fluency. It is a difference in something older: the ability to think precisely about **what you want a system to do**, **under what conditions**, **within what limits**, and **how you will know when it has done it**. 

This is not a new skill category invented by large language models. It is an ancient human capacity — the capacity for intentional design — that has become the primary technical differentiator in an age where code is cheap.

The problem is that without a name, this skill cannot be taught, measured, or systematically improved. It remains tacit, distributed unevenly across teams, exercised well by some and poorly by others with no shared framework for the difference.

**Intent engineering is the name for this work.**

---

## The Resolution

### A Definition

**Intent engineering** is the discipline of designing, specifying, communicating, and governing the intent behind software systems — so that intent can be executed reliably by agents, validated accurately by humans, and evolved safely over time.

It is a discipline, not a methodology. Methodologies prescribe steps. Disciplines cultivate judgment. You cannot follow a checklist to become a good intent engineer any more than you can follow a checklist to become a good architect. But you can develop the vocabulary, the patterns, and the critical faculties that enable reliable practice — which is what this book is for.

---

### What Intent Engineering Is Not

Several adjacent concepts are easy to confuse with intent engineering. The distinctions matter.

**It is not prompt engineering.**
Prompt engineering is the craft of eliciting desired outputs from a language model through the careful construction of single-turn or multi-turn inputs. It is a real and valuable skill. But it operates at the level of immediate interaction — one model, one conversation, one output. Intent engineering operates at the level of systems: persistent specifications, long-running agents, delegated authority across time and context. The relationship is similar to the difference between writing a good email and designing an organizational communication system.

**It is not requirements engineering.**
Traditional requirements engineering — born in the waterfall era — was about capturing what stakeholders wanted so that human developers could build it. Requirements were primarily documentation for humans: imprecise, open to interpretation, completed before development and rarely touched again. Intent engineering assumes that specifications are **executable operating instructions for machines**. They must be precise enough to act on, constrained enough to prevent misuse, and alive enough to evolve. This requires a fundamentally different epistemology.

**It is not AI governance.**
AI governance addresses the organizational, regulatory, and ethical oversight of AI systems at an institutional level. It is important and related, but it operates at policy level. Intent engineering operates at design level: the individual decisions about what a system is authorized to do, how it communicates uncertainty, and when it escalates to human judgment. Good governance creates the environment for good intent engineering; it does not substitute for it.

**It is not software architecture.**
Traditional software architecture addresses structure: components, interfaces, data models, deployment topology. These concerns remain relevant. But a system's architecture tells you *how it is built*; intent engineering tells you *why it exists*, *what it is permitted to do*, and *under whose authority*. In agent systems, these are the higher-order concerns.

---

### The Three Fundamental Questions

Intent engineering is organized around three questions that must be answered for every system that involves agent delegation:

**1. What is this system trying to achieve?**

This is the *intent question*. It asks not just "what does it do?" but "what purpose does it serve, for whom, and within what definition of success?" Intent is not a feature list. It is a statement of the goal the system is meant to serve — specific enough to act on, rich enough to disambiguate edge cases.

**2. Within what constraints must it operate?**

This is the *constraint question*. It asks: what must never happen? What boundaries may not be crossed regardless of efficiency or cost? What rights, rules, or architectural decisions are non-negotiable? Constraints are the encoded judgment of the people who understand the system's context — they are how experienced reasoning is made durable against agent execution at speed.

**3. How will we know when it is working correctly?**

This is the *validation question*. It asks not just "how do we test it?" but "what does correct behavior look like from the perspective of the intent?" This requires defining success criteria that are verifiable, tied to the stated purpose, and honest about uncertainty. A system that passes its tests but fails its users has a validation gap — and the gap is always in the intent, not the code.

These three questions are the foundation of every spec template, every archetype, and every governance model in this book. They appear explicitly in the [Canonical Spec Template](../sdd/07-canonical-spec-template.md).

---

### The Four Activities of Intent Engineering

In practice, intent engineering involves four recurring activities:

**Framing** — Decomposing a vague problem or goal into a precise, solvable statement. Framing is the most intellectually demanding activity because it requires simultaneously holding the business perspective (what does success look like for stakeholders?), the technical perspective (what kind of system can actually be built?), and the ethical perspective (what should and should not be automated?).

**Specification** — Translating framed problems into machine-executable structures: intent statements, success criteria, constraints, context, and scope boundaries. The spec is the primary artifact of intent engineering. Its quality determines system quality more directly than any code decision.

**Delegation** — Choosing what to give to agents, what to retain for human decision, and how to structure the handoff. Delegation includes designing the capability boundaries, selecting the appropriate archetype, and setting up the oversight model. It is the act of authorizing agency.

**Validation** — Evaluating agent outputs against the original intent. This is not testing in the traditional sense (though it includes testing). It is the human act of asking: *does this system behave as intended? Are there gaps between what was specified and what was understood? Does the spec need to be revised?* Validation is the feedback loop that makes specs living artifacts.

---

### Why "Engineering"?

The choice of the word "engineering" is deliberate and worth defending.

Engineering implies the application of systematic knowledge to solve real problems with predictable reliability. It implies a body of theory, a set of proven methods, standards for what constitutes good work, and accountability for the consequences of that work.

All of this applies to intent engineering.

The criticism that might be raised — "isn't this just communication? Isn't this what good product managers and architects have always done?" — misses the structural shift. In the past, a vague requirement was eventually made concrete by a skilled developer who compensated for ambiguity through judgment. That compensatory mechanism no longer exists in the same form. The agent executes what it is given. The intent engineer is now the last human in the translation chain, and the quality of their work propagates directly into system behavior.

This is engineering. The material is language, the tools are specs and archetypes, and the consequences are real.

---

## Therefore

> **Intent engineering is the discipline of designing, specifying, and governing the intent behind systems delegated to agents. It is organized around three fundamental questions — what is this system trying to achieve, within what constraints, and how will we know it is working? — and four activities: framing, specification, delegation, and validation. It is the load-bearing discipline of an age where code is cheap and judgment is scarce.**

---

## Connections

**This pattern assumes:**
- [Why Architecture Must Become Law](../foundations/06-why-architecture-must-become-law.md)
- [From Translation to Orchestration](../foundations/02-from-translation-to-orchestration.md)

**This pattern enables:**
- [Intent vs. Implementation](02-intent-vs-implementation.md) — the first and most important conceptual distinction
- [What Spec-Driven Development Really Means](../sdd/01-what-sdd-means.md) — SDD as the practice of intent engineering
- [The Modern Engineering Skill Matrix](../operating/01-skill-matrix.md) — what skills this discipline requires

---

*Next: [Intent vs. Implementation](02-intent-vs-implementation.md)*

