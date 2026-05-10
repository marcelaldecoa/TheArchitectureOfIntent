# Signs Your Architecture of Intent Is Degrading

**Part 5 — Evolve**

---

> *"The discipline is not the spec, the canvas, or the design session. The discipline is the daily refusal to skip them."*

---

> *Where this sits in v2.0.0: this chapter is part of **Part 5 — Evolve**. The Discipline-Health Audit is the per-quarter cadence that catches loop decay before it becomes terminal; the audit's instrument is the twelve-anti-pattern catalog this chapter develops. The audit fires on each system the team operates, on a calendar (not on incident-driven) cadence, and produces a one-paragraph verdict per anti-pattern. The three running scenarios in v2.0.0 each include an audit at day 90 — see the customer-support, coding-pipeline, and docs-qa Evolve chapters for worked examples. The twelfth anti-pattern (citation theater) was elevated to the catalog in v2.1.0 after first surfacing in Scenario 3's Evolve chapter as a team-proposed addition.*

---

## Context

You have adopted the framework. You ran the [Intent Design Session](../theory/07-intent-design-session.md). You have a spec, an oversight model, instrumented metrics, a rollout plan. The first pilot shipped. A few more followed. Six months in, something feels off — but the artifacts are all still there. The spec exists. The dashboard exists. The team still uses the vocabulary. Why does it feel like the discipline has stopped doing work?

Because the artifacts can be preserved long after the function has gone. A discipline that produces structures is durable only as long as those structures keep doing something — keep constraining behavior, keep surfacing disagreements, keep getting amended after incidents. When the structures freeze and the function quietly drains, you get a team that *calls itself spec-driven but is actually code-driven, with paperwork*.

This chapter catalogs the predictable ways the Architecture of Intent decays in practice. It is the anti-pattern catalog of the discipline itself, not of the systems built with it. (For the latter — the seven fix-locus failure categories Cat 1–7 — see [Failure Modes and How to Diagnose Them](../theory/05-failure-as-design-signal.md).)

This pattern assumes [The Intent Design Session](../theory/07-intent-design-session.md), [Proportional Governance](04-governance.md), [Intent Review Before Output Review](05-reviewing-intent.md), and [Adoption Playbook](11-adoption-playbook.md).

---

## The Problem

Frameworks degrade in a specific shape: **form is preserved while function decays.** The decay is hard to spot from inside, because the artifacts all still exist. The spec is still in the repository. The oversight gate still fires. The dashboards still show numbers. The team still uses the vocabulary. What has gone is the *work* the artifacts were doing — the constraint they imposed, the disagreement they surfaced, the amendment they triggered after an incident.

Three structural reasons this is the dominant failure mode:

- **The artifact is more visible than the work.** A spec is easy to point at; the conversations that produced it are not. After launch, only the artifact persists. The team can preserve the artifact perfectly while losing every conversational habit that gave it meaning.
- **Drift is gradual.** No single decision moves an Advisor into Executor territory. Each feature addition is locally reasonable. The cumulative effect surfaces only when you compare the system today against the spec as written, and most teams never do.
- **The rituals get optimized for throughput.** The Intent Design Session takes 3–4 hours. Reviewing every output gate takes 30 seconds × N runs. Both feel expensive when the system is running well. The natural pressure is to compress them — first into a shorter session, then into a faster review, then into a "trust the team" pass-through. The rituals decay before the team notices.

The cure is not vigilance. Vigilance is exhausting and unreliable. The cure is naming the anti-patterns in advance, agreeing on the *signs*, and running a periodic discipline-health audit against them.

---

## Forces

- **Operational throughput vs. discipline depth.** Slower discipline catches more drift; faster operation ships more pilots. Most teams over-correct toward speed once a few systems are healthy and discover the cost a quarter later.
- **Artifact visibility vs. function visibility.** A team can produce, store, and reference artifacts without the artifacts ever doing structural work. Distinguishing live artifacts from museum pieces requires explicit signs.
- **Optimism vs. honest reporting.** A team that is using the framework wants to believe it is working. Reports tend to surface successes and bury slippages. Anti-pattern audits are uncomfortable because they require the team to look for failures of its own discipline.

---

## The Solution

Eleven anti-patterns, organized into three clusters: **form without function**, **drift**, and **process degradation**. Each entry names the shape, the signs, and the fix.

When you run a discipline-health audit (we recommend quarterly, paired with the [Adoption Playbook](11-adoption-playbook.md)'s ongoing-practice review), walk this list. For each anti-pattern, ask whether the signs apply to one or more of your live systems. Anti-patterns surfaced by the audit are not failures — they are the audit doing its job. Resolution goes into the spec evolution log of the affected system.

---

### Cluster 1 — Form without function

The biggest cluster. The team has the artifact; the artifact has stopped working.

**1. Spec theater.**

*The shape.* A spec exists in the repository. It was written once, posted in a doc, never amended after the first incident, never referenced in design conversations. The form is preserved; the function is gone. The agent's actual behavior is governed by the prompt and tribal knowledge.

*The signs.* The spec evolution log (§13) has zero entries after launch. The most recent commit to the spec is older than the most recent agent behavior change. When asked "where in the spec is this constraint?" the team doesn't know.

*The fix.* Reopen the spec at the next incident — *any* incident — and amend it with the gap that was just exposed. If you can't trace the incident to a missing or wrong spec clause, the spec is incomplete; that is itself a Cat 1 finding. A spec that has gone six months without an entry in §13 is the strongest possible signal that the team is no longer running spec-driven development.

**2. Oversight kabuki.**

*The shape.* Humans review every output. The form of oversight (Output Gate, Periodic, etc.) is preserved. But the review takes 5 seconds, the approval rate is 99.5%, and reviewer comments are mostly "LGTM." The judgment that the oversight model was supposed to inject is gone.

*The signs.* First-pass-validation rate is suspiciously high (>98% for a non-trivial system). Sampling reviewer activity reveals that approvals come within seconds of agent output, with no substantive engagement. The team would be unable to identify a single agent output that was caught and corrected by the gate in the last month.

*The fix.* Either downgrade the oversight model honestly (move from Output Gate to Periodic; document the move in the spec evolution log) or re-engage by sampling: pick 1 in 20 outputs for deeper review and require the reviewer to write a paragraph about whether anything was off. The choice the framework forbids is keeping the form of high-touch oversight while doing low-touch work; that is the worst of both — the cost of the gate, none of the value.

**3. Metrics theater.**

*The shape.* The four signal metrics — spec-gap rate, first-pass validation, cost per correct outcome, oversight load — are instrumented and appear on a dashboard. No one looks at the dashboard. The metrics never trigger a discussion, never appear in a retrospective, never inform a spec amendment.

*The signs.* When asked "what's our spec-gap rate this quarter?" the answer is "I'd have to check." There is no recurring forum (sprint review, monthly governance pass, retrospective) where the metrics are reported. The metrics dashboards have lower view counts than any other operational dashboard.

*The fix.* Tie the metrics to a recurring forum. The simplest version: a 15-minute monthly governance pass per pilot, with the four metrics as the agenda. If a metric crossed a threshold, name the spec amendment that responds. If no metric crossed a threshold, name what the team actually learned from this month's runs. A metric that does not produce a discussion does not exist.

**4. Pattern inventory.**

*The shape.* The spec lists bound patterns, but each pattern is bound to "general best practice" rather than to a specific clause. The patterns are inventory, not design — they sit alongside the spec without doing structural work for it.

*The signs.* Removing a bound pattern triggers the question "what spec clause was this satisfying?" and no one can answer. The pattern list grew over time without corresponding spec amendments. Two specs in the same team have wildly different pattern lists for similar systems, with no spec-clause justification for the differences.

*The fix.* For every bound pattern, write the one-line justification tying it to a specific spec clause. Patterns whose justification reads "good practice" or "we always do this" are inventory; either remove them or amend the spec to add the clause that justifies them. The discipline named in the [Intent Design Session's Bind Patterns phase](../theory/07-intent-design-session.md#phase-5-bind-patterns-45-60-min-skeptic-leads-architect--operator-participate) — *patterns are picked by spec implications, not team taste* — is what this anti-pattern violates.

**5. Calibration without commitment.**

*The shape.* §4 of the spec declares values for the four dimensions, but each value is a hand-wave. "Agency: medium." "Autonomy: high." Without a specific decision-space and gate logic to back each value, the dimensions don't constrain anything.

*The signs.* When the system misbehaves, the team can't reference §4 to diagnose which dimension was wrong. Two team members asked separately to describe what "Autonomy: high" means in this system give different answers. The values were never revisited after the original spec write.

*The fix.* Re-do §4 as if you were running the [Intent Design Session](../theory/07-intent-design-session.md) phase 3 today. Each value gets a one-sentence operational answer ("Agency narrow: the system decides X but never Y"; "Autonomy bounded: every Z action gates on a human confirmation"). Disagreement during this re-do is productive; resolve it before signing off, and update the spec.

**6. Citation theater.**

*The shape.* Every Synthesizer-mode answer cites a URL. The form is preserved. But a sample audit reveals that some non-trivial fraction of citations are *technically grounded* (the URL contains the claim) but *contextually shallow* — the cited sentence is taken out of a larger context that, read in full, complicates or contradicts the answer. The agent has learned to satisfy the citation-grounding check at the level the check operates on, without the citation actually grounding the asker's understanding.

*The signs.* The citation-grounding classifier reports near-100% pass rate. The first-answer-satisfaction metric is healthy. But asker feedback occasionally flags answers as *"technically right but missed the point"* — and re-reading the cited source confirms the citation is there but the surrounding context says something different. The classifier doesn't catch this because its training focuses on sentence-level grounding rather than contextual completeness. The audit's *active* flag fires when ≥5% of a 50-answer monthly sample audit surfaces this pattern.

*The fix.* Two parts: (1) extend the grounding check with a *contextual-completeness* score that re-reads the citation's larger neighborhood (paragraph, section) for material that complicates the claim; (2) add a per-month sample-audit cadence (e.g., 50 random answers, manual deep-grounding check) that catches what the automated check misses. Both fixes are structural — the audit cadence and the classifier extension — not promptual. The third fix the team's instinct reaches for, *"tell the model to read more context before citing,"* is a prompt patch that doesn't compound; the structural fixes do.

*Applies primarily to:* Synthesizer-flavored systems where citation discipline is load-bearing. Less applicable to Executor- or Guardian-flavored systems whose primary act is bounded action rather than composed retrieval. The anti-pattern was first surfaced by the docs-platform team's day-90 Discipline-Health Audit in [Scenario 3's Evolve chapter](../evolve/scenarios/docs-qa.md) and elevated to the framework's catalog in v2.1.0.

---

### Cluster 2 — Drift

The system the spec describes is no longer the system you have.

**7. Prompt-patch drift.**

*The shape.* When the agent misbehaves, fixes land in the system prompt instead of in the spec, the manifest, the oversight model, or a CI guard. Each prompt patch is local and fast; cumulatively they form an undocumented constitution that the actual artifact (the spec) doesn't reflect.

*The signs.* The system prompt has more recent commits than the spec. Comparing prompt commits to spec commits over six months shows a >2× ratio in favor of the prompt. Specific behaviors observed in production are explained by the team as "well, the prompt says..." — language that should never replace "the spec says."

*The fix.* Run a prompt-to-spec diff. For every prompt patch, identify whether it should be a spec amendment, a tool-manifest restriction, an oversight-gate addition, or a CI guard. The load-bearing discipline named in the [Introduction](../introduction.md#what-is-the-architecture-of-intent) — *structural fixes live in spec, manifest, CI, or platform — never only in the prompt* — is what this anti-pattern most directly violates. A team that is not periodically auditing the prompt against the spec has effectively forked the system's constitution.

**8. Archetype drift.**

*The shape.* A system declared as Advisor gradually acquires Executor behaviors. Each addition was reasonable in isolation: "let's let it draft the email"; "let's let it send the email if the user clicks send"; "let's let it send the email automatically for low-risk recipients." Each step was small; the cumulative shift moved the system across an archetype boundary without the spec, the oversight model, or the calibration following.

*The signs.* The actions the system takes don't match the actions §3 (Scope) of the spec authorizes. Reviewing the last quarter's feature additions shows several that crossed the archetype's invariant ("the violation to watch for" passages in [Pick an Archetype](../architecture/02-canonical-intent-archetypes.md)) without an archetype re-classification. The oversight model from launch is unchanged despite the system now operating as a different archetype.

*The fix.* When archetype drift is suspected, run [Governed Archetype Evolution](../architecture/06-evolving-archetypes.md). Either roll back the drift (revert the features that crossed the boundary) or accept the new archetype and re-do the calibration, the oversight model, the bound patterns, and the signal metrics for the new shape. The framework does not forbid re-classification; it forbids *implicit* re-classification.

**9. Glossary by import.**

*The shape.* The team uses the framework's vocabulary but means something subtly different by each term. "Executor" in code review means "any agent that takes action," not the canonical archetype with its specific governance profile. "Spec" means whatever document is named "spec.md," not the canonical 12-section template.

*The signs.* New team members join and ask "what do you mean by Executor here?" — and get a different answer from each existing member. The [Glossary](../appendices/glossary.md) is rarely cited in design conversations. When asked to point to where a term is defined, team members point to a slide deck or a chat message rather than to the canonical book entry.

*The fix.* Make the canonical glossary the source of record for the team. In design conversations, when a term is used loosely, *say so* — "we're using Executor here in the loose sense; the canonical Executor archetype would require X." That single re-anchoring habit, repeated weekly, restores the vocabulary's load-bearing function. Specs use the canonical terms; if the team needs domain-specific extensions, they go in a [team-specific glossary fragment](../repertoires/01-why-repertoires-matter.md), not in redefinitions of canonical terms.

**10. Composition by accident.**

*The shape.* A system was built by stacking patterns until it worked, then "documented" with a single archetype label that doesn't match its actual behavior. The composition (Patterns A–E in [Composing Archetypes](../architecture/05-composing-archetypes.md)) isn't declared; the cross-mode invariants aren't named; the transitions are implicit.

*The signs.* §4 of the spec has a single archetype declaration but the implementation has features only valid under multiple archetypes (a "mostly Synthesizer" system that also writes to a database). When asked "what triggers the system to switch from drafting to writing?" the answer is implementation-level rather than spec-level.

*The fix.* Add the [Composition Declaration](../architecture/05-composing-archetypes.md#the-composition-declaration-in-the-spec) sub-block to §4. Name the governing archetype, the embedded components or modes, the transitions (if Pattern E), and the cross-mode invariants. If you can't fill in the cross-mode invariants section, that gap is itself the design surface that's been missing — a Cat 1 finding waiting to happen.

---

### Cluster 3 — Process degradation

The artifacts are healthy; the rituals that produced them have stopped.

**11. The retrofit IDS.**

*The shape.* A team runs an Intent Design Session *after* the system has shipped, "to document what we built." The session rationalizes existing implementation rather than constraining future implementation. The spec produced exactly matches the system that already exists — no clauses surfaced as gaps, no calibration disagreements, no spec-conflict resolutions.

*The signs.* The IDS produced a spec that the implementation already passes. No items went into §10 (Assumptions and Open Questions). No follow-up tickets were created from the session. The IDS lasted under 90 minutes (the real ones rarely do, except for genuinely small scopes).

*The fix.* Acknowledge what just happened — that was a documentation pass disguised as a design session. Call it that. Then run the *real* IDS as a refactor session: assume the system is already in v1, but the design surface is genuinely open for v2. Phase 5 (Bind Patterns) is the most important phase in this case, because the existing patterns may have been inventory rather than design.

**12. The Adoption Playbook problem.**

*The shape.* The team treats "adopting the framework" as a checklist completed at launch, not as an ongoing practice. After 30 days, no one has run the post-launch retrospective. After 90 days, no one has updated the spec. After 180 days, the framework is "what we used at the start," and the system is operating outside its boundaries.

*The signs.* The most recent spec evolution log entry is the launch entry. The post-launch retrospective scheduled in §14 (Planned Evolution) was canceled, postponed, or skipped. The team's most recent reference to the framework's vocabulary in any artifact is the launch IDS notes.

*The fix.* Re-anchor the cadence. The [Adoption Playbook](11-adoption-playbook.md) names the rhythm; the discipline-health audit (this chapter) is part of that rhythm. The first signal of decay is the missed retrospective. Run it now — late is fine; never is the failure mode. Restart §13 as a living log: every incident, every model upgrade, every feature addition gets an entry, even small ones. The log is what the next team member will read to understand the system; if it's empty, the system has no institutional memory.

---

### Running a discipline-health audit

The twelve anti-patterns above are the audit checklist. We recommend running the audit quarterly, paired with the [Adoption Playbook](11-adoption-playbook.md)'s ongoing-practice review, and tied to a specific live system rather than to "the team's practice in general."

The audit takes ~60 minutes per system (allow ~5 additional minutes for the citation-theater entry on Synthesizer-flavored systems; the entry is brief on systems where it doesn't apply). One auditor (rotating; not the system's primary owner) walks the twelve entries against the system's artifacts and writes a one-paragraph verdict per anti-pattern: *not present*, *early signs*, or *active*. Anti-patterns flagged *active* go into the spec evolution log as findings, with named follow-up actions and dates.

The audit's value is not in catching every drift. It is in *naming* the drift in a vocabulary the team already shares, so the conversation can happen without anyone having to invent the language for it on the spot. The hardest part of catching discipline decay is having the words for it.

---

### What this chapter is not

Not a comprehensive failure taxonomy of the discipline. Eleven anti-patterns is an opinionated working set, not a derived classification. Real teams will surface variants and additions; encourage that, name them, and contribute the named ones back.

Not a substitute for the system-level failure taxonomy in [Failure Modes and How to Diagnose Them](../theory/05-failure-as-design-signal.md). The Cat 1–7 categories tell you which artifact to update when a *system* misbehaves. This chapter tells you when the *artifacts themselves* have stopped doing work. Both audits matter; they are not interchangeable.

Not an indictment of teams that surface anti-patterns during an audit. Surfacing a degradation is the audit working as designed. The teams that fail are the ones whose audits return clean for two consecutive years.

---

## Resulting Context

After this pattern is in place:

- **Decay has names.** When a team member senses something is off, they have a vocabulary for it. The conversation moves from "this feels off" to "this looks like spec theater; let me check the §13 log."
- **The discipline becomes auditable.** A quarterly audit produces a written record of which anti-patterns were present, what was done about them, and what improved by the next audit. The discipline accumulates evidence of its own health.
- **Form-without-function is the named failure mode.** Teams stop confusing artifact preservation with discipline health. The presence of a spec is necessary but not sufficient; the spec also has to be *doing work*.
- **The artifacts stay live.** Live artifacts get amended. Spec evolution logs accumulate entries. Bound patterns trace to specific clauses. Glossary terms get re-anchored in design conversations.

---

## Therefore

> **The Architecture of Intent is durable only as long as its artifacts keep doing work. Eleven predictable anti-patterns describe the ways the discipline decays in practice — five forms of *form without function* (spec theater, oversight kabuki, metrics theater, pattern inventory, calibration without commitment), four forms of *drift* (prompt-patch drift, archetype drift, glossary by import, composition by accident), and two forms of *process degradation* (the retrofit IDS, the Adoption Playbook problem). Run a 60-minute discipline-health audit per live system per quarter. Anti-patterns the audit surfaces are the audit working; the failure mode is an audit that returns clean for two consecutive years.**

---

## Connections

**This pattern assumes:**
- [The Intent Design Session](../theory/07-intent-design-session.md) — the ritual whose decay several of these anti-patterns describe
- [Failure Modes and How to Diagnose Them](../theory/05-failure-as-design-signal.md) — the system-level failure taxonomy this chapter complements
- [Proportional Governance](04-governance.md) and [Intent Review Before Output Review](05-reviewing-intent.md) — the governance practices that surface drift
- [Four Signal Metrics](06-metrics.md) — the metrics whose theater this chapter names
- [Adoption Playbook](11-adoption-playbook.md) — the ongoing practice this audit is paired with

**This pattern enables:**
- A discipline-health audit cadence on top of system-level pilot governance
- A vocabulary for honest reporting on the framework's decay, not just on its successes

---
