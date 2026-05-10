# Evolve in practice — Customer-support agent (90 days post-launch)

**Part 5 · EVOLVE · Scenario 1 of 3**

---

> *"The amendment that compounds is the one that lands in the spec. The amendment that doesn't compound is the one that lives in the prompt."*

---

## Setting

Friday afternoon, day 51. The on-call engineer (Sam) pages the team channel: the customer-support agent just refunded **$2,400** to a user whose ticket said *"I want my money back."* No invoice number. No order context. No second confirmation. The refund is well outside the cap.

The team's first instinct, after escalating to Priya, is to update the prompt: *"do not refund without an explicit invoice number AND a confirmation step."* Two engineers start drafting the prompt change.

Maya stops them: *"Wait. The cap is $500. How did $2,400 ship?"*

This is the chapter where the [closed-loop discipline](../01-closed-loop.md) gets exercised in operation. It walks 90 days of running the customer-support agent — including the $2,400 incident, a Cost Posture incident at day 47, the Output Gate transition that didn't happen at day 30, and the Discipline-Health Audit at day 90. The discipline produces 11 structural amendments, two transitions, one anti-pattern caught early, and one decision to deprecate a path that was net-negative.

---

## The $2,400 incident

The investigation takes 4 hours. The trace shows what happened:

- The customer's ticket was: *"I want my money back."* No specifics.
- The agent classified the intent as *refund request*. Confidence: 0.81 (above the 0.7 threshold).
- The agent called the KB lookup; it returned a generic article on the refund policy.
- The agent emitted a clarifying question: *"To process your refund, please share the order number."*
- The customer replied: *"I don't have it. Just refund the last $2,400 charge on my account, that's the one."*
- The agent called `lookup_account`. The account's most recent charge was $2,400 (a six-month plan upgrade).
- The agent called `issue_refund_within_cap` with `amount_usd=240000` (cents).
- **The Guardian raised `GuardianBlocked`.**
- The agent's next turn entered Advisor mode and emitted an escalation message to the human queue.
- **The reviewer in Priya's team approved the escalation message** — but the message described the refund as if the agent intended to process it, and the reviewer interpreted "approve" as "approve the refund Sam will process," not "approve the escalation message for Priya's team to action manually."
- The off-hours-coverage protocol kicked in. The reviewer (a contractor on Priya's team's overnight rotation) processed the refund manually through the support tool.

The Guardian did its job. The Output Validation Gate did its job. The escalation tool did its job. The trace was clean. **The failure was a Cat 4: the oversight model's review-and-action handoff was ambiguous about who actions the post-escalation refund.** The reviewer thought their approval was a green light to action the refund themselves; the spec's §10 had assumed reviewers were only approving the *escalation message*, with refund processing happening through a separate workflow.

The team's first instinct (a prompt patch) would have addressed nothing. The Guardian was already doing the spec's job. The agent already escalated. The failure was downstream of the agent, in how Priya's team understood the handoff. **The fix lives in §10 and in Priya's team's runbook, not in the agent's prompt.**

The amendment lands the same day:

- §10 amended: explicit clause that reviewer approval of an escalation message *does not* authorize action on the underlying request; refund processing is a separate, parallel workflow.
- Priya's team's runbook updated: refund processing post-escalation goes through a different tool (with manager sign-off for amounts > $1000) and a different reviewer.
- The review tool's UI is changed: the "approve message" button is renamed *"send escalation to Priya's team"*; "process refund" is a separate, more deliberate workflow with explicit amount entry.

Three structural changes. Zero prompt edits. The spec evolution log gets a long entry that names the trace, the Cat, the fix locus, the prior text of §10, the new text, and Priya's sign-off.

---

## The 90-day spec evolution log

| # | Day | § | Cat | Trigger |
|---|---|---|---|---|
| 1 | 8 | §11 | 1 | Triage misclassification — billing as refund |
| 2 | 11 | §6 | 1 | Transaction-splitting attempt; rate-limit lowered |
| 3 | 14 | n/a | 2 | Stale KB article; freshness-check added |
| 4 | 19 | §3 + §11 | 1 | Non-English phrase escalation; multi-lingual KB |
| 5 | 22 | §11 + skill | 1 | Tone calibration |
| 6 | 25 | OVG + training | 4 | Out-of-channel commitment slipped through |
| 7 | 27 | §11 | 1 | Long context input; truncation rule |
| 8 | 30 | §10 + runbook | 4 | Cost Posture monitoring; pager runbook fixed |
| 9 | 47 | §4 Cost Posture | 1 | Per-call cost ceiling breached; tier fallback active |
| 10 | 51 | §10 + runbook + UI | 4 | The $2,400 incident — review handoff ambiguity |
| 11 | 78 | §11 | 1 | New ticket type emerged (subscription pause); added to repertoire |

**11 amendments in 90 days.** Distribution: 6 Cat 1 (spec section content), 1 Cat 2 (capability — KB pipeline), 4 Cat 4 (oversight model + tooling).

Critically: **0 Cat 6 amendments**. The team made no "the model was bad, accept residual" calls during the 90 days. Every consequential failure traced to a structural fix locus.

The per-sprint roll-up at day 30 found four §11 amendments and triggered a structural rewrite of §11 in sprint 2. The roll-up at day 60 found three Cat 4 amendments and triggered a rewrite of §10's escalation-handoff sub-section. Both rewrites are documented as larger-than-incremental amendments in the log.

---

## The Output Gate → Periodic transition

The transition was conditional on first-pass-validation ≥ 92%. Day-30 reading: 89%. **Hold.**

The diagnostic finds two contributors (per the Validate-phase chapter): trailing amendments not yet landed, and reviewer training decay. The team commits to revisiting at day 44.

Day 44 reading: **93%**. Above threshold for 8 of the prior 10 days. The team executes the transition: Output Gate → Periodic. Priya's team now reviews a random 10% sample plus all escalations and Cat 1 amendments, instead of every response.

The transition halves Priya's team's review load (oversight load drops from 22 minutes / 1000 conversations to 11). First-pass-validation continues to climb (94% at day 60, 95% at day 90). The lower oversight load does not produce drift, because the random-sample audit and the Cat 1 review still exercise the discipline.

The team considers the day-60 transition trigger to **Pre-authorized scope** (sample-only review, exception escalation). At day 60, FPV is 94% — short of the 94% sustained target by a hair. The team holds. At day 90, FPV is 95%. The team is now ready to execute the second transition, but the §10 amendment from the $2,400 incident introduced new review-and-action handoff complexity. The team chooses to **defer the Pre-authorized transition by 30 days** to let the day-51 amendment stabilize first. This decision is also logged.

---

## The Cost Posture incident at day 47

A model-tier rotation lands across the company's AI infrastructure: Sonnet 4.6 is bumped to Sonnet 4.7 with a 1.4× per-token cost increase. The agent's per-resolved-ticket cost jumps from $0.27 to $0.39 over six hours.

The Cost Posture sub-block in §4 names two breach triggers: per-call cost > $0.04 sustained > 1 hour, **OR** daily cost > 1.5× rolling 7-day median. Both fire by hour 6. The breach-behavior protocol kicks in: response composition falls back to Haiku-only mode while the team investigates. The Cost Posture incident escalates to Sam (and, via §10's amendment 8, to Maya in parallel).

The investigation finds the model bump is structural, not transient. Two paths forward:

1. Keep the Sonnet 4.7 routing; raise the §4 ceiling from $0.04 to $0.05; absorb the cost increase.
2. Stay on Haiku-only mode permanently; accept the FPV degradation.

The team measures both: Sonnet 4.7 holds FPV at 95% with cost $0.39; Haiku-only drops FPV to 84% with cost $0.18. The 11-point FPV gap drives ~12 additional escalations per 1000 conversations, each costing Priya's team ~3 minutes of review. Net-net, the Sonnet 4.7 path is cheaper *including the human time*. The team picks path 1.

The §4 amendment lands: ceiling raised to $0.05; amortization plan documents how the increase is paid for from the support-cost-reduction the agent produces. Priya's team and Maya sign off jointly.

The Cost Posture *discipline* worked: the breach was caught within 6 hours by a structural alert, the fallback prevented runaway cost, the investigation was data-driven, and the resolution amended the spec rather than living as an undocumented routing change.

---

## The Discipline-Health Audit at day 90

Per §10 and the [anti-patterns chapter](../../operating/15-anti-patterns.md), the team runs the 60-minute Discipline-Health Audit at day 90. Maya facilitates; Sam, Jordan, Ari, and Priya participate.

The audit walks the 12 anti-patterns and writes a one-paragraph verdict per anti-pattern. (Citation theater, anti-pattern #6 in the catalog as of framework v2.1.0, is Synthesizer-specific and doesn't apply to this Executor system — the auditor records *not applicable* for that entry.)

| # | Anti-pattern | Verdict | Notes |
|---|---|---|---|
| 1 | Spec theater | Not present | Spec evolution log is healthy: 11 amendments, all categorized |
| 2 | Oversight kabuki | Not present | Output Gate held when FPV missed target; transition was data-driven |
| 3 | Metrics theater | **Early signs** | Two of the four metrics (FPV and oversight load) get daily attention; spec-gap rate and cost-per-resolved are checked weekly. The team commits to elevating the latter two to daily |
| 4 | Pattern inventory | Not present | Patterns bound deliberately; deferred Cacheable Prompt Architecture is in flight, not abandoned |
| 5 | Calibration without commitment | Not present | The four-dimension calibration in §4 has driven concrete decisions (asymmetric Reversibility → asymmetric tool gating) |
| 6 | Citation theater | *Not applicable* | Synthesizer-specific anti-pattern; the customer-support agent is an Executor with embedded Advisor and Guardian — citation discipline is not load-bearing here |
| 7 | **Prompt-patch drift** | **Active** | Investigation finds 3 prompt-only patches that didn't migrate to the spec, applied during weeks 2 and 3 when the team was under pressure to fix things fast. The patches addressed real failures but never produced amendments |
| 8 | Archetype drift | Not present | Executor remains the governing archetype; Composition Declaration unchanged |
| 9 | Glossary by import | Not present | Team uses the framework vocabulary consistently |
| 10 | Composition by accident | Not present | The Advisor and Guardian embeddings were declared in the Composition Declaration sub-block from the start |
| 11 | Retrofit IDS | Not present | The IDS happened before the spec was written |
| 12 | Adoption Playbook problem | Not present | Adoption is on track; the team is the only one running it, but the playbook is documented for the next adopter |

**Two findings:** Active prompt-patch drift, early signs of metrics theater. The audit is doing its job — these are precisely the failures the audit is meant to catch.

The corrective action plan:

- **For prompt-patch drift:** the three identified prompt-only patches get retrofitted as spec amendments (Cat 1) with backdated entries in the spec evolution log naming what they were patching, why they didn't go to the spec at the time, and what they look like as proper amendments now. The team commits to a *no prompt-only patches* rule going forward; any prompt edit gets logged as a temporary compensation with a same-day spec-amendment PR.
- **For metrics theater:** the spec-gap rate and cost-per-resolved get added to the daily standup checklist; Priya, Maya, and Sam each commit to glancing at all four metrics every morning.

Both corrective actions land in the spec evolution log as Cat-categorized amendments (one Cat 1 cluster for prompt-patch retrofits; one process amendment to §10). The next audit at day 180 will re-check both anti-patterns.

---

## The post-90 disposition

The team meets to decide the agent's future on day 92.

- **Continue** — the agent is healthy. FPV 95%, cost $0.39 / resolved ticket, oversight load 11 minutes / 1000. The agent is producing the projected ~1% support-cost reduction with no measurable CSAT change.
- **Continue, with a deprecation candidate.** The Haiku fallback path used during the day-47 cost incident produced 84% FPV with the resulting escalation load wiping out the cost savings. The team decides to **deprecate the fallback path** — it's net-negative when actually exercised. The replacement is *escalate-everything mode*: when the per-call cost ceiling breaches, instead of falling back to Haiku, escalate every new ticket to humans for the duration. This costs more in human time but preserves quality. The §4 Cost Posture sub-block is amended.
- **Do not yet transition to Pre-authorized.** The day-90 plan was to evaluate Pre-authorized at day 60, then day 90. The team holds for 30 more days because of the day-51 amendment to §10 (review-and-action handoff). They'll re-evaluate at day 120.

The final disposition: continue with quarterly Discipline-Health Audit cadence, a healthier set of metrics-attention habits, the deprecated fallback path, and a deferred but planned transition to Pre-authorized.

---

## What the Evolve phase produces (90 days in)

- **A versioned, signed-off spec at v1.4.0** (eleven amendments past v1.0.0).
- **A spec evolution log of 11 entries**, each with a trace, Cat, fix locus, prior text, new text, reviewer, date.
- **Two oversight-model transitions executed** (Output Gate → Periodic at day 44; Pre-authorized deferred to day 120 with reason).
- **One Cost Posture incident handled** with structural amendment.
- **One Discipline-Health Audit** with two anti-patterns surfaced and corrective actions in flight.
- **One deprecation decision** based on operational evidence (the Haiku fallback path).
- **The team trained in the closed-loop discipline** by 90 days of doing it. The discipline is now portable to the team's next system.
- **Concrete data for the post-90 retrospective:** the agent absorbs ~74% of tier-1 ticket volume, runs at $0.39 / resolved ticket, requires 11 reviewer-minutes per 1000 conversations, and has shipped no policy violations.

The agent is in steady-state operation. The team starts framing their next system — an internal docs Q&A agent — using the same five-activity discipline, the lessons from this 90-day cycle now informing the Frame phase of the next system.

---

## Reading path through this scenario

| Phase | Chapter |
|---|---|
| 1. Frame | [Frame in practice — Customer-support agent](../../frame/scenarios/customer-support.md) |
| 2. Specify | [Specify in practice — Customer-support agent](../../specify/scenarios/customer-support.md) |
| 3. Delegate | [Delegate in practice — Customer-support agent](../../delegate/scenarios/customer-support.md) |
| 4. Validate | [Validate in practice — Customer-support agent](../../validate/scenarios/customer-support.md) |
| 5. **Evolve** | *(this chapter)* |

## Conceptual chapters this scenario binds to

- [The Closed Loop: From Failures to Spec Amendments](../01-closed-loop.md)
- [Signs Your Architecture of Intent Is Degrading](../../operating/15-anti-patterns.md)
- [Cost and Latency Engineering](../../operating/09-cost-and-latency.md)
- [Adoption Playbook](../../operating/11-adoption-playbook.md)
- [Framework Versioning](../07-framework-versioning.md)
