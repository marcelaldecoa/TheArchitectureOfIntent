# Proportional Oversight

**Agents**

---

> *"The question is not whether to watch — it is where to place your eyes. At the intention or at the action? At the design or at the output? The answer determines whether oversight is a control or a recovery mechanism."*

---

## Context

We have agents that can execute complex tasks with operational autonomy, using tools within defined capability boundaries, guided by skills that encode organizational knowledge. The final design question before examining failure is: where does human attention go, and when?

Human oversight is not a single mechanism. It is a family of patterns, each appropriate to a different point in the execution lifecycle, a different risk posture, and a different relationship between the human and the work. Treating oversight as binary — either the human approves everything, or the human is not involved — is the failure mode this chapter prevents.

This pattern assumes familiarity with the archetype framework from Part III, particularly the four oversight dimensions: Agency Level, Risk Posture, Oversight Model, and Reversibility.

---

## The Problem

Organizations newly deploying agents typically oscillate between two extremes:

**Over-supervision**: The human approves every action. Every tool call gets a confirm dialog. Every output is reviewed before use. The agent generates no output without a sign-off. This is called "human in the loop" and it is sometimes appropriate — but when applied universally, it eliminates the productivity benefit of the agent entirely. The human is now doing the same amount of work, just differently.

**Under-supervision**: The agent runs. The human sees the output. If the output causes a problem, the human finds out later. This is called "autonomous operation" but is more precisely described as "unsupervised delegation." It works until it doesn't, and when it doesn't, the damage is already done.

Between these extremes is a spectrum of oversight designs, each with a different cost-benefit profile. The engineering discipline is choosing the right model for each deployment context — not defaulting to either extreme.

The second problem is that "human oversight" is often understood as output review: a human sees what the agent produced and judges whether it's acceptable. This is the lowest-quality form of oversight because it occurs after execution, meaning any irreversible effects have already been produced.

---

## Forces

- **Oversight completeness vs. operational throughput.** Reviewing every output guarantees nothing is missed but eliminates the productivity advantage of agents. Reviewing nothing risks undetected harm.
- **Pre-execution review vs. post-execution review.** Pre-execution oversight (spec review) is highest leverage but requires investment before seeing results. Post-execution oversight is reactive but catches implementation failures.
- **Spec maturity vs. oversight intensity.** New specs need intensive oversight. Mature specs with established track records can operate under lighter oversight. The transition requires explicit criteria.
- **Cost of watching vs. cost of not watching.** Oversight has a real human time cost. Not-watching has a probabilistic harm cost. The optimal level is where these costs cross.

---

## The Solution

### The Four Oversight Models

Building on the archetype framework's Oversight Model dimension, four patterns apply across agent deployments. These use the same labels (A–D) defined in [Four Dimensions of Governance](../architecture/03-archetype-dimensions.md):

**Model A — Monitoring**

Human attention is triggered by anomalies or metrics, not by every output. The system runs continuously; humans review exceptions. During normal operation, no per-output human review occurs.

This model is appropriate when:
- The task is well-understood and has been executed successfully before
- All actions taken are reversible or low-consequence
- Anomaly detection tooling is available to flag deviations in log patterns

Typical archetypes: Advisor, Guardian.

**Model B — Periodic Review**

Human reviews a sample of outputs on a scheduled cadence. The agent executes continuously; at defined intervals or milestones, the human reviews a representative set of outputs and can adjust course. Not real-time approval, but regular human checkpoints.

This model is appropriate when:
- The task spans multiple phases with qualitatively different outputs
- Some phases produce artifacts that are expensive to redo if the direction is wrong
- The total task is long enough that a final-output review would be expensive to fail

Typical archetypes: Synthesizer, Executor in established workflows.

**Model B** also applies as a *risk-triggered* checkpoint: the agent pauses not on a schedule, but when it detects it is about to take an action with above-threshold consequence or irreversibility. The spec should declare what the threshold is and what "pause" means in context.

**Model C — Output Gate**

Human reviews and approves (or rejects) before any output is released or acted upon. Real-time review. The agent generates output; the human decides whether it proceeds.

This model is appropriate when:
- The task involves irreversible or high-consequence actions
- The system is newly deployed and trust has not been established
- Regulatory or policy requirements mandate pre-action approval

Typical archetypes: Orchestrator, high-risk Executor deployments.

**Model D — Pre-authorized Scope + Exception Gate**

Human defines the authorized scope in advance (the spec's constraint section). The system acts within scope without per-output review. Any action outside the pre-authorized scope must surface for human decision before executing. This is the most powerful production model — it enables high-velocity autonomous execution while preserving human authority at the boundaries.

This model is appropriate when:
- The agent has an extensive track record of reliable operation in this domain
- The task domain is well-bounded and fully covered by the spec
- A robust exception-handling path exists and is tested
- The consequence of undetected errors within scope is manageable

Typical archetypes: Mature Executor deployments, bounded Orchestrators.

### Matching Oversight Model to Deployment Context

The selection framework depends on four variables:

| Variable | Model A (Monitoring) | Model B (Periodic Review) | Model C (Output Gate) | Model D (Pre-auth Scope) |
|---|---|---|---|---|
| Reversibility of actions | Fully reversible | Mixed | Low reversibility | Fully or mostly reversible |
| Consequence of error | Low | Medium | Medium-high | Low-medium |
| Task novelty | Familiar | Mixed | Novel or high-risk | Well-established |
| Spec maturity | High | Medium | Medium | Very high |

This is not a strict lookup — it is a set of considerations. When multiple variables point in different directions (high reversibility but high consequence), resolve conservatively: use the model that matches the most constraining variable.

### The Spec-Based Oversight Shift

The most valuable insight from SDD about oversight is this: **when you have a good spec, the primary oversight moment is spec review, not output review**.

A human who approves a well-written spec has already made every consequential decision:
- What the agent will do and won't do
- What tools it may use and under what constraints
- What success looks like and how it will be validated
- What to do if unexpected situations arise

Output review still happens — but it answers the question "did the agent follow the spec?" rather than "do I agree with this output?" These are very different questions. The first has an objective answer. The second requires re-doing the judgment work that should have happened at spec time.

This shift has real consequences for how oversight is designed into an organization's workflows:
- Spec review should be a formal step, with a reviewer identity and a sign-off requirement
- Output review should validate against the spec, not against reviewer preference
- Deviations between output and spec are unambiguous failures; deviations between output and unstated preference are spec gaps to address

### Escalation Triggers

Every agent deployment should have a set of defined escalation conditions — circumstances under which the agent should pause execution and request human input rather than proceeding. These should be written in the spec (Section 8: Oversight and Escalation). Common categories:

**Scope uncertainty.** The agent is about to take an action that might be within its authorization but is ambiguous. Better to pause than to proceed on an uncertain interpretation of an irreversible action.

**Resource unavailability.** A tool the agent needs is unavailable. The agent cannot complete the task as specified. Attempting to route around the unavailability is outside scope; escalating is correct.

**Unexpected data.** The agent encounters data that significantly changes the nature of the task — far more records than expected, data in an unexpected format, evidence that the task preconditions were not true.

**Conflict between spec sections.** The agent identifies an apparent contradiction between constraints in the spec. Silently resolving it is a scope expansion. Escalating is correct.

**Confidence below threshold.** For agents in domains where confidence can be estimated (classification, extraction, prediction), operating below a declared confidence threshold should trigger escalation rather than low-confidence execution.

Escalation should be designed to be low-friction for the agent. If escalating is onerous, the agent will avoid it. A well-designed escalation path: the agent surfaces a structured summary of what it found and what decision it needs, with the available options. The human makes the call in under a minute. The agent continues.

### The Oversight Cost Function

Oversight is not free. Every checkpoint, confirmation request, and log review consumes human attention. The design discipline is deploying oversight where the cost of not having it exceeds the cost of having it.

```
Oversight cost = (human time per review) × (frequency of review)
Non-oversight cost = (probability of undetected error) × (cost of that error)

Correct oversight level: the point where reducing oversight
increases expected total cost rather than decreasing it.
```

This is not an argument for eliminating oversight — it is a framework for deploying it efficiently. Organizations that apply maximum oversight to every agent action are not running a governance program; they are eliminating the productivity advantage of agents while creating the overhead of governance. The discipline is proportionality.

### Oversight at High Velocity

The oversight models described above assume human-scalable volume. When agent systems produce thousands or hundreds of thousands of outputs per hour, direct human review of every output is no longer feasible — even under the lightest oversight model.

At high velocity, oversight shifts from individual output review to statistical and structural mechanisms:

- **Sampling-based review.** A random or stratified sample of outputs is reviewed at a cadence that maintains statistical confidence. The sample rate is proportional to risk: higher for irreversible or high-consequence outputs, lower for fully reversible outputs with established track records.
- **Automated invariant checking.** Constraints from the spec are encoded as automated validators that run against every output. These are not oversight — they are enforcement. But they reduce the surface area that human oversight must cover.
- **Anomaly detection.** Statistical monitoring of output distributions detects drift from established baselines. Anomalies trigger human review of the anomalous outputs and potentially a broader audit.
- **Escalation-only human involvement.** At the highest velocity and maturity levels, human oversight is exercised only when the agent escalates, when automated checks fail, or when anomaly detection triggers. The governance model shifts from "review outputs" to "review the system that produces outputs" — which is spec review, constraint auditing, and periodic behavior audits.

The key principle: high-velocity systems require that governance be encoded in the spec and the constraints, not in per-output human review. The spec becomes the primary oversight artifact, and spec quality becomes the binding constraint on safe scaling.

---

## Resulting Context

After applying this pattern:

- **Spec approval becomes the primary oversight moment.** When specs are well-written, the consequential decisions have already been made at spec time. Output review validates execution, not intent.
- **Four oversight models provide a vocabulary for deployment decisions.** Teams can select and justify their oversight level against explicit criteria rather than defaulting to maximum or minimum.
- **High-velocity systems remain governable.** Sampling, automated invariant checking, and anomaly detection extend oversight to scales where per-output review is infeasible.
- **Oversight proportionality becomes a design discipline.** Organizations deploy oversight where the cost of not watching exceeds the cost of watching.

---

## Therefore

> **Human oversight is a family of four models — monitoring, periodic review, output gate, and pre-authorized scope with exception gate — each appropriate to different combinations of reversibility, consequence, task novelty, and spec maturity. These correspond to Models A–D as defined in the archetype dimension framework. The most consequential oversight moment in a spec-driven system is spec approval, not output review; approval at spec time makes every downstream oversight decision less expensive. Design oversight proportionally: where the cost of not watching exceeds the cost of watching.**

---

## Connections

**This pattern assumes:**
- [Autonomy Without Agency](02-autonomy-vs-agency.md)
- [The Executor Model](03-agents-as-executors.md)
- [The Five Archetypes](../architecture/02-canonical-intent-archetypes.md)
- [The Canonical Spec Template — Section 8](../sdd/07-canonical-spec-template.md)

**This pattern enables:**
- [Six Failure Categories](07-failure-modes.md)
- Governance, Escalation Design *(Part VII)*

---
