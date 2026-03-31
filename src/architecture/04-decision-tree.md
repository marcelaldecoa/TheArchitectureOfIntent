# The Archetype Selection Tree

**Governance & Architecture**

---

> *"The most expensive design decision is not the one that costs the most to make. It is the one you made without realizing you were making it."*

---

## Context

You are at the beginning of specifying an agent system — or you are reviewing a system that already exists and wondering if it was designed coherently. You need a practical tool for selecting (or validating) the correct archetype.

This pattern provides the decision tree. It is meant to be used — in design sessions, in spec reviews, when onboarding a new system. It is deliberately brief at the top, expanding into nuance as needed.

This pattern assumes [The Five Archetypes](02-canonical-intent-archetypes.md) and [Four Dimensions of Governance](03-archetype-dimensions.md).

---

## The Problem

The five archetypes describe stable categories, but real systems don't announce what they are. A brief description — "it automates customer support" — does not tell you which archetype applies. "It helps users find answers" could be an Advisor. "It resolves tickets autonomously" could be an Executor. "It checks that responses comply with policy" could be a Guardian.

The wrong archetype selection is not just an organizational mistake. It produces tangible design failures: oversight models that don't fit the actual risk, capability boundaries that don't match the real action space, invariants that weren't designed for the system's true function.

A decision tree that is fast to use and hard to game is the antidote to archetype drift before it begins.

---

## Forces

- **Speed vs. precision.** A decision tree must be fast enough to use in active development. Yet speed must not sacrifice correctness \u2014 misclassification early leads to wrong governance from the start.
- **Generality vs. ambiguity.** Some questions are clear-cut. Others are genuinely ambiguous. The tree must resolve ambiguity without requiring extended conversation.
- **Objective inquiry vs. contextual judgment.** The earliest questions should be observable facts about the system. Yet eventually judgment is required. The tree must bridge from observation to judgment.
- **Reusability vs. customization.** The tree should be the same for every organization. Yet some organizations have specific concerns. The tree must be both standard and customizable.

---

## The Solution

### The Primary Decision Tree

Apply these questions in order. Stop at the first match.

```
┌─────────────────────────────────────────────────────────────────────┐
│ QUESTION 1: Does this system take any consequential action           │
│ in the world — writing data, sending messages, calling APIs,         │
│ executing code, modifying state — without a human act between        │
│ its output and the consequence?                                      │
└─────────────────────────────────────────────────────────────────────┘
         │
         ▼
    NO   ──────────────────────────────────────────► ADVISOR
         
    YES  ──────────────────────────────────────────► continue to Q2
         
┌─────────────────────────────────────────────────────────────────────┐
│ QUESTION 2: Is the system's PRIMARY purpose to protect a boundary,   │
│ enforce a constraint, or prevent a violation — rather than to        │
│ accomplish a positive goal?                                          │
└─────────────────────────────────────────────────────────────────────┘
         │
    YES  ──────────────────────────────────────────► GUARDIAN
         
    NO   ──────────────────────────────────────────► continue to Q3
         
┌─────────────────────────────────────────────────────────────────────┐
│ QUESTION 3: Does this system's work fundamentally involve            │
│ directing, coordinating, or allocating work across OTHER agents,     │
│ tools, or services — rather than doing the work itself?              │
└─────────────────────────────────────────────────────────────────────┘
         │
    YES  ──────────────────────────────────────────► ORCHESTRATOR
         
    NO   ──────────────────────────────────────────► continue to Q4
         
┌─────────────────────────────────────────────────────────────────────┐
│ QUESTION 4: Is this system's primary output a synthesized artifact   │
│ — a summary, report, combined analysis, or composed document —       │
│ rather than an action taken on a target system or service?           │
└─────────────────────────────────────────────────────────────────────┘
         │
    YES  ──────────────────────────────────────────► SYNTHESIZER
         
    NO   ──────────────────────────────────────────► EXECUTOR
```

---

### Resolving Ambiguity at Each Question

**Q1 — Ambiguous cases:**

*"It writes to a staging environment, not production."* — The staging write is still a consequential action; the system is not an Advisor. Proceed to Q2.

*"It shows users what it would do before doing it."* — If the preview-then-confirm pattern includes a human confirmation step before execution, this can be Advisor-class for the advisory phase, and Executor-class for the execution phase. This is a composition. See [Composing Archetypes](05-composing-archetypes.md).

*"It only writes to a scratch file for the user to review."* — Review carefully. If the user's review is a genuine gate (they can reject the output and nothing happens), this is Advisor-class with a draft artifact. If the output typically gets applied without substantive review, treat as Executor.

---

**Q2 — Ambiguous cases:**

*"It validates AND fixes compliance issues."* — This system has a Guardian component (enforcing the constraint) and an Executor component (taking remediation action). This is a composition — it needs both governance models. See [Composing Archetypes](05-composing-archetypes.md).

*"It enforces rate limits but can also provision resources."* — Rate limit enforcement is Guardian behavior. Resource provisioning is Executor behavior. These are separate components with separate governance requirements. Do not blend into one archetype.

---

**Q3 — Ambiguous cases:**

*"It calls one external API."* — Calling one external service is not orchestration in the archetype sense. Orchestration means systematically allocating work *across* agents or services with coordination logic. A single API call is an Executor capability.

*"It has a pipeline with three steps."* — A linear pipeline is not necessarily an Orchestrator. If the steps are always the same and there is no conditional routing, parallel dispatch, or inter-agent coordination, this is an Executor with multiple actions. If there is dynamic routing, parallelism, or inter-agent state management, it is an Orchestrator.

---

**Q4 — Distinguishing Synthesizer from Executor:**

The key test: does the system *produce an artifact for humans to evaluate* (Synthesizer) or *produce a change in a target system* (Executor)?

A system that generates a structured report: **Synthesizer**.  
A system that generates a structured report *and publishes it to the company portal*: **Synthesizer + Executor** composition.  
A system that reads multiple APIs and writes the combined result to a database: **Executor** (the primary act is writing state, not producing an artifact for review).

---

### The Risk Override

After selecting an archetype, apply one override check:

> **If the system's consequence-of-failure is Critical (broad impact, high severity, or slow detectability), document that explicitly and escalate the governance tier — regardless of archetype category.**

An Advisor system that advises millions of people on medical decisions is still an Advisor by structure, but it carries Critical risk by impact scope. It needs Oversight Model C (output gate) even though most Advisors use Monitoring. The archetype defines the minimum. Risk overrides the minimum upward.

---

### Archetype Profile Card (Quick Reference)

| Question | Advisor | Guardian | Orchestrator | Synthesizer | Executor |
|----------|:-------:|:--------:|:------------:|:-----------:|:--------:|
| Takes autonomous action? | ✗ | Block only | ✓ | sometimes | ✓ |
| Primary purpose is enforcement? | ✗ | ✓ | ✗ | ✗ | ✗ |
| Coordinates other agents? | ✗ | ✗ | ✓ | ✗ | ✗ |
| Primary output is an artifact? | ✓ | ✗ | ✗ | ✓ | sometimes |
| Default oversight model | Monitoring | Monitoring + alert | Output gate | Periodic/gate | Pre-auth scope |
| Minimum agency level | 1–2 | 2 (veto) | 4–5 | 3 | 3–4 |

---

### Documenting the Selection

Every spec should include an explicit archetype declaration. This is not bureaucracy — it is a design decision that the reader needs to understand quickly, and that the agent needs as architectural context.

Canonical form in a spec:

```markdown
## Archetype

**Classification:** Executor  
**Agency Level:** 3 — Bounded (decides how to accomplish defined tasks 
                  within a constrained module scope)  
**Risk Posture:** Medium (impacts production codebase; partially reversible 
                  via git history)  
**Oversight Model:** D — Pre-authorized scope with exception gate  
**Reversibility:** Partially reversible (commits can be reverted; PR creation 
                  is observable; no direct production writes)
```

One paragraph. Written before behavioral specification begins. Reviewed by the same person who would authorize the archetype definition itself.

---

## Resulting Context

After applying this pattern:

- **Classification becomes observable.** A decision tree grounded in observable questions makes the archetype classification verifiable by examining the system, rather than debating its intent.
- **Risk overrides are explicit.** The tree acknowledges that risk can require a governance tier higher than the archetype minimum. The override is named and documented.
- **Misclassification risk is reduced.** By starting with the most discriminating question and proceeding downward, the tree minimizes misclassification.
- **Newcomers can classify consistently.** With an explicit decision tree, a new team member can classify a system using the same reasoning as an experienced architect.

---

## Therefore

> **Archetype selection follows a four-question decision tree: Does it act? Does it primarily enforce? Does it coordinate agents? Does it produce an artifact? The first three questions determine whether you have a Guardian, Orchestrator, or need to distinguish Synthesizer from Executor. Nothing should be specced until the archetype is declared and reviewed. The declaration is the most consequential sentence in the spec.**

---

## Connections

**This pattern assumes:**
- [The Five Archetypes](02-canonical-intent-archetypes.md)
- [Four Dimensions of Governance](03-archetype-dimensions.md)

**This pattern enables:**
- [Archetype Composition](05-composing-archetypes.md) — when one archetype isn't enough
- [The Canonical Spec Template](../sdd/07-canonical-spec-template.md) — the archetype declaration section
- [SpecKit](../sdd/04-speckit.md) — SpecKit's archetype integration

---
