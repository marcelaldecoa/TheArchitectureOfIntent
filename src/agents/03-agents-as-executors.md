# Pattern 5.3 — Agents as Executors of Intent

**Part V: Agents & Execution** · *3 of 7*

---

> *"The musician does not compose while performing. That work was done before the first note. Performance is execution — and execution, when the intent is clear, is a kind of freedom."*

---

## Context

We have defined what agents are and clarified the autonomy question. We now arrive at the central architectural claim of this book: that agents are, fundamentally, *executors of intent* — not decision-makers, not collaborators in the full sense, not participants in the process of determining what should be done. They are specialized instruments for doing what has been decided, under conditions that have been specified.

This is not a limitation to be overcome. It is the architecture's foundational design principle, and understanding it changes how you write specs, how you assign tasks, how you evaluate outputs, and how you attribute failure.

This chapter assumes Parts I–IV in full. It is the theoretical pivot point between the introductory chapters of Part V and the concrete design patterns that follow.

---

## The Problem

The prevailing mental model for working with AI agents is conversational: you talk to the agent, the agent responds, you adjust, it adjusts, you converge on something good. This model works for exploration. It is a poor foundation for execution at scale.

The conversational model creates several structural problems:

**Accountability diffusion.** When expectations are set in a conversation, no one can determine afterwards what was actually agreed. The human remembers their intent; the agent has no persistent state of what was "agreed." The output cannot be validated against a defined standard because the standard was never externalized.

**Non-reproducibility.** If you run the same conversation twice, you get two different outputs — not because the world changed, but because conversations don't constrain. An agent operating in conversational mode has wide latitude to make different choices each time.

**Silent renegotiation.** In a conversation, the agent adapts to feedback. This is useful for exploration but dangerous for execution: the agent may interpret feedback as an update to the objective rather than a correction to the path. The goal shifts without acknowledgment.

**Invisible scope creep.** Conversational framing often escalates the agent's role from executor to co-designer. The agent starts completing gaps, making assumptions, and extending the brief — none of which is visible unless the output is compared against an externalized intent document.

---

## The Resolution

### The Executor Model

In the executor model, the agent's role is defined in three parts:

**Pre-execution:** A human produces a complete specification of the work — what to produce, under what constraints, with what success criteria. The spec is validated before any execution begins.

**Execution:** The agent works against the spec as its primary directive. It uses the tools in its capability set, follows the constraints in the spec, and pursues the defined outcome. It does not add scope, change objectives, or re-prioritize without explicit authorization.

**Post-execution:** A human validates the output against the spec. If the output satisfies the spec, it is accepted. If it does not, the first diagnostic question is whether the spec was correct; the second is whether the execution deviated from the spec.

This loop — spec, execute, validate — is the entire architecture. Everything else in this book is detail about how to do each stage well.

### What Executors Need from a Spec

An agent acting as an executor needs, at minimum:

| Spec Element | Why It's Required |
|---|---|
| Objective statement | What success looks like — the agent must know when to stop |
| Scope declaration | What is in and out — prevents capability expansion into adjacent work |
| Constraint list | What the agent may *not* do — the outer fence on execution |
| Tool/resource list | What capabilities are available and pre-authorized |
| Success criteria | Validation tests — how to verify the output before surfacing it |
| Escalation conditions | When to pause and request human input rather than proceeding |

An agent without these elements is not under-supported — it is under-specified. It will complete the task in some way, because completeness is trained into it. What it will not do is complete the task in the *correct* way, because correct requires a definition, and no definition was provided.

### What Executors Do Not Need

The executor model also clarifies what agents do not need:

**Motivation.** An agent does not need to understand *why* the task matters. Motivation is a human property. The agent needs only to know what to do and how to verify it is done correctly. Explaining organizational context in a spec is useful for cases where it changes the *what* — but philosophical rationale is waste.

**Autonomy beyond task scope.** An agent executing a defined task has no business deciding that a related task also needs doing and doing it. The executor framing explicitly prohibits scope extension. The agent should finish what was asked, surface what it found, and stop.

**Judgment about the objective.** The human who writes the spec exercises the judgment about what should be done. The agent exercises judgment about *how to do it* within the constraints — which tool, which path, which phrasing. The consequential judgment belongs to the spec author.

### The Spec-Execute-Validate Loop in Practice

The loop is deceptively simple:

```
Spec → Execute → Validate
 ↑                    │
 └────────────────────┘
   (if spec was wrong: update spec)
   (if execution was wrong: re-execute)
```

The critical discipline is the feedback path. When validation fails, the first question is *which kind of failure?*

- If the spec was ambiguous or incorrect, the loop goes back to the spec. Fix the spec. Re-execute against the corrected spec. Do not patch the output without patching the spec — that creates spec debt.
- If the spec was correct and the execution deviated, re-execute against the same spec. If the deviation recurs, investigate the capability — the agent may lack a tool, or a tool may be behaving unexpectedly.
- If the spec was correct, the execution was faithful, but the outcome was still not desired — the human's intent was not captured in the spec. This is the most instructive failure: it reveals an assumption that was never externalized.

### The "Brilliant New Hire" Analogy — and Why It Falls Short

A common framing for AI agents is the "brilliant new hire" — a highly capable person with excellent skills and no organizational context. The framing is pedagogically useful for explaining why agents need onboarding (skills) and context (spec). But it carries implications that mislead.

A brilliant new hire has initiative. They will, correctly, ask clarifying questions, push back on under-specified tasks, and recognize when the assignment doesn't make sense. An agent will not do these things reliably. It will proceed on the most plausible interpretation of what it was given. It will fill gaps with what seems reasonable, not with what was intended.

A brilliant new hire develops judgment over time and internalizes organizational values. An agent's "judgment" is frozen in training. Its sense of what is reasonable was calibrated on a distribution of text that may or may not reflect your organizational context.

The executor model is more accurate and more useful. An executor is not hired for judgment about what to do — they are engaged to do a specific thing with excellence. The excellence is in the execution, not the objective-setting. This is not diminishment — it is specialization, and specialization is what makes high-quality delegation possible.

### Implications for How You Write Specs

The executor model has direct consequences for spec quality:

**Write specs as if the agent has no good judgment.** Not because agents are incompetent, but because judgment about what you want lives in your head and nowhere else. Write it out. Every assumption, every constraint, every preference for how an edge case should be handled.

**Include what the agent should *not* do.** Executors are bounded by their instructions. Without explicit prohibitions, an agent operating in the "reasonable interpretation" space will expand. The NOT-authorized section of a spec is not a formality — it is the fence.

**Test the spec before you run it.** Ask: if a competent person who had never spoken with me executed exactly this spec, would they produce the output I want? If the answer is no, the spec is not ready.

---

## Therefore

> **Agents are executors of intent: they operate with maximum competence within a defined space, but they do not set the space, expand the space, or evaluate whether the space is the right one. The spec is the boundary of that space. Every failure to specify is a delegation of a decision the human should have made — and the agent will make it, quietly, in whatever direction seems most plausible.**

---

## Connections

**This pattern assumes:**
- [What Agents Are (and Are Not)](01-what-agents-are.md)
- [Operational Autonomy vs. Genuine Agency](02-autonomy-vs-agency.md)
- [What Spec-Driven Development Really Means](../sdd/01-what-sdd-means.md)
- [Writing Specs for Agents](../sdd/05-writing-specs-for-agents.md)

**This pattern enables:**
- [Tools, MCP, and Capability Boundaries](04-tools-mcp-capability-boundaries.md)
- [Human Oversight Models](06-human-oversight-models.md)
- [Failure Modes in Agent Systems](07-failure-modes.md)
- [The Canonical Spec Template](../sdd/07-canonical-spec-template.md)

---

*Next: [Tools, MCP, and Capability Boundaries](04-tools-mcp-capability-boundaries.md)*


