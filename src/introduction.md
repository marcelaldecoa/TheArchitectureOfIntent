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

## What is the Architecture of Intent?

**The Architecture of Intent** is the discipline of designing intent — what a delegated system is supposed to do, what it must never do, and how we will know it is working — so that a non-human executor can act on it reliably and a human can validate the action accurately.

Three questions every delegated system has to answer:

1. *What is this system trying to achieve?*
2. *Within what constraints?*
3. *How will we know it is working?*

Five activities answer them:

- **Frame.** Commit to an archetype (Advisor, Executor, Guardian, Synthesizer, or Orchestrator) and to a calibration of the four dimensions — agency, autonomy, responsibility, reversibility — *before any spec is written*. The category is the strongest single predictor of how the system will behave under stress; choosing it deliberately costs an hour and saves a quarter.
- **Specify.** Write the artifact the agent executes against and humans review against. Twelve canonical sections; each section operationalizes one of the four dimensions. The spec is not a requirements document for humans, not a design document for developers — it is an operating instruction for machines that humans can audit.
- **Delegate.** Bind cross-cutting patterns (capability, integration, coordination, safety, observability, testing, state, deployment) by what the spec implies, not by what the team likes building. Pick one of four oversight models — Monitoring, Periodic, Output Gate, or Pre-authorized — proportional to autonomy and reversibility.
- **Validate.** Track four signal metrics. When something fails, diagnose by *fix locus* — which artifact upstream needs to change — across seven failure categories. The diagnosis closes the loop back to the next intent.
- **Evolve.** Turn each diagnosed failure into a structural change — a spec amendment, a manifest tightening, a CI guard, or a framework version bump — never only a prompt patch. The closed-loop discipline is what makes the practice survive the team that built it; it is also where the framework itself versions and where adoption either compounds or quietly degrades.

Three properties make this an *architecture* rather than an *art*:

- **Intent is a designed artifact.** Distinct from *implementation* (what the executor produces), distinct from *requirements* (what stakeholders ask for), distinct from *policy* (what the organization or law requires across all systems). The author of the spec is the author of the system that executes it.
- **Fixes live in structure, not in prompts.** When a spec gap surfaces as a wrong agent action, the durable response amends the spec, the manifest, the oversight model, or the CI guard. A patch in the prompt layer does not compound across teams or runs; a change in the structural layer does. This is the load-bearing discipline of the framework: *structural fixes live in spec, manifest, CI, or platform — never only in the prompt.*
- **Calibration is deliberate.** Each system commits to specific levels of agency and autonomy within its archetype's envelope, rather than getting as much of either as the model technically allows. The framework's worked claim is that the four calibration dimensions are *orthogonal* — independently controllable — and that collapsing them into a single "automation level" loses design space practitioners need.

The framework's primary worked instance is AI agent systems, which are the most-acute current case of delegation. The book defaults to that frame. The same vocabulary — archetypes, dimensions, fix-locus failure categories, signal metrics — applies to other delegated systems too: automated pipelines, organizational delegation, regulated workflows. The book notes generalizations where they hold and stops short of claiming them where they don't.

---

## The framework on one page

The five activities and every load-bearing list in the framework — five archetypes, four calibration dimensions, twelve spec sections, eight pattern categories, four oversight models, seven failure categories, four signal metrics — fit on a single page. The canvas below is that page, with each construct in the activity row where it does work. The rest of the book elaborates this picture; when you get lost, return here.

![The Architecture of Intent on One Page. Three questions every delegated system answers (top); the five activities that work them out — Frame, Specify, Delegate, Validate, Evolve; the load-bearing constructs each activity binds; and the four signal metrics on the right rail that close the loop back to the next intent.](images/architecture-of-intent-canvas.png)

> *The canvas figure above currently shows the v1.x four-activity layout (Frame, Specify, Delegate, Validate). v2.0.0 introduces **Evolve** as a peer fifth activity — the closed-loop discipline by which production findings flow back into spec amendments, framework versioning, and structural change. The canvas redraw to a five-row layout follows in v2.0.0-rc2; the prose, the SUMMARY structure, and the [`CHANGELOG.md`](https://github.com/marcelaldecoa/TheArchitectureOfIntent/blob/main/CHANGELOG.md) already reflect the new shape.*

The book is organized around the five activities. **Part 1 — FRAME** stands up the archetypes, the four dimensions, and composition first-class. **Part 2 — SPECIFY** stands up the canonical spec template, the Composition Declaration and Cost Posture sub-blocks, the Intent Design Session, and the repertoires. **Part 3 — DELEGATE** stands up agent classes, capability and tool-manifest patterns, MCP, oversight, and the patterns that bind to what the spec implies. **Part 4 — VALIDATE** stands up failure diagnosis (the seven Cats), the four signal metrics, evals, red-team protocol, and the safety / observability / testing patterns that emit the validation signal. **Part 5 — EVOLVE** stands up the closed loop, governance, the Adoption Playbook, MVP-AoI, anti-patterns, framework versioning, and DevSquad co-adoption. **Part 6 — REFERENCE** is the catalog: cross-cutting coordination and state patterns, code standards, the legacy worked pilots that v2.0.0 supersedes with the in-practice scenarios, and the appendices.

Each of Parts 1–5 ends with three short *in practice* chapters that walk one of three running scenarios — a customer-support agent, a coding-agent pipeline, and an internal docs Q&A agent built by a DevSquad team — through that activity. You can read the book linearly by phase, or follow one scenario end-to-end across all five activities; the *in practice* chapters cross-link both ways.

---

## What you will have at the end

A pilot you can defend. Concretely, the artifact each row of the canvas above should produce by the time you ship:

1. **An archetype** *(Frame)*. A pre-committed answer to *"what kind of system is this — Advisor, Executor, Guardian, Synthesizer, or Orchestrator?"* — with the agency, autonomy, responsibility, and reversibility profile that follows from that choice.
2. **A spec** *(Specify)*. A written, reviewable artifact in twelve sections that says what the agent must do, what it must never do, what success looks like, and what context it operates in. The agent executes against this. Humans review against this.
3. **An agent** *(Delegate)*. A system prompt, a set of skills, a tool manifest, and a capability boundary that match the archetype, with the cross-cutting patterns (safety, observability, coordination, state) bound to what the spec implies.
4. **An oversight model** *(Delegate)*. A specific answer to *"who reviews what, when, and what triggers escalation?"* — one of Monitoring, Periodic, Output Gate, or Pre-authorized — proportional to the blast radius of the agent's actions.
5. **Metrics that mean something** *(Validate)*. Four signal metrics — spec-gap rate, first-pass validation, cost per correct outcome, and oversight load — that tell you whether the pilot is healthy without manufacturing a dashboard for its own sake.
6. **A deployment plan** *(Validate)*. Canary, rollback, and spec versioning so you can ship without making the change irreversible.
7. **A closed-loop discipline** *(Evolve)*. A spec evolution log, a Discipline-Health Audit cadence, and an explicit commitment that diagnosed failures produce *structural* amendments — not prompt patches — so the practice compounds across teams and survives turnover.

If you finish the book and don't have those seven things, the book has failed you. Tell us what was missing.

---

## Who this is for

This book has one primary reader: the **tech lead, staff engineer, or platform-team member who is on the hook for an agent system going to production**. Everything in the book is aimed at making that person's next decision better.

It is also useful for:

- **Architects and principal engineers** responsible for the structural integrity of systems that agents now help build. Parts 1, 4, and 5 are most relevant.
- **Engineering managers** trying to understand what their teams are actually doing when they "use AI." The Prologue and Part 1 give you the vocabulary; Part 5 gives you what to ask for in reviews.
- **Platform teams** building shared agent infrastructure (MCP servers, spec templates, archetype catalogs). Parts 3, 4, and the Cross-Cutting Patterns section are the spine of your platform.

This book is **not** a tutorial on a specific AI tool, a survey of the model landscape, or a strategy document about whether to adopt AI. It assumes you've already decided to ship something with agents and now need to do it without regret.

---

## How to use it

Two reading modes, both supported.

**Linear.** Start at the Prologue and read straight through. Each Part assumes the previous one. By the end you have the full vocabulary and the full pilot kit. Estimated time: 6–10 hours, but that's not how anyone actually reads a field guide. Read a Part, apply it, come back.

**Work-shaped.** Enter at the decision you're currently stuck on. The [Pattern Index](appendices/pattern-index.md) and the [Glossary](appendices/glossary.md) are your navigation tools. Common entry points:

| If you are... | Start at |
|---------------|----------|
| Just trying to see the framework applied in one screen | [A Miniature Pilot, End-to-End](miniature-pilot.md) |
| Choosing how to structure a new agent system | [Pick an archetype](architecture/02-canonical-intent-archetypes.md) |
| Writing a spec right now | [The canonical spec template](sdd/07-canonical-spec-template.md) |
| Designing oversight for an agent that's about to ship | [Proportional Oversight](agents/06-human-oversight-models.md) |
| Diagnosing a failure | [Failure modes and how to diagnose them](theory/05-failure-as-design-signal.md) |
| Setting up safety controls | [Safety patterns](patterns/safety/prompt-injection-defense.md) |
| Walking one running scenario across all five activities | [Frame in practice — Customer-support](frame/scenarios/customer-support.md), [Coding-agent pipeline](frame/scenarios/coding-pipeline.md), or [Internal docs Q&A (DevSquad)](frame/scenarios/docs-qa.md) |
| Looking at a v1.x worked pilot (legacy) | [Designing an AI Coding Agent](examples/03-coding-agent/README.md) — superseded by the running scenario chapters above |

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

If you want to see the framework applied to one concrete system in one screen before going any further, read [A Miniature Pilot, End-to-End](miniature-pilot.md) next. It is the canvas walked top-to-bottom on a recognizable pilot, with one failure traced back to its fix locus.

If you want the argument for why this discipline matters — what changed structurally about software when code stopped being the bottleneck — read the [Prologue](prologue.md) instead. It's three pages.

If you'd rather just start with the first decision you have to make, go to [Pick an archetype](architecture/02-canonical-intent-archetypes.md).

---

*Continue to [A Miniature Pilot, End-to-End](miniature-pilot.md) to see the framework applied to one concrete system, or jump to the [Prologue](prologue.md) for why this work matters.*
