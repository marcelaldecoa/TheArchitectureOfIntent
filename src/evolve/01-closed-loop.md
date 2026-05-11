# The Closed Loop: From Failures to Spec Amendments

**Part 5 — Evolve**

---

> *"A failure that doesn't change a structural artifact is a failure the team will see again."*

---

## Context

Friday afternoon. The on-call engineer pages the team channel: the customer-support agent just refunded $2,400 to a user whose ticket said "I want my money back." No invoice number, no order context, no second confirmation. The refund is well outside the cap. The team's first instinct, after escalating to the customer-support manager, is to update the prompt: *"do not refund without an explicit invoice number AND a confirmation step."* Two engineers start drafting the prompt change.

That is the failure mode this chapter exists to prevent.

The failure isn't the refund. The failure was already in the spec. §4 *NOT-authorized scope* didn't enumerate "refund without invoice"; the §11 *execution instructions* described the confirmation step but not as a hard gate; the tool manifest gave the agent unrestricted refund authority within the cap. The prompt patch will work this Friday. Next Friday, when a different shape of unauthorized refund happens, the prompt grows another sentence. By month three the prompt is a fragmentary war journal, the spec is decorative, and the team has no record of which fixes were actually attempted.

**Closed loop is the discipline that prevents this.** Every diagnosed failure produces a structural change — to the spec, the manifest, a CI guard, or a [framework version bump](07-framework-versioning.md) — and the prompt is the *last* place a fix is allowed to live alone.

This chapter sits at 5.1, the opener of Part 5, because every other practice in the Part — adoption, MVP-AoI, governance, cost posture, anti-patterns, framework versioning, DevSquad co-adoption — is a *practice that supports the loop*. Get the loop wrong and the rest is decoration.

---

## The problem

When an agent system fails in production, the team has three obvious responses: patch the prompt, escalate to a human reviewer, or attribute the failure to the model. Each is sometimes correct. None of them, by itself, evolves the system.

The team that *only* patches prompts produces a system whose behavior is governed by an accreted prompt nobody wrote, whose spec is an aspirational document, and whose new hires inherit no understanding of why the prompt looks the way it does. Each fix works locally; nothing compounds.

The team that *only* escalates produces oversight load that grows linearly with traffic and a queue of unresolved failures that fills up faster than the reviewers can drain it. The agent's actual capability stops growing, because every novel failure routes around it instead of through structural amendment.

The team that *only* attributes to the model produces a permanent backlog of "wait for the next model" while accumulating known failures the spec could have prevented. The Cat 6 attribution is sometimes right, but using it as the default skips the diagnostic work and breaks the loop.

The closed-loop discipline is not a fourth option. It is the *integration* of all three responses around a structural artifact: each diagnosed failure produces an amendment to the spec, the manifest, the oversight model, or a CI guard, and the structural change is what compounds. The prompt patch may be a temporary compensation while the structural fix ships; the human escalation may be where the diagnosis happens; the model attribution may be the correct outcome of categorization. None of those substitutes for the structural amendment.

---

## Forces

- **Speed of fix vs. durability of fix.** A prompt patch ships in hours. A spec amendment with review takes days. Production pressure pushes toward the prompt; the closed-loop discipline pushes toward the spec. Most teams over-correct toward speed once a few systems are healthy and discover the cost a quarter later.

- **Visible artifact vs. invisible discipline.** The spec is easy to point at; the per-incident loop that updates it is not. A team can preserve the artifact perfectly while losing every habit that gave it meaning. The [Discipline-Health Audit](../evolve/15-anti-patterns.md) exists because this drift is hard to spot from inside.

- **Per-incident discipline vs. per-sprint discipline.** Doing the loop per-incident (trace, categorize, amend, ship) is mechanical. Rolling the spec evolution log up per-sprint to find systemic patterns is judgment-heavy and easily skipped. Teams that are good at per-incident often plateau because they're not doing per-sprint.

- **Cat 6 as honest answer vs. Cat 6 as cop-out.** Some failures are genuinely model-level. Naming them as such is correct. Naming *every* failure as Cat 6, or reaching for Cat 6 first, is the failure mode that breaks the loop.

---

## The solution

### The loop in detail

Four steps, executed per consequential failure:

**1. Trace.** Every consequential action emits a structured trace — input, retrieved context, tool calls, outputs, oversight decisions, the spec version the agent was running against. Production telemetry is what makes diagnosis possible. Without traces, you have an after-the-fact narrative; with them, you have evidence. The [Production Telemetry](../operate/04-production-telemetry.md) chapter names what to instrument.

**2. Categorize.** Apply the diagnostic test from [Failure Modes and How to Diagnose Them](../foundations/05-failure-as-design-signal.md): *"If a perfectly competent agent had executed this spec exactly as written, would the outcome have been correct?"* The answer determines the category:

| Answer | Category | What it means |
|---|---|---|
| Yes | Cat 2 / 4 / 6 / 7 | Execution problem; spec was correct |
| No | Cat 1 / 3 / 5 | Spec problem; the spec needed to be different |
| "I can't tell" | Cat 1 | Spec is too ambiguous to evaluate against; that's itself an intent failure |

**3. Trace to fix locus.** Each Cat names the artifact that updates:

| Cat | Fix locus |
|---|---|
| Cat 1 — Spec | Spec sections §1–§12; usually §4 (NOT-authorized) or §11 (execution instructions) |
| Cat 2 — Capability | Tool manifest; usually adding a tool, tightening a permission, or fixing a tool description |
| Cat 3 — Scope creep | §3 NOT-authorized scope clause |
| Cat 4 — Oversight | Oversight model in §10; usually a gate definition or escalation trigger |
| Cat 5 — Compounding | Spec + checkpoint discipline; an explicit handoff verification |
| Cat 6 — Model-level | Narrow scope, switch model, or accept residual; rarely a spec change |
| Cat 7 — Perceptual | Confirmation gate + grounding step at the perception/action boundary |

The fix-locus framing is what makes the loop *structural* rather than reactive. A team that traces every failure to a specific spec section or manifest field is doing closed-loop work; a team that traces every failure to "let's update the prompt" is not.

**4. Amend.** The amendment lands in the structural artifact. For a Cat 1, the spec gets updated and re-published — the [Living Spec](../specify/06-living-specs.md) chapter names the mechanics. For a Cat 2, the tool manifest gets a new permission boundary or fixed description. For a Cat 3, a NOT-authorized clause gets added or sharpened. The change ships through the spec evolution log.

A prompt patch may exist in parallel as a *temporary compensation* while the structural amendment is in review. When that happens, it is logged as such — a prompt patch with no corresponding structural amendment is the failure mode this discipline exists to prevent.

### Spec evolution log discipline

Every amendment names six things: which §, which Cat triggered it, the prior text, the new text, the reviewer, the date. The log is co-located with the spec (typically `spec-evolution.md` next to it) and grows monotonically — entries are added, never removed. The team's behavior at any point in time is derivable from the spec plus the log.

Why a log and not just git history? Both can exist. The log adds intentional structure that git history doesn't: each entry says *why* the change happened (a real failure trace), not just *what* changed. A team reading the log a year later understands not just the spec's current state but the failures that shaped it. The log is also where the *spec-gap rate* signal metric is computed — entries per 1000 production runs is the most direct measure of whether the spec is converging or drifting.

A near-empty log over months of production is a signal, not an achievement. It usually means the team is patching prompts without recording the fix as a structural amendment. The Discipline-Health Audit calls this *prompt-patch drift* (anti-pattern 6), and it is the most common loop-break.

### The loop at three time-scales

**Per-incident — hours.** A failure happens; the on-call engineer traces, categorizes, and files the amendment. The structural change ships within the day if it's a manifest tightening or a CI guard, or within a few days if it's a spec amendment that needs review. The prompt is *not* edited unless the spec amendment hasn't shipped yet, and even then the prompt edit is a temporary compensation noted in the log as such.

**Per-sprint — weeks.** The team rolls up the spec evolution log entries for the sprint and looks for patterns. A cluster of Cat 1 amendments to §11 means the spec is drifting from how the agent is actually being asked to operate; the team schedules a structural rewrite of §11. A cluster of Cat 3 amendments means the original §4 was incomplete in a class-coherent way; the team adds a new sub-clause or invariant rather than enumerating each instance. The per-sprint pass is where the highest-value structural amendments get scheduled.

**Per-quarter — months.** The [Discipline-Health Audit](../evolve/15-anti-patterns.md) (60 minutes per system) walks the 12 anti-patterns and writes a one-paragraph verdict per anti-pattern — *not present*, *early signs*, or *active*. Most relevantly here: prompt-patch drift, archetype drift, calibration without commitment, and metrics theater are the four anti-patterns that most directly indicate the closed loop has stopped functioning. If the audit surfaces any of those as *active*, the structural amendment cadence is the artifact to fix, not the system the audit was nominally about.

### What breaks the loop

Five common loop-break patterns, each with its diagnostic sign:

1. **The prompt-only patch.** Fix lives in the prompt, never migrates to the spec. *Sign:* the spec evolution log is near-empty, but the prompt is growing.
2. **The tribal-knowledge fix.** Fix lives in someone's head ("yeah, we always check X before refunding"). *Sign:* new team members violate the implicit rule because nobody told them.
3. **The Cat 6 cop-out.** Every failure attributed to "the model is bad." *Sign:* the spec evolution log is empty; the team's explanation for failures is uniform across categories.
4. **The spec evolution log nobody reads.** Entries are added (good), but nobody reviews the log per-sprint to find systemic patterns (bad). *Sign:* per-incident discipline holds; per-sprint roll-up doesn't happen; structural amendments stay reactive instead of getting ahead of the failure pattern.
5. **The audit nobody runs.** Discipline-Health Audit gets scheduled and skipped quarter after quarter. *Sign:* the team has artifacts but doesn't know whether they're still doing structural work.

Each of these is a *visible* failure if the audit is run. The audit is the periodic mechanism that catches loop decay before it becomes terminal.

---

## Why this chapter opens Part 5

Validate is *learning in production*. Evolve is *what you do with what you learned*. The two are inseparable in practice — a team that traces and categorizes well is doing both — but the *discipline of structural amendment* is the Evolve commitment, not the Validate commitment.

This chapter sits at 5.1 because everything else in Part 5 is a *practice that supports the loop*:

- The [Adoption Playbook](../operate/05-adoption-playbook.md) keeps the loop going as the team grows.
- [MVP-AoI](../evolve/16-minimum-viable-aoi.md) is the closed loop in compressed form for systems too small for the full discipline.
- [Proportional Governance](../operate/01-governance.md) gives the loop a role-and-responsibility frame.
- [Cost and Latency Engineering](../operate/02-cost-and-latency.md) and [Cacheable Prompt Architecture](../operate/03-cacheable-prompt-architecture.md) name the particular Cat that needs its own escalation pattern (Cost Posture incidents).
- [Production Telemetry](../operate/04-production-telemetry.md) is the trace surface that step 1 of the loop requires.
- The [Anti-patterns chapter](../evolve/15-anti-patterns.md) catalogs the discipline failures the loop is meant to prevent.
- [Framework Versioning](07-framework-versioning.md) is the loop at the longest time-scale — when the framework itself acquires new capability, every system inherits it through controlled upgrade rather than ad-hoc adoption.
- The [DevSquad mapping](../operate/06-devsquad-mapping.md) and [Co-adoption](../operate/07-co-adoption-with-devsquad.md) chapters show how the loop composes with DevSquad Copilot's *Refine continuously* phase.

---

## The closed loop as a worked discipline

The three running scenarios end in their Evolve chapters, each showing the loop in operation:

- [Customer-support agent (90 days post-launch)](scenarios/customer-support.md) walks the loop's first 90 days for the agent in this chapter's opening vignette: 11 amendments, the Output Gate → Periodic transition, a Cost Posture incident, the Discipline-Health Audit at the 90-day mark.
- [Coding-agent pipeline](scenarios/coding-pipeline.md) walks the loop for an agent whose Cat 1s ship as CI-guard changes and tool-manifest tightenings rather than prose amendments — the structural form the loop takes for code-generating systems.
- [Internal docs Q&A (DevSquad)](scenarios/docs-qa.md) walks the loop embedded in DevSquad Copilot's *Refine continuously* phase, showing the AoI ↔ DevSquad activity mapping at scenario grain.

Read at least one end-to-end before adopting the loop in your team. The vocabulary is portable; the rhythm of the discipline is what has to be learned in operation.

---

## Related material

- [Failure Modes and How to Diagnose Them](../foundations/05-failure-as-design-signal.md) — the seven Cats and the diagnostic test
- [The Living Spec](../specify/06-living-specs.md) — the artifact the loop updates
- [Intent Review Before Output Review](../validate/05-reviewing-intent.md) — the review discipline that surfaces Cat 1s
- [Spec Versioning](../patterns/deployment/spec-versioning.md) — the deployment pattern for amended specs
- [Signs Your Architecture of Intent Is Degrading](../evolve/15-anti-patterns.md) — the audit that catches loop decay
- [Framework Versioning](07-framework-versioning.md) — the loop at the longest time-scale
