# The Intent Design Session

**Working Practice**

---

> *"A discipline you cannot run on a calendar invite is a discipline you do not have. The session is where the framework becomes work."*

---

## Context

You have read Part 1. You understand archetypes, dimensions, failure modes, intent versus implementation. You have seen the canvas in the [Introduction](../introduction.md#the-framework-on-one-page). You know what a spec looks like (Part 2) and roughly which patterns exist (Parts 3–4). What you do not yet have is a *ritual* that puts these pieces together for one specific system you are about to build.

This chapter gives you the ritual.

The **Intent Design Session** is a time-boxed working session — typically 3 to 4 hours, run once per system or once per major spec revision — that walks a team through the four activities of the framework (Frame · Specify · Delegate · Validate) in seven concrete phases. It produces a calibrated archetype commitment, a draft spec, a bound set of patterns, an oversight model, and a rollout plan. By the end of the session, the team has the artifacts it needs to start building. By the next session (the post-launch retrospective), the team has the artifacts it needs to learn.

This pattern is the connective tissue between Part 1 (the decisions) and Part 2 (the spec). It assumes you have read [Pick an Archetype](../architecture/02-canonical-intent-archetypes.md), [Calibrate Agency, Autonomy, Responsibility, Reversibility](03-agency-autonomy-responsibility.md), and [Failure Modes and How to Diagnose Them](05-failure-as-design-signal.md). It produces an artifact you will write up using [The Canonical Spec Template](../sdd/07-canonical-spec-template.md).

---

## The Problem

Without a ritual, a framework's pieces stay disconnected. A team that has read the book does not automatically run a coherent design pass. Five common failure modes recur:

- **Patterns picked by team taste.** Someone on the team likes building MCP servers, so the system gets an MCP layer. Someone else has been reading about RAG, so the system gets retrieval. Neither was driven by what the spec implies. The patterns were picked by enthusiasm, not by intent.
- **Oversight bolted on at the end.** The spec gets written, the agent gets built, and only late in the cycle does someone ask "wait, who reviews the output?" — at which point the answer is whichever model produces the least friction at launch, which is rarely the model the system actually needs.
- **Calibration left implicit.** The team commits to "an Executor" and "high autonomy" without writing down what those mean, what the agency boundary is, where reversibility is irrecoverable, or who carries authorial versus operational responsibility. When the system misbehaves, the post-mortem cannot diagnose which calibration was wrong.
- **Spec written by one person, alone.** The spec is the artifact the agent executes against and humans review against. If only one person was in the room when it was written, only one person's mental model is encoded in it. The first divergence between agent output and intent is usually a difference between that person's tacit assumptions and someone else's — and the gap shows up at runtime, not at review time.
- **No commitment to learning.** Without a planned post-launch retrospective, every spec gap stays a private surprise. Without a record, the same gap recurs in the next system.

The Intent Design Session addresses all five at once. It puts the right people in the room for the right amount of time, walks them through the framework's activities in order, and ends with a written set of artifacts that other people can read.

---

## Forces

- **Time pressure vs. design depth.** Teams will not sit through a multi-day design retreat for every system; they will sit through a focused half-day for a system that matters. Time-boxing is what makes the discipline scalable.
- **Discipline vs. flow.** A rigid script kills the conversation; a script-less session reverts to whoever talks loudest. The session needs phases that constrain *what* gets discussed without scripting *how*.
- **Senior judgment vs. team ownership.** The strongest ideas in a session often come from senior practitioners; the strongest commitment comes from the team that will operate the system. The session has to extract both.
- **Specificity vs. portability.** The artifacts the session produces must be specific enough to drive implementation and portable enough that someone joining the team a quarter later can read them and understand the design.

---

## The Solution

### Who attends

Five roles, all required. Two people may share a role; one person should not hold more than one role unless the system is small enough that a one-person session is honest.

| Role | Responsibility in the session |
|---|---|
| **Spec author** *(must)* | The person who will own the spec after the session. Drives the agenda; writes during phases 4 and 6. |
| **Architect / tech lead** *(must)* | Makes the archetype commitment and the dimensional calibration in phases 2 and 3. Has authority to say "that crosses the archetype's invariant." |
| **Operator** *(must)* | The person who will be on-call when the system runs in production. Makes the oversight-model and metrics commitments in phase 6. Holds the operational responsibility locus. |
| **Domain owner** *(must)* | The person who knows what the system is being built for, in the domain language of the people it serves. Frames the problem in phase 1. Validates the acceptance criteria in phases 4 and 7. |
| **Skeptic** *(should)* | Someone who is *not* on the building team and whose explicit job for the session is to ask "what could go wrong?" Surfaces failure modes in phase 5. Often a security or platform person; sometimes a Cat 7 specialist if the system is computer-use. |

If you cannot fill the five roles, do not run the session — write the spec alone and accept that you have not done the discipline. Calling a single-person spec-write an "Intent Design Session" defeats the purpose.

### What to bring

- **The canvas** ([Introduction](../introduction.md#the-framework-on-one-page)) — printed or projected, used as the running agenda.
- **The archetype catalog** ([Repertoire](../repertoires/02-archetype-catalog.md)) — for phase 2.
- **The canonical spec template** ([Spec Template](../sdd/07-canonical-spec-template.md)) — populated live during phase 4.
- **The pattern index** ([Pattern Index](../appendices/pattern-index.md)) — referenced during phase 5.
- **Any prior post-mortem from a related system** — concrete failures in phase 5 are sharper than imagined ones.
- **Absence of laptops for everyone except the spec author and the architect.** The other roles should be present, not editing.

### The seven phases

The phases follow the canvas top-to-bottom. The time-boxes assume a 3.5-hour session for a medium-scope system. Scale up or down by ±50% for larger or smaller scopes.

#### Phase 1: Frame *(15 min, domain owner leads)*

The domain owner answers the three questions on the canvas's top strip:

1. *What is this system trying to achieve?*
2. *Within what constraints?*
3. *How will we know it is working?*

The output is one paragraph per question, captured by the spec author. No archetype talk yet. No pattern talk yet. No spec writing yet. The phase ends when the team can repeat each question's answer back without looking at notes.

If a team cannot agree on the framing in 15 minutes, stop and reschedule. There is no point continuing — the rest of the session will design a system the team has not yet agreed exists.

#### Phase 2: Categorize *(20 min, architect leads)*

The architect walks the [archetype selection tree](../architecture/04-decision-tree.md) against the framing from phase 1. The team commits to one of the five archetypes. If a *risk override* applies (irreversible state, regulated data, safety-critical control), the team applies it explicitly and records the elevated archetype.

If the system genuinely composes archetypes (an Orchestrator over Executors with a Guardian on the boundary), the team commits to the *primary* archetype and names the composed components. Each composed component will get its own row in the spec; do not collapse them into a single archetype label.

Output: one line in the spec, e.g. *"Archetype: Executor (with Guardian-on-boundary for sensitive-data validation), risk override applied because output triggers external state change."*

#### Phase 3: Calibrate *(20 min, architect + operator co-lead)*

The architect and operator set the four dimensions on the canvas's calibration bar:

- **Agency** — what classes of decision can the system make without consulting a human?
- **Autonomy** — what steps run without per-step approval?
- **Responsibility** — who owns the spec (authorial), who runs each call (operational), who approves the output (validation)?
- **Reversibility** — what is the worst-case state the system can leave behind, and what is the cost to recover?

Each dimension gets a one-sentence answer recorded in the spec's Archetype Declaration section. Disagreement between the architect and the operator at this phase is *productive* — it is the point at which "what we want the system to do" meets "what I will be paged about at 3am." Resolve before moving on.

#### Phase 4: Populate Spec *(45–60 min, spec author leads, all participate)*

The spec author opens the [canonical spec template](../sdd/07-canonical-spec-template.md) and the team walks all twelve sections in order. Most sections take 2–5 minutes; sections §3 (Scope), §6 (Invariants), and §8 (Authorization Boundary) take longer because they encode the calibration from phase 3 into testable clauses.

The spec author writes; everyone else watches and challenges. Do not draft offline and present; the value of this phase is the conversation that produces each clause. A clause no one questioned in the session will be the clause everyone disputes during the first incident.

Output: a draft spec covering all twelve sections, marked Draft. It is not Approved yet — phases 5–7 will surface gaps that send some sections back for revision.

#### Phase 5: Bind Patterns *(45–60 min, skeptic leads, architect + operator participate)*

This is the connective tissue. The team reads the draft spec aloud, clause by clause, and binds patterns to what each clause implies. The skeptic asks "what could go wrong?" at each clause; the team answers with a pattern.

The binding is driven by what the spec *implies*, not by what the team likes. Use the table below as the starting point:

| If the spec says or implies… | Bind these patterns |
|---|---|
| **The agent talks to the outside world** (web, email, customer-facing UI, untrusted document ingest) | [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md) · [Sensitive Data Boundary](../patterns/safety/sensitive-data-boundary.md) · [Output Validation Gate](../patterns/safety/output-validation-gate.md) |
| **The agent takes consequential action** (writes to a database, sends a message, modifies code, calls a paid API) | [Human-in-the-Loop Gate](../patterns/coordination/human-gate.md) · [Output Validation Gate](../patterns/safety/output-validation-gate.md) · [Blast Radius Containment](../patterns/safety/blast-radius-containment.md) · [The Idempotent Tool](../patterns/integration/idempotent-tool.md) |
| **The agent runs long-horizon work** (multi-step plans, multi-day tasks, recursive sub-tasking) | [Checkpoint and Resume](../patterns/state/checkpoint-resume.md) · [Cost Tracking per Spec](../patterns/observability/cost-tracking.md) · [Distributed Trace](../patterns/observability/distributed-trace.md) · [Anomaly Detection Baseline](../patterns/observability/anomaly-baseline.md) |
| **The agent coordinates other agents** (Orchestrator pattern, multi-agent system) | [Agent-to-Agent Contract](../patterns/coordination/agent-contract.md) · [Supervisor Agent](../patterns/coordination/supervisor.md) · [Multi-Agent Integration Test](../patterns/testing/multi-agent-integration.md) · [Agent Registry](../patterns/state/agent-registry.md) |
| **The agent perceives a screen and acts on it** (computer-use, browser-use, GUI automation) | Confirmation gate before high-consequence actions · DOM-grounded element allowlist · Screenshot-then-verify · See [Computer-Use Agents](../agents/09-computer-use-agents.md) for the full Cat 7 pattern set |
| **The agent uses retrieval or domain knowledge** (RAG, skill files, long memory) | [Retrieval-Augmented Generation](../patterns/capability/rag.md) · [Grounding with Verified Sources](../patterns/capability/grounding.md) · [The Skill File](../patterns/capability/skill-file.md) · [Context Window Budget](../patterns/capability/context-budget.md) |
| **The agent writes code** (coding agent, code-gen pipeline) | [Spec Conformance Testing](../patterns/testing/spec-conformance.md) · [Code Execution Sandbox](../patterns/integration/code-sandbox.md) · [The Tool Manifest](../patterns/capability/tool-manifest.md) · scope-locked file-system access · See [Coding Agents](../agents/08-coding-agents.md) |
| **The agent's output is consumed by another agent** (pipeline composition) | [Agent-to-Agent Contract](../patterns/coordination/agent-contract.md) · [Spec Conformance Testing](../patterns/testing/spec-conformance.md) · [Sequential Pipeline](../patterns/coordination/sequential-pipeline.md) |
| **The system runs at >100 calls/day** (production scale, cost-sensitive) | [Cacheable Prompt Architecture](../operating/14-cacheable-prompt-architecture.md) · [Cost Tracking per Spec](../patterns/observability/cost-tracking.md) · [Cost and Latency Engineering](../operating/09-cost-and-latency.md) |
| **The system is being introduced for the first time** (new agent class, new domain) | [Adversarial Input Test](../patterns/testing/adversarial-input.md) · [Red-Team Protocol](../operating/08-red-team-protocol.md) · [Canary Deployment](../patterns/deployment/canary.md) |

The table is not exhaustive — it is a starting set. The skeptic's job is to surface implications the table misses. Every bound pattern goes into the spec's *Implementation Notes* section with a one-line justification ("we bind output-validation-gate because §3 authorizes external state change").

If the team finds itself binding patterns that the spec does not yet imply, that is a signal: either the patterns are unnecessary or the spec is missing a clause. Resolve by amending the spec, not by accepting unjustified patterns.

#### Phase 6: Oversight & Metrics *(20 min, operator leads)*

The operator commits to one of the four oversight models — **Monitoring, Periodic, Output Gate, or Pre-authorized** — proportional to the autonomy and reversibility set in phase 3. The mapping is straightforward: high autonomy + low reversibility forces Output Gate; low autonomy + high reversibility allows Pre-authorized; the middle cases pick Periodic or Monitoring based on the cost of a missed signal.

The operator also commits to the four signal metrics — *spec-gap rate*, *first-pass validation*, *cost per correct outcome*, *oversight load* — and where each is instrumented. The metrics are not optional; a system without them cannot diagnose its own failures.

Output: §11 (Agent Execution Instructions) and the metrics-instrumentation plan in the spec.

#### Phase 7: Stage Rollout *(15 min, all)*

The team commits to a rollout plan: canary scope, success criteria for graduation, rollback trigger, and the date of the post-launch retrospective. The retrospective is non-negotiable; it is the next Intent Design Session for this system, run with the spec gap log open.

Output: §13 (Spec Evolution Log) seeded with the launch entry; §14 (Planned Evolution) seeded with the retrospective date.

### What the session produces

By the end of a properly run session, the team has:

1. A **draft spec** in twelve sections, marked Draft, ready for asynchronous review.
2. A **bound pattern set** justified by spec clauses, recorded as an Implementation Notes section.
3. An **oversight model commitment** with a metrics instrumentation plan.
4. A **rollout plan** with a scheduled retrospective.
5. A **list of open questions** captured during the session that did not block the design — these go into §10 (Assumptions and Open Questions) for follow-up.

The artifacts together are sufficient to start implementation. The spec is not yet Approved — it goes through asynchronous review against the [Intent Review Before Output Review](../operating/05-reviewing-intent.md) discipline before promotion.

### When to break the script

The seven-phase structure is the default. Deviate when:

- **Scope is small** (a one-week pilot, a throwaway prototype). Compress to a 90-minute session: combine Frame + Categorize, combine Calibrate + Populate Spec, keep Bind Patterns and Oversight as full phases. Skip Stage Rollout for true throwaways and document that you skipped it.
- **Stakes are very high** (regulated domain, safety-critical, irreversible at scale). Expand to a two-day session with the skeptic role split into a dedicated security pass and a dedicated domain-expert pass. Schedule a *second* Intent Design Session after the first implementation iteration; do not assume one session is enough for a high-stakes system.
- **The system is a refactor** (rewriting an existing agent that already shipped). Run the session with the existing spec as the starting artifact and the post-mortem log as the skeptic's input. Phase 5's pattern binding is more important than Phase 4's spec drafting in this case.
- **A team member is remote.** Allow it; do not split the session across two timezones. The conversation density that makes the session work depends on everyone being mentally present at the same time.

### Anti-patterns

- **The retrofit session.** Running the session after the system has shipped, "just to document the design we already built." This is not an Intent Design Session — it is a post-mortem disguised as a design session, and it produces a spec that rationalizes existing implementation rather than constraining it. Run a real retrospective instead.
- **The single-person session.** "I ran the IDS by myself last weekend." A session of one is a spec write. Call it that.
- **The hand-wave at Bind Patterns.** Listing pattern names in the spec without binding each to a clause. The pattern list becomes inventory rather than design. The fix: every bound pattern has a one-line justification tied to a specific spec clause; if you can't write the justification, drop the pattern.
- **Skipping the skeptic.** A session that is all builders produces a spec that is all enthusiasm. The skeptic's role is to ask the questions the builders' incentives suppress. If the team lacks an internal skeptic, borrow one from a different team for the session.
- **Recording without writing.** Recording a session you intend to write up later means you will not write it up. Write during the session. The participants leave with the artifact, not with a promise of it.

---

## Resulting Context

After this pattern is in place:

- **Patterns are picked by spec implications, not team taste.** The bound-patterns table makes this explicit: every pattern in the system traces back to a clause that justifies it. Patterns the spec does not justify do not enter.
- **Oversight is calibrated, not bolted on.** The operator owns the oversight commitment in the same session that sets the dimensions, so the oversight model is matched to the autonomy and reversibility from the start.
- **Calibration is written down.** Disagreements about agency or autonomy surface during phase 3 instead of during the first incident, and the resolved values are recorded as spec clauses rather than as tribal knowledge.
- **The spec is a team artifact.** Five people watched each clause get written; five people will recognize the divergence when an agent's output drifts from the clause; the spec gap log gets entries that all five people agree on.
- **Learning is scheduled.** The retrospective is on the calendar before launch. The spec gap log is opened with the launch entry. The next session for this system has a date.

This is what the framework looks like as a working practice. Without the session, the framework is a vocabulary; with it, the framework is a discipline.

---

## Therefore

> **The Intent Design Session is the time-boxed working ritual through which a team applies the Architecture of Intent to one specific system. It runs in seven phases that follow the canvas top-to-bottom — Frame, Categorize, Calibrate, Populate Spec, Bind Patterns, Oversight & Metrics, Stage Rollout — with five required roles in the room, takes 3–4 hours for a medium-scope system, and produces the artifacts (a draft spec, a bound pattern set, an oversight commitment, a rollout plan with a scheduled retrospective) the team needs to start building and to start learning. Run it before every system worth building deliberately; the systems for which the session is genuinely too heavy are also the systems too small to need the framework.**

---

## Connections

**This pattern assumes:**
- [Pick an Archetype](../architecture/02-canonical-intent-archetypes.md) — the categorization vocabulary used in phase 2
- [Calibrate Agency, Autonomy, Responsibility, Reversibility](03-agency-autonomy-responsibility.md) — the calibration dimensions used in phase 3
- [Failure Modes and How to Diagnose Them](05-failure-as-design-signal.md) — the failure taxonomy the skeptic uses in phase 5
- [The Canonical Spec Template](../sdd/07-canonical-spec-template.md) — the spec artifact populated in phase 4

**This pattern enables:**
- [Spec-Driven Development](../sdd/01-what-sdd-means.md) — the SDD operating model has the IDS as its origin ritual
- [Intent Review Before Output Review](../operating/05-reviewing-intent.md) — the post-session asynchronous review discipline
- [Four Signal Metrics](../operating/06-metrics.md) — the metrics committed during phase 6
- [Adoption Playbook](../operating/11-adoption-playbook.md) — running the IDS is the first concrete practice a new team adopts

**This pattern is calibrated by:**
- The canvas in the [Introduction](../introduction.md#the-framework-on-one-page) — used as the running agenda

---
