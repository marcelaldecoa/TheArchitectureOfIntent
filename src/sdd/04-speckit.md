# Pattern 4.4 — SpecKit

**Part IV: Spec-Driven Development** · *4 of 7*

---

> *"A tool that enforces good practice is worth more than a guideline that recommends it."*

---

## Context

You are implementing Spec-Driven Development on a team that uses AI coding assistants — GitHub Copilot or similar. You want the SDD lifecycle to happen in the same environment where code is written, not in a separate document management system. You want the spec to live next to the code.

SpecKit is a concrete, opinionated implementation of SDD designed for that environment. This pattern explains how SpecKit aligns with the Architecture of Intent, where it fits in the lifecycle, and what its use reveals that raw SDD practice often obscures.

This pattern assumes [The Spec Lifecycle](03-spec-lifecycle.md) and all preceding patterns.

---

## The Problem

SDD as a discipline and SDD as a practice are two different things. The discipline is well-defined: write the spec before code, make specs testable, fix the spec on failure, evolve specs as living documents. The practice depends on tooling, team habits, and where the spec lives relative to the work.

Without tooling that embeds the spec into the development workflow, SDD degrades into documentation that engineers write before PRs and nobody reads. The spec is written, filed, and forgotten. The feedback loop — Phase 5 flowing back into Phase 2 — never closes because there is no mechanism that keeps the spec adjacent to the agent's execution context.

SpecKit solves this specific problem. It puts the spec in the repository, in the codebase, and in the agent's context. It makes the spec executable, not just readable.

---

## Forces

- **Discipline vs. integration.** SDD as discipline is understood, but practicing it requires making specs central to the workflow. Without tooling, specs are separate documents, easy to ignore.
- **Automation vs. clarity.** SpecKit automates some drafting. But automation can hide what is being decided. The spec must remain human-readable even when produced by automation.
- **Constitution vs. flexibility.** The constitution enforces project-wide constraints. This is powerful but can become inflexible. Systems with special requirements need override mechanisms.
- **Adoption vs. overhead.** Adding SpecKit increases the number of concepts developers need to know. Yet total time cost (spec + code + rework) should decrease.

---

## The Solution

### What SpecKit Is

SpecKit is an open toolkit built around a set of agent instructions that guide AI assistants through the SDD lifecycle. It operates through structured commands — slash commands in the agent prompt — that correspond to phases in the spec lifecycle.

The primary commands:

| Command | Phase | What it does |
|---------|-------|--------------|
| `/specify` | Phase 2 | Guides the agent to produce a structured spec from a problem description |
| `/speckit.clarify` | Phase 3 | Surfaces ambiguities and gaps in an existing spec |
| `/speckit.constitution` | Constitutional | Loads project-wide rules, constraints, and standards that apply to all specs |

SpecKit's model: the agent is the instrument, the spec is the score, and the `/speckit.constitution` is the key signature that tells the agent what rules apply before any note is played.

### How SpecKit Maps to the Architecture of Intent

SpecKit aligns with the SDD lifecycle at three levels:

**Level 1: The lifecycle level.** SpecKit's command sequence (`/specify` → `/speckit.clarify` → execute → review) maps directly to Phases 2–5 of the SDD lifecycle. For teams using SpecKit, Phase 1 (intent capture) is the natural language input to `/specify`. The agent's clarifying questions are Phase 3. Execution is the agent producing code from the spec. Validation is the human PR review against the spec.

**Level 2: The spec template level.** SpecKit's spec output aligns with the categories in the canonical spec template: problem statement, desired outcome, scope, functional intent, constraints, acceptance criteria. SpecKit does not prescribe the same section structure verbatim, but teams using SpecKit should augment its output with the canonical template's invariant and agent-execution sections where relevant.

**Level 3: The constitutional level.** `/speckit.constitution` maps to the archetype layer at the top of the control hierarchy. It is the place where cross-system constraints are declared — the things that are true for all specs in a project. In the Architecture of Intent, this is where archetype defaults, organizational invariants, and non-negotiables live.

### SpecKit as the Architecture of Intent's Execution Engine

When a team has:
- Archetype definitions (from Part III)
- A constitutional spec layer (via `/speckit.constitution`)
- A canonical spec template (from Pattern 4.7)
- The SDD lifecycle (from Pattern 4.3)

...SpecKit is the tooling that makes all three work together in a development workflow.

The practical setup:

```markdown
<!-- .speckit.constitution (in the repository root) -->

# Project Constitution

## Archetype Defaults

All agent systems in this repository are governed by the archetype 
framework defined in [link to pattern 3.1–3.4]. New agent systems 
must include an explicit Archetype section in their spec.

## Invariants That Apply Across All Specs

1. No system writes to production databases without an approval gate.
2. No system stores PII without explicit data classification.
3. All outputs of Executor-class systems are logged before application.
4. Reversibility of all R3–R4 actions must be addressed in the spec.

## Standards That Apply to All Generated Code

- [Link to language-specific code standards from Part VI]
- Test coverage requirement: all acceptance criteria must have tests.
- Error handling: structured error types only; no untyped exceptions.
```

With this constitution loaded, any spec produced by `/specify` in this repository inherits these constraints automatically. The agent doesn't need to be reminded of them in each spec — they are pre-committed at the constitutional level.

### Where SpecKit Extends the Architecture of Intent

SpecKit adds something the Architecture of Intent's pure spec discipline does not give you out of the box: **tooling-enforced starting points**.

In a pure SDD practice without tooling, whether a spec gets written depends on team habit. SpecKit makes writing a spec the path of least resistance — the `/specify` command is the entry point to agent-assisted coding, not a separate step before it. The spec is produced as part of starting the work.

This is significant. Behavioral economics shows that the default path determines most outcomes. SpecKit makes the spec-first path the default. Teams that adopt SpecKit practice SDD more consistently than teams that have the SDD discipline documented but not tooled.

### Where SpecKit Needs Augmentation

SpecKit is excellent at Phase 2–3 (specification and clarification) and at making the spec machine-executable. It is intentionally minimal about several things that the Architecture of Intent treats as critical:

**Living specs and evolution tracking.** SpecKit supports iterative refinement via slash commands, but it does not prescribe a spec evolution log. Teams should add the evolution log section from the canonical spec template.

**Explicit scope boundaries and invariants.** SpecKit encourages constraints via the constitution but does not foreground out-of-scope declarations and invariants as first-class spec sections. Teams should add these explicitly.

**Archetype declaration.** SpecKit does not know about the archetype framework. For agent systems, teams should add the archetype section to every spec produced by `/specify`. This is most easily done by including the archetype template fragment in the `/speckit.constitution`.

**Validation checklist.** SpecKit's model assumes the human reviewing the PR is the validator. The Architecture of Intent's validation checklist makes this explicit: *what are the specific clauses being checked?* Teams should treat PR review as spec-conformance review, not aesthetic review.

The augmentation of SpecKit with these additions is not a rejection of SpecKit. It is SpecKit operating as designed — a minimal core that teams customize to their needs. The Architecture of Intent provides the framework for that customization.

### The Organizational Argument for SpecKit

For teams that resist SDD because it "adds overhead before you can start," SpecKit provides the pragmatic counter: the overhead is front-loaded and short, the rework reduction is back-loaded and large.

The typical pattern without SDD:
- Write a prompt (2 minutes)
- Get output (1 minute)
- Correct output (20–60 minutes, often more)
- Repeat 3–5 times before the output is acceptable

With SpecKit:
- `/specify` produces a draft spec (5 minutes)
- Review and refine spec (10 minutes)
- Execute (1 minute)
- Validate against spec (10 minutes)
- Done

The total time is similar; the rework rate is dramatically lower; the spec is now a reusable organizational asset; and the knowledge of what was decided lives in the repository, not in someone's memory.

---

## Resulting Context

After applying this pattern:

- **Spec-first becomes the default path.** By making the spec command the entry point, SpecKit makes writing a spec the easiest choice.
- **Constitution propagates automatically.** Project-wide constraints are loaded and inherited by every spec produced. Teams do not have to remember to include them.
- **Specs live next to code.** By keeping specs in the repository, version control applies to specs the same way as code.
- **Teams can customize SDD to their practice.** SpecKit is intentionally minimal. Teams extend it with their own governance needs.

---

## Therefore

> **SpecKit is a practical implementation of Spec-Driven Development that embeds the spec lifecycle into the coding workflow via structured agent commands. Its `/specify`, `/clarify`, and `/constitution` commands map directly to the SDD lifecycle phases. Augmented with archetype declarations, scope invariants, and the spec evolution log, SpecKit becomes the execution engine for the Architecture of Intent's complete governance model.**

---

## Connections

**This pattern assumes:**
- [The Spec Lifecycle](03-spec-lifecycle.md)
- [Constitutional Archetypes](../architecture/01-archetypes-as-constitutional-law.md)
- [The Spec as Control Surface](02-specs-as-control-surfaces.md)

**This pattern enables:**
- [Writing for Machine Execution](05-writing-specs-for-agents.md)
- [The Canonical Spec Template](07-canonical-spec-template.md)
- [Spec Template Library](../repertoires/03-spec-template-library.md)

**External reference:** [github/spec-kit](https://github.com/github/spec-kit) *(verify current availability — tooling evolves rapidly)*

---

*Next: [Writing for Machine Execution](05-writing-specs-for-agents.md)*


