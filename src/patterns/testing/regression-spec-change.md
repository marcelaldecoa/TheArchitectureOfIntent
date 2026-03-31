# Regression on Spec Change

---

> *"The spec changed. Does the agent still behave correctly?"*

---

## Context

A spec was updated — a constraint was tightened, a new success criterion was added, a scope was expanded. The agent now operates under the updated spec. You need to verify that the change produces the intended effect without breaking existing behavior.

---

## The Solution

Re-run the **full conformance suite** after every spec change. Compare behavior before and after.

1. **New constraints need new tests.** Every new constraint added to the spec must have corresponding conformance tests before the spec is deployed.
2. **Tightened constraints may break previous behavior.** If the spec now prohibits something that was previously allowed, expect previously-passing tests to need updates. This is intentional — document why.
3. **Relaxed constraints should not break tests.** If a constraint is relaxed, no previously-passing test should fail. If one does, the relaxation had unintended side effects.
4. **Golden output comparison.** For critical outputs, compare the new output against a known-good reference. Deviation beyond a threshold triggers review.

---

## Therefore

> **Re-run the full conformance suite after every spec change. New constraints need new tests. Tightened constraints need documented expectation changes. Relaxed constraints should not break existing tests.**

---

## Connections

- [Spec Conformance Test](spec-conformance.md) — the suite that gets re-run on spec change
- [The Living Spec](../../sdd/06-living-specs.md) — spec changes flow from the living spec practice
- [Spec Versioning](../deployment/spec-versioning.md) — regression tests are linked to spec versions
- [Canary Deployment](../deployment/canary.md) — canary deploys compare old and new spec versions in production
