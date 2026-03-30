# Validation & Acceptance Templates

**Part VI: Standards & Repertoires** · *5 of 5*

---

> *"You cannot validate what you did not specify. But you also cannot specify without knowing what validation will look like. The template makes both disciplines converge."*

---

## Context

Every spec in this framework includes success criteria — the section that defines what "correct" looks like before execution begins. Good success criteria make validation possible; poor ones collapse it into personal judgment.

Validation templates are the repertoire's answer to the same variability problem that spec templates solve: left to their own, practitioners write success criteria at wildly different levels of precision, covering different categories of correctness, and producing outputs that cannot be consistently validated by different reviewers.

This chapter provides validation templates — structured sets of success criteria for common output types — that practitioners copy into their specs and populate, rather than constructing from scratch.

---

## The Problem

Validation is where the spec-execute-validate loop either closes or breaks. It breaks in two characteristic ways:

**Criteria are not stated in advance.** The spec describes what to produce but not how to verify it. The human reviewer must decide during review whether the output is correct — without a reference standard. This makes review slow (each reviewer must derive their own standard) and inconsistent (different reviewers derive different standards). It also makes re-execution difficult: if you can't pass validation, you don't know what to fix.

**Criteria exist but aren't testable.** A success criterion like "the code should be clean and readable" cannot be validated — it is an aesthetic judgment. "Functions must be ≤40 lines; cyclomatic complexity ≤10; all public APIs must have documentation comments" can be validated. The difference is not pedantry; it is the difference between criteria that close the loop and criteria that defer judgment.

A second failure: validation categories are incomplete. A spec that validates functional correctness but not error handling will produce code that works on the happy path and fails silently on edge cases. A spec that validates output content but not output format will produce reports that are informationally correct but structurally wrong.

---

## The Resolution

### Validation Template Structure

Each validation template covers the major categories of correctness for a specific output type. For each category, it provides:

- **A criterion title** (the thing being validated)
- **A test formulation** (the question to ask when validating)
- **Pass/fail definition** (what constitutes passing; what constitutes failing)
- **Automation status** (automatable with tooling / manual review required)

The practitioner copies the template into their spec, marks which criteria are applicable, and fills in the specific values (e.g., "response time ≤ 200ms" rather than just "response time within declared limit").

---

### Template: Code Output

Use for any spec that produces code — features, fixes, refactors, scripts.

| Category | Criterion | Test | Pass Condition |
|----------|-----------|------|----------------|
| Functional | Unit test coverage | Run test suite | All existing tests pass; new code has tests for declared behaviors |
| Functional | Edge cases covered | Review against spec's edge case list | All listed edge cases have either test coverage or explicit handling |
| Structural | Naming conventions | Automated linter / style check | Zero violations against standards file |
| Structural | File organization | Manual review | Files in correct directories; no orphan files; imports clean |
| Structural | Complexity bounds | Static analysis | No function exceeds declared line/complexity limit |
| Error handling | Error paths tested | Manual review + unit tests | Every error condition in spec has explicit handling; no unhandled exceptions in declared paths |
| Error handling | Error messages | Code review | Error messages are actionable; no raw system exceptions surfaced to users |
| Performance | No regressions | Run performance baseline | No measured regression beyond declared tolerance |
| Security | No new vulns | Automated scan + manual review | No OWASP Top 10 violations; secrets not in code or logs |
| Documentation | Public APIs documented | Doc coverage check | All public methods, classes, and endpoints have documentation comments |

**Conditional criteria (include when applicable):**
- If spec includes async code: cancellation token handling verified; no fire-and-forget
- If spec touches database: migration is reversible; no locking queries on hot tables
- If spec adds external dependency: dependency is pinned; license is approved

---

### Template: Document Output

Use for specs that produce documents — reports, analyses, proposals, summaries.

| Category | Criterion | Test | Pass Condition |
|----------|-----------|------|----------------|
| Content completeness | All required sections present | Check against spec's output format | Every declared section exists; none are empty |
| Content accuracy | Key claims verifiable | Manual review | Every factual claim is traceable to a cited source or explicit attestation |
| Source coverage | All spec'd sources used | Cross-reference | Every source in spec's Section 12 is represented in the output |
| Contradiction handling | Conflicting sources surfaced | Manual review | Contradictions between sources are noted, not silently resolved |
| Format compliance | Structure matches spec | Template comparison | Document structure matches the declared output format exactly |
| Audience appropriateness | Tone and terminology | Manual review | Technical depth matches declared audience; no undefined jargon |
| Length compliance | Length within bounds | Word/page count | Output is within ±20% of declared length target |

---

### Template: API or Integration Output

Use for specs that produce API integrations, data pipelines, or system connections.

| Category | Criterion | Test | Pass Condition |
|----------|-----------|------|----------------|
| Contract compliance | Request/response matches spec | Integration test | All endpoints/events produce exactly the structure declared in spec |
| Error behavior | Error codes and messages | Integration test with forced errors | All declared error conditions produce the correct error code and structured response |
| Rate limits | Behavior under high load | Load test | System degrades gracefully; no data loss; correct back-pressure signals |
| Idempotency | Duplicate calls | Integration test with repeats | Idempotent operations produce identical results on repeat calls |
| Authentication | Auth boundary | Security test | All protected endpoints require valid credentials; rejected credentials produce correct error |
| Logging | Audit trail | Log inspection | All operations produce structured log entries with required fields |
| Rollback | Partial failure recovery | Failure injection test | Failure at any defined checkpoint leaves system in a known, recoverable state |

---

### Template: Configuration or Infrastructure Output

Use for specs that produce IaC, deployment configurations, environment definitions.

| Category | Criterion | Test | Pass Condition |
|----------|-----------|------|----------------|
| Idempotency | Re-apply produces no change | Apply twice; diff | Second apply produces zero-diff |
| Naming compliance | Resources named correctly | Linter + manual | All resources conform to naming standard |
| Secrets management | No secrets in config | Automated scan | Zero secrets in plaintext; all secret references use approved secrets manager |
| Drift detection | Actual state matches declared | State comparison | Deployed resources match declared state |
| Rollback plan | Rollback procedure tested | Manual test or documented procedure | Rollback procedure is documented and verified to restore known-good state |
| Cost impact | Estimated cost within declared limit | Cost estimation tool | Projected cost is within the declared budget limit for this deployment |

---

### Composing Validation Into Specs

In the canonical spec template, Section 6 (Success Criteria & Acceptance Tests) is where these templates land. The practitioner:

1. Selects the appropriate validation template(s) from the library
2. Marks which criteria are applicable for this specific task
3. Fills in the specific values (numbers, limits, tools)
4. Adds any task-specific criteria not covered by the template
5. Signs the criteria as reviewable: "A reviewer who validates this output should be able to answer all questions above with a definitive yes or no."

The test for good success criteria is the last sentence: if any criteria cannot be answered definitively yes or no by a human reviewer who has only the spec and the output, those criteria are aspirational statements, not validation criteria. Rewrite them until they can be evaluated.

---

## Therefore

> **Validation templates provide structured, category-complete success criteria for common output types — code, documents, APIs, and infrastructure. They solve the two failure modes of validation: missing criteria (nothing to validate against) and untestable criteria (judgment deferred to review time). Used as the starting point for spec Section 6, they ensure every spec closes the spec-execute-validate loop with the same rigor regardless of who wrote it.**

---

## Connections

**This pattern assumes:**
- [Why Repertoires Matter](01-why-repertoires-matter.md)
- [The Canonical Spec Template — Section 6](../sdd/07-canonical-spec-template.md)
- [Failure Modes in Agent Systems](../agents/07-failure-modes.md)

**This pattern enables:**
- Org-specific validation template additions
- The Spec Gap Log as a validation quality driver
- Governance review against consistent acceptance standards *(Part VII)*

---

*This concludes Part VI: Standards & Repertoires.*

*Continue to [Part VII: Operating the System](../operating/01-skill-matrix.md)*


