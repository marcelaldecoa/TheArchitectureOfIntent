# Reading Paths

**Appendices**

---

> *"A field guide is a book you re-enter, not a book you finish."*

---

This appendix is a navigation aid. The book is structured to support more than one reading order — and in practice, the reader who tries to read it linearly cover-to-cover gets less out of it than the reader who picks an entry point that matches what they're working on. This appendix lists the entry points the book is designed to support, with the chapters and the order for each.

The default recommendation is **the linear field-guide read** below, but only because it produces the most-complete vocabulary in one pass. If you have a system you're shipping in the next quarter, the **scenario reads** are operationally more useful.

---

## 1. The linear field-guide read

> *Recommended for: serious adoption; readers who want the full vocabulary in one pass.*  
> *Time: 6–10 hours, but read a Part, apply it, come back.*

Top-to-bottom by Part:

1. **Foreword** — [Prologue](../prologue.md)
2. **Introduction** — [Why this book exists, and the framework on one page](../introduction.md), [A Miniature Pilot, End-to-End](../miniature-pilot.md), [How to Read This Book](../how-to-read.md)
3. **Part 0 — FOUNDATIONS** — top-to-bottom: [What is the Architecture of Intent?](../foundations/01-what-is-aoi.md), [Intent vs. Implementation](../foundations/02-intent-vs-implementation.md), [Calibrate A/A/R/R](../foundations/03-agency-autonomy-responsibility.md), [Failure Modes (Cat 1–7)](../foundations/05-failure-as-design-signal.md), [What Changes for the Senior Engineer](../foundations/08-what-changes-for-senior-engineers.md), [The Intent Design Session](../foundations/07-intent-design-session.md). The conceptual preface every other Part stands on.
4. **Part 1 — FRAME** — top-to-bottom; ends with the three *Frame in practice* scenario chapters
5. **Part 2 — SPECIFY** — top-to-bottom; ends with the three *Specify in practice* scenario chapters
6. **Part 3 — DELEGATE** — top-to-bottom; ends with the three *Delegate in practice* scenario chapters
7. **Part 4 — VALIDATE** — top-to-bottom; ends with the three *Validate in practice* scenario chapters
8. **Part 5 — EVOLVE** — top-to-bottom; ends with the three *Evolve in practice* scenario chapters
9. **Part 7 — REFERENCE** — browse rather than read linearly

---

## 2. Scenario read — Customer-support agent (S1)

> *Recommended for: teams shipping an Executor-flavored agent (action-taking, with bounded scope, with structural invariants).*  
> *Time: ~2 hours; ~25 pages of prose plus the conceptual chapters each scenario chapter binds to.*

The customer-support scenario walks a 5-person team across 90 days from Frame through Evolve. The five chapters share a recognizable team — Maya, Ari, Sam, Jordan, Priya — and a concrete system (a tier-1 support agent at a mid-stage SaaS).

| Phase | Chapter |
|---|---|
| 1. Frame | [Frame in practice — Customer-support agent](../frame/scenarios/customer-support.md) |
| 2. Specify | [Specify in practice — Customer-support agent](../specify/scenarios/customer-support.md) |
| 3. Delegate | [Delegate in practice — Customer-support agent](../delegate/scenarios/customer-support.md) |
| 4. Validate | [Validate in practice — Customer-support agent](../validate/scenarios/customer-support.md) |
| 5. Evolve | [Evolve in practice — Customer-support agent (90 days post-launch)](../evolve/scenarios/customer-support.md) |

After the five chapters, optionally pick up the conceptual chapters each scenario binds to — listed at the end of every scenario chapter under *Conceptual chapters this scenario binds to*. Read those after the scenario, not before; they make more sense once the operational shape is clear.

The companion paper's §5 condenses this scenario into ~6 pages of paper-grade prose if you'd prefer the academic-voice version. The paper PDF is at [`paper/architecture-of-intent.pdf`](https://github.com/marcelaldecoa/TheArchitectureOfIntent/blob/main/paper/architecture-of-intent.pdf) in the repository.

---

## 3. Scenario read — Coding-agent pipeline (S2)

> *Recommended for: teams shipping a coding agent or any system with mode-switching composition.*  
> *Time: ~2 hours.*

The coding-agent scenario walks a 4-person platform team across 17 services and 90 days. It shows **Pattern E (mode-switching) composition** — the framework's strongest case for composition first-class — at scenario grain, with structural CI guards as the load-bearing form of Cat 1 amendments.

| Phase | Chapter |
|---|---|
| 1. Frame | [Frame in practice — Coding-agent pipeline](../frame/scenarios/coding-pipeline.md) |
| 2. Specify | [Specify in practice — Coding-agent pipeline](../specify/scenarios/coding-pipeline.md) |
| 3. Delegate | [Delegate in practice — Coding-agent pipeline](../delegate/scenarios/coding-pipeline.md) |
| 4. Validate | [Validate in practice — Coding-agent pipeline](../validate/scenarios/coding-pipeline.md) |
| 5. Evolve | [Evolve in practice — Coding-agent pipeline](../evolve/scenarios/coding-pipeline.md) |

Pair with paper §4.3 (*Coding agents*) for the agent-class deep-dive that this scenario instantiates — see [`paper/architecture-of-intent.pdf`](https://github.com/marcelaldecoa/TheArchitectureOfIntent/blob/main/paper/architecture-of-intent.pdf).

---

## 4. Scenario read — Internal docs Q&A (S3, DevSquad-built)

> *Recommended for: teams shipping a Synthesizer-flavored system, teams using Microsoft DevSquad Copilot, or teams whose primary win is **discovering** what they don't have rather than answering what they do.*  
> *Time: ~2 hours.*

The docs-qa scenario walks a 4-person docs-platform team building an internal docs Q&A agent for ~200 internal engineers, using DevSquad Copilot's eight-phase iterative cycle. It shows the **Synthesizer + Advisor composition**, the **citation-grounding discipline** as the structural defense against the worst Synthesizer failure, and the **AoI ↔ DevSquad activity mapping** inline at every phase. The scenario's most-important framing decision is committing to *docs-gap-finding rate as a positive signal* — the agent's most-valuable accidental product is revealing real coverage gaps in the docs.

| Phase | Chapter |
|---|---|
| 1. Frame | [Frame in practice — Internal docs Q&A](../frame/scenarios/docs-qa.md) |
| 2. Specify | [Specify in practice — Internal docs Q&A](../specify/scenarios/docs-qa.md) |
| 3. Delegate | [Delegate in practice — Internal docs Q&A](../delegate/scenarios/docs-qa.md) |
| 4. Validate | [Validate in practice — Internal docs Q&A](../validate/scenarios/docs-qa.md) |
| 5. Evolve | [Evolve in practice — Internal docs Q&A](../evolve/scenarios/docs-qa.md) |

Pair with [Mapping the Framework to the DevSquad 8-Phase Cadence](../operate/06-devsquad-mapping.md) and [Co-adoption with DevSquad Copilot](../operate/07-co-adoption-with-devsquad.md) for the framework-level vocabulary mapping that this scenario instantiates at scenario grain.

---

## 5. The conceptual-only read

> *Recommended for: readers evaluating the framework before adopting; reviewers; people writing about the framework.*  
> *Time: ~3 hours of focused reading.*

Skip the scenarios entirely. The simplest version is **read all of Part 0 and a few additional binding chapters**:

1. [Prologue](../prologue.md) and [Introduction](../introduction.md) — the framing
2. **All of Part 0 — FOUNDATIONS** in order: [What is the Architecture of Intent?](../foundations/01-what-is-aoi.md), [Intent vs. Implementation](../foundations/02-intent-vs-implementation.md), [Calibrate A/A/R/R](../foundations/03-agency-autonomy-responsibility.md), [Failure Modes (Cat 1–7)](../foundations/05-failure-as-design-signal.md), [What Changes for the Senior Engineer](../foundations/08-what-changes-for-senior-engineers.md), [The Intent Design Session](../foundations/07-intent-design-session.md)
3. [Pick an Archetype](../frame/02-canonical-intent-archetypes.md) and the five archetype pages it links to — the taxonomy in detail
4. [Composing Archetypes](../frame/05-composing-archetypes.md) — composition first-class
5. [The Canonical Spec Template](../specify/07-canonical-spec-template.md) — the 12-section structure with the Composition Declaration and Cost Posture sub-blocks
6. [Proportional Oversight](../delegate/06-human-oversight-models.md) — the four oversight models
7. [Four Signal Metrics](../validate/06-metrics.md) — the four signals
8. [The Closed Loop: From Failures to Spec Amendments](../evolve/01-closed-loop.md) — the discipline that opens Part 5 — Evolve

After this read you have the framework's full vocabulary without the operational color the scenarios provide. The companion paper at [`paper/architecture-of-intent.pdf`](https://github.com/marcelaldecoa/TheArchitectureOfIntent/blob/main/paper/architecture-of-intent.pdf) is the same vocabulary at paper grain (~20 pages with §5's worked customer-support pilot included).

---

## 6. The minimum read

> *Recommended for: readers who have ~90 minutes total, not 6 hours.*  
> *Time: 60–90 minutes.*

The smallest read that still gives you the framework as a working tool:

1. [Introduction](../introduction.md) — the canvas on one page
2. [A Miniature Pilot, End-to-End](../miniature-pilot.md) — the framework applied to one system in one screen
3. [The Closed Loop: From Failures to Spec Amendments](../evolve/01-closed-loop.md) — the discipline that makes the framework survive contact with operations
4. *Optional:* one Evolve-in-practice chapter from a scenario whose system shape matches yours

If you have only 30 minutes, read items 1 and 2 only. The miniature pilot is the framework on one page, instantiated against one concrete system; you can decide whether the framework is worth deeper investment based on the pilot alone.

---

## 7. Per-role reads

Different roles consume different parts of the framework. The chapters below are the *minimum* relevant set per role; each role can extend into adjacent chapters as time permits.

### Tech lead / staff engineer

> *On the hook for an agent system going to production.*

The full linear read (path 1) is the right shape; if compressed:

1. **Foreword** + Introduction
2. **Part 1 — FRAME** in full (you own the archetype and dimensions decisions)
3. **Part 2 — SPECIFY** in full (you own the spec)
4. The scenario whose system shape best matches yours, end-to-end
5. **Part 5 — EVOLVE** in full (you own the closed-loop discipline)

Skip details of Part 3 — Delegate's pattern catalog if your team's pattern selection is delegated to others; binding decisions still need your sign-off via the spec.

### ML engineer / agent builder

> *Will write the spec and the prompts.*

1. **Part 1 — FRAME** for vocabulary
2. **Part 2 — SPECIFY** in depth — especially [The Canonical Spec Template](../specify/07-canonical-spec-template.md), [Writing for Machine Execution](../specify/05-writing-specs-for-agents.md), [The Living Spec](../specify/06-living-specs.md)
3. **Part 3 — DELEGATE** in depth — especially [The System Prompt](../patterns/capability/system-prompt.md), [The Tool Manifest](../patterns/capability/tool-manifest.md), [Least Capability](../delegate/04-tools-mcp-capability-boundaries.md)
4. The Specify and Delegate chapters of the scenario whose system shape matches yours

### SRE / on-call

> *On the pager when the agent fails in production.*

1. [Failure Modes and How to Diagnose Them](../foundations/05-failure-as-design-signal.md) — the seven Cats and the diagnostic test
2. [The Closed Loop: From Failures to Spec Amendments](../evolve/01-closed-loop.md)
3. **Part 4 — VALIDATE** in full — especially [Production Telemetry](../operate/04-production-telemetry.md) and the [Distributed Trace](../patterns/observability/distributed-trace.md) pattern
4. The Evolve chapter of the scenario whose system shape matches yours
5. [Cost and Latency Engineering](../operate/02-cost-and-latency.md) and [Cacheable Prompt Architecture](../operate/03-cacheable-prompt-architecture.md) — the cost-incident response surface

### Engineering manager / domain owner

> *Owns the outcome the agent is producing; not necessarily building it.*

1. **Foreword** — [Prologue](../prologue.md), [What Changes for the Senior Engineer](../foundations/08-what-changes-for-senior-engineers.md)
2. [The Intent Design Session](../foundations/07-intent-design-session.md) — the working ritual you'll be a required participant in
3. [Roles & Responsibilities (RACI) Card](raci-card.md) — your seat at the table
4. **Part 5 — EVOLVE** in full — especially [Adoption Playbook](../operate/05-adoption-playbook.md), [Proportional Governance](../operate/01-governance.md), [Signs Your Architecture of Intent Is Degrading](../evolve/15-anti-patterns.md)

You don't need Part 3 — Delegate in detail; the team builds the agent. You do need to know what you're committing to in Frame and what to ask for in Validate and Evolve.

### Product manager / domain owner (non-engineer)

> *Owns the customer-facing outcome; not technical.*

1. [Introduction](../introduction.md) — the canvas
2. [The Intent Design Session](../foundations/07-intent-design-session.md) — your role in the ritual
3. The Frame and Evolve chapters of the scenario whose system shape best matches yours

This read is intentionally short. The framework's vocabulary travels with engineering; the PM's job is to bring the customer-facing intent and the constraint surface, which the Frame session formalizes.

---

## 8. Problem-driven entry points

The [Pattern Index](pattern-index.md) is the canonical entry-by-problem table; this list is its short form for the most-common questions:

| If you are... | Start at |
|---|---|
| Just trying to see the framework applied in one screen | [A Miniature Pilot, End-to-End](../miniature-pilot.md) |
| Choosing how to structure a new agent system | [Pick an archetype](../frame/02-canonical-intent-archetypes.md) |
| Writing a spec right now | [The canonical spec template](../specify/07-canonical-spec-template.md) |
| Designing oversight for an agent that's about to ship | [Proportional Oversight](../delegate/06-human-oversight-models.md) |
| Diagnosing a production failure | [Failure Modes and How to Diagnose Them](../foundations/05-failure-as-design-signal.md) and [The Closed Loop](../evolve/01-closed-loop.md) |
| Setting up safety controls | [Safety patterns](../patterns/safety/prompt-injection-defense.md) — start anywhere; cross-link from there |
| Introducing the framework to your team | [Adoption Playbook](../operate/05-adoption-playbook.md) and [Minimum Viable Architecture of Intent](../evolve/16-minimum-viable-aoi.md) |
| Composing with DevSquad Copilot | [Mapping the Framework to the DevSquad 8-Phase Cadence](../operate/06-devsquad-mapping.md), [Co-adoption with DevSquad Copilot](../operate/07-co-adoption-with-devsquad.md), and Scenario 3's chapters |
| Auditing whether your discipline is decaying | [Signs Your Architecture of Intent Is Degrading](../evolve/15-anti-patterns.md) |
| Evaluating the framework for your org | The companion paper at [`paper/architecture-of-intent.pdf`](https://github.com/marcelaldecoa/TheArchitectureOfIntent/blob/main/paper/architecture-of-intent.pdf), then path 5 (conceptual-only) above |

---

## A note on re-entry

This is a field guide; it is structured to be re-entered, not finished. You will come back to it after your first incident, after your first model-tier rotation, after your first cross-team adoption — each return is shorter than the last because more of the vocabulary is yours. The book's job is to give the vocabulary; the work of using it is yours. Welcome back, when you do.
