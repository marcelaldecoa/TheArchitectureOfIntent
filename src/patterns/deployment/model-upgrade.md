# Model Upgrade Validation

---

> *"The model changed. The spec didn't. Does the agent still behave correctly?"*

---

## Context

The underlying language model is being upgraded — a new version of the same model family, a different provider's model, or a fine-tuned variant. The specs, tools, skills, and governance framework remain the same. But model behavior is not deterministic across versions; a new model may follow constraints differently, reason with different patterns, produce outputs with different characteristics, or cost more per token.

---

## Problem

A research synthesis agent uses a particular model and has a spec declaring: "Synthesis must cite sources for every factual claim." The conformance test suite passes; the spec is enforced. The team upgrades to a newer model version, believing it to be a straightforward improvement. In production, 8% of synthesis outputs are missing citations — the new model reasons well but cites less frequently than the old one. The spec was correct. The model's ability to follow the constraint changed. Diagnosis takes days because the failure is intermittent and looks like a spec gap rather than a model behavioral shift.

---

## Forces

- **Specs assume consistent model behavior.** When the model changes, constraint-following may change even though the spec is unchanged. A passing test suite on model A does not guarantee passing on model B.
- **Quality changes are often invisible to structural tests.** Token distribution, reasoning depth, output style, and citation behavior may shift in ways that pass schema validation but change substantive quality.
- **Cost-benefit analysis is opaque until measured.** A new model may improve quality on some dimensions but increase cost per request by 40%. You need data before deciding whether to upgrade.
- **Rollback is simpler if you test first.** Finding an issue before production deployment means rollback is a non-event rather than an incident.

---

## The Solution

Re-run the **full validation suite against the new model** before deploying model changes to production. Include conformance tests, quality comparisons, and cost analysis.

1. **Run all conformance tests against the new model.** Every spec that will execute against this model runs its test suite on the new model version. Track which tests pass and fail on old vs. new. Failures indicate behavioral changes the spec didn't anticipate.
2. **Compare output quality using golden outputs or judge agents.** Conformance tests catch constraint violations. Quality comparison catches changes that don't fail tests but change output characteristics — reasoning depth, citation frequency, tone, accuracy. Use a judge agent to evaluate a sample of outputs from both models against the same quality criteria.
3. **Measure cost changes.** Track tokens-per-completion and cost-per-correct-output on both models. A model that doubles token cost but produces 10% better quality may or may not be worth it — that's a business decision, not a technical one.
4. **Model changes that cause spec violations require an explicit decision.** If the new model can't follow a constraint the old model followed, the decision tree is: (a) update the spec to relax the constraint, (b) keep the old model for this agent, or (c) add skill/prompt adjustments to help the new model follow the constraint. Never silently accept a spec violation.

**Example:** A compliance agent has 247 conformance tests. Before upgrading models, the team runs all 247 tests against the new model. 245 pass; 2 fail. Both involve edge-case tax code interpretations where the new model reasons differently. The team reviews: one is a legitimate interpretation difference (spec needs clarification), one is a misunderstanding fixable with a prompt adjustment. A judge agent compares output quality: the new model produces more detailed reasoning and cites regulations more precisely. Cost per token increases 22%, but cost per correct output (including reduced rework) decreases 5%. The team approves the upgrade with the spec clarification and prompt fix.

---

## Resulting Context

- **Model changes are validated before production exposure.** Spec violations and cost changes are known before deployment, not discovered by users.
- **The decision to upgrade is data-driven.** The team knows exactly what quality changes and cost changes they're accepting.
- **Specs remain enforceable across model generations.** If a new model can't follow the spec, that's discovered in testing, not in production incidents.
- **Model upgrades become routine rather than risky.** With a systematic validation process, teams upgrade models more frequently and with smaller risk per upgrade.

---

## Therefore

> **Before deploying a model upgrade, re-run all conformance tests and compare output quality against the previous model. Spec violations from model changes require spec review — not silent acceptance.**

---

## Connections

- [Spec Conformance Testing](../testing/spec-conformance.md) — the test suite that gets re-run
- [Evaluation by Judge Agent](../testing/judge-agent.md) — semantic quality comparison across model versions
- [Cost Tracking per Spec](../observability/cost-tracking.md) — model changes affect cost
- [Canary Deployment](canary.md) — model upgrades can be canary-deployed to compare in production
