# How to Use These Examples

**Applied Examples**

---

> *"Theory tells you what is possible. Examples tell you what is real. The gap between them is where most practitioners live and where most learning happens."*

---

## What These Examples Are

The previous seven Parts of this book established a vocabulary, a set of patterns, and a collection of practices. This part demonstrates them working together on problems that resemble what practitioners actually encounter.

These are not toy problems. They are not "hello world" agents. They are simplified versions of the real systems that motivated the ideas in this book — simplified enough to explain clearly, realistic enough to surface the tensions that matter.

**Example 1: Designing an AI Customer Support System** — A mid-size retailer deploys a four-agent system to automate Tier 1 customer inquiries. This example shows the full arc: archetype selection across a multi-agent architecture, a complete SDD spec for the most complex agent, the actual agent instructions derived from that spec, an acceptance test suite, and a postmortem from a real failure that the spec's constraints did not prevent.

**Example 2: A Code Generation Pipeline** — A platform engineering team builds a three-agent pipeline that takes a feature intent document and a data schema and produces a complete service scaffold, automatically checked against their code standards. This example shows how agent systems work differently when the consumer is other software rather than a human, and how pipeline dynamics change the archetype and spec choices.

---

## How to Read These Examples

Each example follows the same structure:

1. **The Scenario** (README) — What the system is for, what problem it solves, the organizational context, and the architecture overview. Start here to understand what you're looking at.

2. **Selecting the Archetypes** — The reasoning process: which archetypes were considered, which were selected and why, which were rejected and why, what dimensions drove each decision. This is the most reusable step — the reasoning applies to analogous systems.

3. **Writing the Spec** — A complete SDD spec for the primary or most complex agent in the system. Annotated with commentary explaining why specific sections were written the way they were, and what alternatives were considered.

4. **Agent Instructions** — The actual instructions derived from the spec: system prompts, constraint statements, tool descriptions, escalation protocols. These are written as if you would hand them to an AI system today.

5. **Validating Outcomes** — The acceptance test suite: what inputs were used, what the spec's success criteria predicted, what the actual outputs were, and how validation failures were categorized and resolved.

6. **Post-mortem Through Intent** *(Example 1 only)* — A real incident that occurred during operation: what failed, how it was detected, root cause diagnosis through the SDD lens (was this a spec gap, execution gap, tool gap, or oversight gap?), and what was changed.

---

## How to Use These Examples for Your Own Systems

### Use the Archetype Selection as a Template

The archetype selection chapters work through the same questions you need to work through for any system. Read them as a thinking protocol, not just as a record of a specific decision:

- What is each agent's relationship to the output: does it produce it, review it, route it, or synthesize it?
- What is the reversibility of the actions authorized?
- What risk posture does the domain require?
- What oversight model matches the available human capacity?

The answers in these examples are specific to these scenarios. The questions transfer to every agent system.

### Use the Specs as Structural Templates

The specs in these examples follow the canonical template from Part IV. When you write your first spec, use these as concrete references for what each section looks like when it is well-populated — not as content to copy, but as a calibration for completeness and specificity.

Pay particular attention to the NOT-authorized sections. The customer support example's NOT-authorized list was not written in one pass — it was built up through spec review as reviewers applied the five questions from Chapter 7.4 and found clauses that needed to be made explicit.

### Use the Validation Suites as Acceptance Test Blueprints

The acceptance tests in these examples are not exhaustive. They are designed to be sufficient — covering the happy path, the boundary cases from the constraint list, the escalation triggers, and the scope violation behavior. When you build your own acceptance suite, these dimensions should be your starting checklist.

### Read the Postmortem with the Spec Open

The postmortem in Example 1 only makes sense in relation to the spec. The failure it describes is not obvious without knowing what the spec said — and what it did not say. Read the postmortem with the spec page open and trace each finding back to a specific section. This is how postmortem analysis works in the SDD practice: every finding should trace to a specific location (or absence) in the spec.

---

## What These Examples Do Not Cover

These examples do not attempt to cover every archetype, every technology, or every industry. They were chosen because they represent two common and distinct deployment patterns:

- **Example 1** is a customer-facing system with multiple agents, mixed reversibility, and real safety requirements. It shows the governance and oversight patterns under load.
- **Example 2** is an internal automation pipeline with a synthetic consumer (other software, not humans) where correctness is the primary value and throughput is the secondary one.

There is no example of a Synthesizer-dominant research system, a Guardian-dominant compliance system, or an Advisor-only knowledge interface. These exist — and the patterns from the book apply to them — but the two examples here cover the higher-stakes and higher-complexity territory where most practitioners need the most guidance.

---

## Apply It to Your Own System

If you want to test this framework against your own context, here is a practical exercise:

1. **Pick one agent system** your team is building or operating.
2. **Run the archetype decision tree** ([Pattern 3.4](../architecture/04-decision-trees-for-archetype-selection.md)). Does the result match what you currently have? If not, document why.
3. **Write the spec** for the agent's most consequential action using the [Canonical Spec Template](../sdd/07-canonical-spec-template.md). Focus on Sections 3 (Constraints) and 6 (Success Criteria). The first draft will feel incomplete — that is the point.
4. **Execute against the spec** and categorize the first three failures using the [six failure categories](../agents/07-failure-modes.md). How many are spec gaps versus model-level limitations?
5. **Document what surprised you.** The gap between what you expected and what happened is the most valuable learning signal the framework produces.

The two examples in this part are meant to show the process. Your system is where the framework gets tested.

---

*Continue to [Designing an AI Customer Support System](01-ai-customer-support/README.md)*


