# The Moral Weight of Specification

**Foundations**

---

> *"A specification is not a technical document. It is a statement of what you are willing to do to the people who use your system — and what you are not. It is a promise, made in advance, on their behalf."*

---

## Context

Part II has built its vocabulary systematically: intent engineering as a discipline, the distinction between intent and implementation, the three dimensions of agency/autonomy/responsibility, reversibility as calibration, and failure as diagnostic signal. This final pattern in Part II completes the theoretical foundation by asking the deepest question:

**Why does any of this matter morally?**

The answer is not complicated, but it is important — and it is the one that distinguishes serious practitioners from technical optimizers. Every specification is an ethical act. Not because the author is philosophizing, but because of the mechanics of what a spec does when agents execute on it at scale.

This pattern assumes the full preceding arc of Part II. It opens Part III by providing the motivation for why archetypes must be treated as constitutional decisions rather than advisory templates.

---

## The Problem

Most discussions of ethics in AI systems focus on the model: on training data, on bias, on the behavior of the underlying system. This is important work. But it misses the most proximate moral actor in the systems we are building: **the person who wrote the spec**.

When an agent acts on a specification and causes harm — exposes user data, produces discriminatory outputs, takes irreversible actions without oversight, scales a bad decision to millions of people — the conversation about responsibility often defaults to vague discussions of "AI accountability." But there is always a chain of human decisions that produced the outcome, and at the head of that chain is the specification.

The question "is this specification ethically responsible?" is almost never asked in design reviews. It is treated as out of scope — a concern for policy teams, legal counsel, ethics boards. Not for the engineer writing the spec.

This is the mistake this pattern addresses.

---

## Forces

- **Technical authority vs. ethical responsibility gap.** Engineers are empowered to write specs but may lack domain knowledge in law, ethics, and policy; yet agent execution at scale means spec authors' decisions propagate consequences that were previously buffered by human judgment.
- **Specification underspecification vs. agent fidelity.** Implicit constraints that seem "obvious" to the author are not obvious to agents; the gap between what was assumed and what was specified gets filled with probability across millions of executions.
- **Scale invisibility vs. moral consequence multiplication.** A problem a human developer might have noticed in 10 cases gets executed — correctly but wrongly — 10 million times before discovery; the agent's fidelity and scale make moral gaps in specifications catastrophic.

---

## The Solution

### What Makes a Spec Moral (or Amoral)

A specification is a moral artifact in the following specific sense: it encodes, explicitly or by omission, a set of **commitments about how the people affected by this system will be treated**.

These commitments include:

**Commitments encoded by constraints** — When a spec says "this system must never expose personal health data to unauthenticated callers," it is making a commitment to the privacy of the users whose health data the system processes. That commitment is a moral claim: *we will protect this about you*.

**Commitments encoded by scope** — When a spec defines what is out of scope, it makes commitments about what the system will *not* do. Omitting something from scope that the agent could plausibly do — and that would harm users if done — is a moral failure of omission. The scope boundary is a promise about restraint.

**Commitments encoded by success criteria** — The success criteria define what "working correctly" means. If success is defined only in terms of technical performance (latency, throughput, test pass rate) and says nothing about outcomes for the humans using the system, the spec has encoded a moral blindspot: that users' experiences are not part of what "correct" means.

**Commitments encoded by omission** — The most dangerous moral dimension of specifications is what they fail to say. An agent operating in the gap created by an underspecified constraint does not have a moral compass it consults. It fills the gap with probability. Every unstated constraint is a decision left to chance.

---

### The Inverse Relationship Between Scale and Moral Distance

Here is the mechanism that makes this urgent rather than abstract:

In a pre-agent world, a specification was executed by a human developer. If the spec was ethically insufficient — if it, for instance, failed to specify that user data should be anonymized before logging — the developer might catch this through their own judgment. They might ask. They might notice the problem and raise it. Human judgment in the execution layer provided a moral buffer between the spec and the harm.

In an agent-mediated world, that buffer is gone. The agent executes the spec with fidelity. If the spec does not specify anonymization, the agent does not anonymize. If the spec does not prohibit discriminatory logic, the agent does not refuse to implement it.

And the agent executes at scale. A problem that a human developer might have caught in ten cases gets executed correctly — wrong — ten million times before anyone notices.

**The moral responsibility of the spec author scales with the capability of the system.** The more powerful the agent, the more consequential the specification, the more seriously the author must treat the ethical dimensions of what they are writing.

This is not an argument against powerful agents. It is an argument for serious specifications.

---

### The Three Moral Dimensions Every Spec Should Address

**1. Non-harm constraints**

Every specification should explicitly address the ways the system could harm the people it touches. Not as a risk register (though that has value) — as a set of named, non-negotiable constraints. "This system must never..." is the opening of a moral commitment.

Common non-harm dimensions:
- Privacy (what data may and may not be used, retained, shared)
- Discrimination (what attributes must not influence outcomes)
- Consent (what actions require explicit user authorization)
- Transparency (what the system must disclose about its operation)
- Autonomy (what decisions must remain with the user, not the system)

**2. Scope of authority**

Every specification should define the scope of what the system is authorized to do — not just what it is capable of doing. Capability and authority are different. A system with access to a database is capable of reading all records. Authority means only reading the records relevant to the task.

The space between capability and authority is the space where unintended harm most commonly originates. Closing this gap is a moral act: it is the decision to not use power that is available.

**3. Oversight adequacy**

If a system can cause harm, the specification should describe how that harm will be detected and by whom. Oversight is not just a governance mechanism — it is a moral commitment that the authors of the system are willing to be accountable for what it does.

A system with no oversight structure is one where the authors have said, implicitly: *we are not responsible for what this does*. That is not a technical claim. It is a moral one.

---

### Specs as Institutional Memory

There is a second moral dimension of specifications that is less obvious but equally important: their role as institutional memory.

When a spec is abandoned — when it is written once, executed, and never updated — it becomes a historical document that no longer reflects the intent of the authors. But the system continues to run. The commitments made in that spec continue to be enacted. Users continue to be affected by decisions that may no longer represent anyone's current understanding of what is right.

The commitment to maintain a living spec — to update it when the problem changes, to revisit it when failures indicate gaps, to sunset it when the system is decommissioned — is a moral commitment to continued accountability.

This is why [The Living Spec](../sdd/06-living-specs.md) is not just a methodology chapter. It is the operational expression of the moral claim in this pattern: the author remains responsible for the system as long as it runs.

---

### The Organizational Corollary

This pattern has an organizational implication that runs through [Delegated Definition Authority](../operating/03-who-defines-archetypes.md) and [Proportional Governance](../operating/04-governance.md):

Not everyone should be empowered to write specifications for all classes of system unilaterally.

This is not because some engineers are less skilled. It is because some specifications encode commitments that require domain knowledge — legal, ethical, business — that a technical practitioner may not possess. Responsibility requires context. Authority should follow responsibility.

The [Archetype system](../architecture/01-archetypes-as-constitutional-law.md) addresses this by pre-committing, at the level of archetype definition (controlled by principals), the most consequential decisions about how a class of system will treat the people it affects. Individual spec authors then operate within that pre-committed frame — with latitude for implementation, but within ethical boundaries already established.

---

## Resulting Context

After applying this pattern:

- **Specifications become explicit moral commitments.** Every spec now encodes, through constraints, scope, success criteria, and omissions, a set of commitments about how people affected by the system will be treated — making ethical accountability design-reviewable.
- **Moral responsibility scales with system power.** As agent capability increases, the responsibility of the spec author for the ethical dimensions of their specification increases proportionally.
- **Archetype pre-commitment distributes moral authority appropriately.** Principals with domain authority pre-commit the most consequential ethical boundaries at the archetype level; individual spec authors then operate with appropriate latitude within those guardrails.

---

## Therefore

> **A specification is a moral artifact: it encodes, through its constraints, scope, success criteria, and omissions, a set of commitments about how the people affected by the system will be treated. The moral responsibility of the spec author scales with the power of the system. Every unstated constraint is a decision delegated to probability. Writing specifications carefully is not just good engineering — it is the primary act of ethical accountability in an age of agent-mediated software.**

---

## A Final Note on Part II

The six patterns of Part II have built a precise vocabulary:

- Intent engineering is the **discipline**
- Intent and implementation are the **two artifacts** it operates across
- Agency, autonomy, and responsibility are the **three governance dimensions**
- Reversibility calibrates the **consequence of delegation**
- Failure is the **feedback signal** that makes specs living
- Moral responsibility is the **weight** that makes this work serious

With this vocabulary, we are ready to move from theory into constitutional design.

Part III introduces the Archetypes — the patterns that encode this vocabulary into reusable, pre-authorized structures for the most common classes of delegated system.

---

## Connections

**This pattern assumes:**
- [Failure as Diagnostic Signal](05-failure-as-design-signal.md)
- [Authorship in Software](../foundations/03-authorship-in-software.md)
- [Three Dimensions of Delegation](03-agency-autonomy-responsibility.md)

**This pattern enables:**
- [Constitutional Archetypes](../architecture/01-archetypes-as-constitutional-law.md) — moral pre-commitment at scale
- [Delegated Definition Authority](../operating/03-who-defines-archetypes.md) — governance as ethical structure
- [Writing for Machine Execution](../sdd/05-writing-specs-for-agents.md) — the practice of morally serious specification

---

*End of Part II. Continue to [Part III: Intent Architecture](../architecture/01-archetypes-as-constitutional-law.md)*

