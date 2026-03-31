# Pattern 3.2 — The Five Archetypes

**Part III: Intent Architecture** · *2 of 6*

---

> *"You do not invent your relationship to power every time you wield it. You inherit a form — or you build one deliberately. The archetypes are the forms built deliberately."*

---

## Context

You understand that archetypes are constitutional frames, not templates (Pattern 3.1). Now you need the archetypes themselves: their names, their precise definitions, their distinguishing characteristics, and the reasoning behind each.

This chapter introduces the five canonical intent archetypes. Each is named, characterized, and distinguished from the others. Detailed per-archetype specifications live in the [Archetype Catalog](../repertoires/02-archetype-catalog.md) and the individual archetype pages.

---

## The Problem

Agent systems vary enormously along multiple dimensions: how much they act vs. advise, how much discretion they exercise, how often humans review their outputs, how reversible their actions are. Without a shared vocabulary for these variations, every system is designed from scratch — with no inherited wisdom about which design decisions are consequential and which are flexible.

The result is systems that are miscalibrated: advisors that gradually acquire executor behaviors, executors deployed without adequate oversight, guardians that are actually orchestrators in disguise. The miscalibration is not always intentional — often it is the product of incremental feature additions, each of which seemed reasonable in isolation.

The five archetypes solve this by naming the recurring, stable forms — the categories that emerge from principled reasoning about agency, authority, and consequence. Every agent-mediated system fits one of these forms, or a deliberate composition of them.

---

## Forces

- **Specificity vs. completeness.** A single archetype framework cannot account for every variation without becoming too granular to be useful. Yet too few categories leave genuine differences in risk and governance unmarked.
- **Stability vs. emergence.** The framework should be stable enough to guide decisions across organizations and time; yet if real systems emerge that don't fit the five archetypes, the framework should be extended rather than forced.
- **Authority clarity vs. discretion.** Some systems need significant autonomy while others should be highly constrained. Each archetype must give enough discretion to be useful while remaining governable.
- **Reusability vs. context-sensitivity.** The archetypes should be recognizable across multiple systems. Yet each system is unique. The framework must allow both consistency and specialization.

---

## The Solution

### How the Five Archetypes Were Derived

The archetypes are not a taxonomy invented for convenience. They emerge from two axes:

**Axis 1: What is the system's primary act?** Does it *inform* (produce knowledge or recommendations for humans to act on), *execute* (take actions in the world), *enforce* (protect constraints and prevent violations), *synthesize* (compose or transform information), or *orchestrate* (coordinate the work of other agents)?

**Axis 2: What is the scope of its discretion?** Does the system decide *how to present* information (minimal discretion), *how to perform* a defined task (bounded discretion), *whether to allow or block* an action (veto discretion), *how to combine* inputs (compositional discretion), or *how to allocate* work across agents (coordination discretion)?

The five archetypes emerge from consistent positions on these axes:

| Archetype | Primary Act | Discretion Scope |
|-----------|-------------|------------------|
| Advisor | Inform | How to present |
| Executor | Execute | How to perform |
| Guardian | Enforce | Whether to allow |
| Synthesizer | Synthesize | How to combine |
| Orchestrator | Orchestrate | How to allocate |

---

### Archetype 1: The Advisor

**Identity:** A system whose role is to surface information, produce analyses, generate recommendations, or suggest options — without taking any action in the world on behalf of the user.

**Defining characteristic:** The human always decides and always acts. The Advisor never acts on the human's behalf. Its outputs are inputs to human decision-making, not substitutes for it.

**Typical forms:** Recommendation engines, analytical dashboards, conversational assistants that answer questions, code review tools that suggest (not apply) changes, trend analysis systems, diagnostic tools that identify problems for human resolution.

**What makes this category distinct:** The Advisor archetype carries the lowest inherent risk of the five, because every consequential action passes through a human decision point. The advisor can be wrong — its recommendation can be poor, its analysis can be flawed — and the harm is bounded by the human's willingness to act on it. This is the primary reason to keep systems in the Advisor category when advisement meets the need: it preserves human judgment at the point of consequence.

**The violation to watch for:** An Advisor that begins *writing* (not just suggesting) changes to code, emails, or production data has drifted into Executor territory. The line is whether the system takes consequential action, not whether it produces text.

→ Full specification: [The Advisor Archetype](archetypes/advisor.md)

---

### Archetype 2: The Executor

**Identity:** A system that carries out well-defined tasks autonomously — taking actions in the world within a precisely specified scope of authority.

**Defining characteristic:** The Executor acts. It produces real outputs: modified files, sent messages, created records, deployed infrastructure. Its agency is bounded but genuine: within its authorized scope, it decides *how* to accomplish the task.

**Typical forms:** CI/CD pipeline agents, code-generation agents operating within a defined module, automated test writers, infrastructure provisioners, content publishing agents, data transformation pipelines with write access.

**What makes this category distinct:** The Executor's power comes from its ability to act reliably within a defined space without requiring human approval at each step. Its safety comes from the precision with which that space is defined. A well-constrained Executor is highly productive and manageable. An under-constrained Executor is dangerous at speed.

**The critical design requirement:** Every Executor must have explicit scope boundaries (what it can affect), explicit invariants (what it must never do even within scope), and an escalation path for situations that fall outside the designed scope. An Executor that encounters ambiguity and guesses is the most common source of compounding failures.

**The violation to watch for:** An Executor that begins making decisions about *what the scope should be* — that expands its own authority based on what seems locally reasonable — has drifted into Orchestrator territory without the corresponding oversight structure.

→ Full specification: [The Executor Archetype](archetypes/executor.md)

---

### Archetype 3: The Guardian

**Identity:** A system whose primary function is to enforce constraints, protect invariants, validate integrity, and prevent violations — acting as a gatekeeper between a request or state and a consequential outcome.

**Defining characteristic:** The Guardian's agency is primarily *negative*: it can block, flag, abort, or alert. It does not initiate actions toward positive goals. It polices boundaries. This one-directional power is intentional — a Guardian that can also act positively is an Executor with a Guardian's constraints, which is a different and more complex design.

**Typical forms:** Security policy enforcers, compliance validators, PII detection layers, schema validators, rate limiters, approval gates in workflows, content safety filters, financial limit enforcers, contract invariant checkers.

**What makes this category distinct:** The Guardian operates on a principle of **minimum necessary power**: it needs only enough authority to block what should be blocked. This deliberate limitation is what makes Guardian systems trustworthy. An organization can deploy a Guardian broadly, with relatively liberal permissions to inspect, because its action space is restricted to refusal.

**The violation to watch for:** A Guardian that begins *remediating* violations (not just flagging them) — rewriting the content that failed the check, substituting compliant behavior for non-compliant behavior — has acquired Executor characteristics that require a different oversight model.

→ Full specification: [The Guardian Archetype](archetypes/guardian.md)

---

### Archetype 4: The Synthesizer

**Identity:** A system that aggregates, distills, transforms, or composes information from multiple sources into structured outputs — exercising discretion about *how* to combine and present, but not about *what to act upon*.

**Defining characteristic:** The Synthesizer's output is a new artifact — a summary, a report, a combined analysis, a transformed dataset, a generated draft. Its discretion is compositional: it decides how to weigh sources, how to structure the output, how to resolve conflicts between inputs. It does not decide what real-world actions the output should trigger.

**Typical forms:** Research synthesis agents, multi-source report generators, knowledge base builders, code documentation agents, meeting transcript summarizers, multi-API data aggregators, contract review systems that produce structured findings.

**What makes this category distinct:** The Synthesizer is the highest-agency archetype that reliably keeps consequential action in human hands — the human acts on the synthesized output, rather than the synthesizer itself triggering real-world change. This makes it appropriate for situations where the *breadth and depth of information processing* needed exceeds human capacity, but where the *judgments about what to do* must remain human.

**The violation to watch for:** A Synthesizer that begins taking action based on its own outputs — sending the report it just generated, implementing the recommendations it just produced — has become a hybrid that requires both Synthesizer and Executor governance simultaneously.

→ Full specification: [The Synthesizer Archetype](archetypes/synthesizer.md)

---

### Archetype 5: The Orchestrator

**Identity:** A system that coordinates the work of multiple agents, tools, or services toward a compound goal — exercising discretion over how work is divided, sequenced, assigned, and integrated.

**Defining characteristic:** The Orchestrator manages agency. It does not primarily do the work itself; it directs systems that do. Its discretion is coordinative: deciding which capability is needed for which step, how to handle partial failures, when to proceed vs. wait, and how to integrate results. Because it is directing systems that themselves have agency, the Orchestrator's errors propagate multiplicatively.

**Typical forms:** Multi-agent development pipelines, research orchestration systems, complex workflow engines, systems that coordinate between customer-facing AI and backend services, automated release orchestrators, multi-step business process agents.

**What makes this category distinct:** The Orchestrator is the only archetype that inherits and multiplies the risk profile of the systems it directs. An Orchestrator managing a set of Executors carries the combined risk of all those Executors plus its own coordination decisions. This is why Orchestrator systems require the most careful governance — not because the Orchestrator itself is particularly powerful, but because it controls what is.

**The violation to watch for:** An Orchestrator with no escalation path — one that is expected to resolve all ambiguity, all partial failures, and all unexpected situations autonomously — is a system where the entire accumulated agency of the orchestrated systems operates without a reliable human decision point.

→ Full specification: [The Orchestrator Archetype](archetypes/orchestrator.md)

---

### The Stability of These Five

Why five? And why these five?

The five archetypes are not an arbitrary taxonomy. They represent the stable points in the space of agent system design when you apply the two axes (primary act × discretion scope) consistently. The stability test: every real system we have encountered fits one of these five, or a deliberate composition of them. The cases that don't fit cleanly are either compositions (treated in [Composing Archetypes](05-composing-archetypes.md)) or systems that have drifted across boundaries without a governance event (treated in [Governed Archetype Evolution](06-evolving-archetypes.md)).

The five are also stable under the principle of minimum necessary power: they represent the smallest number of categories that distinguish systems with genuinely different risk profiles, oversight requirements, and design constraints.

The formal argument for exhaustiveness: the two axes — primary act and discretion scope — partition the design space because every agent system must have a primary act (what it does) and a discretion scope (how much latitude it has in doing it). The five archetypes occupy distinct regions in this space: Advisor (inform / narrow), Guardian (enforce / narrow), Executor (execute / bounded), Synthesizer (compose / moderate), and Orchestrator (coordinate / broad). Additional archetypes would either overlap with one of these five (failing the "genuinely different governance" test) or represent compositions of them (treated in [Composing Archetypes](05-composing-archetypes.md)). This is not a claim of mathematical proof — it is a design claim validated against observed systems. If a genuinely new archetype emerges that requires a governance model none of the five can provide, the taxonomy should be extended; that extension would be a significant event in the framework's evolution.

---

## Resulting Context

After applying this pattern:

- **Shared vocabulary reduces miscalibration.** With named archetypes, discussions about what kind of system is being built become precise. Miscalibration — advisors that drift into executor territory — becomes visible because the category is explicit.
- **Governance inherits from category choice.** Once an archetype is selected, the minimum oversight model, risk profile, and authority boundaries follow. Teams do not reinvent governance from scratch for each system.
- **Risk profiles are transparent.** Each archetype carries a canonical risk posture. Teams can reason about whether a particular system matches the risk the organization is accepting, before implementation begins.
- **Composition becomes deliberate.** When multiple archetypes must be combined in one system, the combination is recognized and named as a design decision, rather than emerging accidentally from feature creep.

---

## Therefore

> **There are five canonical intent archetypes — Advisor, Executor, Guardian, Synthesizer, and Orchestrator — each defined by its primary act (inform / execute / enforce / synthesize / orchestrate) and its discretion scope. These are not stylistic categories but governance categories: each carries a different minimum oversight model, a different risk posture, and different design requirements. Selecting the correct archetype before writing any spec is the most consequential design decision in agent system development.**

---

## Connections

**This pattern assumes:**
- [Constitutional Archetypes](01-archetypes-as-constitutional-law.md)

**This pattern enables:**
- [Four Dimensions of Governance](03-archetype-dimensions.md) — formal axes for describing archetype properties
- [The Archetype Selection Tree](04-decision-tree.md) — how to choose
- Individual archetype specifications: [Advisor](archetypes/advisor.md), [Executor](archetypes/executor.md), [Guardian](archetypes/guardian.md), [Synthesizer](archetypes/synthesizer.md), [Orchestrator](archetypes/orchestrator.md)
- [The Intent Archetype Catalog](../repertoires/02-archetype-catalog.md) — the reference implementation of all five

---

*Next: [Four Dimensions of Governance](03-archetype-dimensions.md)*

