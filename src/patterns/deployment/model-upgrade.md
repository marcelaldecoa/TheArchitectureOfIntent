# Model Upgrade Validation

---

> *"The model changed. The spec didn't. Does the agent still behave correctly?"*

---

## Context

The underlying language model is being upgraded — a new version, a different model, a fine-tuned variant. The specs, tools, and skills remain the same. You need to verify that existing specs still work correctly under the new model.

---

## The Solution

Re-run the **full validation suite against the new model** before deploying model changes to production.

1. **Run all conformance tests.** Every spec's test suite runs against the new model. Failures indicate behavioral changes that the spec didn't anticipate.
2. **Compare output quality.** Use golden output comparison or judge agent evaluation to detect quality changes that don't fail tests but change output characteristics.
3. **Track cost changes.** New models may have different token economics. Cost per correct output may change.
4. **Model changes that cause spec violations require spec review.** If the new model can't follow a constraint that the old model followed, the decision is: update the spec, or don't upgrade the model for this agent.

---

## Therefore

> **Before deploying a model upgrade, re-run all conformance tests and compare output quality against the previous model. Spec violations from model changes require spec review — not silent acceptance.**

---

## Connections

- [Spec Conformance Test](../testing/spec-conformance.md) — the test suite that gets re-run
- [Evaluation by Judge Agent](../testing/judge-agent.md) — semantic quality comparison across model versions
- [Cost Tracking](../observability/cost-tracking.md) — model changes affect cost
- [Canary Deployment](canary.md) — model upgrades can be canary-deployed to compare in production
