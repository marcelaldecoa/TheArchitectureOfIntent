# What is the Architecture of Intent?

**Part 0 — Foundations**

---

> *"Three questions, five activities, one canvas. Read this once; come back when you get lost."*

---

## Context

This is the one-page definition of the framework. It opens **Part 0 — Foundations** because every other chapter in the book references the vocabulary it establishes — the three questions, the five activities, the three properties that make the discipline an *architecture* rather than an *art*. A reader can decline to read the rest of the book; this chapter is the minimum the framework asks you to keep.

If you're skimming, the canvas figure in the [Introduction's *framework on one page* section](../introduction.md#the-framework-on-one-page) is the ~15-second version. If you want the canonical statement, read on.

---

## The framework, in one paragraph

**The Architecture of Intent** is the discipline of designing intent — what a delegated system is supposed to do, what it must never do, and how we will know it is working — so that a non-human executor can act on it reliably and a human can validate the action accurately.

---

## Three questions every delegated system has to answer

1. *What is this system trying to achieve?*
2. *Within what constraints?*
3. *How will we know it is working?*

These three questions are the conceptual minimum. A team that cannot answer them does not yet have an Architecture of Intent for the system they are about to build, regardless of whether they have a spec, a model, a deployment plan, or a Slack channel named after the project. The discipline begins by answering them.

![The three questions every delegated system has to answer, and the five activities (Frame, Specify, Delegate, Validate, Evolve) that answer them. Read the rest of the chapter, then return to this picture when you get lost. Every subsequent chapter elaborates one row.](../images/foundations-three-questions.png)

---

## Five activities that answer them

- **Frame.** Commit to an archetype (Advisor, Executor, Guardian, Synthesizer, or Orchestrator) and to a calibration of the four dimensions — agency, autonomy, responsibility, reversibility — *before any spec is written*. The category is the strongest single predictor of how the system will behave under stress; choosing it deliberately costs an hour and saves a quarter.
- **Specify.** Write the artifact the agent executes against and humans review against. Twelve canonical sections; each section operationalizes one of the four dimensions. The spec is not a requirements document for humans, not a design document for developers — it is an operating instruction for machines that humans can audit.
- **Delegate.** Bind cross-cutting patterns (capability, integration, coordination, safety, observability, testing, state, deployment) by what the spec implies, not by what the team likes building. Pick one of four oversight models — Monitoring, Periodic, Output Gate, or Pre-authorized — proportional to autonomy and reversibility.
- **Validate.** Track four signal metrics. When something fails, diagnose by *fix locus* — which artifact upstream needs to change — across seven failure categories. The diagnosis closes the loop back to the next intent.
- **Evolve.** Turn each diagnosed failure into a structural change — a spec amendment, a manifest tightening, a CI guard, or a framework version bump — never only a prompt patch. The closed-loop discipline is what makes the practice survive the team that built it; it is also where the framework itself versions and where adoption either compounds or quietly degrades.

The activities map 1:1 to the book's five Parts (Part 1 — FRAME through Part 5 — EVOLVE). Each Part ends with three *in practice* chapters — one per running scenario — that walk a real team through the activity for one specific system.

---

## Three properties that make this an *architecture*, not an *art*

- **Intent is a designed artifact.** Distinct from *implementation* (what the executor produces), distinct from *requirements* (what stakeholders ask for), distinct from *policy* (what the organization or law requires across all systems). The author of the spec is the author of the system that executes it.
- **Fixes live in structure, not in prompts.** When a spec gap surfaces as a wrong agent action, the durable response amends the spec, the manifest, the oversight model, or the CI guard. A patch in the prompt layer does not compound across teams or runs; a change in the structural layer does. This is the load-bearing discipline of the framework: *structural fixes live in spec, manifest, CI, or platform — never only in the prompt.*
- **Calibration is deliberate.** Each system commits to specific levels of agency and autonomy within its archetype's envelope, rather than getting as much of either as the model technically allows. The framework's worked claim is that the four calibration dimensions are *orthogonal* — independently controllable — and that collapsing them into a single "automation level" loses design space practitioners need.

---

## Where the framework applies

The framework's primary worked instance is AI agent systems, which are the most-acute current case of delegation. The book defaults to that frame. The same vocabulary — archetypes, dimensions, fix-locus failure categories, signal metrics — applies to other delegated systems too: automated pipelines, organizational delegation, regulated workflows. The book notes generalizations where they hold and stops short of claiming them where they don't.

---

## Where to go next

- For the visual summary, see the [framework on one page](../introduction.md#the-framework-on-one-page) in the Introduction.
- For the foundations the rest of the book stands on, continue reading **Part 0** in order: [Intent vs. Implementation](02-intent-vs-implementation.md) → [Calibration](03-agency-autonomy-responsibility.md) → [Failure as a Design Signal](05-failure-as-design-signal.md) → [What Changes for the Senior Engineer](08-what-changes-for-senior-engineers.md) → [The Intent Design Session](07-intent-design-session.md).
- For the working ritual that turns the vocabulary into practice for one specific system, jump ahead to [The Intent Design Session](07-intent-design-session.md).
- For a worked pilot in one screen, see [A Miniature Pilot, End-to-End](../miniature-pilot.md).
- To read along a single scenario rather than linearly, see the [Reading Paths](../appendices/reading-paths.md) appendix.
