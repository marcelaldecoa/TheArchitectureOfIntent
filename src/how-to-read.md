# How to Read This Book

---

This book is structured as a **field guide**, organized in the order in which the decisions actually have to be made.

---

## The Six Parts

| Part | What you do here |
|------|------------------|
| **Prologue** | The short version of what changed and what's at stake. Three pages. |
| **1. Decisions** | The decisions you commit to *before* you start: archetype, calibration, failure anticipation, intent vs. implementation. |
| **2. The Spec** | What spec-driven development means and how to write the spec the agent will execute against. |
| **3. The Agent** | What agents are structurally, what capabilities they need, and how to bound them via tools and MCP. |
| **4. Oversight, Safety & Operations** | Proportional oversight, safety patterns, retry, observability, and spec conformance testing. |
| **5. Ship** | Canary, rollback, spec versioning, governance cadence, the four signal metrics, intent review. |
| **6. Worked Pilots** | Two end-to-end examples calibrated against the framework. |

After Part 6 the book becomes reference material: a flat **Cross-Cutting Patterns** section for the coordination and state patterns you'll consult once your pilot is running, code standards by language, and **Appendices** (glossary, archetype card, quick references, pattern index). Most of the framework's patterns live inside Parts 3–5 alongside the chapters they relate to; this section gathers the cross-cutting ones that don't tie to a specific archetype or agent class.

---

## Two reading modes

**Linear.** Read straight through. Each part assumes the previous one. By the end you have all six things on the introduction's punch list — archetype, spec, agent, oversight, metrics, deployment plan.

**Work-shaped.** Enter at the decision you're currently stuck on. Use the table below, the [Pattern Index](appendices/pattern-index.md), or the [Glossary](appendices/glossary.md). Then radiate outward through the Connections section at the bottom of each chapter.

| If you are... | Start at |
|---------------|----------|
| Wanting the framework on one screen | [A Miniature Pilot, End-to-End](miniature-pilot.md) |
| Structuring a new agent system | [Pick an archetype](frame/02-canonical-intent-archetypes.md) |
| Writing a spec | [The canonical spec template](specify/07-canonical-spec-template.md) |
| Designing oversight | [Proportional Oversight](delegate/06-human-oversight-models.md) |
| Diagnosing a failure | [Failure modes and how to diagnose them](foundations/05-failure-as-design-signal.md) |
| Setting up safety controls | [Prompt injection defense](patterns/safety/prompt-injection-defense.md), [output validation](patterns/safety/output-validation-gate.md) |
| Choosing an oversight cadence | [Proportional Governance](evolve/04-governance.md) |
| Defining what to measure | [Four Signal Metrics](validate/06-metrics.md) |
| Looking at a real example | One of the v2.0.0 [running scenarios](appendices/reading-paths.md) (recommended) — or the [Legacy v1.x Worked Pilots Archive](appendices/legacy-pilots.md) for the v1.x set |
| Confused about a term | [Glossary](appendices/glossary.md) |

---

## Chapter format

Each chapter is short and follows a consistent shape so you can scan it:

1. **Context** — Where this pattern applies and what it assumes.
2. **The Problem** — The specific tension this chapter resolves.
3. **The Solution** — The structure, with examples and tables. Where useful, a worked anti-pattern.
4. **Therefore** — The resolution in one bold sentence. Many readers read only this.
5. **Connections** — What this chapter assumes, and what it enables next.

Some chapters also include code examples, spec fragments, or named anti-patterns.

---

## About the code

Code in this book is **authoritative by intent, not by completeness**. Snippets are written to the patterns described in the Cross-Cutting Patterns section and code standards, and are meant to anchor agent behavior — structures that can be extended, not copied verbatim.

Languages covered: C# / .NET, TypeScript / Node, Python, REST API design, infrastructure as code.

Every code example includes:
- A comment naming the pattern it instantiates
- The spec constraint it satisfies
- The boundary it must not cross

---

## About the archetypes

The five archetypes — Advisor, Executor, Guardian, Synthesizer, Orchestrator — are the core vocabulary of this book. They appear in specs, in agent instructions, in design reviews, and in governance conversations.

If you encounter a reference to "the Executor archetype" or "the Guardian pattern" and don't recognize it, the [Archetype Quick-Select Card](appendices/archetype-card.md) gives you a one-page summary. The full deep-dives live in [`frame/archetypes/`](frame/archetypes/advisor.md).

---

*You're ready. Begin with the [Prologue](prologue.md), or jump to [Pick an archetype](frame/02-canonical-intent-archetypes.md).*
