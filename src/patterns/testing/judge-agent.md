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

## Forces

- **Automation vs. subjectivity.** Semantic evaluation of quality is inherently subjective. Different humans rate the same output differently. Automating that judgment requires training an agent on your specific quality criteria, which itself requires human calibration and ongoing adjustment.
- **Judge reliability vs. judge calibration cost.** A judge agent that has been carefully calibrated against human evaluations is reliable but expensive to train. An uncalibrated judge might confidently agree with bad outputs. The investment in calibration is front-loaded.
- **Judge scope vs. judge independence.** If the judge agent is too similar to the agent being judged (same model, same training), it may not catch the errors the original agent makes. If it's too different (different model, different capabilities), it may evaluate dimensions the original agent never attempted. The judge needs independence but not so much that it evaluates a completely different task.

---

## The Solution

Deploy a **judge agent** — a separate agent (Advisor archetype) that evaluates another agent's output against declared quality criteria.

1. **The judge has its own spec.** It is not the same agent evaluating its own output. It is a separate agent with independent constraints and criteria.
2. **Quality criteria are declared.** The judge evaluates against specific dimensions: completeness, accuracy, relevance, coherence, citation quality — whatever the spec defines as success.
3. **The judge produces a structured evaluation,** not a pass/fail. Scores per criterion, specific citations of strengths and weaknesses, overall assessment.
4. **The judge does not modify the output.** It evaluates. Modification is a separate step, triggered only if the evaluation identifies issues.
5. **Judge reliability is measured.** Compare judge evaluations against human evaluations on a sample. Calibrate the judge's criteria when its assessments diverge from human judgment.

**Example:** Code review agent produces a 300-line review of a proposed refactor. Judge agent is given the review instructions: "Evaluate the code review on: completeness (all major changes mentioned?), correctness (does the reviewer understand the code?), tone (constructive, not dismissive?), and actionability (would the author know what to do with this feedback?)" Judge produces: `{ completeness: 8/10, correctness: 9/10, tone: 7/10, actionability: 8/10, summary: "Review covers most changes. One misunderstanding on line 47. Feedback is honest but could be more collaborative." }` The judge doesn't fix the review — it flags it. Humans then decide whether to send it as-is or route it back for revision.

---

## Resulting Context

- **Quality variation is detectable.** An agent that usually produces thorough, coherent analysis but occasionally producesoratory boilerplate is caught by the judge, not invisibly released to users.
- **Judge disagreement is diagnostic.** When the judge's evaluation diverges from human assessment on a sample, it's a signal to adjust the judge's criteria or the original spec.
- **Output quality is traceable.** Each output has a judge's evaluation. You can correlate judge scores with downstream outcomes (was the recommendation acted on? was it correct?), improving the quality model over time.
- **Standards are explicit and tunable.** The judge's criteria (completeness: 8/10 required) are visible and can be adjusted. Teams can see what the bar is.

---

## Therefore

> **When output quality requires semantic evaluation, deploy a judge agent with its own spec and declared quality criteria. The judge evaluates; it does not modify. Calibrate the judge against human evaluations periodically.**

---

## Connections

- [Output Validation Gate](../safety/output-validation-gate.md) — the judge is the semantic tier of the validation gate
- [Spec Conformance Test](spec-conformance.md) — conformance tests handle structural validation; the judge handles semantic evaluation
- [The Advisor Archetype](../../architecture/archetypes/advisor.md) — the judge is an Advisor: it informs, it does not act
- [Anomaly Detection Baseline](../observability/anomaly-baseline.md) — judge score trends can detect quality drift