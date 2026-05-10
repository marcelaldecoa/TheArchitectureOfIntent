# Frame in practice — Customer-support agent

**Part 1 · FRAME · Scenario 1 of 3**

---

> *"We haven't framed yet. Pick the archetype first; the spec writes itself once the archetype is committed."*

---

## Setting

Mid-stage e-commerce SaaS, ~200 employees, ~50,000 active customers. The customer-support team handles ~3,000 inbound chats per day across two tiers; tier-1 (account questions, order status, returns within policy, refunds within $500) absorbs ~80% of volume. The product manager has greenlit *"AI-assisted tier-1 support for the next quarter"* with a specific revenue-protection target — 1% reduction in human-support cost, no SLA degradation, no measurable change in CSAT.

The team:

- **Maya** — engineering tech lead, owns the system end-to-end
- **Ari** — ML engineer, will write the spec
- **Sam** — SRE, will own the build and the on-call rotation
- **Jordan** — full-stack engineer
- **Priya** — customer-support manager, *domain owner* (per the [RACI Card](../../appendices/raci-card.md))

The team gathers for a 90-minute Frame session in a conference room with a whiteboard. Their first instinct, as engineers, is to start specifying — Jordan opens a doc and types *"the agent must..."*. Maya stops them: *"We haven't framed yet. Pick the archetype first; the spec writes itself once the archetype is committed."* The doc gets closed. The whiteboard gets marker.

---

## The three questions

Before the archetype tree, the team answers the three questions every delegated system has to answer. The whole [Architecture of Intent](../../introduction.md#what-is-the-architecture-of-intent) hangs on getting these right; rushing them is the most common Frame failure.

**1. What is this system trying to achieve?**

The room agrees on: *"resolve tier-1 support tickets that fit a documented response repertoire, and route the rest to humans without losing context."* Note what the framing rejects: *"answer customer questions"* (too broad — would license the agent to invent facts about the product), *"reduce support cost"* (too vague — describes a business outcome, not a system intent), *"deflect tickets"* (frames the customer as adversarial, sets the wrong incentive).

**2. Within what constraints?**

Priya owns this answer. The team writes:

- Refund authority is bounded at $500 per transaction; above that, escalate.
- The agent cannot communicate outside the support channel (no email, no SMS, no calls).
- The agent cannot change account ownership, security settings, or billing details.
- The agent cannot promise behavior of other systems ("your refund will arrive in 3 days") without grounding in current SLAs.
- PII may not leave the support context — no copying account numbers into KB lookups, no logs that retain conversational history beyond 90 days.

These are *constraints*, not preferences. They become §4 NOT-authorized clauses in the spec next phase.

**3. How will we know it's working?**

The team commits to four signals (the [four signal metrics](../../validate/06-metrics.md), instantiated for this system):

- *Spec-gap rate* — amendments per 1000 conversations. Target trajectory: high in month 1 (the spec is new), declining through month 3.
- *First-pass validation* — % of agent responses Priya's team accepts without rework. Target: ≥ 92% by day 30.
- *Cost per resolved ticket* — tokens + escalation cost / tickets resolved without human takeover. Target: ≤ $0.40.
- *Oversight load* — Priya's team's review minutes per 1000 conversations. Target: < 30 minutes.

These are written down before any spec is drafted. If the team can't agree on the targets, they don't yet have the framing they think they have.

---

## The archetype call

The team walks the [archetype selection tree](../../frame/04-decision-tree.md), question by question:

**Q1 — does the system *act*, or only *inform*?** It acts: it issues refunds, drafts customer-facing responses, escalates with context. *Not Advisor alone.*

**Q2 — does the system *coordinate other agents*, or *act directly*?** It acts directly. There is no other agent in the deployment. *Not Orchestrator.*

**Q3 — is the system's primary purpose to *block or veto* (Guardian) or to *act within scope* (Executor)?** It acts within scope. The refund cap is an invariant the system *enforces on itself* but the system's primary job is to take action, not to gatekeep someone else's action. *Executor.*

**Q4 — does the action involve *combining inputs into a new whole* (Synthesizer)?** No. The agent retrieves canned responses from a KB and parameterizes them; it doesn't compose a novel response from disparate sources. *Not Synthesizer.*

The archetype is **Executor**.

The team considers the *risk-override caret* on the canvas: *"irreversible · regulated · safety-critical → elevate one step toward Orchestrator."* Refunds are partially irreversible (a refund to a closed account is not recoverable), and the company is regulated (PCI, GDPR for EU customers). Does this warrant elevation?

The team decides no, for two specific reasons: (1) the refund cap of $500 makes the irreversible portion bounded — even a worst-case unauthorized refund is recoverable through the chargeback workflow; (2) PCI / GDPR concerns are addressed by the §4 NOT-authorized clauses, not by the archetype. Elevating to Orchestrator would imply a coordinator-of-agents shape that the deployment doesn't have. The team commits to Executor and writes the rejection of the elevation in the Frame artifact — so a future reviewer doesn't second-guess the decision without the context.

---

## Composition declaration

The team uses [composition first-class](../../frame/05-composing-archetypes.md) (Pattern A — *Confirm-then-Act* and Pattern B — *Executor + Guardian*) rather than treating the system as a single Executor. Specifically:

- **Executor (governing).** The agent acts on tier-1 tickets within the documented response repertoire.
- **Advisor (embedded).** When the agent escalates to a human supervisor, it does so in *Advisor mode* — surfacing the relevant KB articles, the candidate response it would have drafted, and its uncertainty. The human picks; the agent doesn't decide for them.
- **Guardian (embedded).** The refund cap is enforced as a Guardian invariant, not as a soft check. The Guardian fires *before* the issue_refund tool can be called; if the proposed refund exceeds the cap, the action is blocked and the request escalates.

The Composition Declaration is written explicitly. It will land in §4 of the spec next phase as the *Composition Declaration sub-block*. The cross-mode invariant — *"every customer-facing message is generated by Executor or Advisor mode; Guardian never speaks to customers, only to Executor"* — is also written down.

---

## Calibration of the four dimensions

The team works the four orthogonal calibration dials ([Calibrate Agency, Autonomy, Responsibility, Reversibility](../../foundations/03-agency-autonomy-responsibility.md)). The temptation is to collapse them into "how autonomous is the agent?" — Maya rejects that explicitly: *"Set them independently. Treat each dimension as its own commitment."*

| Dimension | Setting | Reason |
|---|---|---|
| **Agency** | low | The agent acts only within a documented response repertoire. Novel situations escalate. |
| **Autonomy** | low–medium | Chained actions (KB lookup → draft response → send) run without per-step approval. Novel actions (refund, escalation) trigger a structural step (Guardian check or handoff). |
| **Responsibility** | shared | Operationally on the agent (it produced the action). Authorially on Priya (she owns the spec). The customer is not responsible for evaluating the agent's correctness; Priya's team is. |
| **Reversibility** | mixed | Messages are high-reversibility (a follow-up message can correct prior tone). Refunds are partially irreversible (R3 — recoverable through chargeback workflow within a window). The spec will treat these classes asymmetrically. |

The asymmetric Reversibility commitment is the calibration that drives the most downstream design. It means the §11 execution instructions will gate the issue_refund tool differently from the draft_response tool, and the oversight model in §10 will treat refund-bearing conversations differently from message-only conversations.

---

## What this Frame produces

A one-page Frame artifact lands in the team's planning doc:

```
SYSTEM:        Customer-support agent (tier-1)
ARCHETYPE:     Executor (governing)
COMPOSITION:   + Advisor (embedded, escalation mode)
               + Guardian (embedded, refund-cap invariant)
CALIBRATION:   Agency low · Autonomy low-medium · Responsibility shared · Reversibility mixed
RISK OVERRIDE: Considered (refund irreversibility, PCI/GDPR); rejected — bounded by cap, addressed by §4
THREE QS:      [as above]
SIGNALS:       [the four metric targets, with month-1/month-3 trajectory]
```

This artifact is the input to [Specify in practice — Customer-support agent](../../specify/scenarios/customer-support.md). The discipline is that nothing in the spec contradicts what's on this page; if a spec section pushes back on the Frame artifact, the team re-runs the Frame discussion before continuing the spec.

The Frame session takes 90 minutes. Maya circulates the artifact for sign-off the same day. Priya signs off as the domain owner. The team starts on the spec the next morning.

---

## Reading path through this scenario

| Phase | Chapter |
|---|---|
| 1. **Frame** | *(this chapter)* |
| 2. Specify | [Specify in practice — Customer-support agent](../../specify/scenarios/customer-support.md) |
| 3. Delegate | [Delegate in practice — Customer-support agent](../../delegate/scenarios/customer-support.md) |
| 4. Validate | [Validate in practice — Customer-support agent](../../validate/scenarios/customer-support.md) |
| 5. Evolve | [Evolve & Operate in practice — Customer-support agent (90 days post-launch)](../../evolve/scenarios/customer-support.md) |

## Conceptual chapters this scenario binds to

- [Pick an Archetype](../../frame/02-canonical-intent-archetypes.md) — the Executor archetype
- [Composing Archetypes](../../frame/05-composing-archetypes.md) — Pattern A (Confirm-then-Act), Pattern B (Executor + Guardian)
- [Calibrate Agency, Autonomy, Responsibility, Reversibility](../../foundations/03-agency-autonomy-responsibility.md) — the four-dial model
- [The Intent Design Session](../../foundations/07-intent-design-session.md) — Frame is its first phase
- [Roles & Responsibilities (RACI) Card](../../appendices/raci-card.md) — Priya as the domain owner

## Source material

The earlier v1.x version of this worked pilot is preserved in [Designing an AI Customer Support System](../../examples/01-ai-customer-support/README.md) for reference. The v2.0.0 phase-by-phase form supersedes it; both are kept so readers comparing the framings can see the difference the activity-spine reorganization makes.
