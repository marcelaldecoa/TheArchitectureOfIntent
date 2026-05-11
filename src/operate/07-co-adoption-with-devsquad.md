# Co-adoption with DevSquad Copilot

**Part 6 — Operations**

---

> *"You don't have to choose. Run DevSquad's cadence, apply this book's vocabulary, let them reinforce each other."*

---

> *Where this sits in v2.0.0: this chapter is part of **Part 6 — Operations**. The co-adoption recommendation is for teams already running DevSquad: the framework's archetype taxonomy, four-dimension calibration, and seven-Cat fix-locus failure analysis are the additions that give the most leverage on top of DevSquad's process scaffolding. [Scenario 3](../frame/scenarios/docs-qa.md) demonstrates the composition end-to-end across all five activities of the AoI cycle paired with the eight phases of the DevSquad cycle.*

---

## Context

Microsoft's [DevSquad Copilot](https://github.com/microsoft/devsquad-copilot) and this book are *parallel works*: independent frameworks that arrive at substantially overlapping conclusions through different lenses. DevSquad gives a delivery cadence (the 8-phase iterative cycle); this book gives a design vocabulary (archetypes, dimensions, failure taxonomy, security/eval/telemetry stacks). They compose cleanly — the convergence on living specs, risk-tiered HITL, principle of least privilege, context isolation, and spec-first failure response is independent rediscovery of what falls out of taking specs and risk seriously when agents are involved.

This chapter is for the team that already runs DevSquad and wants to know: **what is the minimum addition from this book that gives me the most leverage?**

If you do not run DevSquad, skip this chapter; the [Adoption Playbook](05-adoption-playbook.md) is the right entry point for you.

---

## The Problem

DevSquad-running teams who pick up this book face a recognizable failure mode: they try to adopt all of it at once, end up duplicating disciplines they already have (DevSquad's amendment process and this book's Spec Gap Log do roughly the same thing), and conclude the book is overhead. The opposite failure also happens: they conclude the two frameworks are alternatives and pick one, losing the load-bearing material the other provided.

The right move is *additive selective adoption* — keep DevSquad's cadence, add the parts of this book that DevSquad doesn't cover, and let the rest stay as reference.

---

## What DevSquad already gives you

If you are a DevSquad-running team, you already have:

- A delivery cadence (the 8 phases)
- Living specs with formal amendment ("specification mismatch is a first-class event")
- ADRs as a first-class durable artifact, persisted beyond any single slice
- Risk-tiered human-in-the-loop (low / medium / high impact) with named ceremony per tier
- Comprehension checkpoint after medium- and high-impact implementations
- Reasoning log artifact ("every decision recorded with principle, alternatives, justification, and confidence level")
- Principle of least privilege per agent (granular MCP tool scopes; first-party servers only)
- Context isolation across sub-agents (coordinator agents delegate to internal workers in private context windows)
- TDD-first implementation
- Independent review (in a fresh sub-agent context)
- Continuous refinement between sprints
- A 20-skill catalog with semantic activation (skills load on-demand based on description match, not explicit invocation)

These cover roughly 60–70% of the operational discipline this book teaches. You don't need this book to learn them. You may need this book for the parts that follow.

---

## The five additions worth making, ranked by leverage

### 1. The archetype framework (highest leverage, smallest cost)

DevSquad uses the term "specialized agent" without formally classifying agent classes. This book's [Five Archetypes](../frame/02-canonical-intent-archetypes.md) (Advisor, Executor, Guardian, Synthesizer, Orchestrator) plus the [Four Dimensions](../frame/03-archetype-dimensions.md) (Agency, Risk, Oversight, Reversibility) give DevSquad's "specialized agent" a structural classification.

**What changes in your practice:**

- Phase 2 (Spec thin slices) gains a step: declare the archetype before writing Sections 3–4. The decision tree in [The Archetype Selection Tree](../frame/04-decision-tree.md) is fast (4 questions, ~5 minutes per agent).
- Phase 3 (Plan with ADRs) gains discipline: ADRs that affect oversight model are now archetype-classified, which makes the risk-tier decision more discriminating than DevSquad's low/medium/high alone.

**Effort:** ~1 hour to read the archetype chapters; ~5 minutes per agent to apply. Compounds across every spec from then on.

**Leverage:** The archetype declaration is the single most useful structural addition. It sharpens DevSquad's risk-tiering by giving you a specific set of governance defaults (oversight model, invariants, reversibility profile) per archetype, which means less freelancing per spec.

---

### 2. The seven-category failure taxonomy and diagnostic protocol (high leverage)

DevSquad's Phase 6 (Learn openly) is the right discipline but doesn't give you a partition for *what kind of learning this is*. This book's [Failure Modes and How to Diagnose Them](../foundations/05-failure-as-design-signal.md) provides the seven-category fix-locus taxonomy (Spec, Capability, Scope creep, Oversight, Compounding, Model-level, Perceptual) and the diagnostic protocol that maps each category to the artifact you change. Cat 7 (Perceptual) applies only to perceiving-then-acting deployments — computer-use, browser-use, robotic — and can be skipped if your team is text-only.

**What changes in your practice:**

- Phase 6 reviews now categorize each finding (Cat 1–7) before deciding the fix. Cat 1 → spec section. Cat 2 → tool manifest or new tool. Cat 3 → NOT-Authorized clause. Cat 4 → oversight model adjustment. Cat 5 → checkpoint review. Cat 6 → model-level (often: narrow scope, switch model, or accept residual risk). Cat 7 → structural controls + verification step at the perception–action interface (computer-use deployments only).
- Phase 8 (Continuous refinement) now has *signal* per category — which categories recur, which are decreasing, which are stuck. Drives prioritization for the next sprint's spec work.

**Effort:** ~30 minutes to read the diagnostic protocol; ~10 minutes per failure to categorize. Pays back the first time a Cat 6 (model-level) failure stops being mis-diagnosed as a Cat 1 (spec) failure.

**Leverage:** DevSquad's "amend the spec" instinct is right when the failure is Cat 1, but wrong when it's Cat 6 (no spec amendment will fix a model-level reliability problem; you need a different model or narrower scope) or Cat 2 (no spec amendment will fix a missing capability; you need to add the tool). Without categorization, teams update specs that should not have been updated, and the gap log fills with non-actionable entries.

---

### 3. Prompt injection and security depth (high leverage if exposed to untrusted input)

DevSquad's "principle of least privilege" is the right structural posture but doesn't go deep on adversarial threats. This book's [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md) and [Red-Team Protocol](../validate/08-red-team-protocol.md) provide:

- The *lethal trifecta* framing (private data + untrusted content + external communication) as the structural risk to assess
- Indirect injection (Greshake et al. 2023) — the attack class that can't be defended at the prompt layer
- The OWASP LLM Top 10 (2025) as a baseline test catalogue
- The four red-team batteries on cadence (pre-launch, per-release, monthly regression, quarterly fresh-attacks)
- Capability gating at the tool layer as the structural defense

**What changes in your practice:**

- Phase 2 (Spec) gains a security review per the lethal-trifecta question: does this agent have all three legs? If yes, can we remove one?
- The team adopts a red-team battery on cadence. For most teams, the pre-launch and monthly regression batteries are the minimum.
- Phase 7 (Independent review) gains an explicit security-conformance check.

**Effort:** ~2 hours to read the relevant chapters; days to weeks to set up the red-team protocol initially; ongoing red-team time per cadence.

**Leverage:** If your agent processes any user-controlled content (RAG over user docs, web fetches, email/issue/ticket bodies), this is non-negotiable. If your agent is internal-only and processes no untrusted content, the leverage is lower but still meaningful for the future-state when scope expands.

---

### 4. The four-level eval stack and external benchmarks (medium-high leverage)

DevSquad's Phase 5 is TDD-first, which gives you the Level 2 eval discipline (spec acceptance suite). It does not give you Level 1 (unit asserts on tool I/O), Level 3 (regression on a golden set), or Level 4 (production sampling). This book's [Evals and Benchmarks](../validate/07-evals-and-benchmarks.md) provides the full stack.

**What changes in your practice:**

- Tool-level unit tests cover the contract layer (per [Least Capability](../delegate/04-tools-mcp-capability-boundaries.md))
- A team golden set is built from real production traces and runs nightly as a regression baseline
- Production sampling at 5% catches distribution shift between sprints
- Public benchmarks (SWE-bench Verified for coding agents, AgentBench, τ-bench) calibrate your harness against external reference points

**Effort:** ~1 sprint to build the initial golden set (50–100 cases); ongoing maintenance.

**Leverage:** Phase 5 catches the failures the spec anticipated. Levels 3 and 4 catch the failures the spec did not. For most teams, Level 4 (production sampling) catches more spec gaps than Phase 5 alone — because reality has more shapes than the team thought of.

---

### 5. Cost & latency engineering and production telemetry (medium leverage; high leverage at scale)

DevSquad doesn't address per-task economics or production telemetry stack guidance directly. This book's [Cost and Latency Engineering](02-cost-and-latency.md) and [Production Telemetry](04-production-telemetry.md) provide:

- Model-tier selection per role (small/medium/large/reasoning) with the typical 70/20/10 cost shape
- Prompt caching as structural cost control (40–70% input cost reduction is typical)
- Latency budget decomposition
- Per-task cost attribution
- The vendor stack landscape (LangSmith, Langfuse, Phoenix, Helicone, Datadog LLM, OpenTelemetry GenAI)

**What changes in your practice:**

- Phase 3 (Plan with ADRs) gains cost/latency-tier ADRs for each agent role
- Phase 8 (Continuous refinement) tracks cost-per-correct-output as a primary metric

**Effort:** ~1 sprint to instrument and configure; ongoing tuning as the model lineup shifts.

**Leverage:** At pilot scale (~hundreds of tasks/day), this is medium leverage. At rollout scale (~thousands or tens of thousands of tasks/day), it is the difference between a program that survives a CFO review and one that doesn't.

---

## Vocabulary translation table

For DevSquad-fluent readers reading this book, the term mappings:

| DevSquad Copilot | This book |
|---|---|
| Specialized agent | Archetype declaration (Advisor / Executor / Guardian / Synthesizer / Orchestrator) |
| Risk tier (low / medium / high) | Reversibility × Agency matrix → Oversight Model A / B / C / D |
| ADR (Architectural Decision Record) | First-class durable artifact ([new chapter](../specify/08-architectural-decision-records.md)); maps onto spec Section 6 (Invariants), Section 8 (Authorization Boundary), or Section 7 (Tool Manifest) per the mapping table in that chapter |
| Thin-slice spec | Sections 1–3 of the canonical spec template, narrowed to the slice |
| Living spec amendment | Spec Gap Log entry → spec revision (per [The Living Spec](../specify/06-living-specs.md)) |
| Socratic over prescriptive | "Surface, don't resolve" discipline (runs through spec template, failure protocol, worked examples) |
| Principle of least privilege | [Least Capability](../delegate/04-tools-mcp-capability-boundaries.md) + Tool Manifest enforcement |
| Context isolation across sub-agents | [Multi-Agent Governance](../frame/07-multi-agent-governance.md) — seam contracts |
| Independent review | [Intent Review Before Output Review](../validate/05-reviewing-intent.md) |
| Continuous refinement | [Four Signal Metrics](../validate/06-metrics.md) trends → constraint library updates |
| TDD-first | Level 2 of the eval stack ([Evals and Benchmarks](../validate/07-evals-and-benchmarks.md)) |
| Comprehension checkpoint | Output Gate (Oversight Model C) calibrated to action class — a structural mid-flight checkpoint distinct from output review |
| Reasoning log | Spec evolution log entry + ADR, with the "principle, alternatives, justification, confidence" fields aligning to the canonical ADR template |
| Loop-over-ladder framing | Living-spec discipline ([The Living Spec](../specify/06-living-specs.md)) — specs evolve when implementation reveals their incompleteness |
| Skills catalog (semantic activation) | [Portable Domain Knowledge](../delegate/05-agent-skills.md) — Anthropic Skills as deployable artifacts |
| Phase (1–8) | Mapped explicitly in [DevSquad Mapping](06-devsquad-mapping.md) |

---

## A 30-day co-adoption plan

For a team already running DevSquad, here is a concrete sequence:

**Week 1:**
- Read [Pick an Archetype](../frame/02-canonical-intent-archetypes.md) and [The Archetype Selection Tree](../frame/04-decision-tree.md). Apply to your existing agents — record the archetype for each.
- Read [Failure Modes and How to Diagnose Them](../foundations/05-failure-as-design-signal.md). Adopt the seven-category fix-locus taxonomy (Cat 1–7, including Cat 7 Perceptual for any computer-use deployments) in your next Phase 6 review.

**Week 2:**
- Read [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md). Run the lethal-trifecta question against every agent. Record findings as ADRs.
- Read [Architectural Decision Records](../specify/08-architectural-decision-records.md). Confirm your ADR format; add the Spec Mapping section if not present.

**Week 3:**
- Read [Evals and Benchmarks](../validate/07-evals-and-benchmarks.md). Build a starter golden set (10–20 cases) for your most-deployed agent.
- Read [Cost and Latency Engineering](02-cost-and-latency.md). Audit current model-tier selection; identify caching opportunities.

**Week 4:**
- Read [Red-Team Protocol](../validate/08-red-team-protocol.md). Schedule a pre-launch full battery for your next agent.
- Read [DevSquad Mapping](06-devsquad-mapping.md). Confirm the artifact-phase alignment; adjust your team's documentation if helpful.

By the end of 30 days: you have archetype declarations, the failure taxonomy, security depth, evals-beyond-Phase-5, cost engineering posture, a red-team plan, and explicit phase-artifact mapping — without disrupting the DevSquad cadence you were already running.

---

## What you can leave on the shelf

If your team is small or your scope is narrow, parts of this book are over-investment for your context:

- The full [Multi-Agent Governance](../frame/07-multi-agent-governance.md) chapter — relevant when you go multi-agent; skippable until then
- The full [Production Telemetry](04-production-telemetry.md) vendor landscape — relevant when you scale; skippable at pilot
- The [Coding Agents](../delegate/08-coding-agents.md) and [Computer-Use Agents](../delegate/09-computer-use-agents.md) chapters — relevant if you build those classes; skippable otherwise
- The [Adoption Playbook](05-adoption-playbook.md) — written for teams not on DevSquad; you don't need it

This is a feature, not a bug. The book is a reference; you read the chapters relevant to your work.

---

## Resulting Context

After applying this co-adoption pattern:

- **Your DevSquad cadence is intact.** No phases removed, no new phases added.
- **Each phase has named artifacts from both frameworks.** ADRs and specs from DevSquad; archetypes, failure categorization, evals, security audits from this book.
- **Selective adoption is the explicit posture.** You added what gives leverage; you left the rest as reference.
- **The team has both vocabularies.** Risk tiers and oversight models, ADRs and invariants, specialized agents and archetypes — the team can communicate in either dialect with no loss of precision.

---

## Therefore

> **Run DevSquad's cadence, apply this book's vocabulary, let them reinforce each other. The minimum additions in priority order: archetype framework (highest leverage, smallest cost), failure taxonomy and diagnostic protocol, prompt injection and security depth (non-negotiable if you process untrusted content), the four-level eval stack, cost/latency engineering and production telemetry. A 30-day sequenced rollout absorbs all five without disrupting the cadence. The two frameworks were independently designed; they compose cleanly because both are responding to the same underlying problem space. Use both.**

---

## References

- Microsoft. (2026). *DevSquad Copilot.* github.com/microsoft/devsquad-copilot.
- Anthropic. (2024). *Building Effective Agents.* anthropic.com/research/building-effective-agents. — The framework family within which both DevSquad and this book sit.

---

## Connections

**This pattern assumes:**
- Familiarity with the DevSquad 8-phase cadence
- [Mapping the Framework to the DevSquad 8-Phase Cadence](06-devsquad-mapping.md) — the phase-by-phase artifact mapping

**This pattern enables:**
- All of Part 5 (Ship) — every chapter applies within DevSquad's cadence at the phase identified in the mapping
- [Adoption Playbook](05-adoption-playbook.md) — comparable sequenced guidance for teams not on DevSquad

---
