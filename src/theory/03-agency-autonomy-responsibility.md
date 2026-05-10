# Calibrate Agency, Autonomy, Responsibility, Reversibility

**Part 0 — Foundations**

---

> *"Autonomy without authority is a faster way of doing what you were told. Agency without accountability is a faster way of causing harm. Reversibility is what determines whether either of those matters."*

---

## Context

A team is mid-Frame, debating whether their data-export agent should be *"high autonomy"* or *"medium autonomy."* The conversation goes in circles for fifteen minutes — every argument for high autonomy turns up a counter-example where high autonomy would be reckless, and every argument for medium turns up a case where medium would be paralyzing. The tech lead stops them: *"We're conflating four things into one word. The agent's autonomy from us during a single export is one decision. Its agency to choose what to export when our instructions don't cover the case is a different decision. Who's accountable when an export goes wrong is a third. And how easily we can undo an export is a fourth. Let's split them out."* Forty minutes later, the team has four committed dial positions instead of one unresolved argument.

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

### What is novel here, and what is borrowed

Reversibility as a governance dial, the autonomy spectrum, and distributed responsibility are all well-established in adjacent literatures. SAE J3016 (the canonical "levels of driving automation" reference) gives a six-level autonomy taxonomy. The HITL / HOTL / HOOTL (Human-In/On/Out-Of-The-Loop) typology has organized human-oversight design in defense and safety-critical systems for over a decade. Shavit, Agarwal et al. (OpenAI, 2023, *Practices for Governing Agentic AI Systems*) explicitly cover action-space, default behaviors, reversibility, attributability, and interruptibility as governance dimensions. NIST AI RMF and ISO 42001 cover responsibility distribution. None of those are being claimed here as new.

What this chapter contributes — and what the rest of the book is built on — is the **insistence that *autonomy* and *agency* are different dials, calibrated separately, with different oversight implications.** Most practitioner sources blur the two; this conflation is the single most common source of mis-calibrated agent oversight.

A nightly `git push` script is highly autonomous and exercises essentially no agency: it follows a predetermined sequence with no discretion. A research agent that runs once a week but plans its own multi-step investigation is much *less* autonomous (one invocation per week, often with checkpoints) but exercises much *more* agency (it interprets goals and fills gaps in instructions). These two systems require qualitatively different oversight even though "how often does a human have to click?" suggests the opposite.

Hold those two dials separately. The rest of the framework — archetype dimensions, oversight models, the spec template — depends on it.

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

Agency has direction — it operates in service of a goal. The system's outputs reflect probabilistic selections among action sequences that, conditioned on the spec and context, the model has been trained to associate with goal advancement. Calling this "the agent's belief" is convenient shorthand; what is actually happening is a constrained search through token sequences that satisfy the prompt.

- **Broad agency** — wide latitude to decide *how* to pursue the goal.
- **Narrow agency** — a tightly defined solution space; the agent can act without human intervention but its options are bounded.

**Key insight:** agency determines exposure. The more latitude the system has, the more critical it is that the goals, constraints, and escalation paths were specified correctly. Every gap in the spec becomes an output the model will produce probabilistically — not a "decision" in the human sense, but a token sequence selected from the constrained space the spec defines. When the spec is loose, that space is wide and unpredictable; when the spec is tight, the space is narrow and the model's probabilistic behavior is bounded into something a human can review.

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
- **The empty oversight seat.** A system with significant agency but no designated human reviewer. The system acts; nobody checks. When the system's outputs go wrong in the discretionary regions the spec didn't constrain, nobody catches it until consequences have compounded.
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

### Cost is not a fifth dimension

Practitioners often ask: *if cost is independently calibratable and shapes every spec choice, why isn't it a fifth dimension alongside agency, autonomy, responsibility, and reversibility?*

The framework's working position is that cost is **not** a fifth calibration dimension. It is a structurally distinct kind of commitment that lives in its own §4 sub-block in the [canonical spec template](../sdd/07-canonical-spec-template.md), alongside (and parallel to) the Composition Declaration. Three reasons.

**Cost is partially derived, not fully independent.** A system's cost is partly a consequence of the four dimensions: high agency, wide autonomy, and engineered reversibility together push cost up. The four behavioral dimensions are *causes*; cost is partly an *effect* of how they're set. Promoting cost to a dimension would conflate dial with derived quantity, which is exactly the conflation the orthogonality argument above tries to *avoid* for agency and autonomy.

**Cost is a different category of commitment.** The four dimensions are *behavioral* commitments about what the system **does** — what decisions it makes, what gates apply, who is accountable, what state it can recover. Cost is a *resource* commitment about what the system **consumes** — model tier, latency budget, cache strategy, per-call ceiling. Behavioral and resource commitments compose, but the framework's argument that the four behavioral dimensions are orthogonal does not extend cleanly to a behavioral-plus-resource fifth.

**The lineage is thin.** The framework's honest accounting (paper §1.3) cites SAE J3016 [@saeJ30162021] and Shavit & Agarwal [@shavitAgarwal2023] as the sources for the four dimensions individually. Neither has cost-as-a-dimension; SAE J3016 treats cost as derived from the automation level, and Shavit & Agarwal's seven operational variables (ability, agency, agency type, autonomy, alignment, accountability, authority) do not include cost. Adding a fifth dimension here would either require a novelty claim (weak — practitioners have been calibrating cost as a resource concern for decades) or a manufactured lineage citation. The framework declines both.

**What we do instead.** Cost gets a structural seat in the spec, but as a §4 *sub-block* rather than a calibration dimension. The Cost Posture sub-block declares: model-tier commitment per step; latency budget; prompt-stability invariant; per-call cost ceiling; cost-incident escalation. The Composition Declaration was the precedent — §4 can absorb structural commitments that aren't dimensions. Cost Posture follows the same shape.

**What the four dimensions still do.** The four-dimension calibration determines the *envelope* within which cost is calibrated. A Reasoning-tier model on every step is cheap if Agency is narrow and Autonomy is bounded (few calls, simple prompts); the same Reasoning-tier commitment is ruinous if Agency is wide and Autonomy is high (many calls, expanding context). The Cost Posture sub-block makes the cost commitment *visible upstream*, where the four-dimension calibration has already constrained what is possible. Operators reading the spec can then see how the behavioral and resource commitments interact, instead of discovering the interaction in the production cost graph.

If a future class of system makes cost behave like a dimension — independently calibratable, orthogonal to A/A/R/R, with a clear governance profile no §4 sub-block provides — the framework can revisit. As of v1.x, no such class has surfaced. The §4 sub-block does the work cleanly, and the orthogonality argument the four behavioral dimensions rest on stays uncluttered.

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

## References

- SAE International. (2021). *J3016 — Taxonomy and Definitions for Terms Related to Driving Automation Systems for On-Road Motor Vehicles.* — The canonical six-level autonomy taxonomy this chapter draws from for the autonomy dimension.
- Shavit, Y., Agarwal, S., et al. (Anthropic, OpenAI). (2023). *Practices for Governing Agentic AI Systems.* OpenAI. — Formalizes action-space, default behaviors, reversibility, attributability, interruptibility as governance dimensions; the closest prior art to this chapter's four dimensions.
- NIST. (2023). *AI Risk Management Framework (AI RMF 1.0).* — Responsibility distribution across "govern, map, measure, manage" functions.
- ISO/IEC 42001:2023. *Information technology — Artificial intelligence — Management system.* — Organizational accountability framework for AI systems.
- *Human-in-the-loop / Human-on-the-loop / Human-out-of-the-loop.* — Standard typology for oversight cadence in safety-critical systems; predates AI agent literature.

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
