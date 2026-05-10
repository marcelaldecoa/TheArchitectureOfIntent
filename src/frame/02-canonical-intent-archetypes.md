# Pick an Archetype

**Part 1 — Frame**

---

> *"You do not invent your relationship to power every time you wield it. You inherit a form — or you build one deliberately. The archetypes are the forms built deliberately."*

---

## Context

A team in a Frame session, 30 minutes in. The whiteboard has the system's three questions answered. The product manager is impatient — they want to start naming features. The tech lead writes one word at the top of the board: **ARCHETYPE**. *"We pick this first. Everything else writes itself once we commit."* The product manager pushes back: *"can't we just start specifying and figure out the shape as we go?"* The tech lead's answer is no. Picking the shape *after* the spec means the spec was written against an implicit shape that the team never agreed on, which is the most-common source of the *"this system grew into something we didn't intend"* failure pattern.

This is the first decision of the pilot. Before any spec is written, before any agent is configured, before any tool is wired up — you commit to a category for the system you're about to build.

The category is the archetype. There are five canonical archetypes — Advisor, Executor, Guardian, Synthesizer, Orchestrator — and the rest of the book follows from which one you pick.

Detailed per-archetype specifications live in the [Archetype Catalog](../repertoires/02-archetype-catalog.md) and the individual archetype pages linked at the end of each section.

---

## What an archetype is

An archetype is a **pre-committed behavioral frame** for a class of system. It is not a template you fill in. It is not a best practice you can ignore. It's a category you operate within.

An archetype defines five things:

1. **Identity** — what kind of system this is at the categorical level (Advisor / Executor / Guardian / Synthesizer / Orchestrator).
2. **Agency Level** — the range of discretion the system is authorized to exercise. What classes of decision can it make autonomously?
3. **Oversight Model** — how human oversight is required to function. Not "some oversight" but: *what kind, at what frequency, triggered by what conditions, performed by whom?*
4. **Reversibility Posture** — what is the reversibility profile of this system's actions, and what design requirements follow? A system with irreversible action potential has a different minimum design standard than one without.
5. **Invariants** — the constraints that cannot be violated under any implementation of this archetype. These are the boundaries between *"still this kind of system"* and *"something that has crossed into a different category."*

### Why archetype before spec

Archetypes and specs are different artifacts with different owners and different lifetimes:

|  | Archetype | Spec |
|---|---|---|
| **Defines** | The category of system | The behavior of this system |
| **Owner** | Architects / platform team | Engineers / product team |
| **Lifetime** | Stable; changes rarely, deliberately | Living; evolves with the system |
| **Scope** | Applies to all systems of this class | Applies to one system |
| **Authority** | Cannot be overridden by individual spec | Operates within archetype bounds |

A spec that attempts to authorize behavior that violates the governing archetype is invalid. The archetype represents decisions made by those with the authority to make them. The spec operates within that frame.

In practice, this means archetype selection is the *first* decision in any spec development process — before any behavioral specification is written. Getting the category right is more important than getting any specific behavior right, because all specific behaviors must remain consistent with the category.

### A note on enforcement

The archetype is enforced through organizational discipline — spec review, governance cadence, authority matrices — not through technical mechanisms that prevent violations at runtime. An agent system can technically take actions outside its declared archetype; nothing in the runtime stops it. The enforcement is procedural and social. This is the same model by which most organizational governance operates, and it works only as well as the review and oversight practices around it. [Proportional Governance](../evolve/04-governance.md) and [Intent Review Before Output Review](../validate/05-reviewing-intent.md) are how that enforcement becomes operational.

---

## The Problem

Agent systems vary enormously along multiple dimensions: how much they act vs. advise, how much discretion they exercise, how often humans review their outputs, how reversible their actions are. Without a shared vocabulary for these variations, every system is designed from scratch — with no inherited wisdom about which design decisions are consequential and which are flexible.

The result is systems that are miscalibrated: advisors that gradually acquire executor behaviors, executors deployed without adequate oversight, guardians that are actually orchestrators in disguise. The miscalibration is not always intentional — often it is the product of incremental feature additions, each of which seemed reasonable in isolation.

The five archetypes solve this by naming five recurring forms that have so far covered most production agent systems we have classified — categories that emerge from principled reasoning about agency, authority, and consequence. Most systems fit one of these forms; the rest are deliberate compositions. The taxonomy is held provisionally, not settled (see "A working taxonomy, not a settled one" later in this chapter).

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

### A working taxonomy, not a settled one

Why five? And why these five?

The five archetypes are not arbitrary. They are the regions of design space that emerge from applying two axes — *primary act* and *discretion scope* — consistently, and they are *currently sufficient* for most production agent systems we have encountered. Every system we have classified fits one of the five, or a deliberate composition of them.

But "currently sufficient" is the right honest claim. This is a working taxonomy — held provisionally, tested against new systems, and extended when extension is genuinely warranted. It is not a settled categorization of agency types and shouldn't be read as one.

**Where the taxonomy is under most pressure.** Three classes of system, all increasingly common as of 2026, do not fit any *single* archetype:

- **Coding agents** (Cursor, Cline, Devin, Claude Code, Codex CLI). Within one session they synthesize structured artifacts (Synthesizer), execute against repositories (Executor), and increasingly orchestrate sub-tasks across files and tools (Orchestrator). The system moves between modes within a single session.
- **Deep-research agents** (long-horizon research with self-directed planning). They synthesize a final report and orchestrate sub-research recursively. The decision tree puts them in Orchestrator; the spec template fits them awkwardly because their sub-agents are often instances of themselves.
- **Self-improving / training agents** (whose primary act is to evaluate or fine-tune *another* agent's behavior). The honest reading is that the deployment is two systems with a clean handoff — a meta-system (Synthesizer over the inner agent's outputs) and an inner agent — rather than one system with a missing archetype.

**Composition is the answer, not a workaround.** Each of these classes pressures the five-archetype frame to extend. The framework's commitment is the opposite: composition is a **first-class design surface** in this book — one governing archetype, embedded components or modes, declared transitions, cross-mode invariants. The chapter on [Composing Archetypes](05-composing-archetypes.md) develops the structural surface in full, including a *Composition Declaration* sub-template fragment for §4 of the canonical spec, and a mode-switching pattern that handles the three pressure-point classes above directly.

**Why we do not propose a sixth archetype.** Adding a sixth would have to name a *primary act* that is not *inform*, *execute*, *enforce*, *synthesize*, or *orchestrate*. Coding agents and deep-research agents do not have a sixth primary act — they have several of the existing five, used in sequence within a session. Naming the absence of a primary act ("operates in multiple modes") would not give a new archetype any governance profile of its own; it would merely re-name composition while losing the structural clarity of declared transitions and cross-mode invariants. Self-improving agents are honestly two-system deployments, not one-system compositions; documenting them as two systems with a clean handoff is the right move.

**The bar for actually adding a sixth.** The framework remains open to extension. A genuine sixth archetype must demonstrate a *governance profile* — agency level, oversight model, reversibility posture, invariant set — that no composition of the existing five provides. Use the [Governed Archetype Evolution](06-evolving-archetypes.md) process. As of 2026, no class of system has met that bar; composition does the work cleanly.

Treat the five as a vocabulary that has earned its keep, not as a taxonomic claim about all possible agents. Treat composition as the structural surface that absorbs the pressure. The book is more useful that way, and so is the framework.

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
- [Prologue](../prologue.md) — what's at stake when delegating power to agents

**This pattern enables:**
- [Calibrate Agency, Autonomy, Responsibility, Reversibility](../foundations/03-agency-autonomy-responsibility.md) — tune the four dials within the archetype's defaults
- [Four Dimensions of Governance](03-archetype-dimensions.md) — formal axes for describing archetype properties
- [The Archetype Selection Tree](04-decision-tree.md) — how to choose when the answer isn't obvious
- Individual archetype specifications: [Advisor](archetypes/advisor.md), [Executor](archetypes/executor.md), [Guardian](archetypes/guardian.md), [Synthesizer](archetypes/synthesizer.md), [Orchestrator](archetypes/orchestrator.md)
- [The Intent Archetype Catalog](../repertoires/02-archetype-catalog.md) — the reference implementation of all five

---
