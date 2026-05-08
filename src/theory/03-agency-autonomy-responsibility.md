# Calibrate Agency, Autonomy, Responsibility, Reversibility

**Part 1 — Decisions**

---

> *"Autonomy without authority is a faster way of doing what you were told. Agency without accountability is a faster way of causing harm. Reversibility is what determines whether either of those matters."*

---

## Context

You have selected an archetype. Now you have to decide, for the system you are about to specify, *how much* of each of four things it gets:

- **Autonomy** — how much of its work runs without human intervention at each step.
- **Agency** — how much discretion it exercises when its instructions don't fully cover the situation.
- **Responsibility** — how accountability for what it does is distributed across the people around it.
- **Reversibility** — how easy or hard it is to undo what it does.

These four are the dials. Every archetype comes with default settings, but the specifics of *your* system live in how you tune them. Tune them deliberately, in the spec, before the agent runs — or they will be tuned for you by accident.

---

## The Problem

Most teams collapse these four into a single intuition: "how autonomous is the agent?" That intuition hides the calibration work that actually matters.

A deployment pipeline that runs on commit is "autonomous." So is an agent that decides to delete files it considers redundant. Treating these with the same design pattern is a category error: the first has high autonomy and almost no agency; the second has high autonomy *and* high agency *and* potentially low reversibility, and it should not be deployed without explicit oversight design.

Similarly, "responsibility" gets used to mean legal liability, ethical answerability, operational accountability, and technical error-catching — all in the same conversation. Without distinguishing them, accountability discussions produce more confusion than clarity.

If you cannot describe an agent's profile across all four dimensions, you cannot decide whether your oversight is proportional, whether your spec is precise enough, or whether deployment is safe.

---

## Forces

- **Automation desire vs. control necessity.** Teams want high autonomy to reduce labor; high autonomy paired with high agency over irreversible actions is ungovernable without explicit accountability structure.
- **System capability vs. human understanding.** Agents can act in domains the original authors didn't fully anticipate; responsibility cannot be left vague — failures with no diagnosis path become unfixable.
- **Probability focus vs. consequence reality.** Engineering risk management traditionally emphasizes reducing probability of failure; agent systems must also govern the *consequence* when failures occur. Reversibility is the dimension that shapes consequence.
- **Operational efficiency vs. oversight overhead.** Testing and review add latency; for irreversible operations, the cost of an undetected failure is so high that adequate oversight is non-negotiable.

---

## The Solution

### Dimension 1 — Autonomy: the operational dimension

**Autonomy** is the degree to which a system executes a process without requiring human intervention at each step.

It's a spectrum, not a binary. Fully manual sits at one end (a human decides and acts every step). Fully automated sits at the other (the system runs a predetermined sequence with no human involvement). Most real systems sit in between.

Autonomy is primarily an operational concept. It says: *how much human labor is required to run this system?*

Autonomy alone doesn't tell you how much discretion the system exercises. A nightly `git push` script is fully autonomous and exercises essentially no discretion. A human who makes one daily deploy decision exercises more discretion than the script despite being "less autonomous."

**Key insight:** raising autonomy reduces human labor. It doesn't *by itself* raise risk — unless it raises agency or interacts with low reversibility.

---

### Dimension 2 — Agency: the discretion dimension

**Agency** is the capacity to make decisions that were not explicitly pre-specified — interpreting goals, weighing options, resolving ambiguity, or acting in situations the original instructors didn't fully anticipate.

Agency is about *discretion*. An agent exercising genuine agency is doing something qualitatively different from a deterministic script: it's filling gaps in its instructions with its own judgment (probabilistic reasoning, in the case of language models).

Agency has direction — it operates in service of a goal. To exercise agency is to take actions the agent believes advance the goal, within constraints that were given.

- **Broad agency** — wide latitude to decide *how* to pursue the goal.
- **Narrow agency** — a tightly defined solution space; the agent can act without human intervention but its options are bounded.

**Key insight:** agency determines exposure. The more discretion the system exercises, the more critical it is that the goals, constraints, and escalation paths were specified correctly. Every gap in the spec becomes a decision the agent will fill with probability.

---

### Dimension 3 — Responsibility: the accountability dimension

Responsibility in agent systems is distributed across multiple parties, each carrying a distinct kind of accountability:

| Layer | Who | What they're accountable for |
|-------|-----|------------------------------|
| **Authorial** | The humans who wrote the spec | The adequacy of the intent as expressed. If the spec authorized something harmful, or failed to constrain something that should have been constrained, the authors are accountable. This is the deepest form of responsibility. It cannot be transferred to the agent. |
| **Operational** | The humans who deployed and operate the system | Ensuring it functions within its designed parameters, that monitoring is adequate, that failures are caught and corrected. Ongoing, not once-at-design-time. |
| **Validation** | The humans who reviewed outputs and decided to act | If an agent produced a recommendation and a human implemented it without review, the accountable party for the outcome is the human who chose to act — not the system that generated the recommendation. |
| **Platform** | The builders of the agent infrastructure | The reliability and safety of the platform (model, orchestration, MCP tools) within its stated operating parameters. |

These responsibilities are **concurrent and non-exclusive**. A failed outcome usually involves accountability at multiple layers — a spec that under-constrained, an operator who didn't monitor, a reviewer who didn't catch the failure, a platform that behaved unexpectedly. Identifying which responsibility layer failed is prerequisite to preventing recurrence.

**The danger zone: high agency + low responsibility clarity.** Three common patterns expose this:

- **The "AI decided" deflection.** When something goes wrong, the response is "the AI did it." This is never a meaningful answer. An AI system acts within a spec, authorized by humans, deployed by humans, running on infrastructure operated by humans. "The AI decided" is shorthand for a chain of human decisions that allocated agency.
- **The empty oversight seat.** A system with significant agency but no designated human reviewer. The system acts; nobody checks. When the agent's discretionary judgment is wrong, nobody catches it until consequences have compounded.
- **The responsibility gap.** Authorial, operational, and validation responsibilities belong to different teams who never coordinated on what "accountable" means in practice.

---

### Dimension 4 — Reversibility: the consequence dimension

**Reversibility** is the degree to which an action can be undone, corrected, or rolled back after it has been taken.

It's a spectrum with four practical zones:

| Zone | Description | Examples |
|------|-------------|----------|
| **Fully reversible** | Action can be completely undone with no residual effect | Generating a draft, editing a local file, creating a test record |
| **Largely reversible** | Action can be undone with some effort or partial side effects | Publishing a blog post (can be unpublished), creating a cloud resource (can be deleted but billed) |
| **Partially reversible** | Primary action can be reversed but side effects persist | Sending one email (you can follow up, but the first email was received), pushing code to a branch (can be reverted, but others may have seen it) |
| **Irreversible** | Action cannot be meaningfully undone | Sending mass email, deleting production data without backup, making a financial transaction, revoking credentials |

**Reversibility is contextual, not intrinsic.** The same action type sits at different points on the spectrum depending on infrastructure and operational context. A database write is largely reversible if you have point-in-time backups and a tested rollback procedure; it's effectively irreversible if you don't. A message in an internal Slack channel is partially reversible; the same message sent to an external customer mailing list is irreversible. When assessing reversibility for a spec, evaluate the action *as deployed in your specific environment*, not the action type in the abstract.

---

### The risk matrix

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

- **Low agency + reversible** — default safe zone. Automate freely. Monitoring is sufficient.
- **High agency + reversible** — productive zone. Grant the agent latitude. Review outputs; don't gate each step. Correct errors cheaply.
- **Low agency + irreversible** — approval zone. The action itself carries consequence. Require a human gate, not because the agent's discretion is high, but because the cost of any error is non-trivial.
- **High agency + irreversible** — maximum oversight zone. Both the range of decisions and the consequences are high. Requires explicit constraints in the spec, mandatory human review before any irreversible action, audit logging, clearly assigned responsibility. Never deploy with informal oversight.

---

### Reversibility is a design choice

Reversibility isn't a fixed property of the problem domain. It's often a design choice. Patterns that *expand* reversibility:

- **Soft deletes instead of hard deletes.** Data marked deleted is reversible; data purged is not.
- **Draft queues before delivery.** An email queued for review is reversible; an email sent is not.
- **Dry-run modes.** An agent that simulates its actions before executing converts irreversible operations into reviewable ones.
- **Approval gates.** A system that batches decisions for human review before executing any of them is more reversible than one that executes each decision immediately.

These patterns don't eliminate the need for good intent specification — they buy time for the oversight loop to catch mistakes. They are the engineering equivalent of a circuit breaker.

---

### The calibration framework

Given the four dimensions, the primary design question for any agent delegation is:

> *For this system, at what level of discretion (agency), at what execution speed (autonomy), with what distribution of accountability (responsibility), and over what reversibility profile, are we operating?*

| Configuration | Design Response |
|--------------|-----------------|
| High agency over irreversible actions | Maximum constraint specification + mandatory human review |
| High autonomy over repetitive, reversible tasks | Light oversight; monitoring for drift is sufficient |
| Unclear responsibility distribution | Resolve before any deployment — do not assume it sorts itself out |
| High agency + unclear responsibility | Do not deploy. Design the responsibility structure first. |
| High autonomy + irreversible actions + low review cadence | Either reduce autonomy, expand reversibility (draft queues, soft deletes), or add a human gate |

---

## Resulting Context

After applying this pattern:

- **Four distinct dials, set deliberately.** Autonomy, agency, responsibility, and reversibility become design parameters tuned upfront in the spec rather than emergent properties discovered after deployment.
- **Three accountability layers, distributed explicitly.** Authorial, operational, and validation responsibilities are assigned to specific teams or individuals before deployment.
- **Risk matrix becomes actionable.** Different combinations of agency and reversibility receive different oversight structures. Low-risk combinations are streamlined; high-risk combinations get mandatory controls.
- **Reversibility becomes a designable property.** Soft deletes, draft queues, and approval gates expand the scope of what can be safely automated.

---

## Therefore

> **Every delegation has four dials: autonomy (how independently it runs), agency (how much discretion it exercises), responsibility (who is accountable for outcomes), and reversibility (how easily an action can be undone). Calibrate them deliberately in the spec. Match oversight to the combination of agency and reversibility, not to the probability of error. Resolve responsibility distribution before deployment.**

---

## Connections

**This pattern assumes:**
- [Pick an Archetype](../architecture/02-canonical-intent-archetypes.md)

**This pattern enables:**
- [Four Dimensions of Governance](../architecture/03-archetype-dimensions.md) — formal encoding of these dials in archetypes
- [The Archetype Selection Tree](../architecture/04-decision-tree.md) — choosing an archetype that matches your calibration
- [Proportional Oversight](../agents/06-human-oversight-models.md) — designing oversight to match the agency × reversibility profile
- [The Canonical Spec Template](../sdd/07-canonical-spec-template.md) — where these dials are written down

---
