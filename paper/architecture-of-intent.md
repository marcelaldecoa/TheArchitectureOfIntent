# The Architecture of Intent: A Framework for Designing Delegated Systems

**Marcel Aldecoa**
*Independent practitioner*

**Status:** Skeleton draft (v0.1). Position/framework paper, ~12–15 pages target. Companion artifact to the book of the same title.

**Target venue:** arXiv (cs.SE / cs.AI cross-listing). Workshop or journal submission to be decided after first arXiv version is released.

---

## Abstract *(target ~200 words; below is the skeleton draft)*

Software systems, organizations, and increasingly AI agent systems share a common structural problem: humans must express intent precisely enough that a non-human actor — code, an automated pipeline, an organization, an LLM agent — can execute it without supervisory rescue. We present *The Architecture of Intent*, a framework for designing delegated systems by treating **intent as a primary design artifact distinct from implementation**. The framework has four load-bearing elements: (i) **archetypes**, five canonical pre-commitments to delegation shape (Advisor, Executor, Guardian, Synthesizer, Orchestrator); (ii) four **orthogonal calibration dimensions** (agency, autonomy, responsibility, reversibility) that make Shavit & Agarwal's [@shavitAgarwal2023] operational variables explicit and separable; (iii) a **fix-locus failure taxonomy** (Cat 1–7) that complements Cemri et al.'s [@cemriMAST2025] empirical multi-agent failure partition (MAST) by indicating *which artifact must change* in response to a failure; and (iv) **Spec-Driven Development** [@githubSpecKit2024] as the protocol for expressing intent precisely enough to be executable and verifiable. We instantiate the framework against AI agent systems and demonstrate composition with Microsoft's DevSquad Copilot eight-phase agentic development lifecycle [@microsoftDevSquadCopilot2024]. The framework introduces one new failure category — Cat 7 (Perceptual Failure) — for perceiving-then-acting systems that prior taxonomies do not address. We frame and qualify the contribution as a position-and-framework paper without empirical validation at scale.

**Keywords:** intent engineering, agentic development lifecycle, spec-driven development, agent governance, multi-agent systems, AI safety, software architecture.

---

## 1. Introduction

### 1.1 The rising delegation curve

Software has always been a delegation. The programmer delegates a computation to a machine; the team delegates production behavior to the codebase; the organization delegates routine decisions to the systems it has built. What changes in 2024–2026 is the *width* of the delegation: a single human action — writing a brief specification, opening a ticket, asking a question — is increasingly enough to commit a system to a long sequence of consequential decisions made by an executor that is not human and that does not, in any operationally useful sense, ask for clarification before acting.

Three forms of delegation now coexist with rising authority. Procedural delegation, in which an organization codifies a decision into policy that humans execute, is the oldest. Mechanical delegation, in which deterministic code or controllers execute a fixed program against a defined input domain, is the standard form of software since the 1950s. Agentic delegation, in which an LLM-driven system makes judgment-laden choices over a domain wider than the spec author can enumerate, is the newest and the one whose behavior most departs from the prior two. SAE J3016 [@saeJ30162021] formalized graduated delegation for driving automation in 2021, identifying six levels at which a vehicle may handle perception, decision, and action without a human between them; the framing transfers to software systems with one important difference. A vehicle's delegation level is constrained by physics — perception must precede action by milliseconds; intervention windows are short; reversibility approaches zero — and the levels move together. A software system's delegation has no such constraint, and the design space is correspondingly larger and easier to misconfigure.

The cost of imprecise intent in each delegation form has been historically absorbed by human implementers. A poorly written policy was repaired in real time by the operator who knew what was meant. A poorly written spec was repaired by the engineer who had built the previous one. The repair was invisible: it produced a working system whose specification was never quite the artifact that governed its behavior, but that mismatch did not surface as a failure because the human implementer was the bridge. This paper's working hypothesis is that the bridge is now automating, and the cost of imprecise intent — until recently a hidden subsidy paid by professional judgment — is becoming an explicit cost paid in agent rework, scope drift, and post-incident churn. The framework that follows is offered as the structural response: design intent as a primary artifact rather than as the implicit ground of implementation.

### 1.2 Two motivating observations

The framework rests on two observations that have been remarked on individually in practitioner literature [@anthropicBuildingEffectiveAgents2024; @shavitAgarwal2023] but that we treat together because they form the gap the framework addresses.

**Observation 1: Human professionals tolerated imprecise intent because they exercised silent judgment to bridge it.** Every senior engineer reading an underspecified ticket has, at some point, supplied missing constraints from experience ("we never delete records that are linked to invoices, so I'll add a check"), escalated ambiguity rather than executing it ("does 'process all orders' include cancelled ones? I'll ask before coding"), and rewritten what was asked into what was clearly meant ("the ticket says 'fix the bug' but the actual fix is a refactor"). None of this judgment was visible to the specification document, which retained its under-specified form because the implementer absorbed the gap. None of it transfers to an automated executor that interprets the document literally. The judgment is real engineering work; it has always been; it has merely been hidden in implementation rather than codified in specification.

**Observation 2: Automated executors make imprecise intent immediately visible as wrong outputs.** Where a senior engineer would have surfaced an ambiguity, an LLM agent will resolve it probabilistically against the latent distribution of similar cases in its training data. The resolution is rarely the one the spec author wanted, but it is rarely random; it is the *most-probable* resolution given the prompt's surface features, which is a stable phenomenon and therefore a debuggable one. The failure mode is not "the agent is broken"; the failure mode is "the agent is doing exactly what the spec said, and the spec was wrong." The cost per call is small — a slightly off-target output, a near-miss at the constraint boundary — but the cost compounds across a deployment, and the post-incident reconstruction is hard precisely because no single call was visibly wrong.

These two observations together produce the framework's central claim: the gap between intent and implementation has not grown; it has merely become *visible*. Spec authors in 2026 are paying explicit costs for what spec authors in 2006 paid implicit costs for. The discipline the framework proposes — naming intent as a designed artifact, shaping it via archetypes, calibrating it along orthogonal dimensions, diagnosing its failures via fix-locus categories, expressing it through Spec-Driven Development — is the discipline that makes the intent layer thick enough to be governable when the implementation layer is automated.

### 1.3 Contribution

This paper contributes a framework for designing delegated systems by treating intent as a primary design artifact distinct from implementation. The framework has four load-bearing elements (introduced in §3, instantiated against AI agent systems in §4): (i) a five-archetype taxonomy committing the system to a delegation shape before design begins; (ii) a four-dimension calibration of agency, autonomy, responsibility, and reversibility, with an explicit *orthogonality argument* extending Shavit & Agarwal's [@shavitAgarwal2023] operational variables; (iii) a *fix-locus* failure taxonomy of seven categories partitioning failures by the artifact whose modification prevents recurrence, and complementing Cemri et al.'s [@cemriMAST2025] empirical multi-agent symptom partition (MAST); and (iv) Spec-Driven Development [@githubSpecKit2024] as the executable protocol layer. The framework's primary worked instance is AI agent systems, and §4 demonstrates clean composition with Microsoft DevSquad Copilot's eight-phase agentic development lifecycle [@microsoftDevSquadCopilot2024].

The paper's *novel* contributions, narrowly framed, are three: the operationalization of autonomy and agency as orthogonal axes (§3.3); the fix-locus framing of the failure taxonomy (§3.4); and **Cat 7 (Perceptual Failure)** as a new category for *perceiving-then-acting systems* (computer-use agents, browser-use agents, robotic systems) that prior taxonomies do not cover, with four sub-categories (misidentification, missed element, hallucinated element, state miscount) and structural fixes for each. The paper does *not* claim novelty for SDD as a discipline (lineage from spec-kit and DevSquad), for archetypes as a concept (lineage from Anthropic's *Building Effective Agents* [@anthropicBuildingEffectiveAgents2024]), for the four dimensions individually (lineage from SAE J3016 and Shavit & Agarwal), or for Cat 1–6 as categories (synthesis from common practice). The synthesis itself is the larger contribution: the four elements bind into a framework with consistent vocabulary that practitioners can apply in design conversations, in spec reviews, and in post-incident diagnosis.

We position this paper as a *position-and-framework paper* without empirical validation at scale. The framework has been applied across the three worked examples in the companion book [@aldecoaArchitectureIntent2026] and in deployments those examples are abstracted from, but quantitative validation across many independent deployments remains future work. §6 enumerates this and the framework's other limitations explicitly.

### 1.4 Paper structure

§2 situates the framework against eight bodies of prior work. §3 develops the framework: intent as a design surface (§3.1), the five archetypes (§3.2), the four-dimension calibration (§3.3), the seven-category fix-locus failure taxonomy (§3.4), and Spec-Driven Development as the protocol (§3.5). §4 instantiates the framework against AI agent systems and the agentic development lifecycle exemplified by DevSquad Copilot, with worked subsections for capability boundaries via the Model Context Protocol, coding agents, and computer-use agents. §5 discusses the framework's applicability boundary, its complementarity with MAST and other multi-agent failure work, and its generalization beyond AI agents. §6 names the framework's limitations honestly. §7 concludes. Appendix A maps each section back to the relevant chapter of the companion book.

---

## 2. Prior work and lineage

> *Section purpose: position the framework against the standing literature it builds on. The honest accounting belongs in this section. We organize the lineage by domain.*

### 2.1 Spec-Driven Development

> *Stub paragraph.* GitHub spec-kit [@githubSpecKit2024] operationalizes spec-first development against AI assistants. Microsoft DevSquad Copilot [@microsoftDevSquadCopilot2024] integrates spec-driven development into an eight-phase iterative cycle for agentic development. Our framework's "Spec-Driven Development" element is direct lineage from these projects, not a new invention; the contribution is positioning SDD as the protocol layer that supports the archetype and dimension layers above it.

### 2.2 Driving automation and graduated delegation

> *Stub paragraph.* SAE J3016 [@saeJ30162021] defines six levels of driving automation as a graduated handoff of operational responsibility from human to system. The structure (operational responsibility shifts as automation widens) is a precedent for the four-dimensions calibration we propose. We draw the *delegation ladder* metaphor explicitly from SAE J3016 and acknowledge the prior work; the contribution is generalizing the ladder to non-driving delegated systems and decomposing the single "automation level" into four orthogonal axes.

### 2.3 Agent governance

> *Stub paragraph.* Shavit & Agarwal et al. [@shavitAgarwal2023] define seven operational variables for governing agentic AI systems: ability, agency, agency type, autonomy, alignment, accountability, and authority. Our four-dimensions framework is a refactoring of a subset of those variables into explicit, separable axes with explicit cross-cutting operationalization. We do not claim novelty for the dimensions individually; we claim novelty for the orthogonality argument and its operationalization in spec design.

### 2.4 Agent design

> *Stub paragraph.* Anthropic's *Building Effective Agents* [@anthropicBuildingEffectiveAgents2024] catalogues practical agent shapes: prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer, autonomous agents. The five archetypes we propose are an opinionated synthesis of these shapes into a smaller, more decision-ready taxonomy. The synthesis is the contribution; the underlying patterns are inherited.

### 2.5 Multi-agent failure analysis

> *Stub paragraph.* Cemri et al. [@cemriMAST2025] propose MAST, a Multi-Agent System failure Taxonomy with 14 empirical failure categories observed across 200+ deployments. MAST partitions failures by *symptom and locus of observation*. Our Cat 1–7 taxonomy partitions failures by *fix locus* — which artifact must change to prevent recurrence. The two are complementary, not competing: MAST tells you what failed; Cat 1–7 tells you who owns the fix. Zhang et al. [@zhangHallucinationSurvey2025] provide finer partition of model-level (Cat 6) failure, which we cite without re-deriving.

### 2.6 Pattern languages and software architecture

> *Stub paragraph.* Alexander, Ishikawa, & Silverstein [@alexanderPatternLanguage1977] establish the pattern-language form: structured catalogues of context-problem-solution-resulting-context entries that compose. We borrow the form for the framework's archetype catalogue but explicitly do not claim to be a pattern language in Alexander's sense — the test for that label requires more empirical pattern derivation than this paper offers. Brooks [@brooksMythicalManMonth1975], Meyer [@meyerDesignByContract1992], and Jackson [@jacksonRequirements1995] anchor the broader software-engineering tradition we extend.

### 2.7 Systems thinking

> *Stub paragraph.* Meadows [@meadowsThinkingInSystems2008] and Reason [@reasonHumanError1990] provide the broader systems-thinking and human-error frame. Reason's distinction between active failures and latent conditions parallels our distinction between Cat 6 (Model-level, active) and Cat 1 (Spec, latent). The connection is acknowledged; we do not attempt a thorough re-derivation.

### 2.8 Inference economics and prompt architecture

> *Stub paragraph.* Pope et al. [@popeInferenceScaling2022] ground the inference-cost economics that prompt caching exposes to API consumers. Liu et al. [@liuLostInTheMiddle2023] document long-context attention degradation ("Lost in the Middle") that motivates the context-budget patterns the framework recommends. These works are referenced for the application section, not the framework section.

---

## 3. The framework

### 3.1 Intent as a design surface

We define **intent** as the human-authored description of what a delegated system should do, the constraints it must respect, and the conditions that distinguish acceptable from unacceptable outcomes. Intent is a designed artifact, separate from three things it is commonly conflated with: implementation, requirements, and policy.

**Intent versus implementation.** Implementation is what the executor produces — code, an action, a refactored document. Intent is what the executor was supposed to produce. The distinction is foundational and chronically collapsed in practice [@brooksMythicalManMonth1975]. Software-engineering literature has named the collapse for decades — Brooks's distinction between *essential* and *accidental* complexity, Jackson's separation of *requirements problem* from *machine* [@jacksonRequirements1995], Meyer's contract-first discipline [@meyerDesignByContract1992] — but the collapse has been tolerable because human implementers absorbed the gap silently. A senior engineer reading a one-line ticket supplied missing constraints from experience, escalated ambiguity rather than executing it, and rewrote what was asked into what was clearly meant. None of that judgment was visible in the specification document, and none of it transfers to an automated executor. When code becomes the executor, the gap between intent and implementation shows up as bugs; when an LLM agent becomes the executor, the gap shows up as outputs that are syntactically reasonable, individually defensible, and collectively wrong.

**Intent versus requirements.** Requirements describe what stakeholders ask for. Intent is what the system author decides to build. The two diverge whenever the request is incomplete (most cases), contradictory (common), or wrong (occasional). A traditional requirements document captures the request; an intent specification captures the synthesized design decision after the request has been interrogated, prioritized, and reduced to a coherent set of behaviors and constraints. The distinction matters because requirements churn and intent must not. A spec that re-litigates requirements every time a stakeholder changes their mind cannot be the control surface an agent executes against; a spec that resists requirement churn by holding the design decision constant is what the framework calls intent.

**Intent versus policy.** Policy is organizational or regulatory — what the company, the law, or the ethics review board requires across all systems. Intent is system-specific. Policy and intent compose: policy provides cross-cutting constraints that every spec inherits; intent provides the per-system behavior the spec describes within those constraints. Conflating the two produces specifications that treat compliance as a feature (causing compliance to drift with system priorities) or treat behavior as compliance (causing organizations to over-formalize routine engineering decisions). The framework holds them apart: policy belongs in a constitutional layer above the spec; intent belongs in the spec.

**Intent as the locus of design.** Once these three distinctions are in place, intent is no longer an implicit shadow of requirements or a soft-touch precursor to code. Intent is the artifact the system author actually designs. The five-archetype framework (§3.2) provides shape; the four-dimension calibration (§3.3) provides axes; the failure taxonomy (§3.4) tells the author where to look when execution diverges from intent; Spec-Driven Development (§3.5) is the protocol that makes intent executable and verifiable. Each subsequent section operates on the assumption that intent is something deliberately authored, not something inferred after the fact.

**Why this matters now.** Three observations make the design-surface framing acute in 2026 in a way it was not in 1995. First, the executor is increasingly an LLM agent rather than a deterministic compiler, and an LLM agent will resolve ambiguity probabilistically rather than escalating it. Second, the rate of delegation is faster: an agent loop completes a sequence of decisions in seconds where a human team would have completed it in days, with the consequence that the cost of imprecise intent is amortized across more decisions per unit time. Third, the locus of design effort has shifted: a software engineer spending an hour on a tightly-bounded spec produces work that an agent loop can extend into hundreds of correct outputs; the same hour spent on the implementation directly produces a single output. The leverage on intent has gone up because the executor's throughput has gone up. The collapse of intent into implementation that human professionals absorbed for decades is no longer free.

The rest of this section operates on intent as a designed artifact. Section 3.2 names five canonical shapes that intent takes; section 3.3 names four dimensions that calibrate it; section 3.4 names seven categories of failure that diagnose where intent broke; section 3.5 names the protocol that makes intent executable.

### 3.2 Archetypes

We propose five canonical archetypes — *Advisor*, *Executor*, *Guardian*, *Synthesizer*, *Orchestrator* — as the smallest decision-ready taxonomy that covers the delegation shapes practitioners actually deploy. Each archetype is a pre-commitment to a behavioral envelope: a posture toward action, a relationship to oversight, a default risk profile, and a set of invariants that follow from the shape. Choosing the archetype is the first design decision an intent author makes, and it constrains every subsequent decision.

**The five archetypes are summarized below.**

| Archetype | Core function | Agency level | Risk posture | Default oversight |
|---|---|---|---|---|
| **Advisor** | Surface information, options, recommendations; never act on the world | Minimal | Low | Human decides and acts |
| **Executor** | Carry out well-defined tasks autonomously within strict bounds | High | Medium | Pre-approved scope; exception-based escalation |
| **Guardian** | Enforce rules, validate integrity, block constraint violations | Low (veto only) | Low | Alerts; humans resolve |
| **Synthesizer** | Aggregate, distill, or compose from multiple sources into a coherent artifact | Moderate | Medium | Output review above threshold |
| **Orchestrator** | Coordinate multiple agents or services toward a compound goal | High | High | Active oversight; escalation paths required |

**The selection tree.** Figure 1 resolves archetype selection in four sequential questions, applied in order, stopping at the first match. The questions are asked in increasing decision difficulty: the first concerns externally observable behavior (does the system act on the world without a human between its output and the consequence?); the second concerns purpose (is the primary function protective rather than productive?); the third concerns relationship to other systems (does the work involve coordinating other agents?); the fourth concerns output shape (is the primary product a synthesized artifact?). The default after all four questions is *Executor*, which captures most well-bounded autonomous-action systems.

A *risk override* sits above the tree's output. If the system's actions touch high-consequence domains (irreversible state changes, regulated data, safety-critical control), the assigned archetype is elevated to the next-most-restrictive in the path *Advisor < Guardian < Synthesizer < Executor < Orchestrator*. The override mechanism encodes the principle that the cost of misclassification is asymmetric: classifying an Executor as an Advisor produces an under-deployed system; classifying an Advisor as an Executor produces a deployment that exceeds its authorization. The override defaults to the conservative direction.

**Composition.** A single deployment frequently hosts more than one archetype. An Orchestrator coordinating Executors, with a Guardian validating each Executor's output before downstream effects, is a common shape in production agent systems. The framework treats composition as the rule, not the exception: each archetype is a per-component classification, not a per-deployment one. Composition's main constraint is that Guardian archetypes — which are protective rather than productive — must sit on the boundary of every productive archetype's effect surface, not in series after it. A Guardian downstream of an Executor's irreversible action is a check that runs after the damage; a Guardian gating the Executor's action is a check that runs before.

**Pre-commitment, not classification.** A practical implication of the archetype framing is that archetype is *committed before* design rather than *inferred after*. A spec author who sits down to design a customer-support system does not write the spec and then ask "is this an Advisor or an Executor?" — that conflates intent with implementation in the way §3.1 forbade. They commit to the archetype first (informed by Figure 1 and the risk override), then design the system within its envelope. The pre-commitment makes downstream design decisions traceable: oversight model is determined by archetype; capability boundary is determined by archetype; invariants follow from archetype. When a deployment exhibits incoherent oversight ("the agent is allowed to do X but the team reviews every output anyway"), the diagnosis is almost always that the archetype was committed implicitly rather than explicitly, and downstream choices were made against a different shape than the one declared.

**Relation to prior work.** The five archetypes are an opinionated synthesis, not an original taxonomy. Anthropic's *Building Effective Agents* [@anthropicBuildingEffectiveAgents2024] catalogues practical agent shapes — prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer, autonomous agents — that overlap with our five along multiple cuts. A routing pattern is what we call an Orchestrator's first decision; an evaluator-optimizer pattern is a Guardian composed with an Executor; an orchestrator-workers pattern is what we call Orchestrator-over-Executors. The contribution is not that these shapes are new; it is that they are reduced to a smaller set of decision-ready categories, each with a defined oversight default and risk posture, indexed by a four-question decision tree. Practitioners report — in a way the present paper cannot empirically verify — that the smaller, opinionated taxonomy is easier to commit to in design conversations than the larger catalogue is.

**Why five.** The five-cardinality choice is a working decision rather than a derived one. Three would force a coarser commitment than the design space supports (Advisor and Executor would have to absorb Synthesizer's distinct shape; Guardian would have to absorb Executor's). Seven or nine would re-fragment the categories that the five-cardinality holds together. The framework offers five as an opinionated default; practitioners are free to refine the catalogue per their domain. What the framework does not permit is operating without an archetype commitment at all.

**Figure 1** (below) is the working version of the selection tree. It is meant to be used in design sessions, in spec reviews, and in onboarding new engineers to the framework — not to be read once and remembered.

![**Figure 1.** The archetype selection tree. Apply questions in order; stop at the first match. The risk-override sidebar elevates the assigned archetype when the system's actions touch high-consequence domains. Composition is permitted: a single deployment may host multiple archetypes.](figures/archetype-decision-tree.svg){#fig:archetype-tree width=85%}

### 3.3 Four dimensions of calibration

The archetype framing of §3.2 commits a system to a delegation shape. The four-dimension calibration framing of this subsection commits the system, *within that shape*, to specific levels of independence, judgment latitude, accountability locus, and recoverability. The four dimensions are **agency**, **autonomy**, **responsibility**, and **reversibility**. The central claim of this subsection is that these four are *orthogonal* — independent in principle and in practice — and that collapsing them into a single "automation level," as SAE J3016 [@saeJ30162021] does for driving, loses design space that practitioners need.

**Agency.** The capacity to choose actions in pursuit of a goal. Wider agency means more decisions the system makes without consulting a supervisor. A code-review Advisor exercises narrow agency: it produces recommendations, and the choice of which recommendations to act on belongs to the human reviewer. An autonomous coding agent like Devin exercises wide agency: it chooses what to refactor, in what order, and against which tests, without consulting the human between decisions. Agency is a property of the system's *decision space* — what the system is permitted to choose.

**Autonomy.** Operational independence from per-step human authorization. Wider autonomy means more operations execute without an approval gate between the system's decision and its effect. A deterministic CI/CD pipeline exercises wide autonomy: every step runs without a human approval. A compliance-review system that surfaces every potential violation for human resolution exercises narrow autonomy: every operation gates on a human. Autonomy is a property of the system's *execution path* — what the system is permitted to execute without supervisory approval at the step level.

**Responsibility.** The locus of accountability for outcomes. Distinct from agency (decision space) and autonomy (execution path), responsibility names *who is on the hook* when things go wrong. The framework distinguishes three sub-loci: *authorial* (who specified the system), *operational* (who is executing it on this run), and *validation* (who validated that this run's output should be accepted). In well-designed systems all three are explicit; in poorly-designed systems responsibility is diffuse, which is the underlying condition that produces both Cat 4 (Oversight) failures and the post-incident finger-pointing that diffuse responsibility enables.

**Reversibility.** The capacity to undo or recover from an incorrect action. Reversibility is a property of the *system's environment and tooling*, not of the system's intent. Soft deletes, draft queues, audit logs that support replay, undo buffers, and approval gates are reversibility-extending mechanisms. Sending an email, processing a payment, deleting a record without an audit trail, and most physical-world actions are reversibility-collapsing. A spec author who treats reversibility as a fixed environmental property is missing a lever; a spec author who recognizes that reversibility can be *designed* — by routing irreversible actions through a draft-and-confirm pattern, by adding a reversal endpoint to a state-changing API, or by adding an approval gate before high-consequence operations — has more dimensions to calibrate.

**The orthogonality argument.** These four dimensions are independent. Figure 2 plots two of the four (Agency × Autonomy) against each other and shows that all four quadrants contain real deployments — meaning the dimensions are not dependent variables that cluster along a diagonal. A system can have wide agency but narrow autonomy: a compliance Guardian with explicit gates exercises high decision latitude per call (it judges whether a transaction is suspicious) but every call surfaces for human approval (no per-step automation). A system can have narrow agency but wide autonomy: a deterministic CI/CD pipeline exercises no judgment per step (the steps are fully prescribed) but executes the entire sequence without per-step approval (no gates). The other two pairs are similarly orthogonal: a system with wide responsibility (clear authorial ownership) and narrow reversibility (every action is permanent) is a high-stakes Executor; a system with diffuse responsibility (no clear owner) and wide reversibility (everything is a draft) is what most undisciplined agent prototypes converge to.

![**Figure 2.** Two of the four calibration dimensions plotted against each other. Each quadrant has real deployments; no quadrant is empty. The other two dimensions (Responsibility, Reversibility) are similarly orthogonal. Treating Agency and Autonomy as a single "automation level" — as SAE J3016 does for driving [@saeJ30162021] — collapses this design space onto a diagonal.](figures/four-dimensions-orthogonality.svg){#fig:orthogonality width=85%}

**Why the orthogonality matters in practice.** When the four dimensions are treated as a single "automation level," spec authors have one lever to pull. The lever has six positions in the SAE J3016 case [@saeJ30162021] and seven operational variables in Shavit & Agarwal [@shavitAgarwal2023]; in either case, the positions are correlated. Pulling the lever toward more automation moves all aspects of the system together — more decisions, fewer gates, more diffuse accountability, less recoverability. This is fine for driving automation, where the underlying physics constrains the dimensions to move together (a vehicle that exercises wide agency needs wide autonomy because human reaction time cannot insert itself between perception and steering); it is wrong for software-system design, where the dimensions are independently controllable and the design space is much larger than a single ladder permits. The framework's contribution at this layer is the *operationalization of the orthogonality*, not the discovery of the dimensions individually — Shavit & Agarwal's seven variables already covered the conceptual ground.

**Mapping to spec clauses.** Each dimension maps to specific clauses in a Spec-Driven Development specification. Agency maps to *§3 (Authorized Scope)* and *§4 (NOT-Authorized Scope)* — the spec clauses that bound the agent's decision space. Autonomy maps to *§4 (Oversight Model)* — the clauses that declare which steps gate on human approval and which run automatically. Responsibility maps to *§1 (Owner)* and *§12 (Validation Checklist)* — the clauses that assign authorial, operational, and validation accountability explicitly. Reversibility maps to *§7 (Tool Manifest)* and *§8 (Authorization Boundary)* — the clauses that distinguish reversible from irreversible tool effects and constrain the latter behind explicit gates. The mapping is not novel to this paper; what the framework adds is the *insistence* that all four mappings be present in every spec, with explicit values, rather than left implicit.

**A worked configuration: a low-agency Guardian.** The compliance Guardian on a financial-transactions platform: agency is *narrow* (the system's decision space is a single classification — flag or pass); autonomy is *narrow* (every flag surfaces for human resolution); responsibility is *clear* (compliance officer authors the spec, the operations team executes, the same compliance officer validates each flag); reversibility is *high* (a flagged-but-not-yet-confirmed transaction is reversible by definition; a passed transaction proceeds, but the system's effect was only the binary flag, which is itself reversible by re-flagging). Net: a tightly-bounded system with high oversight, high recoverability, and concentrated accountability — the right calibration for the domain.

**A worked configuration: a high-agency Executor.** A coding agent (in-loop, on a real repository, mid-sized scope): agency is *wide* (the system chooses what files to modify, what abstractions to introduce, which tests to extend); autonomy is *wide* per task but gated at PR boundaries (no per-step approval, but every set of changes surfaces as a PR for human merge); responsibility is *distributed* (the human ticket author is the authorial owner; the agent is the operational executor; the human merging the PR is the validator); reversibility is *moderate* (uncommitted changes are fully reversible; committed-but-unmerged changes are reversible by reset; merged changes require a revert). Net: a system that converts a single human task ticket into a substantial body of work, with the gate at the boundary where reversibility is still cheap.

The four dimensions, used as design levers, generate spec configurations that match the deployment's risk profile rather than its taxonomy label. The Guardian and the coding agent above are different archetypes, but the dimensional analysis is the same conceptual procedure: name the value on each axis, justify each value, write the spec clauses that operationalize each value.

### 3.4 The fix-locus failure taxonomy (Cat 1–7)

When a delegated system produces a wrong outcome, the operationally useful question is not *what failed* but *which artifact has to change so this doesn't happen again*. We propose a seven-category partition by *fix locus* — the artifact whose modification prevents the failure's recurrence. The first six categories synthesize common practice. The seventh, *Perceptual Failure*, is novel to this work and addresses a class of failure that emerges in *perceiving-then-acting* systems (computer-use agents, browser-use agents, robotic systems) which prior taxonomies do not cover.

**The seven categories.**

| Category | Failure shape | Fix locus |
|---|---|---|
| Cat 1 — Spec | Spec said the wrong thing, omitted a needed clause, or left an ambiguity the executor resolved against the author's intent | The spec |
| Cat 2 — Capability | Capability boundary was wrong: tool manifest exposed a tool that should have been restricted, lacked a tool the task required, or scoped a tool too broadly | Tool manifest; capability authorization |
| Cat 3 — Scope creep | Agent acted outside the authorized scope, often by interpreting the spec's positive clauses without enforcing its NOT-authorized clauses | Spec NOT-authorized clauses; agent system prompt |
| Cat 4 — Oversight | A needed oversight gate did not fire, or the gate fired but the human reviewer's judgment was misaligned with the spec's criteria | Oversight model; gate configuration; reviewer training |
| Cat 5 — Compounding | A chain of individually defensible steps produced an incorrect cumulative outcome; no single step was wrong, the composition was | System spec; checkpoint pattern; evaluator-optimizer composition |
| Cat 6 — Model-level | The model produced confidently incorrect content despite a correct spec, a correct manifest, and intact oversight; the failure is at the underlying capability layer | Structural validation; allowlist resolution; accept residual risk |
| **Cat 7 — Perceptual** | **A perceiving-then-acting system's perception did not match the actual state of the environment; the system acted on a wrong model of reality** | **Confirmation gate; screenshot-then-verify; multimodal grounding; element-allowlist** |

**The fix-locus framing.** A failure's *symptom* is what was observed (a wrong refund amount; a deleted test; a clicked button on the wrong domain). A failure's *fix locus* is the artifact whose modification eliminates the failure's recurrence. The two are not the same and frequently diverge. A wrong refund amount may have been observed in production (symptom), but the spec was the locus that authorized the wrong amount (fix locus: spec, Cat 1). A deleted test was observed in CI (symptom), but the spec did not forbid test deletion (fix locus: spec, Cat 1; or capability, Cat 2, if the agent should not have had write access to the test directory). The fix-locus framing is what makes the taxonomy operationally useful: it tells the team *which artifact to update*, which is what the post-incident response actually requires.

**Cat 7 — Perceptual Failure: the novel category.** Computer-use agents [@anthropicComputerUse2024; @openaiOperator2025; @googleGeminiComputerUse2025] perceive a screen via vision and act via simulated input. Their failures include shapes that prior taxonomies, including MAST [@cemriMAST2025] and the hallucination survey of Zhang et al. [@zhangHallucinationSurvey2025], do not partition: the system's perception of the environment diverges from the environment's actual state, and the system acts on the wrong perception. We name this *Perceptual Failure* and identify four sub-categories:

- **Misidentification.** The system identifies an interface element correctly as a category (e.g., "a button") but assigns it the wrong role (e.g., a "Cancel" button identified as "Confirm"). The fix is structural: a confirmation gate before high-consequence actions, where the gate's prompt is generated from the system's claimed intent ("you are about to click Confirm — is that what you mean?") and surfaces the discrepancy to a human reviewer or a Guardian.
- **Missed element.** The system fails to perceive an element that was present and material to the action (a modal dialog, an error toast, a form-validation message). The fix is structural: screenshot-then-verify before proceeding, where the verification step asserts the expected state of the screen against the system's plan and halts on mismatch.
- **Hallucinated element.** The system perceives an element that was not present (a button it expected to see, a list item it expected to find), and acts on the perception. The fix is element-allowlist plus DOM-grounded verification where DOM is available; for canvas-rendered or image-only environments, the fix is reduced reliability and required human checkpoints.
- **State miscount.** The system asserts a position-based fact about a list, scroll position, or sequence that was true at one moment but no longer true at the moment the system acted on it (e.g., "the third item" became the second after a scroll). The fix is re-verification of position-based facts at the moment of use, not at the moment of perception.

These four sub-categories are not exhaustive — perception failure modes will continue to be discovered as more computer-use deployments surface them — but they cover the failure shapes practitioners report most often as of 2026 and are sufficient for the category to be operationally useful in spec design and in red-team protocols.

**Why Cat 7 is necessary.** No prior taxonomy partitions perceiving-then-acting failure as a distinct class. MAST [@cemriMAST2025] is empirically derived from text-based multi-agent systems and does not specifically address vision-language perception failure modes. The hallucination survey of Zhang et al. [@zhangHallucinationSurvey2025] partitions hallucination at the model output layer (tool-call, planning, instruction-following) rather than at the perception-action interface. OWASP LLM Top 10 [@owaspLLMTop10_2025] addresses prompt-injection categories (LLM01 multimodal sub-category) and improper output handling (LLM05) but treats perception failure as a downstream consequence rather than a first-class failure category. The result is that practitioners deploying computer-use agents in 2026 lack a taxonomy slot for the failures they actually observe, and the fixes (confirmation gates, screenshot-verification, element-allowlists) get reinvented per deployment. Cat 7 is the smallest contribution that gives the taxonomy a slot.

**Composition with prior work.** The fix-locus framing complements rather than replaces the symptom-locus framings of prior work. MAST tells the team *what failed at the symptom layer*: the agent emitted an incorrect tool call, the supervisor failed to verify, the handoff dropped state. The Cat 1–7 framing tells the team *which artifact must change*: the spec, the manifest, the oversight model, the structural validation, the perception-verification step. Together, they form a two-axis classification: a finding's MAST category (what failed) and its Cat 1–7 (where to fix it). A single MAST finding may map to multiple Cat 1–7 categories (a spec gap that allowed a manifest exposure that produced an incorrect tool call is Cat 1 + Cat 2), and a single Cat 1–7 fix may resolve multiple MAST findings (tightening the spec's NOT-authorized clauses is Cat 1 work that closes several MAST symptoms at once).

**The taxonomy's limits.** The seven categories partition the failure space coarsely, which is its operational virtue and its conceptual limit. Reasonable readers may propose six (collapsing Cat 6 and Cat 7 into a single "model-level" with sub-types) or eight (separating *spec gap* from *spec ambiguity* in Cat 1, as the book's living-spec chapter does). The framework's working choice is seven. The contribution is the *fix-locus framing* and the *Cat 7 partition*; the precise cardinality is opinionated rather than derived.

### 3.5 Spec-Driven Development as the protocol

The three previous subsections name what to design (intent), how to shape it (archetypes), and how to calibrate it (dimensions); §3.4 names how to diagnose its failures. None of those by themselves produces an executable artifact. **Spec-Driven Development (SDD)** is the protocol that does — the discipline of writing a complete, validated specification *before* the executor runs, treating the spec as the authoritative source against which output is reviewed, and updating the spec rather than the output when execution reveals the spec was wrong.

SDD as a discipline predates this paper. GitHub's spec-kit [@githubSpecKit2024] operationalizes spec-first practice with AI assistants; Microsoft's DevSquad Copilot [@microsoftDevSquadCopilot2024] integrates SDD into an eight-phase iterative cycle for agentic software delivery. Neither project originated the idea: the contract-first thread runs through Meyer's Design by Contract [@meyerDesignByContract1992] and Jackson's specifications work [@jacksonRequirements1995]; the spec-as-truth thread runs through formal-methods literature decades earlier. What SDD adds, in its 2024–2025 form, is the recognition that *agentic execution makes spec-first non-optional*: a spec that exists only to satisfy a process review, while engineers code from informal understanding, is a documentation artifact; a spec that an agent literally executes against is a control surface. The framework relies on the latter.

**The spec lifecycle.** SDD operates on a five-phase cycle: *intent capture* (the system author articulates what is to be designed), *specification* (the intent becomes a structured document with archetype, scope, constraints, oversight model, acceptance criteria), *execution* (the agent or automated executor produces output against the spec), *validation* (a human or a Guardian validates the output against the spec's acceptance criteria), and *evolution* (the spec is updated when validation reveals the spec, not the output, was wrong). The framework's contribution at this layer is the recognition that the *evolution* phase is where the failure taxonomy of §3.4 operationalizes: a Cat 1 failure produces a spec update; a Cat 2 failure produces a manifest update; a Cat 4 failure produces an oversight-model update; and so on. The taxonomy is the diagnostic that drives the evolution phase.

**The canonical template.** A SDD specification, in the framework's canonical form, contains thirteen sections — problem statement, objective, authorized scope, NOT-authorized scope (with the archetype declared in this same section), tool manifest, invariants, non-functional constraints, acceptance criteria, agent execution instructions, oversight model, validation checklist, spec evolution log, and the gap log. We do not re-derive the template here; the companion book contains the full development. What this paper claims is that the four-dimension calibration of §3.3 maps cleanly to specific clauses in this template (§3 and §4 carry agency; §4's oversight model carries autonomy; §1 and §12 carry responsibility; §7 and §8 carry reversibility), and that the seven failure categories of §3.4 map cleanly to specific update sites in the same template (Cat 1 updates §3, §4, or §6 depending on the gap; Cat 2 updates §7; Cat 4 updates §4's oversight clauses; Cat 5 updates §11 with checkpoint or evaluator-optimizer instructions; Cat 7 updates §11 with verification-before-action requirements). The mapping makes the framework operational: a failure category dictates which clause to update, and the spec evolution log records the change.

**The living-spec discipline.** A spec that never updates is either a spec for a system that has never been used or a spec the team has stopped governing. A spec that updates with every preference change is a spec being abused as a conversation transcript. The living-spec discipline names a middle path: *spec gaps* (Cat 1) and *spec ambiguities* (a sub-class of Cat 1 the book treats separately) trigger spec updates; *implementation failures* (Cat 6, sometimes Cat 2) and *preference changes* (which the framework explicitly excludes from the taxonomy) do not. The discipline is what prevents both spec rot and spec churn. Empirically, teams that adopt SDD without the living-spec discipline degrade within two quarters into either form of failure mode; teams that adopt the discipline maintain spec-as-control-surface over multiple quarters [@microsoftDevSquadCopilot2024 reports analogous observations].

**Why SDD is the protocol layer rather than a fifth element of the framework.** Archetypes (§3.2), dimensions (§3.3), and the failure taxonomy (§3.4) are *descriptive* — they tell the system author how to think about a delegated system. SDD is *prescriptive* — it tells the author how to write down the result so that an executor can act on it and a validator can check it. The framework treats SDD as a substrate rather than a peer element: archetypes commit at the archetype-declaration clause of an SDD spec; dimensions calibrate at specific other clauses; the taxonomy operates on the spec evolution log. Without SDD as the substrate, the framework's other elements are concepts without artifacts — a vocabulary the team can use in conversation but cannot enforce in code. With SDD, they become the structure of an executable specification.

The framework, in summary, is: *intent as a designed artifact* (§3.1), shaped by *archetypes* (§3.2), calibrated along *four orthogonal dimensions* (§3.3), diagnosed against *seven failure categories* (§3.4), expressed and evolved through *Spec-Driven Development* (§3.5). Section 4 instantiates the framework against AI agent systems as the most-acute current application; §5 discusses generalization beyond agents; §6 names the framework's limitations honestly.

---

## 4. Worked application: AI agent systems

> *Section purpose: instantiate the framework against the most-acute current case. The book provides three full worked examples (a customer support multi-agent system, a code-generation pipeline, an in-loop coding agent); the paper summarizes the third because it is the most-deployed agent class of 2024–2026 and the compositional shape is rich.*

### 4.1 The agentic development lifecycle and DevSquad Copilot

> *Stub paragraph.* Microsoft DevSquad Copilot [@microsoftDevSquadCopilot2024] defines an eight-phase iterative cycle: envisioning → spec thin slices → plan with ADRs → decompose → TDD-first implement → learn openly → independent review → continuous refinement. The cycle exemplifies the broader *agentic development lifecycle* — the practice of using AI agents in iterative software delivery alongside human engineers. The Architecture of Intent composes cleanly with this cycle: archetypes commit at envisioning; dimensions calibrate during spec thin slices; the failure taxonomy operates during learn openly; SDD threads through every phase. We provide a phase-to-artifact mapping table (full version in the book; abbreviated here).

### 4.2 Capability boundaries via the Model Context Protocol

> *Stub paragraph.* MCP [@anthropicMCP2024] is the protocol that makes capability boundaries operationally enforceable. The framework's *Least Capability* discipline — agents receive only the tools their authorized scope requires — is implementable in MCP terms via per-tool authorization at the server. We summarize the MCP-specific patterns from the book.

### 4.3 Coding agents: a worked archetype-by-deployment-posture analysis

> *Stub paragraph: ~800 words.* Coding agents (Cursor, Cline, Devin, Claude Code, Codex CLI) resist clean archetype partitioning. The framework resolves this by archetype-by-deployment-posture: pair-programmer mode is Advisor; in-loop mode is Executor with optional Synthesizer composition; autonomous mode is Orchestrator-over-self. Each posture has different oversight, different capability boundaries, different failure surface. We work through three structural controls (branch protection, dependency allowlist, sandboxed execution) and the most common Cat 1/3 hybrid (the deleted-tests failure: agent removes failing tests instead of fixing them). External calibration benchmarks: SWE-bench Verified [@jimenezSweBenchVerified2024].

### 4.4 Computer-use agents: where Cat 7 becomes necessary

> *Stub paragraph: ~600 words.* Computer-use agents [@anthropicComputerUse2024; @openaiOperator2025; @googleGeminiComputerUse2025] perceive a screen via vision and act via simulated input. Their failure surface includes shapes that don't exist for text-only agents: lookalike domain navigation, visual instruction injection [@greshakeIndirectInjection2023; @willisonLethalTrifecta], modal popup interception, state miscount in dynamic lists. Cat 7 (Perceptual Failure) is the framework's response. Four structural controls follow from the analysis: sandboxed environment, authentication scope minimization, domain allowlist, high-consequence confirmation gates. We also note: when an API exists, computer-use should be the option of last resort. External calibration benchmarks: WebArena [@zhouWebArena2024], OSWorld [@xieOSWorld2024]. The OWASP LLM Top 10 [@owaspLLMTop10_2025] provides the baseline attack-surface enumeration we extend.

---

## 5. Discussion

### 5.1 When the framework helps

> *Stub paragraph.* The framework helps most when the system has nontrivial autonomy and the cost of failure is high enough to make spec-precision investment pay back. For low-autonomy, low-consequence deployments, the framework's overhead exceeds its value; teams should adopt the vocabulary (archetypes, dimensions, failure taxonomy) without the full SDD apparatus.

### 5.2 When it doesn't

> *Stub paragraph.* Three honest limitations: (i) regulated industries (healthcare, finance, defense) have compliance requirements that go beyond what the framework addresses; (ii) multi-organizational agent systems where agents from different orgs interact have governance problems the framework does not solve; (iii) cost-benefit analysis for adopting the practices depends on factors that vary too widely to generalize.

### 5.3 Relation to MAST and other multi-agent failure work

> *Stub paragraph.* We position the framework as complementary to MAST [@cemriMAST2025], Zhang et al.'s hallucination survey [@zhangHallucinationSurvey2025], and OWASP LLM Top 10 [@owaspLLMTop10_2025]. None of those compete with Cat 1–7; they cover different partitions of the failure space. We show the mapping.

### 5.4 Generalization beyond AI agents

> *Stub paragraph: ~400 words.* The framework's claims do not depend on the delegated actor being an AI agent. The five archetypes describe delegation shapes that recur in human teams (an Advisor team, an Executor team, a Guardian role, etc.); the four dimensions calibrate any delegated system; the fix-locus taxonomy partitions any failure by which artifact must change. AI agent systems are the most-acute current instance because the delegation is wider and faster than at any prior point — but the framework is not specific to them. We discuss two non-agent applications briefly: organizational delegation and CI/CD pipelines.

### 5.5 What this paper does not claim

> *Stub paragraph.* We do not claim empirical validation at scale. We do not claim novelty for SDD, archetypes-as-concept, or the four dimensions individually. We do not claim Cat 1–6 are new categories — only that the fix-locus framing is a useful complement to MAST. The genuinely new contributions are: (i) Cat 7 (Perceptual Failure); (ii) the autonomy-vs-agency operationalization; (iii) the orthogonality argument; (iv) the synthesis as a coherent framework with consistent vocabulary.

---

## 6. Limitations

> *Section format: bullet list of explicit limitations. Reviewers reward this section more than they reward the introduction.*

- **Position-paper status.** The paper is offered as a structural design tool, not as an empirical intervention. The framework's claims are normative ("you should design this way") rather than descriptive ("we measured what works").
- **No empirical validation at scale.** The book provides three worked examples (customer support, code-generation pipeline, coding agent); these are existence proofs, not statistical evidence. Quantitative validation across many deployments is future work.
- **Archetype taxonomy is opinionated.** The five archetypes are a working taxonomy, not a derived classification. A different practitioner might propose three, seven, or nine; the contribution is the act of canonicalizing rather than the specific cardinality.
- **Cat 7 is preliminary.** The category is named but not yet stress-tested across many computer-use deployments. Sub-categories may need to be revised as more deployments surface failure modes.
- **Generalization beyond AI agents is asserted, not demonstrated.** §5.4 argues the framework generalizes; we do not provide worked examples for non-agent applications in this paper.
- **Vocabulary friction.** The paper introduces several coined or refactored terms (intent as a design surface, fix-locus taxonomy, Cat 7). Adoption requires the vocabulary to spread; the framework's value is partly contingent on linguistic uptake.

---

## 7. Conclusion

> *Stub paragraph.* The cost of imprecise intent has always existed; we have been getting away with it because human professionals exercised silent judgment to bridge it. As delegation widens — to AI agents, to automated pipelines, to organizations — the bridge automates and the imprecision becomes immediately visible. The Architecture of Intent proposes a structural design framework for delegated systems with explicit intent architecture. The framework's bet is that, as delegation widens, intent precision compounds in value. The paper offers the framework as a tool for practitioners shipping AI agent systems today; the same tool, we argue, applies to other delegated systems as the lessons travel out.

---

## References

> Bibliography is generated from `references.bib` at compile time. The Markdown source uses Pandoc-style `[@key]` inline citations resolved by `pandoc --citeproc --bibliography references.bib`. The `references.bib` file in this directory contains full BibTeX entries (~30 sources across 9 domains). Citation style: numeric (arXiv default for first version). For workshop or journal submission we will normalize to the venue's required style.

::: {#refs}
*Bibliography rendered here at compile time.*
:::

---

## Appendix A: Mapping to the book

> *For readers of the companion book (Aldecoa 2026), this appendix maps each section of the paper to the relevant book chapter so the paper can be read as a distillation rather than a substitute.*

| Paper section | Book chapter |
|---|---|
| §3.1 Intent as a design surface | Theory ch. 2 (Intent vs. Implementation) |
| §3.2 Archetypes | Architecture ch. 2–6 |
| §3.3 Four dimensions | Theory ch. 3 (Calibrate Agency, Autonomy, Responsibility, Reversibility) |
| §3.4 Cat 1–7 | Theory ch. 5 (Failure Modes and How to Diagnose Them) |
| §3.5 SDD as the protocol | Part 2 (The Spec) |
| §4.1 Agentic development lifecycle | Operating ch. 12–13 (DevSquad Mapping & Co-adoption) |
| §4.2 MCP capability boundaries | Agents ch. 4, MCP ch. 1–3 |
| §4.3 Coding agents | Agents ch. 8; Examples ch. 3 |
| §4.4 Computer-use agents | Agents ch. 9 |

---

*End of skeleton draft. To convert this into a finished paper: expand each `*Stub paragraph*` block to its target word count; convert tables and bullet lists to LaTeX where appropriate; finalize citations to a consistent style (likely ACM or arXiv default); add figures (one decision-tree figure for §3.2; one orthogonality plot for §3.3 if it survives review).*
