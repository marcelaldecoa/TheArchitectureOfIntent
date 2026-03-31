# The Canonical Spec Template

**Specification**

---

> *"A spec is a contract between humans and agents. Its clauses are the terms. The agent's output is the performance. Validation is the audit."*

---

## Context

You have understood the principles of Spec-Driven Development. You need the artifact.

This pattern is different from the others in Part IV: it is primarily reference material. It presents the canonical spec template in full, with an explanation of each section, the key questions each section must answer, and examples of what good and weak entries look like.

Use this pattern as:
- The primary reference when writing a new spec
- The evaluation framework when reviewing a spec
- The structural model when building project-specific template variants
- The template fragment library when adding spec sections to SpecKit's constitution

This pattern assumes all of Part IV.

---

## The Canonical Spec Template

Copy the template below as the starting point for any spec. Sections marked `[required]` must be present and complete before the spec is marked *Approved*. Sections marked `[required for agent systems]` are required when the spec describes an agent-class system.

---

```markdown
# [Spec Title]

**Status:** Draft | Approved | In Progress | Validated | Superseded  
**Version:** 1.0  
**Owner:** [Name / Role]  
**Date:** [YYYY-MM-DD]  
**Archetype:** [Classification / Agency Level] — [required for agent systems]

---

## 1. Problem Statement [required]

*One paragraph maximum.*

[What problem are we solving? Who is affected? Why does this matter now? 
What would break or be lost if this were not solved?]

---

## 2. Desired Outcome [required]

**Primary Outcome**

[The single most important thing that must be true when this is successful.
Written as an observable state, not an activity.]

**Secondary Outcomes** *(optional)*

- [Additional benefit that would be valuable but is not required for success]
- [Another secondary outcome]

> Success is defined by observable outcomes, not implementation choices.

---

## 3. Scope [required]

**In Scope**

- [Explicitly included behavior or capability]
- [Another included behavior]

**Out of Scope**

- [Explicitly excluded behavior or capability — what this will NOT do]
- [Another excluded behavior]

> This section prevents agents and humans from over-building.
> If something is not listed here, it is out of scope by default.

---

## 4. Archetype Declaration [required for agent systems]

**Classification:** [Advisor | Executor | Guardian | Synthesizer | Orchestrator]  
**Agency Level:** [1–5] — [Label and one-line justification]  
**Risk Posture:** [Low | Medium | High | Critical] — [One-line rationale]  
**Oversight Model:** [A | B | C | D] — [One-line description of the oversight mechanism]  
**Reversibility:** [R1 | R2 | R3 | R4] — [One-line description of recovery options]

*For archetype definitions, see the [Intent Archetype Catalog](../architecture/02-canonical-intent-archetypes.md).*

---

## 5. Functional Intent [required]

*Describe what the system must do, not how.*

**Core Capabilities**

- The system must [capability 1 — observable, testable]
- The system must [capability 2]
- The system must [capability 3]

**The system must NOT:**

- [Forbidden behavior 1 — explicit exclusion]
- [Forbidden behavior 2]

**Key Flows** *(for complex systems)*

- Flow A: [User/system action] → [system response] → [outcome]
- Flow B: [User/system action] → [system response] → [outcome]

> Use clear declarative language: "The system must..." and "The system must not..."
> Do not describe implementation. Describe observable behavior.

---

## 6. Invariants [required]

*These conditions must always be true. They cannot be traded off for 
performance, convenience, or edge-case handling. Violations are failures 
regardless of other spec compliance.*

1. [Invariant 1 — absolute, unconditional]
2. [Invariant 2]
3. [Invariant 3]

> If any invariant is ever wrong, it must be updated via the spec evolution 
> process — never silently violated.

---

## 7. Non-Functional Constraints [required]

| Category | Constraint | Testable Threshold |
|---|---|---|
| Performance | [Requirement] | [e.g., P95 response < 200ms] |
| Reliability | [Requirement] | [e.g., graceful degradation on downstream failure] |
| Security | [Requirement] | [e.g., no PII in logs] |
| Compliance | [Requirement] | [e.g., must satisfy policy X] |
| Cost | [Requirement] | [e.g., < $X/month at 10k requests/day] |
| Scalability | [Requirement] | [e.g., must support N concurrent users] |
| Observability | [Requirement] | [e.g., all errors logged with correlation ID] |

*Remove rows that genuinely don't apply. Add rows for constraints specific to 
this system.*

---

## 8. Authorization Boundary [required for agent systems]

**This system is authorized to:**

- Read: [specific data sources, scopes, access levels]
- Write to: [specific targets, with conditions]
- Call: [specific APIs or services, with rate limits or conditions]
- Invoke: [specific sub-agents or tools, with invocation conditions]

**This system is NOT authorized to:**

- [Explicit exclusion 1]
- [Explicit exclusion 2]

**Exception gate:**  
Any situation not covered above → [halt | escalate | log and continue] and surface to [designated role/process].

---

## 9. Acceptance Criteria [required]

*Define success in testable terms. If it cannot be tested or measured, it is 
not complete.*

**Functional Acceptance**

- Given [precondition], when [action], then [expected result]
- Given [precondition], when [action], then [expected result]
- [Edge case]: given [precondition], when [action], then [expected result]

**Non-Functional Acceptance**

- [Metric/threshold that proves a non-functional constraint was met]
- [Another metric]

> Acceptance criteria are what Phase 5 validation checks. Write them so 
> they can be evaluated independently of the author.

---

## 10. Assumptions and Open Questions

**Assumptions** *(things believed to be true but not verified)*

- [Assumption 1] — *Owner: [who should verify this]*
- [Assumption 2]

**Open Questions** *(decisions that must be made before execution)*

- [Question 1] — *Owner: [who decides]* · *Decision needed by: [date or phase]*
- [Question 2]

> Agents must surface uncertainty rather than invent answers. If an open 
> question remains unresolved at execution time, the agent should halt and 
> surface it rather than decide autonomously.

---

## 11. Agent Execution Instructions [required for agent systems]

*Written directly to the agent. Second person, imperative.*

**Skills to load** *(optional)*

- [skill-name]: [Why this skill is relevant to this task]
- [skill-name]: [Scope or conditions under which to apply it]

> Skills teach domain-specific workflows and organizational context. List only 
> skills that are directly relevant. If no skills apply, omit this sub-section.
> See [Agent Skills](../agents/05-agent-skills.md) for the skills framework.

**You are authorized to:**

- [Action type 1]: [Scope or conditions]
- [Action type 2]: [Scope or conditions]

**You are NOT authorized to:**

- Make decisions not specified in this spec
- Expand scope beyond section 3
- Resolve open questions in section 10 without surfacing them first
- [Specific forbidden action]

**If you encounter a situation this spec does not cover:**  
Stop execution. List the specific gap. Present it for human resolution before continuing.

**If this spec appears to have a contradiction:**  
Do not resolve it by choosing one side. Surface the contradiction.

**Required outputs from this execution:**

- [ ] [Output artifact 1]
- [ ] [Output artifact 2]
- [ ] [Any additional deliverable]

---

## 12. Validation Checklist [required]

*Completed by the human validator after execution. Check against the spec, 
not against preference.*

- [ ] Output satisfies the Desired Outcome (section 2)
- [ ] All acceptance criteria in section 9 are met
- [ ] No invariants in section 6 were violated
- [ ] No out-of-scope behaviors were produced (section 3)
- [ ] Authorization boundary (section 8) was respected
- [ ] All assumptions in section 10 were either validated or remain pending
- [ ] Spec evolution log updated based on findings (section 13)

> If validation fails: categorize the failure (spec gap, spec ambiguity, 
> or implementation failure) before deciding how to respond.

---

## 13. Spec Evolution Log [required]

*Specs are living artifacts. Every change is recorded here with its reason.*

| Version | Date | Change Summary | Trigger | Author |
|---------|------|----------------|---------|--------|
| 1.0 | [date] | Initial specification | New work | [name] |
| | | | | |

---

## 14. Planned Evolution *(optional)*

*Use when this spec represents Phase 1 of a planned transition.*

**Current classification:** [Archetype and agency level]  
**Target classification (Phase N):** [Target archetype and agency level]  
**Transition criteria:**

- [Criterion 1 that must be met before transitioning]
- [Criterion 2]

**What will NOT change at transition:** [Invariants that carry forward]
```

---

## Section-by-Section Guidance

### Section 1: Problem Statement

**Purpose:** Establish shared understanding of why this work exists.

**Key questions it must answer:**
- What is broken, missing, or inadequate?
- Who experiences the problem, and how?
- Why address it now? (If the answer is "we're just supposed to," that's a sign the problem statement isn't done.)
- What is the observable cost of not solving it?

**Weak:**
> "We need a better way to handle customer support."

**Strong:**
> "Customer support agents spend an average of 12 minutes per ticket searching across 4 internal systems for relevant account history. This delay causes a 23% first-contact-resolution gap against our SLA. The information exists; the problem is retrieval time. This becomes critical in Q2 when support volume is projected to double."

The strong version is falsifiable: you can measure the 12 minutes, the 23% gap, the Q2 projection. The solution can be validated against it.

---

### Section 2: Desired Outcome

**Purpose:** Define success in terms of observable state.

The primary outcome is one thing. Not a list. The single most important state that must be true when the work is done. Secondary outcomes are valuable but don't gate completion.

**Weak:**
> "Better, faster, more efficient customer support experience."

**Strong:**
> "A support agent handling a common account inquiry can retrieve all relevant account history within 30 seconds of opening the ticket, without navigating away from the support interface."

---

### Section 3: Scope

**Purpose:** Prevent overbuilding and underbuilding. Establish what success does not require.

The out-of-scope section is often equal in importance to the in-scope section. "We are not building a general-purpose search across all company data" prevents an agent from building something five times bigger than needed.

Every out-of-scope line is a decision: we decided NOT to do this, for this work, at this time. That decision should survive scrutiny.

---

### Section 4: Archetype Declaration

**Purpose:** Establish the governance framework for agent systems.

This section is the most consequential sentence in the spec for agent systems. See [Four Dimensions of Governance](../architecture/03-archetype-dimensions.md) for the dimension definitions and [Decision Tree](../architecture/04-decision-tree.md) for how to arrive at the classification.

The archetype declaration cannot be generic. "It's an agent, so it's an Executor" is not a declaration. The declaration names the specific agency level (1–5), the risk posture rationale, the oversight model mechanism, and the reversibility assessment.

---

### Section 6: Invariants

**Purpose:** Establish the unconditional constraints that no execution discretion can override.

The distinction between an invariant and a constraint: a constraint has acceptable conditions under which it can be relaxed (performance constraints under exceptional load, for example). An invariant never has such conditions. It is always true.

The test for an invariant: *Is there any circumstance under which violating this would be acceptable?* If yes, it is a constraint, not an invariant.

---

### Section 9: Acceptance Criteria

**Purpose:** Make validation independent of the author.

The test for an acceptance criterion: *Could a person who was not involved in writing this spec determine whether this criterion was met by examining the output?*

If no: the criterion is not ready. Rewrite it.

Given/When/Then format is excellent for functional criteria because it forces the conditions, trigger, and expectation to be stated separately.

---

### Section 11: Agent Execution Instructions

**Purpose:** Communicate directly and unambiguously with the executing agent.

This section should be written last, after all other sections are complete — because it summarizes what the agent may and may not do, and that summary must accurately reflect the entire spec.

The **Skills to load** sub-section specifies which Agent Skills the agent should activate for this task. Skills are packaged domain knowledge — organizational workflows, brand guidelines, specialized analysis procedures — that extend what the agent knows how to do well. A skill is not an authorization; it is a capability enhancement. The authorization boundary is still governed by section 8. See [Portable Domain Knowledge](../agents/05-agent-skills.md) for the full treatment.

The most important clauses are the "NOT authorized" clauses. Agents are expansive by default; without explicit prohibitions, they tend to fill gaps. The explicit prohibition list is the fence around the pre-authorized scope.

---

## Part IV Closing: The Spec As The Work

The canonical spec template is not a bureaucratic instrument. It is the distillation of a discipline: that the work of engineering systems in an age of agent execution is fundamentally the work of expressing intent precisely.

*"If you can't specify it, you don't understand it well enough yet."*

This statement, which appears in the SDD source material that preceded this book, is the organizing truth of Part IV. The spec is not something you write after you understand the problem. It is the thing that tells you whether you understand the problem. Writing a spec that cannot be completed — because the problem statement is too vague, the desired outcome is unknowable, the acceptance criteria are untestable — is the earliest possible discovery that the work is not ready to start.

The spec, written well, is the work. Everything after it is execution.

---

## Therefore

> **The canonical spec template structures intent into fourteen sections across four categories: context (1–3), governance (4, 8), precision (5–7, 9–11), and memory (12–14). Required sections must be complete before execution begins. Agent-system sections formalize the archetype governance framework at the per-task level. The spec evolution log closes the feedback loop. The spec, written with precision, is not paperwork before the work — it is the work.**

---

## Connections

**This pattern assumes all of Part IV:**
- [Spec-Driven Development](01-what-sdd-means.md)
- [The Spec as Control Surface](02-specs-as-control-surfaces.md)
- [The Spec Lifecycle](03-spec-lifecycle.md)
- [SpecKit](04-speckit.md)
- [Writing for Machine Execution](05-writing-specs-for-agents.md)
- [The Living Spec](06-living-specs.md)

**This pattern is used by:**
- [Spec Template Library](../repertoires/03-spec-template-library.md) — variant templates for feature specs, agent instructions, integrations
- [Archetype deep dives](../architecture/archetypes/) — each archetype's spec template fragment
- Part VII (Operating Intent Systems) — spec review as governance practice

---

*Part IV is complete. Continue to [Part V: Agents & Execution](../agents/01-what-agents-are.md).*




