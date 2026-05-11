# How to Read This Book

---

This book is structured as a **field guide**, organized in the order in which the decisions actually have to be made.

---

## The eight Parts

| Part | What you do here |
|------|------------------|
| **Prologue / Introduction / How to read** | What changed, what's at stake, and how to navigate the book. |
| **0. Foundations** | The vocabulary: what AoI is, intent vs. implementation, the four calibration dimensions, the seven failure categories, the Intent Design Session. Read once; come back when you get lost. *Chapter 08 — What Changes for the Senior Engineer is the one Foundations chapter with an audience-specific scope; skip on first read if you are not personally navigating the transition.* |
| **1. Frame** | Pick an archetype, calibrate the four dimensions, compose archetypes, govern multi-agent systems. The decision you commit to *before* writing a spec. |
| **2. Specify** | Spec-driven development, the canonical 12-section template, the Composition Declaration and Cost Posture sub-blocks, the Living Spec, ADRs, SpecKit, the repertoires. |
| **3. Delegate** | What agents are, autonomy vs. agency, the executor model, least capability, agent skills, agent classes (coding, computer-use), MCP, oversight models, capability / integration / coordination patterns. |
| **4. Validate** | Intent review, the four signal metrics, evals, red-team protocol, safety / observability / testing patterns. |
| **5. Evolve** | The closed loop, the anti-pattern catalog, framework versioning, the Minimum Viable Architecture of Intent, deployment patterns (canary, rollback, spec versioning, model-upgrade validation, deprecation). |
| **6. Operations** | The sustaining-ops layer that runs alongside the five activities: proportional governance, cost and latency engineering, cacheable prompt architecture, production telemetry, the Adoption Playbook, DevSquad mapping and co-adoption. Not a sixth activity — the day-to-day machinery that keeps the discipline durable. |
| **7. Reference** | Cross-cutting coordination and state patterns, code standards by language, and the appendices (glossary, pattern index, reading paths, companion paper, legacy pilots archive, references, quick-select cards). |

Each of Parts 1–5 ends with three *in practice* chapters that walk one of three running scenarios (a customer-support agent, a coding-agent pipeline, an internal docs Q&A agent built by a DevSquad team) through that activity, so you can read by Part or by scenario.

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
| Choosing an oversight cadence | [Proportional Governance](operate/01-governance.md) |
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
