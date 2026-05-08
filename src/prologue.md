# Prologue

**What changed, and what's at stake**

---

This is the short version of why this book exists. If you want the long version, read someone else's book — there are several good ones. This one is for people who already know they need to ship an agent system and now need to do it without regret.

---

## What changed

For most of computing history, the rate-limiting step in software was **translation**: business intent was ambiguous, machines were literal, and the developer was the bridge. The whole edifice of software engineering — requirements documents, design patterns, code reviews, hiring pipelines, career ladders — was built around the scarcity of people who could reliably do that translation.

Code generation is no longer scarce. Models can produce syntactically correct, structurally sound code at machine speed. The bottleneck moved.

It moved upstream, to the things teams used to do imperfectly because code was the expensive part:

- **Framing** — what problem are we actually solving?
- **Constraints** — what must never happen?
- **Scope** — what is genuinely out of scope?
- **Success** — what does *done* mean, measurably?
- **Accountability** — who is responsible for what outcome?

These questions existed before agents. They were addressed loosely. A skilled developer compensated for a vague requirement by exercising judgment late in the process. The compensation was invisible — nobody measured it — but it was the real reason senior engineers were valuable.

That compensation mechanism does not exist when an agent is doing the implementation. The agent executes the spec with high fidelity and without the compensatory judgment. Every gap in the spec gets filled with probability, at scale, across systems that interact in ways no single conversation can anticipate.

---

## What's at stake

Three structural risks emerge when teams add agents without changing how they work:

**1. Capability scales faster than judgment.**  Agent capability grows by model release. Human judgment about *when* and *how* to use that capability grows by experience and reflection — much more slowly. Any domain where power scales faster than judgment produces predictable disasters. Output increases, quality becomes inconsistent in ways that are hard to diagnose, architectural coherence erodes, and technical debt accumulates exactly where no human exercised judgment.

**2. Authorship gets murky.**  When a human wrote the code, the decision trail was legible. When an agent writes code from a spec written by one person, configured by a platform team, running on a model trained on billions of documents, and validated by tests written by another agent — *who authored the harm* when something goes wrong? The answer is not "the AI." The answer is the chain of human decisions that allocated agency to the agent. The question is whether that chain is legible, or whether it dissolves into "the AI did it."

**3. Architecture stops being enforceable through culture.**  In slow systems, architectural coherence is preserved through code review and shared understanding. In fast systems, agents make thousands of small architectural choices a day, and informal convention cannot keep up. Architecture has to become *encoded* — in archetypes, in specs, in constraints that apply whether or not anyone remembers to apply them. The alternative is invisible drift until the cost of correction is enormous.

---

## What this book gives you

A discipline for the specific problem the existing frameworks weren't designed for: **how to specify, govern, and oversee the delegation of work to AI agents at scale.**

It is not a replacement for Agile, DevOps, or systems thinking. It runs *inside* those practices. Sprints still happen. CI/CD still ships. The difference is that the spec — not the conversation, not the ticket, not the pull request — becomes the primary artifact of engineering judgment.

Specifically, the book gives you:

- **A vocabulary** that lets a team distinguish between intent and implementation, agency and autonomy, reversibility and risk, and reason precisely about each.
- **Five archetypes** — Advisor, Executor, Guardian, Synthesizer, Orchestrator — that pre-commit a system to a category before any specific behavior is designed.
- **A canonical spec template** that the agent executes against and humans review against.
- **Four oversight models** matched to agency level and reversibility.
- **A failure taxonomy** with six categories and a diagnostic protocol that lets you fix what actually broke instead of patching the output.
- **Four signal metrics** to tell you whether your pilot is healthy.
- **Two worked end-to-end pilots** to calibrate against.

---

## A short note on responsibility

A specification is not a neutral technical document. Every constraint in it is a commitment about how the people affected by the system will be treated. Every gap in it is a decision delegated to probability. When the agent acts, the author of the spec authored the action.

You don't have to take this as philosophy. Take it as engineering: the more powerful the system, the more load-bearing the specification, and the more seriously the spec author has to treat what's written and what's missing. Everything else in this book follows from that.

---

*Continue to [Part 1: Decisions](architecture/02-canonical-intent-archetypes.md) — pick an archetype.*
