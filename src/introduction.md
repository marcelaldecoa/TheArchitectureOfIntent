# Introduction

**A Field Guide to Designing and Shipping AI Agent Systems**

---

## Why this book exists

Most teams adopting AI agents discover the same pattern within a quarter:

- The first demo is fast and impressive. The second pilot is slower than expected. By the third, the team is debugging output instead of shipping outcomes.
- Architectural coherence quietly degrades because no one is reviewing what the agent decided to do — only whether the test passed.
- The "AI made a mistake" incident reveals that nobody actually agreed, in writing, what the agent was authorized to do, what it must never do, or who was supposed to catch it when it drifted.
- Adding agents made the team faster on individual tasks and slower at shipping reliable systems. The bottleneck moved, but nobody renegotiated the work to match.

This is a structural problem, not a model problem. The model is doing what it was told. The trouble is that *being told* — what we ask of the agent, what we forbid it, how we check what it did — is the part the team did not learn how to do.

This book is the discipline that addresses that gap. It is a field guide for the people writing the spec, building the agent, and owning the on-call pager when something breaks.

---

## What you will have at the end

A pilot you can defend. Specifically:

1. **An archetype.** A pre-committed answer to *"what kind of system is this — Advisor, Executor, Guardian, Synthesizer, or Orchestrator?"* — with the agency, oversight, and reversibility profile that follows from that choice.
2. **A spec.** A written, reviewable artifact that says what the agent must do, what it must never do, what success looks like, and what context it operates in. The agent executes against this. Humans review against this.
3. **An agent.** A system prompt, a set of skills, a tool manifest, and a capability boundary that match the archetype.
4. **An oversight model.** A specific answer to *"who reviews what, when, and what triggers escalation?"* — proportional to the blast radius of the agent's actions.
5. **Metrics that mean something.** Four signal metrics — spec gap rate, first-pass validation, cost per correct outcome, and oversight load — that tell you whether the pilot is healthy without manufacturing a dashboard for its own sake.
6. **A deployment plan.** Canary, rollback, and spec versioning so you can ship without making the change irreversible.

If you finish the book and don't have those six things, the book has failed you. Tell us what was missing.

---

## Who this is for

This book has one primary reader: the **tech lead, staff engineer, or platform-team member who is on the hook for an agent system going to production**. Everything in the book is aimed at making that person's next decision better.

It is also useful for:

- **Architects and principal engineers** responsible for the structural integrity of systems that agents now help build. Parts 1, 4, and 5 are most relevant.
- **Engineering managers** trying to understand what their teams are actually doing when they "use AI." The Prologue and Part 1 give you the vocabulary; Part 5 gives you what to ask for in reviews.
- **Platform teams** building shared agent infrastructure (MCP servers, spec templates, archetype catalogs). Parts 3, 4, and the Pattern Reference are the spine of your platform.

This book is **not** a tutorial on a specific AI tool, a survey of the model landscape, or a strategy document about whether to adopt AI. It assumes you've already decided to ship something with agents and now need to do it without regret.

---

## How to use it

Two reading modes, both supported.

**Linear.** Start at the Prologue and read straight through. Each Part assumes the previous one. By the end you have the full vocabulary and the full pilot kit. Estimated time: 6–10 hours, but that's not how anyone actually reads a field guide. Read a Part, apply it, come back.

**Work-shaped.** Enter at the decision you're currently stuck on. The [Pattern Index](appendices/pattern-index.md) and the [Glossary](appendices/glossary.md) are your navigation tools. Common entry points:

| If you are... | Start at |
|---------------|----------|
| Choosing how to structure a new agent system | [Pick an archetype](architecture/02-canonical-intent-archetypes.md) |
| Writing a spec right now | [The canonical spec template](sdd/07-canonical-spec-template.md) |
| Designing oversight for an agent that's about to ship | [Proportional Oversight](agents/06-human-oversight-models.md) |
| Diagnosing a failure | [Failure modes and how to diagnose them](theory/05-failure-as-design-signal.md) |
| Setting up safety controls | [Safety patterns](patterns/safety/prompt-injection-defense.md) |
| Looking at a worked pilot | [Designing an AI Coding Agent](examples/03-coding-agent/README.md) (recommended starting example) — or [How to use these examples](examples/00-how-to-use.md) for the full set |

---

## What the book does not promise

It does not promise that following these patterns guarantees a successful pilot. Models change, requirements shift, and some failures are genuinely model-level and unfixable by better specs. What this book gives you is the smallest set of structures that make a pilot's failures *diagnosable* and *correctable* rather than mysterious.

It does not promise that every pattern applies to every team. Regulated industries (healthcare, finance, defense) have compliance requirements that go beyond what's covered here. Multi-organizational agent systems — where agents from different orgs interact — have governance problems this framework does not solve. Cost-benefit analysis for adopting these practices depends on factors that vary too widely to generalize.

It does not promise to settle every open question in the field. *How precise is "precise enough"?* *What happens when model capability outpaces governance?* *Can intent engineering scale to truly autonomous systems?* These questions are real and unresolved. This book stakes out a working position; treat it as something to test against your own context, not as final word.

---

## Honest scope: what this book is, and what it isn't

This book's strongest contribution is a **design vocabulary and a diagnostic discipline**: archetypes, the four dimensions, the failure taxonomy, the spec template, the oversight models. Teams that adopt it report that their *conversations* about agent systems get sharper — which is exactly what you'd expect when a shared vocabulary replaces ad-hoc framing.

It is **not** a complete technical playbook. Specifically, the book is light on:

- **Prompt caching as architecture** (covered briefly in [Cost and Latency Engineering](operating/09-cost-and-latency.md); deserves more depth for any system at 100+ runs/day).
- **Model-tier selection** under specific budget and latency constraints — the [Model-Tier Quick-Select Card](appendices/model-tier-card.md) gives a decision matrix; the underlying chapter goes deeper.
- **Multi-tenant fleet governance** — when 50 teams deploy agents against shared infrastructure, spec evolution and constraint-library merging become harder problems than this book solves.
- **CI/CD wiring details** — when does the eval suite gate a merge versus alert versus observe? The disciplines are described; the specific platform integration is not.

Read the book for the vocabulary, the structural patterns, and the failure diagnosis. Bring your own platform expertise for the wiring.

---

## A note on style

This is a working book, not a literary one. Chapters are short, the vocabulary is consistent, and the templates are meant to be copied. Where a pattern can be stated in two pages, it is. Where a pattern needs a diagram, a table, or a worked example, it gets one. There is no philosophical preamble, because the reader of this book is presumed to already be working on the problem and to need the tools, not the argument.

If you want the argument anyway — why this discipline matters, what changed structurally about software when code stopped being the bottleneck — read the [Prologue](prologue.md) next. It's three pages.

If you'd rather just start with the first decision you have to make, go to [Pick an archetype](architecture/02-canonical-intent-archetypes.md).

---

*Continue to the [Prologue](prologue.md) for the short version of why this work matters, or jump straight to [How to read this book](how-to-read.md).*
