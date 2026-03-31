# Pattern 2.4 — Design for Reversibility

**Part II: Theory of Intent Engineering** · *4 of 6*

---

> *"A decision is only as dangerous as the cost of being wrong. Design your oversight proportionally to that cost — not to the probability of error."*

---

## Context

You are calibrating how to delegate work to an agent: how much autonomy to grant, what oversight to require, how tight to make the constraints. The previous pattern gave you vocabulary for agency, autonomy, and responsibility. This pattern gives you the fourth and most practically important calibration variable: **reversibility**.

Reversibility is the variable that determines how much a mistake matters. High agency is acceptable when mistakes are cheap to fix. Even low agency can be dangerous when mistakes cannot be undone.

This pattern assumes [Three Dimensions of Delegation](03-agency-autonomy-responsibility.md) and is a prerequisite for [Four Dimensions of Governance](../architecture/03-archetype-dimensions.md).

---

## The Problem

Most engineering risk management focuses on the **probability** of failure. We write tests to reduce failure probability. We do code review to reduce failure probability. We use staging environments to reduce failure probability.

But probability of failure is only half the risk equation. The other half is the **consequence of failure** — which is shaped primarily by reversibility.

A highly autonomous agent that generates draft documentation has very low consequence of failure: the drafts can be reviewed and discarded. A highly autonomous agent that sends emails to ten thousand customers on your behalf has very high consequence of failure: the emails cannot be recalled. Both might have the same probability of making a mistake. The risk profiles are incomparably different.

Teams that do not reason explicitly about reversibility will:
- Over-constrain low-consequence, high-reversibility systems (because they feel risky due to high automation) — slowing them down unnecessarily
- Under-constrain high-consequence, low-reversibility systems (because they feel familiar) — creating latent catastrophic failure risk

The pattern of under-constraining familiar irreversible systems is particularly dangerous. Sending emails, modifying production databases, calling billing APIs, pushing git commits, posting to social accounts — these all feel like "simple tasks" and they are all, in varying degrees, irreversible.

---

## Forces

- **Probability focus vs. consequence reality.** Engineering risk management traditionally emphasizes reducing probability of failure; intent engineering must also govern the consequence when failures still occur, which reversibility shapes.
- **Automation appeal vs. irreversibility danger.** Systems that feel safe and simple often take irreversible actions; high automation on irreversible operations is dangerous regardless of error probability.
- **Operational efficiency vs. oversight overhead.** Testing and review add cost and latency; but for irreversible operations, the cost of undetected failure is so high that sufficient oversight is non-negotiable.

---

## The Solution

### Defining Reversibility

**Reversibility** is the degree to which an action can be undone, corrected, or rolled back after it has been taken.

Reversibility is a spectrum with four practical zones:

| Zone | Description | Examples |
|------|-------------|---------|
| **Fully reversible** | Action can be completely undone with no residual effect | Generating a draft, editing a local file, creating a test record |
| **Largely reversible** | Action can be undone with some effort or partial side effects | Publishing a blog post (can be unpublished), creating a cloud resource (can be deleted, but billed) |
| **Partially reversible** | Primary action can be reversed but side effects persist | Sending one email (can follow up, but first email was received), pushing code to a branch (can be reverted, but others may have seen it) |
| **Irreversible** | Action cannot be meaningfully undone | Sending mass email, deleting production data without backup, making a financial transaction, revoking credentials |

---

### The Risk Matrix

The practical design tool is the intersection of agency and reversibility:

```
              LOW AGENCY        HIGH AGENCY
              
REVERSIBLE    ┌─────────────┬─────────────┐
              │  LOW RISK   │  MEDIUM RISK│
              │  Automate   │  Constrain  │
              │  freely     │  well; light│
              │             │  oversight  │
IRREVERSIBLE  ├─────────────┼─────────────┤
              │  MEDIUM RISK│  HIGH RISK  │
              │  Gate on    │  Maximum    │
              │  human      │  oversight; │
              │  approval   │  mandatory  │
              │             │  human gate │
              └─────────────┴─────────────┘
```

**Low agency + reversible:** The default safe zone. Automate freely. Monitoring is sufficient oversight.

**High agency + reversible:** The productive zone. Grant the agent latitude to decide how to achieve the goal. Review outputs; don't gate each step. Correct errors cheaply.

**Low agency + irreversible:** The approval zone. The action itself carries consequence, so require a human gate — not because the agent will make a bad decision (its agency is low) but because the cost of any error is non-trivial.

**High agency + irreversible:** The maximum oversight zone. Both the range of decisions and the consequences of error are high. This combination requires: explicit constraints in the spec, mandatory human review before any irreversible action executes, audit logging, and clearly assigned responsibility. Never deploy this combination with informal oversight.

---

### Reversibility in Spec Design

Every spec for a system that takes actions in the world should include a reversibility assessment. This is not a formal audit — it is a deliberate thinking exercise:

**For each action the system can take:**
- Is this action reversible?
- If not, what is the consequence of taking this action incorrectly?
- What oversight gate protects this action?
- Is the oversight gate proportional to the consequence?

A well-designed spec will often reveal that most actions in a system are reversible (or easily made reversible), and a small number are not. Those irreversible actions become the focus of oversight design.

---

### Making Things More Reversible: A Design Choice

Reversibility is not a fixed property of the problem domain. It is often a design choice.

**Soft deletes instead of hard deletes.** Data marked deleted is reversible. Data purged from the database is not.

**Draft queues before delivery.** An email queued for review is reversible. An email sent is not.

**Dry-run modes.** An agent that can simulate its actions before executing them converts irreversible operations into reviewable ones.

**Approval gates.** A system that collects a set of decisions and presents them for human review before executing any of them is more reversible than one that executes each decision immediately.

These patterns do not eliminate the need for good intent specification — they buy time for the oversight loop to catch mistakes. They are the engineering equivalent of a circuit breaker: a mechanism that limits consequence when the actual prevention mechanism (good specs, good constraints) was insufficient.

---

### Reversibility and Living Specs

There is a temporal dimension to reversibility that matters for [Living Specs](../sdd/06-living-specs.md): the longer a system runs on a spec that has not been reviewed, the more likely it is that the original intent has drifted from the current reality. Irreversible systems that have been running unreviewed are potentially executing on outdated intent.

The practical rule: the oversight cadence for a system should be proportional to its irreversibility. A system making irreversible changes to production data should be reviewed more frequently than a system generating draft content.

---

## Resulting Context

After applying this pattern:

- **Risk matrices become actionable design tools.** Different combinations of agency and reversibility demand different oversight structures; low-risk combinations can be streamlined while high-risk ones receive mandatory controls.
- **Reversibility becomes a designable property.** Soft deletes, draft queues, and approval gates convert what appears irreversible into manageable, reviewable work — expanding the scope of what can be safely automated.
- **Oversight intensity calibrates to actual consequence.** High agency is acceptable when mistakes are cheap to fix; low reversibility demands structured oversight regardless of how "simple" the task feels.

---

## Therefore

> **Reversibility is the most important risk calibration variable in agent system design. The combination of high agency and low reversibility requires the highest oversight. The combination of low agency and high reversibility can be automated freely. Design oversight structures proportional to this combination — not to the probability of error, which agents can reduce, but to the consequence of error, which only humans can govern.**

---

## Connections

**This pattern assumes:**
- [Three Dimensions of Delegation](03-agency-autonomy-responsibility.md)

**This pattern enables:**
- [Failure as Diagnostic Signal](05-failure-as-design-signal.md) — what happens when this calibration fails
- [Four Dimensions of Governance](../architecture/03-archetype-dimensions.md) — reversibility as a formal archetype axis
- [Proportional Oversight](../agents/06-human-oversight-models.md) — designing oversight to match reversibility
- [The Canonical Spec Template](../sdd/07-canonical-spec-template.md) — the "must never happen" and oversight sections

---

*Next: [Failure as Diagnostic Signal](05-failure-as-design-signal.md)*

