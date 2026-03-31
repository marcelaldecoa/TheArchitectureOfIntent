# Evaluation by Judge Agent

---

> *"When correctness can't be checked programmatically, let another agent evaluate — under its own spec."*

---

## Context

An agent produces output whose quality cannot be verified by schema checks or keyword matching — a written analysis, a code review summary, a synthesized recommendation. A human could evaluate it, but human review doesn't scale. You need automated quality evaluation that goes beyond structural validation.

---

## Problem

Programmatic validation catches structural errors but misses semantic quality: is the analysis insightful or superficial? Is the code review thorough or perfunctory? Is the recommendation well-reasoned or generic? Without semantic evaluation, these quality dimensions go unmeasured.

---

## The Solution

Deploy a **judge agent** — a separate agent (Advisor archetype) that evaluates another agent's output against declared quality criteria.

1. **The judge has its own spec.** It is not the same agent evaluating its own output. It is a separate agent with independent constraints and criteria.
2. **Quality criteria are declared.** The judge evaluates against specific dimensions: completeness, accuracy, relevance, coherence, citation quality — whatever the spec defines as success.
3. **The judge produces a structured evaluation,** not a pass/fail. Scores per criterion, specific citations of strengths and weaknesses, overall assessment.
4. **The judge does not modify the output.** It evaluates. Modification is a separate step, triggered only if the evaluation identifies issues.
5. **Judge reliability is measured.** Compare judge evaluations against human evaluations on a sample. Calibrate the judge's criteria when its assessments diverge from human judgment.

---

## Therefore

> **When output quality requires semantic evaluation, deploy a judge agent with its own spec and declared quality criteria. The judge evaluates; it does not modify. Calibrate the judge against human evaluations periodically.**

---

## Connections

- [Output Validation Gate](../safety/output-validation-gate.md) — the judge is the semantic tier of the validation gate
- [Spec Conformance Test](spec-conformance.md) — conformance tests handle structural validation; the judge handles semantic evaluation
- [The Advisor Archetype](../../architecture/archetypes/advisor.md) — the judge is an Advisor: it informs, it does not act
- [Anomaly Detection Baseline](../observability/anomaly-baseline.md) — judge score trends can detect quality drift
