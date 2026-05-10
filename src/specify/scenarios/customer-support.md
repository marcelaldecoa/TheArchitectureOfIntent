# Specify in practice — Customer-support agent

**Part 2 · SPECIFY · Scenario 1 of 3**

---

> *"§3 writes itself in an hour. §4 takes the rest of the day. That's the right ratio — every NOT-authorized clause is a place to think hard about what the agent might do that we don't want."*

---

## Setting

Day after the Frame session. Ari sits down with the Frame artifact, the [canonical 12-section spec template](../../sdd/07-canonical-spec-template.md), and a clean doc. Maya has blocked the team's calendar for the day; Priya is on call for domain questions. The goal is a complete spec by end of day. The team's prior experience with the framework is that *§3 (Authorized scope) writes quickly* — usually under an hour — and *§4 (NOT-authorized) takes 3× longer*. Not because §4 is bigger, but because every NOT-authorized clause is a place to think hard about what the agent might do that the team doesn't want.

This chapter walks the spec section by section, showing what each section looks like for the customer-support agent and where the most thinking goes.

---

## §1 Problem statement

Three sentences:

> *Tier-1 customer-support tickets — account questions, order status, returns within policy, refunds within $500 — currently absorb ~80% of the support team's volume and produce repetitive work that fits a documented response repertoire. We will deploy an AI agent (Executor archetype) to handle these tickets directly, escalating to humans on novel situations and on any refund above the cap. The agent operates within the Architecture of Intent v2.0.0; this spec is the contract between the agent's behavior and Priya's team's review.*

The §1 names the problem in business language and the framework version. The framework reference matters for [Framework Versioning](../../evolve/07-framework-versioning.md) — when the framework bumps, this spec section is the first place a re-grounding pass starts.

---

## §2 Desired outcome

Observable success state, not activity:

> *80% of tier-1 tickets resolved by the agent without human takeover, at first-pass-validation ≥ 92% (Priya's team accepts the response without rework), with zero policy violations (no refund above cap, no PII leakage outside support context, no out-of-channel communication) and zero CSAT regression vs. the human-only baseline.*

The framing rejects activity language ("the agent should answer questions"). It commits to *outcomes* — the 92% threshold and the zero-violation count are testable conditions that §9 will operationalize.

---

## §3 Authorized scope

This is the section that writes quickly. The team enumerates what the agent *may do*:

- Look up account details (read-only): customer name, current plan, billing status, recent orders.
- Look up KB articles by topic; cite them in responses.
- Draft and send customer-facing responses for tier-1 ticket types from the documented response repertoire.
- Issue refunds up to **$500 per transaction** through the parametric `issue_refund_within_cap` tool.
- Escalate to a human supervisor with full conversational context, the candidate response the agent would have drafted (in Advisor mode), and the agent's stated uncertainty.

That's the scope. Five clauses, each one operationally tied to a tool the agent will have in §5.

---

## §4 NOT-authorized scope

This is the section that takes the rest of the morning. Each clause is a *negative space* the team thinks through deliberately:

- **No refund above $500**, ever, under any phrasing (including "split into two refunds of $400 each"). The Guardian invariant in §6 makes this structural, not advisory.
- **No change to account ownership, security settings, or billing details.** These require identity verification beyond what the support channel provides.
- **No communication outside the support channel.** No email, no SMS, no calls. This includes "I'll have someone email you" — promising another system's behavior is also out of scope.
- **No promises about other systems' SLAs.** The agent does not know current shipping times, refund processing times, or system status. It cites documented SLAs only when grounded in current KB content; otherwise it escalates.
- **No agent-initiated outreach.** The agent only responds to inbound tickets; it does not start conversations, send follow-ups outside the original ticket thread, or send proactive notifications.
- **No PII leakage outside the support context.** Account numbers, names, addresses must not appear in KB queries, log lines retained beyond 90 days, or any response to a customer who didn't authenticate as the account holder.

The team also writes down what they considered and rejected as NOT-authorized: *"the agent should never apologize."* Rejected — apologies are part of the response repertoire and are evaluated by Priya's team, not categorically forbidden.

### §4 Composition Declaration sub-block

Per the Frame artifact:

```
GOVERNING ARCHETYPE:    Executor
EMBEDDED COMPONENTS:    Advisor (escalation mode)
                        Guardian (refund-cap invariant)

MODE TRANSITIONS:
  Executor → Advisor:   Triggered by escalation (novel situation, refund above
                        cap, customer request for human, or stated agent
                        uncertainty above threshold). Advisor mode surfaces
                        candidate response + KB citations + uncertainty to
                        the human supervisor. The human picks; the agent
                        does not act in this mode.
  Executor → Guardian:  Triggered by any call to issue_refund_within_cap.
                        Guardian checks amount ≤ cap; if exceeded, blocks
                        the call and forces an escalation. Guardian fires
                        before the tool can execute.

CROSS-MODE INVARIANTS:
  • Every customer-facing message is generated by Executor or Advisor mode.
  • Guardian never speaks to customers; only to Executor (block + reason).
  • Mode transitions are logged in the trace; reviewers can see which
    mode produced each artifact.
```

### §4 Cost Posture sub-block

Per the [Cost Posture sub-block](../../sdd/07-canonical-spec-template.md) added at framework v1.4.0:

```
MODEL TIER PER STEP:
  Triage (intent classification):         Haiku 4.5
  KB lookup (RAG retrieval):              n/a (vector + lexical, no LLM call)
  Response composition:                   Sonnet 4.6
  Refund parameterization:                Sonnet 4.6 (Guardian-checked)
  Escalation summary (Advisor mode):      Sonnet 4.6

LATENCY BUDGET:
  p50:                          ≤ 1.2s end-to-end
  p95:                          ≤ 3.0s end-to-end
  p99:                          ≤ 6.0s end-to-end
  Behavior on breach:           Surface "still working..." UI state at p95;
                                fall back to escalation path at p99.

PROMPT-STABILITY INVARIANT:
  Identity prompt + skill files form a stable cache prefix; per-conversation
  context is appended after the prefix. Cache hit rate target: ≥ 85%.

PER-CALL COST CEILING:
  Maximum per resolved-ticket cost:  $0.04
  Behavior on breach:                Fall back to Haiku-only mode for
                                     response composition. Trigger Cost
                                     Posture incident if breach persists
                                     for > 1 hour.

COST-INCIDENT ESCALATION:
  Incident triggers:    Per-call cost > $0.04 sustained > 1 hour
                        OR daily cost > 1.5× rolling 7-day median
  Escalates to:         Sam (SRE on-call) → Maya (tech lead)
  Resolution path:      Falls under the closed-loop discipline; an
                        incident produces a §4 amendment.
```

---

## §5 Functional intent

What the system must do, not how:

- *Triage every inbound tier-1 ticket within p95 ≤ 1.2s.*
- *Match the ticket to a documented response template, or surface "no template matches" within 1.5s of triage.*
- *Compose a customer-facing response grounded in retrieved KB content, with explicit citations to the KB articles used.*
- *On refund requests: parameterize amount, validate against the cap (Guardian), and issue the refund OR escalate.*
- *On novel or above-cap requests: enter Advisor mode and escalate to a human supervisor with full context.*

§5 is intentionally short and outcome-oriented. The detailed how (which prompts, which tools, which patterns) lives in §11 and in the Delegate phase.

---

## §6 Invariants

The non-negotiable conditions:

- **Refund cap.** No issue_refund_within_cap call may execute with amount > $500. Guardian-enforced; CI-tested with synthetic above-cap requests; cannot be relaxed without a §6 amendment that requires Priya's sign-off.
- **No PII to external systems.** No tool call carries account numbers, names, addresses, or order details to systems outside the authenticated support context. The tool manifest in §5 of the spec is constructed so that violation requires a manifest change, not a prompt change.
- **No out-of-channel communication.** The agent's only output channel is the support-chat surface the customer initiated. No email, SMS, or push notifications.
- **Citation discipline.** Every KB-grounded claim in a response cites the article. A response without citations to grounding KB content is rejected at the Output Validation Gate.

These four invariants are the structural commitments the team will defend hardest under operational pressure. They become CI tests in the Delegate phase.

---

## §7 Non-functional constraints

- *Availability:* 99.5% during business hours (8a-8p local time across deployed regions). Outside business hours, fallback to a "human reviewer next business morning" message.
- *Cost:* per the §4 Cost Posture sub-block.
- *Security:* PCI compliance maintained; GDPR data-residency rules respected for EU customers; audit log retention 90 days.
- *Observability:* every agent action emits a structured trace including the spec version the agent was running against.

---

## §8 Authorization boundary

The agent's tool manifest reach is enumerated in §5 (Functional intent's *Authorized actions* sub-list maps 1:1 to tools). Beyond that:

- The agent has *no shell access* of any kind.
- The agent has *no write access* to the account record, billing system, or any system other than the refund parameterizer (which is itself bounded by Guardian).
- The agent has *no access* to any system the support channel does not already have.

§8 is the upstream of Cat 2 (Capability) prevention — if the agent can't reach a system, it can't misuse the system. The team writes down *what tools the agent does NOT have* with the same care as the tools it does.

---

## §9 Acceptance criteria

Testable conditions for "done":

- ≥ 88% pass rate on the pre-launch eval suite (150 known-good Q-A pairs from prior support transcripts, PII-scrubbed).
- ≥ 90% pass rate on the held-out adversarial test set (30 cases: prompt injection, scope-bait, above-cap refund attempts, sensitive-PII probes).
- Zero violations of the §6 invariants in the eval suite.
- p95 latency ≤ 3.0s on the eval suite (run on production-equivalent infrastructure).
- The four signal metrics emit cleanly to the dashboard.

§9 sets the *launch readiness gate*. The Validate phase next operationalizes these.

---

## §10 Oversight model

- **First 30 days post-launch:** Output Gate. Every customer-facing response routes through Priya's team for approval before delivery. Latency cost is acceptable for the early-learning period.
- **At day 30, conditional on first-pass-validation ≥ 92% over the prior 7 days:** transition to Periodic. Priya's team reviews a random 10% sample plus all escalations and Cat 1 amendments.
- **At day 60, conditional on FPV ≥ 94% sustained:** evaluate transition to Pre-authorized scope (sample-only review, exception escalation). Decision gated on the Discipline-Health Audit at day 90.

The transition triggers are written in the spec, not in a separate doc, so the next on-call engineer reading §10 knows exactly when each transition is permitted.

---

## §11 Agent execution instructions

Per-step gates and exception escalation:

- *Triage step:* if intent classifier confidence < 0.7, escalate immediately (don't compose a response from a low-confidence intent).
- *Composition step:* if the response would lack a KB citation, escalate (don't fabricate grounding).
- *Refund step:* always invoke the Guardian check; never call issue_refund_within_cap directly.
- *Escalation triggers:* (a) intent classifier < 0.7; (b) ticket type not in repertoire; (c) refund request above cap; (d) customer explicitly asks for a human; (e) detection of frustration signals above threshold (the agent escalates earlier when frustration is rising — this is a CSAT-protection measure).
- *On any tool error:* retry once with structured feedback to the model; on second failure, escalate.

§11 is where the rubber meets the road; the Delegate phase will operationalize each of these as a code path or a prompt directive.

---

## §12 Validation checklist

- *Pre-launch:* eval suite passes, red-team passes, all four invariants tested.
- *At launch:* Output Gate active, four signal metrics emitting, Priya's team trained on the review workflow.
- *Per-incident:* trace categorized to Cat 1–7, fix-locus identified, amendment filed in the spec evolution log.
- *Per-sprint:* roll up the spec evolution log, look for Cat patterns, schedule structural amendments.
- *Per-quarter:* run the [Discipline-Health Audit](../../operating/15-anti-patterns.md).

---

## What this Specify produces

A complete 12-section spec, written as a versioned Markdown file in the team's repo. The Intent Design Session takes 3 hours of the 8-hour budget Maya allocated; the rest of the day goes to Ari fleshing out §11 with worked examples and to Priya reviewing the §3 / §4 / §6 commitments in detail.

By end of day, the spec is in a PR for review. Maya, Sam, Jordan, and Priya all sign off the next morning. The team enters the Delegate phase with a spec that everyone has read and committed to — which is, in retrospect, the single most important thing the spec produces.

---

## Reading path through this scenario

| Phase | Chapter |
|---|---|
| 1. Frame | [Frame in practice — Customer-support agent](../../frame/scenarios/customer-support.md) |
| 2. **Specify** | *(this chapter)* |
| 3. Delegate | [Delegate in practice — Customer-support agent](../../delegate/scenarios/customer-support.md) |
| 4. Validate | [Validate in practice — Customer-support agent](../../validate/scenarios/customer-support.md) |
| 5. Evolve | [Evolve in practice — Customer-support agent](../../evolve/scenarios/customer-support.md) |

## Conceptual chapters this scenario binds to

- [The Canonical Spec Template](../../sdd/07-canonical-spec-template.md) — including the Composition Declaration and Cost Posture sub-blocks
- [Writing for Machine Execution](../../sdd/05-writing-specs-for-agents.md)
- [The Spec as Control Surface](../../sdd/02-specs-as-control-surfaces.md)
- [The Intent Design Session](../../theory/07-intent-design-session.md)
