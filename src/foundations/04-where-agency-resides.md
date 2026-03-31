# Distributed Agency, Explicit Authority

**Foundations**

---

> *"Agency is not a property of a tool. It is a property of the relationship between the tool, its instructions, and the human who set it in motion."*

---

## Context

You are designing systems where multiple actors — humans, agents, tools, orchestrators — share the work of producing outcomes. You need to reason about **who or what is making decisions** at each point in the system, and what that means for accountability, reversibility, and oversight.

This pattern builds on [Authorship in Software](03-authorship-in-software.md) and prepares for [Three Dimensions of Delegation](../theory/03-agency-autonomy-responsibility.md).

---

## The Problem

The word "agency" is overloaded. In everyday speech, we call a tool that executes automatically an "agent." But this papers over a distinction that matters enormously: the difference between **operational autonomy** (executing a pre-defined process without human intervention at each step) and **genuine agency** (making decisions with discretion, in contexts that the original instructors did not fully anticipate).

A thermostat has operational autonomy. A chess engine playing on your behalf has something more. A language model responding to a prompt about an unfamiliar edge case in your business logic has something more still.

When a system acts in the world — sends a message, modifies data, calls an external service, commits code — the question "who decided to do that?" has a real answer, and that answer is not always "the agent."

---

## Forces

- **Operational autonomy vs. genuine agency.** Executing a defined process is not the same as making decisions with discretion in unforeseen contexts; the distinction matters for oversight design.
- **Authorization scope vs. runtime discretion.** How much freedom the specification allows the executor is directly proportional to the executor's effective agency in the system.
- **Distributed agency vs. singular accountability.** Multiple actors participate in decisions, yet someone must be accountable for what the system does.
- **Reversibility vs. authority.** Broad discretion is tolerable for reversible actions; narrow discretion is required for irreversible actions.

---

## The Solution

Agency in a system is distributed across multiple actors, each carrying a portion of the decision-making authority:

**The Instructor** (spec author, prompt writer, system designer) allocates agency by defining the space of allowed actions, the goals to pursue, and the constraints that bound the system's discretion. The instructor's choices determine how much latitude the agent has.

**The Executor** (the agent, the tool, the orchestrator) operates within the space defined by the instructor. The broader the instructions, the more genuine agency the executor has. The narrower the constraints, the less.

**The Oversight Function** (the human reviewer, the validation step, the approval gate) can reduce effective agency by introducing checkpoints where a human re-examines and confirms before consequences become irreversible.

The practical implication: **where you put agency matters**. Delegation without constraint gives broad agency to the executor. Delegation with tight constraints narrows it. Delegation with active oversight narrows it further still.

The [Four Dimensions of Governance](../architecture/03-archetype-dimensions.md) chapter formalizes exactly this: the agency dimension of an archetype expresses how much discretion the system is authorized to exercise.

---

## Agency and Reversibility

The most important design question about agency is not "how much?" but "at what stakes?"

An agent with broad discretion over reversible actions (writing draft documents, suggesting code edits, generating test cases) is low-risk. An agent with narrow discretion over irreversible actions (sending emails to customers, modifying production data, approving financial transactions) is high-risk.

The **reversibility dimension** of a system is as important as the agency dimension. Systems that combine high agency with low reversibility require the strongest oversight structures.

---

## Resulting Context

After applying this pattern:

- **Specification becomes an authorization frame.** What an agent is allowed to do is deliberately constrained at design time, not discovered through iteration.
- **Agency analysis becomes a design practice.** Teams reason explicitly about where agency should reside for each type of decision and consequence.
- **Oversight structures match agency levels.** High agency requires stronger oversight; low agency can be paired with lighter checkpoints.
- **Escalation becomes systematic.** When an agent encounters situations outside designed scope, the system escalates rather than executing with discretion beyond intent.

---

## Therefore

> **Agency is distributed, not localized. When designing systems with agents, deliberately decide where agency resides at each step: in the specification (what is allowed), in the executor (what is decided at runtime), or in the oversight function (what is reviewed before consequences land). Design your oversight proportionally to the combination of agency level and irreversibility.**

---

## Connections

**This pattern assumes:**
- [Authorship in Software](03-authorship-in-software.md)

**This pattern enables:**
- [When Power Scales Faster Than Judgment](05-when-power-scales-faster-than-judgment.md)
- [Three Dimensions of Delegation](../theory/03-agency-autonomy-responsibility.md)
- [Design for Reversibility](../theory/04-reversibility-as-design-dimension.md)
- [Four Dimensions of Governance](../architecture/03-archetype-dimensions.md)
- [Proportional Oversight](../agents/06-human-oversight-models.md)

---
