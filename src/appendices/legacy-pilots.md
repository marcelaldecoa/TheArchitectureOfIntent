# Legacy v1.x Worked Pilots Archive

**Appendix**

---

> *"Old worked examples are not embarrassments. They are the calibration record — the artifact that lets readers see what the framework looked like before, and what changed."*

---

## What this is

Three worked pilots from framework v1.x, kept here as a v1.x → v2.0 comparison artifact. Each pilot is a complete walk through one agent system, structured as: scenario → archetype selection → spec → agent instructions → validation suite → (where applicable) post-mortem.

The v2.0.0 release reorganized the book around the five activities (Frame → Specify → Delegate → Validate → Evolve) and introduced three running scenarios that walk one project through every activity in sequence — the *in practice* chapters at the end of each Part. Those scenarios supersede the v1.x pilots as the primary reading path: they are denser, more concrete, and they thread the same teams and systems through the full lifecycle.

The pilots remain useful for two readers:

1. **Comparing framings.** Two of the v2.0.0 scenarios — [Customer-support agent](../frame/scenarios/customer-support.md) and [Coding-agent pipeline](../frame/scenarios/coding-pipeline.md) — explicitly reference these pilots as their v1.x predecessors. Reading the v1.x pilot and the v2.0.0 scenario side by side shows what the activity-spine reorganization changed.
2. **Reaching for a canonical example of a single artifact.** The pilots' individual chapters (Selecting the Archetypes, Writing the Spec, Validating Outcomes, Post-mortem Through Intent) remain referenced from [the pattern index](pattern-index.md) and [the references appendix](references.md) when those artifacts are useful as standalone reading.

---

## The three pilots

### Designing an AI Customer Support System

A mid-size retailer deploys a four-agent system to automate Tier 1 customer inquiries. Multi-agent Orchestrator + Executor + Guardian + Advisor composition; full SDD spec for the most complex agent; 14-test acceptance suite; post-mortem on a $0.00-refund incident traced to a specific spec gap.

- [Overview](../examples/01-ai-customer-support/README.md)
- [Selecting the Archetypes](../examples/01-ai-customer-support/archetypes.md)
- [Writing the Spec](../examples/01-ai-customer-support/spec.md)
- [Agent Instructions](../examples/01-ai-customer-support/agent-instructions.md)
- [Validating Outcomes](../examples/01-ai-customer-support/validation.md)
- [Post-mortem Through Intent](../examples/01-ai-customer-support/postmortem.md)

Superseded by: [Customer-support agent (running scenario)](../frame/scenarios/customer-support.md) — Frame through Evolve and Operations across 90 days.

### A Code Generation Pipeline

A platform engineering team builds a three-agent pipeline that takes a feature intent document and a data schema and produces a complete service scaffold. Synthesizer-Executor-Guardian composition with no live human in the loop; non-conversational instructions for all three agents; 9-test pipeline acceptance suite.

- [Overview](../examples/02-code-generation-pipeline/README.md)
- [Selecting the Archetypes](../examples/02-code-generation-pipeline/archetypes.md)
- [Writing the Spec](../examples/02-code-generation-pipeline/spec.md)
- [Agent Instructions](../examples/02-code-generation-pipeline/agent-instructions.md)
- [Validating Outcomes](../examples/02-code-generation-pipeline/validation.md)

Superseded by: [Coding-agent pipeline (running scenario)](../frame/scenarios/coding-pipeline.md) — Frame through Evolve and Operations across 90 days.

### Designing an AI Coding Agent

An in-loop coding agent for an internal repository. Executor with Synthesizer composition, with the explicit decision *against* Devin-style autonomy recorded; capability-minimalist tool manifest (no general shell, no web fetch, no merge/close); four-level eval stack instantiated against a 75-issue golden set; post-mortem on a deleted-tests incident producing spec v1.1 → v1.2 with a constraint-library entry.

- [Overview](../examples/03-coding-agent/README.md)
- [Selecting the Archetypes](../examples/03-coding-agent/archetypes.md)
- [Writing the Spec](../examples/03-coding-agent/spec.md)
- [Agent Instructions](../examples/03-coding-agent/agent-instructions.md)
- [Evals and Acceptance](../examples/03-coding-agent/evals.md)
- [Post-mortem Through Intent](../examples/03-coding-agent/postmortem.md)

No direct v2.0.0 successor; the [Coding-agent pipeline scenario](../frame/scenarios/coding-pipeline.md) covers similar territory in the activity-spine form, and [Coding Agents](../delegate/08-coding-agents.md) covers the agent-class concept.

---

## Reading guidance

If you are new to the book, **do not start here.** Start with the [Introduction](../introduction.md), the [Miniature Pilot](../miniature-pilot.md), or one of the v2.0.0 *in practice* scenarios. The legacy pilots are a reference resource, not a learning path.

If you are evaluating how the framework matured between v1.x and v2.0, read one v1.x pilot (recommended: [Designing an AI Coding Agent](../examples/03-coding-agent/README.md)) and the matching v2.0.0 scenario back-to-back. The differences you will notice — the explicit five-activity arc, the running-team continuity across phases, the closed-loop emphasis in the *Evolve in practice* chapters — are what v2.0 added structurally.

---

*The legacy pilots' original front-matter chapter, [How to Use These Examples](../examples/00-how-to-use.md), is preserved for reference.*
