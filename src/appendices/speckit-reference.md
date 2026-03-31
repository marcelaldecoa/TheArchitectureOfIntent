# SpecKit Quick Reference

**Appendices** · *Appendix D*

---

> *"SpecKit is scaffolding, not substance. It reduces friction for the practice; it doesn't perform the practice for you."*

---

This reference covers SpecKit's commands, the 11-section spec template in quick-reference format, constraint writing patterns, success criteria patterns, and archetype-to-oversight pairing defaults. For the full conceptual treatment, see [SpecKit](../sdd/04-speckit.md).

---

## Quick-Reference: Slash Commands

SpecKit integrates with AI coding tools (GitHub Copilot, Claude, Cursor, and compatible VS Code extensions) as a set of slash commands. Each command is invoked in your AI chat interface.

### `/spec new`

Opens an interactive spec creation session. SpecKit asks a structured set of questions mapped to the 11-section canonical template and assembles a draft spec document for review.

**Typical prompts SpecKit will ask:**
1. What problem are you solving? (→ Problem Statement)
2. What is the single measurable outcome you want? (→ Objective)
3. What is the agent authorized to do? (→ Authorized Scope)
4. What is the agent explicitly NOT authorized to do? (→ NOT-Authorized Scope)
5. What constraints must always hold? (→ Constraints)
6. How do you know the output is correct? (→ Success Criteria)
7. What tools does the agent need? (→ Tool Manifest)
8. What oversight model applies? (→ Oversight Model)

**Options:**
```
/spec new --archetype executor    # Pre-populate with Executor archetype defaults
/spec new --from feature-spec     # Start from the Feature Spec template
/spec new --minimal               # Sections 1-6 only (abbreviated spec)
```

---

### `/spec review`

Applies the five spec approval questions to an existing spec and returns a structured review report.

**The five questions applied:**

1. Does the Objective describe a single measurable outcome, not a process?
2. Are the NOT-authorized clauses sufficient to prevent the most likely misuse vectors?
3. Are the Success Criteria testable without human interpretation?
4. Does the selected archetype match the actual risk posture and reversibility?
5. Is the Tool Manifest minimal — does any tool grant more access than the spec requires?

**Usage:**
```
/spec review                      # Reviews the spec in your current file
/spec review --focus constraints  # Deep review of §4 and §5 only
/spec review --checklist          # Returns a filled-in checklist instead of prose
```

---

### `/spec validate`

Compares an agent's output against a spec's Success Criteria section and produces a structured validation report.

**Output format:**
```
Spec: [spec identifier]
Criteria checked: [n]
Passed: [n]
Failed: [n]

Failures:
  SC2: [criterion text] — [how output failed]
  SC4: [criterion text] — [how output failed]

Failure category: spec gap | instruction gap | execution gap | environment
```

**Usage:**
```
/spec validate                    # Validates output against spec in current workspace
/spec validate --output <path>    # Validates a specific file
/spec validate --strict           # Treat warnings as failures
```

---

### `/spec gap`

Creates a Spec Gap Log entry from a validation failure. Structures the gap with: date, spec version, section, gap type, description, resolution status.

**Usage:**
```
/spec gap                         # Interactive: asks for gap details
/spec gap --from-validation       # Imports failures from most recent /spec validate output
```

---

### `/spec update`

Applies a proposed update to an existing spec, increments the version number, and creates a changelog entry.

**Usage:**
```
/spec update §5 "Add constraint C8: ..."
/spec update --section constraints "New constraint text"
/spec update --bump-version minor
```

---

### `/spec diff`

Compares two versions of a spec and highlights what changed between them — useful for spec review before re-execution.

```
/spec diff v1.1 v1.2
/spec diff --section constraints  # Only diff the constraints section
```

---

### `/spec scaffold`

Generates agent instructions directly from an approved spec. Translates each spec section into the appropriate instruction component.

```
/spec scaffold                    # Full system prompt from current spec
/spec scaffold --section 3,4,5   # Only authorized/not-authorized/constraints
/spec scaffold --format markdown  # Output as a markdown system prompt block
```

---

## Quick-Reference: The 11-Section Canonical Template

A minimal but complete spec covers these sections. Sections marked ★ are the most critical.

| § | Section | What it must answer | Minimum content |
|---|---------|---------------------|----------------|
| 1 | **Problem Statement** | What real problem is being solved, and why now? | 2–4 sentences with context and consequence |
| 2 ★ | **Objective** | What is the single measurable outcome? | One sentence; must be evaluable |
| 3 ★ | **Authorized Scope** | What is the agent permitted to do? | Numbered list; each item independently testable |
| 4 ★ | **NOT-Authorized Scope** | What is forbidden, even if not explicitly asked? | Minimum 5 items; include social engineering vectors |
| 5 ★ | **Constraints** | What rules must always hold, without exception? | Numbered C1–Cn; each maps to an acceptance test |
| 6 ★ | **Success Criteria & Acceptance Tests** | How do you know the output is correct? | SC1–SCn; each criterion maps to a test scenario |
| 7 | **Tool Manifest** | What tools does the agent have, and what does each do? | One entry per tool with auth level and failure behavior |
| 8 | **Oversight Model** | What human review is required, and when? | Model A/B/C/D; escalation triggers; audit requirements |
| 9 | **Risks & Mitigations** | What could go wrong, and what prevents it? | Table: risk / likelihood / impact / mitigation |
| 10 | **Spec Gap Log** | What gaps have been found and closed? | Running table; updated when gaps are identified |
| 11 | **Agent Skills** | What SKILL.md files should be loaded? | List of skill names; explicit NOT-applicable list |

**Minimal viable spec:** For low-risk, short-lived tasks, sections 2, 3, 4, 5, and 6 are the irreducible minimum. Do not ship a spec without these five.

---

## Quick-Reference: Constraint Writing

Constraints (§5) are the most commonly written poorly. These patterns help.

### The constraint must be verifiable

❌ Weak: "The agent should be careful with customer data."  
✅ Strong: "The agent must not surface payment card numbers in any response. Any response containing the pattern `\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b` is a constraint violation."

### The constraint must name the action, not the intent

❌ Weak: "The agent must protect user privacy."  
✅ Strong: "The agent must not access `customer.payment_methods` under any circumstances. This tool is not in the tool manifest."

### The constraint must handle the edge case you're worried about

❌ Weak: "The agent must only process authorized refunds."  
✅ Strong: "The refund amount passed to `refund.initiate()` must be derived from `order.lookup()`, not from a customer-stated amount. If `total_value` is $0.00, the agent must not initiate a refund."

### The NOT-authorized list is not the same as the constraints list

- **NOT-authorized** (§4): things the agent can never do — high-level prohibitions
- **Constraints** (§5): operational rules on how the agent does the things it is permitted to do

Both are needed. A common gap: a thorough NOT-authorized list with no constraints governing how authorized actions are performed.

### Constraint pattern templates

```
C[n] — [Name]
[The agent / Tool call] must [do X / not do Y] [condition].
[What to do if constraint would be violated]: [behavior].

Example:
C3 — Amount verification
The amount field in refund.initiate() must be derived from 
order.lookup(), not from conversation input. If order.lookup() 
returns total_value = 0.00, do not initiate a refund; escalate.
```

---

## Quick-Reference: Success Criteria Writing

Success criteria (§6) are the spec's acceptance tests stated as requirements. Each one must have a corresponding test.

### The criterion must be binary

❌ Weak: "The output should be well-formatted and clear."  
✅ Strong: "The output must include a tracking number if one is available from `order.lookup()`, and must omit the tracking number field if none is available."

### The criterion must be testable from the outside

❌ Weak: "The agent must have understood the customer's intent correctly."  
✅ Strong: "Given a customer message containing the word 'cancel,' the agent must not initiate any refund action, and must respond with an escalation offer within 2 turns."

### There must be a criterion for each dimension

A complete success criterion set covers:
- **Happy path** — does it work correctly for the primary use case?
- **Boundary cases** — does it handle edge cases from the constraint list?
- **Scope rejection** — does it decline NOT-authorized requests correctly?
- **Failure handling** — does it behave correctly when tools fail?
- **PII/security** — does it avoid surfacing sensitive data?

### Success criterion pattern template

```
SC[n] — [Name]
Given [input scenario], the agent [expected behavior] within [turn/time limit].

Example:
SC4 — Refund amount constraint
Given a refund request where the customer states an amount different 
from the order record, the agent uses the order record amount, 
not the customer-stated amount.
```

---

## Quick-Reference: Archetype + Oversight Pairing Defaults

These are the default pairings. Override them with explicit justification in §8.

| Archetype | Default Oversight Model | Default Escalation Trigger |
|-----------|------------------------|--------------------------|
| Advisor | A (post-review) | Significant factual error detected in log review |
| Executor | C (constrained execution) | Action outside authorized scope attempted |
| Guardian | A / continuous monitoring | Any trigger event (monitor fires immediately) |
| Synthesizer | B (human approval on high-stakes outputs) | Output above confidence threshold; outputs above scope size |
| Orchestrator | C (active oversight at key decision points) | Sub-agent failure; unexpected state; scope expansion |

**The oversight models:**

| Model | Name | Description |
|-------|------|-------------|
| A | Post-review | Agent executes; human reviews output after. Suitable for low-risk, reversible tasks |
| B | Approval gate | Human approves before execution or before output is delivered. Per-action or per-output |
| C | Constrained execution | Agent executes autonomously within pre-approved constraints; exceptions trigger escalation |
| D | Human-in-loop | Human makes or approves every significant decision; agent assists but does not act |

---

## Quick-Reference: The Spec Gap Log Entry

Every validation failure that reveals a spec deficiency becomes a Spec Gap Log entry. Minimum fields:

```markdown
| Date | [YYYY-MM-DD] |
| Spec | [spec name + version] |
| Section | [§ number and name] |
| Gap type | scope gap / constraint gap / success criterion gap / oversight gap / archetype mismatch |
| Description | [What the spec said, what was implied, and how the agent behaved] |
| Caught by intent review? | Yes / No |
| Why not caught (if No) | [reviewer checklist gap / input edge case not considered / other] |
| Resolution | spec updated / constraint library updated / archetype catalog updated / no action |
| Acceptance test added | SC[n] added / T-[n] test updated |
```

---

## Quick-Reference: First Spec Checklist

Before submitting a spec for intent review, verify:

- [ ] §2 Objective is one sentence and testable
- [ ] §3 Authorized Scope uses numbered items, each independently testable
- [ ] §4 NOT-Authorized Scope has ≥ 5 items, including at least one social engineering vector
- [ ] §5 Constraints are numbered, verifiable, and each maps to an acceptance test
- [ ] §6 has happy path, boundary, scope rejection, and failure handling criteria
- [ ] §7 Tool Manifest lists every tool with auth level (read/write) and failure behavior
- [ ] §8 names the oversight model explicitly and lists escalation triggers
- [ ] No constraint says "should" — all use "must" or "must not"
- [ ] No success criterion uses subjective language ("good," "clear," "appropriate")
- [ ] The NOT-authorized list has been reviewed by someone other than the spec author

---

*For the full conceptual treatment of each section, see [The Canonical Spec Template](../sdd/07-canonical-spec-template.md).*  
*For worked examples of complete specs, see [Writing the Spec (Example 1)](../examples/01-ai-customer-support/spec.md) and [Writing the Spec (Example 2)](../examples/02-code-generation-pipeline/spec.md).*


