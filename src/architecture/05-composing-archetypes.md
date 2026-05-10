# Archetype Composition

**Governance & Architecture**

---

> *"A city is not a simple object but a complex of objects that arise together in a particular way. The parts are not less important than the whole — they are the whole."*  
> — Christopher Alexander, *The Timeless Way of Building*

---

## Context

You have assigned an archetype to a system. You know it is, say, an Executor — it takes bounded, pre-authorized action. But the system also has a component that checks its own outputs before applying them, another that reports results to a dashboard, and a third that refuses to act if a given condition is violated.

Real systems are not atomic. They are compositions. The question is how to manage that composition without losing the clarity the archetype gave you.

This pattern assumes [The Five Archetypes](02-canonical-intent-archetypes.md), [Four Dimensions of Governance](03-archetype-dimensions.md), and [The Archetype Selection Tree](04-decision-tree.md).

---

## The Problem

Two failure modes emerge when multiple functional concerns are present in one system:

**Failure Mode 1: Archetype blending.** The system is classified as "mostly an Executor with some Advisor-like features," and a single governance model is applied to the whole. The embedded advisory component gets Executor-level constraints (too strict for its risk) or the Executor component gets Advisor-level oversight (too loose for its risk). Neither is correct.

**Failure Mode 2: Archetype fragmentation.** Every sub-function is classified separately, producing a sprawling multi-archetype design document that no one reads, with overlapping and sometimes contradictory governance requirements. The boundaries between sub-components are not enforced.

The first failure produces incorrect governance. The second produces unreadable governance. Both eventually produce the same outcome: a system that is harder to reason about than if no archetype framework had been used at all.

There is a structural solution — and it requires treating composition as a first-class design operation.

---

## Forces

- **Atomicity vs. reality.** The five archetypes describe atomic types, but real systems combine multiple functions. Forcing one archetype onto a multi-archetype system either miscategorizes it or fragments the spec.
- **Clarity vs. expressiveness.** Allowing composition means accepting systems that resist a single label. Yet disallowing composition creates pressure to misclassify or physically decompose architecturally coherent systems.
- **Simple governance vs. complex reality.** A pure archetype inherits a clear governance profile. A composed system requires per-component governance that must integrate coherently.
- **Reusability vs. specificity.** If composition is ad-hoc, every composed system requires custom governance reasoning. Named composition patterns allow pre-thought-through governance.

---

## The Solution

### The Composition Principle

> A system has *one governing archetype* and *zero or more embedded components* that serve different archetype roles. The governing archetype is determined by the highest-risk autonomous action in the system. Embedded components are declared explicitly and governed by their own constraints within the parent system.

The governing archetype determines:
- The default oversight model for the system as a whole
- The risk posture label in the spec
- The invariants that cannot be overridden

Embedded components determine:
- Which behaviors inside the system require additional, locally-specific constraints
- Which outputs of embedded components are visible vs. internal
- Whether the embedded component needs its own spec section or is sufficiently covered by the governing spec

The key move: you do not blend. You layer.

---

### Common Composition Patterns

**Pattern A: Advisor → Executor (Confirm-then-Act)**

The system shows the user what it intends to do before acting. The advisory phase is Advisor-class; the execution phase is Executor-class.

```
┌─────────────────────────────────────────────────────────────┐
│  GOVERNING ARCHETYPE: Executor                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Embedded advisory layer: Advisor                     │  │
│  │  • Generates proposed action with rationale           │  │
│  │  • Outputs to human confirmation step                 │  │
│  │  • Human confirmation IS the oversight gate           │  │
│  └───────────────────────────────────────────────────────┘  │
│                         ↓ (confirmed)                        │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Executor core: acts within pre-authorized scope      │  │
│  │  • Governed by Oversight Model C (output gate)        │  │
│  │  • The advisory phase IS the output gate              │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

Governing archetype: **Executor**. The advisory phase is explicitly how this Executor implements Oversight Model C — the human confirmation serves as the output gate. The architectural insight is that a confirm-then-act pattern is not two archetypes; it is an Executor implementing its required oversight model via an embedded advisory step.

---

**Pattern B: Executor + Guardian (Act-within-enforced-limits)**

The system takes action but has a Guardian component that enforces a non-negotiable constraint. The Guardian is not optional or configurable — it is always in the path.

```
┌─────────────────────────────────────────────────────────────┐
│  GOVERNING ARCHETYPE: Executor                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Guardian layer: invariant enforcement                │  │
│  │  • Cannot be disabled or bypassed                     │  │
│  │  • Evaluated before every consequential action        │  │
│  │  • Violation → halt + surface, never silent skip      │  │
│  └───────────────────────────────────────────────────────┘  │
│                         ↓ (passes)                           │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Executor core                                        │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

The Guardian layer is specified with Guardian-class constraints: what exactly it enforces, what constitutes a violation, and what happens when a violation is detected. The Executor core is specified with Executor-class constraints. These are separate sections in the spec, with the Guardian layer having its own invariants that cannot be overridden by the Executor section.

---

**Pattern C: Orchestrator with typed sub-agents**

An Orchestrator coordinates several distinct agents, each of which is a different archetype.

```
┌─────────────────────────────────────────────────────────────┐
│  GOVERNING ARCHETYPE: Orchestrator                           │
│                                                              │
│  Coordinates:                                                │
│  ┌────────────────┐  ┌───────────────┐  ┌──────────────┐   │
│  │ Agent A        │  │ Agent B       │  │ Agent C      │   │
│  │ (Advisor)      │  │ (Executor)    │  │ (Guardian)   │   │
│  │ • Summarizes   │  │ • Takes       │  │ • Validates  │   │
│  │   retrieved    │  │   remediation │  │   all outputs│   │
│  │   context      │  │   actions     │  │   pre-post   │   │
│  └────────────────┘  └───────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

Each sub-agent in an Orchestrator composition should be specced with its own archetype. The Orchestrator's spec defines: what it coordinates, how it routes, what it does with results, and what it is not permitted to do itself. The Orchestrator should not be acting as an Executor, Advisor, Guardian, or Synthesizer simultaneously — if it is, it has a sub-agent that should be made explicit.

This pattern is particularly common in complex support systems: an Advisor agent surfaces options, an Executor agent applies a selected resolution, a Guardian agent validates that the resolution doesn't violate support policy.

---

**Pattern D: Synthesizer + Executor (Compose-then-Publish)**

The system produces a composed artifact and then publishes or deploys it. The composition is Synthesizer-class; the publication is Executor-class.

The governing archetype is **Executor** — the final action is what determines the risk profile. The synthesis phase is how the Executor prepares its output. The spec should describe both the synthesis behavior and the execution behavior, with particular attention to the approval gate between them: who reviews the synthesized artifact before it is executed?

If there is no review gate — synthesis automatically triggers publish — this system is a pure Executor with a complex preparation step. Document it that way. Do not refer to it as a "Synthesizer with an execution capability" because that construction hides the autonomous action.

---

**Pattern E: Mode-switching compositions (the 2026 pressure-point classes)**

The four patterns above are *layered* compositions — every archetype is active simultaneously. Pattern E names a different shape: at any given moment the system is in *one* archetype's mode, and it transitions between modes within a single session. The transitions are first-class events with their own invariants. This is the structural answer to the three pressure-point classes named in [Pick an Archetype — A working taxonomy, not a settled one](02-canonical-intent-archetypes.md#a-working-taxonomy-not-a-settled-one).

**Coding agents.** A Cursor / Claude Code / Cline / Devin session moves between Synthesizer mode (planning, summarizing changes, explaining intent) and Executor mode (writing files, running tests, opening PRs). On harder tasks the same session may also enter Orchestrator-over-self mode (delegating sub-tasks to itself or to subordinate agents). The governing archetype is **Executor** — it is the highest-risk action mode the system reaches — and the embedded modes are Synthesizer and (sometimes) Orchestrator.

```
GOVERNING ARCHETYPE: Executor
  Mode 1: Synthesizer (plan, explain, summarize)
  Mode 2: Executor (write files, run tests, open PR)  ← governing
  Mode 3: Orchestrator-over-self (delegate sub-task)

Cross-mode invariants (cannot break, regardless of active mode):
  • File-system scope: identical in every mode
  • Test-deletion: forbidden in every mode
  • Authorized-domain list for outbound traffic: same in every mode
```

The structural insight: invariants that hold in *every* mode go in the spec at the system level (a sub-section of §6 Invariants in the canonical spec template, declared in §4's Composition Declaration). Invariants that hold only within a mode go in that mode's component spec. This is the failure-prevention discipline — every documented coding-agent failure (deleted tests, unauthorized refactors, scope-creep PRs) has been a cross-mode invariant that was not declared as cross-mode.

**Deep-research agents.** A long-horizon research agent moves between Synthesizer mode (composing the final report from gathered sources) and Orchestrator-over-self mode (planning what to search next, dispatching parallel sub-research). The governing archetype is **Synthesizer** — its deliverable is a composed artifact and it does not act on the world during research. Embedded: Orchestrator-over-self for planning.

```
GOVERNING ARCHETYPE: Synthesizer
  Mode 1: Synthesizer (compose report)              ← governing
  Mode 2: Orchestrator-over-self (plan further searches)

Cross-mode invariants:
  • Do not act on the world: never make API calls outside the
    read-only research tool manifest
  • Every claim in the synthesized report cites a source URL
    (see Grounding with Verified Sources)
  • The agent does not recurse beyond depth N (cost cap)
```

**Self-improving / training agents.** A system whose primary act is to evaluate or fine-tune *another* agent's behavior. The honest reading is that this is **two systems with a clean handoff**, not one mode-switching system: the meta-system is a Synthesizer (it produces a training signal or fine-tune dataset); the inner agent is an Executor or whichever archetype its deployment shape calls for. Document them with two specs and an explicitly-defined handoff. The handoff itself is the design surface — what data crosses, who validates it, what audit trail the meta-system leaves on the inner agent's training history.

```
META-SYSTEM (Synthesizer)         INNER AGENT (Executor, separate spec)
  Reads inner agent's outputs       Operates on its own deployment
  Composes a training signal        ↑ Handoff (validated, audited)
  Outputs to fine-tune queue  ─────→ Loaded as new model weights
```

**The contrast with the layered patterns.** In Patterns A through D, all archetypes are active simultaneously and the layering is structural. In Pattern E, the system is in *one* mode at a time and the transitions are temporal. This places extra weight on the spec's transition logic — what triggers a mode change, what state the agent carries across the change, and what invariants from the previous mode persist. A spec that documents the modes but not the transitions is missing the load-bearing surface.

---

### The Composition Declaration in the spec

For systems with embedded components (Patterns A–D) or mode-switching (Pattern E), §4 of the [canonical spec template](../sdd/07-canonical-spec-template.md) (Archetype Declaration) is extended with a **Composition Declaration** sub-block. The fragment below is the canonical form:

```markdown
## 4. Archetype Declaration

**Classification:** Executor (governing)

**Composition:** Mode-switching (Pattern E) — coding agent shape
- Mode 1: Synthesizer — plan, explain, summarize the change
- Mode 2: Executor — write files, run tests, open PR  (governing)
- Mode 3: Orchestrator-over-self — delegate sub-tasks across files

**Mode transitions:**
- Synthesizer → Executor: when the user accepts a plan
- Executor → Synthesizer: when a sub-task is blocked or the spec
  is ambiguous; produce a clarification request, do not guess
- Executor → Orchestrator-over-self: when a sub-task requires
  more than 5 file edits; surface a sub-task plan for confirmation

**Cross-mode invariants** (hold regardless of active mode):
- File-system scope: read+write limited to repository root,
  excluding the test directory in every mode
- Test deletion forbidden
- No outbound traffic except to whitelisted domains
- Spec amendments cannot be made by the agent; only by humans
  via spec review

**Per-mode oversight** (referenced in §11 Agent Execution Instructions):
- Synthesizer mode: Periodic — sample 1 in 5 plans
- Executor mode: Pre-authorized scope, exceptions escalate
- Orchestrator-over-self mode: Output Gate at PR boundary
```

Two things this fragment guarantees:

1. **Cross-mode invariants are written down where the spec author had to think about them.** They cannot be "implicitly assumed" across modes. A reviewer reading §4 sees them as first-class declarations, not as scattered constraints.
2. **The transitions become a reviewable surface.** A reviewer can ask "what triggers this transition? what state carries across? which invariants persist?" before the system ships, instead of after the first incident.

Without this fragment, mode-switching systems often have *implicit* transitions that nobody specced. Cat 1 (Spec) failures in coding agents are disproportionately *transition* failures: the agent moved from Synthesizer mode into Executor mode without re-checking a constraint that the spec only declared in one of the two modes. Declaring the transitions makes those failures visible at review time.

For Patterns A–D (layered compositions), the Composition Declaration is simpler — it names the governing archetype and lists the embedded components with their archetype roles, instead of naming modes and transitions. The cross-component invariants section still applies: invariants that hold across all components go in §6 at the system level, not inside any single component's section.

---

### Worked example: spec-conflict resolution in an Advisor + Executor composition

The four patterns above describe well-formed compositions. In practice, two archetypes' specs eventually conflict on a specific case the framework didn't anticipate. The resolution rules from [Multi-Agent Governance](07-multi-agent-governance.md) — *(1) higher-tier invariant wins; (2) earlier-in-pipeline-wins-on-read, later-on-write; (3) tie-break: surface, don't resolve* — apply here too. This worked example shows the rules in action.

**The system.** A customer-facing financial-planning agent. Pattern A (Advisor → Executor confirm-then-act). The Advisor surfaces investment options; the Executor places trades on the user's confirmation.

**The Advisor's spec (excerpt):**
- *§3 Scope:* "Surface up to five options across the user's stated risk profile, including options that maximize expected return."
- *§5 Constraint A1:* "Always include at least one option above the user's stated risk profile when available, clearly flagged. Users may want to be aware of higher-return options even if they ultimately choose conservatively."

**The Executor's spec (excerpt):**
- *§3 Scope:* "Place trades for options the user confirms."
- *§5 Constraint E1 (invariant):* "Never place trades that exceed the user's stated risk profile. Any such request must surface."
- *§5 Constraint E2:* "Trade size limited to $5,000 per session without secondary confirmation."

**The conflict.** The Advisor surfaces a higher-risk option per A1. The user, attracted by the return, confirms it. The Executor receives a confirmation for a trade that violates E1. Two specs are in tension: A1 expects the system to surface higher-risk options; E1 forbids placing those trades.

**Naive resolutions, both wrong:**

- *"The user confirmed, so the Executor should proceed."* This treats user confirmation as overriding the Executor's invariant. It does not. Invariants are not waivable by user request — they are by definition the constraints that cannot be traded.
- *"The Advisor should not surface options the Executor cannot place."* This treats the Advisor's job as constrained by the Executor's authorization. But the Advisor's job (per A1) is to inform — including about options the user may not be authorized for. Restricting it would lose information value.

**Correct resolution, applying the three rules:**

1. **Rule 1 (higher-tier invariant wins).** E1 is declared as an invariant. A1 is a constraint. The invariant binds. The trade does not happen.
2. **Rule 2 (earlier-on-read, later-on-write).** The Advisor reads the user's risk profile and informs; that is its read-side authority. The Executor writes (places the trade); on the write side, the Executor's constraints bind. Rule 2 reinforces Rule 1 here.
3. **Rule 3 (surface, don't resolve).** Even with Rules 1 and 2 deciding the outcome, the *user* needs to know what happened. The system surfaces: "You selected an option above your stated risk profile. To proceed with this trade, please update your risk profile through [process Y] and reconfirm. Otherwise, please select a different option."

**What the system spec should encode (above the per-component specs):**

```
Conflict resolution policy:
- Advisor's information surface is bounded only by Advisor §3 and §5.
- Executor's authorization-to-act is bounded by Executor §3 and §5.
- When user confirms an Advisor-surfaced option that the Executor's
  invariant forbids: do not act; surface the conflict to the user
  with the specific invariant cited and the path to resolve it
  (update risk profile, choose different option).
- The system never silently downgrades a user's selection. The user
  is told their selection cannot be acted on and why.
- The Advisor's flagging discipline (A1's "clearly flagged") is the
  first line of defense — if the user is well-informed about which
  options exceed their profile, the conflict rate drops. This is
  measured: target conflict-surface rate < 5% of confirmed selections.
```

**The lesson, generalizing.** Spec conflicts in compositions are common and expected. The rule is not "design specs that never conflict" — that's not achievable. The rule is "make the resolution policy explicit at the system level, before the conflict happens." The three rules give a default; the system spec can refine them per case. What is forbidden is silent resolution by either component, which is itself a Cat 1 spec failure of the *system spec* even when both component specs are individually correct.

---

### The Composition Checklist

When a system involves more than one archetype role, verify:

- [ ] The governing archetype has been identified (highest-risk autonomous action)
- [ ] Each embedded component or mode has been named and typed
- [ ] Guardian-class embedded components cannot be bypassed by the governing layer
- [ ] Advisory-class embedded components feeding confirm-then-act patterns are recognized as oversight model implementations, not separate systems
- [ ] Each sub-agent in an Orchestrator composition has its own archetype declaration
- [ ] **For mode-switching systems (Pattern E):** every transition between modes is documented with its trigger and the state that carries across
- [ ] **For mode-switching systems:** every invariant that must hold across modes is declared once at the system level, not duplicated (or worse, omitted) in mode-specific sections
- [ ] The spec includes a §4 Composition Declaration naming the governing archetype, the embedded components or modes, the transitions (if any), the cross-mode/cross-component invariants, and the per-component or per-mode oversight notes
- [ ] The governing invariants are written at the system level, not the component level
- [ ] No section of the spec says "mostly X with some Y" — each component has a definite type

---

### What Composition is Not

Composition is not a license to make a system do anything by slicing it into enough pieces.

If you find yourself classifying a system as "Advisor for the retrieval step, Executor for the action step, Guardian for the safety step, Synthesizer for the reporting step, Orchestrator at the top" — you are probably describing a system that is too large to govern coherently as a single entity.

The question to ask: *Would a single on-call engineer be able to understand and halt any part of this system within five minutes?* If not, the system is not too complex to classify — it is too complex to run. Break it into separately deployable systems with separately governable boundaries.

Composition is meant to clarify layering within a coherent unit. It is not a way to make complexity legible in documentation while leaving it ungovernable in production.

---

## Resulting Context

After applying this pattern:

- **Governing archetype determines risk.** By identifying the highest-risk autonomous action and using that to set the governing archetype, the composition privileges safety.
- **Embedded components are constrained separately.** Guardian components embedded in an Executor cannot be bypassed by Executor-level decisions. The Guardian operates in its own governance tier.
- **Confirm-then-act becomes a governance pattern.** An Advisor phase feeding into an Executor phase is recognized as an Executor implementing its required oversight gate.
- **Coherence without fragmentation.** A composed system has one authoritative spec, not multiple specs in contradiction.

---

## Therefore

> **Real systems layer or mode-switch across multiple archetype roles, and composition is the structural surface that captures both. Give the system one governing archetype — determined by its highest-risk autonomous action — and declare embedded components or modes explicitly with their own constraints, transitions, and cross-mode invariants in a §4 Composition Declaration. A Guardian embedded in an Executor cannot be disabled by Executor-level decisions. An Advisor embedded as a confirmation step is how the Executor implements its oversight model. A coding agent's Synthesizer-Executor-Orchestrator mode-switching is a single Executor with declared transitions, not three systems and not a missing archetype. Composition clarifies layering and mode-switching; it is not a substitute for decomposing a system that is too complex to govern.**

---

## Connections

**This pattern assumes:**
- [The Five Archetypes](02-canonical-intent-archetypes.md)
- [Four Dimensions of Governance](03-archetype-dimensions.md)
- [The Archetype Selection Tree](04-decision-tree.md)

**This pattern enables:**
- [Governed Archetype Evolution](06-evolving-archetypes.md)
- [The Canonical Spec Template](../sdd/07-canonical-spec-template.md) — multi-component spec structure
- Each archetype deep-dive: [Advisor](archetypes/advisor.md), [Executor](archetypes/executor.md), [Guardian](archetypes/guardian.md), [Synthesizer](archetypes/synthesizer.md), [Orchestrator](archetypes/orchestrator.md)

---
