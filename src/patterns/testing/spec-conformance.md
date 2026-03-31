# Spec Conformance Testing

---

> *"For every constraint in the spec, there must be a test that would fail if the constraint were violated. And every time the spec changes, those tests must run again."*

---

## Context

An agent operates under a spec. The spec declares constraints, success criteria, invariants, and scope boundaries. You need to verify — systematically, not by subjective judgment — that the agent follows the spec. And when the spec changes (constraints tightened, scope expanded, criteria added), you need to verify that the change produces the intended effect without breaking existing behavior.

---

## Problem

Without conformance tests, validation is subjective. A reviewer reads the output and decides if it "looks right." Different reviewers reach different conclusions. Constraints that were carefully written into the spec are never systematically checked. When the spec changes, there is no baseline to compare against — the team doesn't know whether the change improved things or broke them.

Two complementary but distinct failures occur:

1. **Initial conformance is never verified.** The spec says "refund amount must come from order data" but no test checks it. The constraint exists on paper; the agent may or may not follow it.
2. **Spec changes break behavior silently.** A tightened constraint causes a previously-working workflow to fail, but nobody knows until a user reports it — days or weeks later.

---

## Forces

- **Spec precision vs. testing overhead.** Each constraint in the spec needs at least one test. A 15-constraint spec needs at least 15 tests. Writing and maintaining them costs effort — but unverified constraints are fiction.
- **Static verification vs. probabilistic output.** Agent outputs are probabilistic. The same input may produce slightly different outputs. Tests must accommodate this variation while still catching constraint violations.
- **Boundary precision vs. fuzzy reality.** Numeric constraints have clear boundaries ($100 max → test $99, $100, $101). Semantic constraints ("responses must be professional in tone") are harder to test programmatically.
- **Regression safety vs. intentional change.** When a spec is tightened, some previously-valid outputs become invalid. This is intentional. The test suite must distinguish intentional behavioral change from unintended regression.

---

## The Solution

Build a **conformance test suite** that maps directly to the spec's constraints and success criteria. Run it on initial deployment. Re-run it on every spec change.

### Initial Conformance

The conformance suite contains five categories of test, each mapping to a different spec element:

- **Constraint tests.** For each numbered constraint (C1, C2, ...), one or more tests that verify compliance. The test supplies inputs designed to exercise the constraint and verifies the agent respects it.
- **Success criteria tests.** For each acceptance criterion, a test that checks it against representative workloads.
- **Boundary tests.** For constraints with numeric limits, tests at and beyond the boundary — verifying that the boundary is enforced, not just observed on typical inputs.
- **Negative tests.** Inputs that should trigger constraint enforcement, verifying the agent refuses or escalates rather than complying.
- **Scope boundary tests.** Requests that are within scope, borderline, and clearly out of scope, verifying the agent handles each category correctly.

The principle: every constraint in the spec becomes at least one test. An untested constraint is a constraint that may not be followed. The conformance suite is the executable version of the spec.

### Regression on Spec Change

When the spec changes, the conformance suite must evolve with it:

- **New constraints need new tests** before the updated spec is deployed.
- **Tightened constraints may invalidate previous behavior.** Document the change and update expected behavior explicitly — this is intentional, not a regression.
- **Relaxed constraints should not break tests.** If one does, the relaxation had unintended side effects.
- **Golden output comparison** for critical outputs: compare agent output under the new spec against a known-good reference from the old spec. Deviation beyond a threshold triggers review.
- **Version-linked test sets.** Each spec version has a corresponding test set version, stored and deployed together.

### Testing Probabilistic Output

Agent output is not deterministic. The same input may produce slightly different outputs across runs. Conformance tests must account for this:

- **Structural tests** (field presence, format, schema) should pass deterministically.
- **Behavioral tests** (constraint compliance) should be evaluated over multiple runs. A constraint violated in 1 of 10 runs is a constraint that will be violated in production.
- **Quality tests** (tone, completeness, coherence) use thresholds and may employ a [judge agent](judge-agent.md) for evaluation.

---

## Resulting Context

- **Specs become enforceable, not advisory.** Every constraint has a test. Violations are caught before deployment.
- **Spec changes are safe.** Regression testing catches unintended side effects before they reach users.
- **Conformance is measurable.** The pass rate across the test suite is a quantitative signal — not a subjective "it looked fine."
- **The test suite becomes the executable spec.** Over time, the conformance suite is the most precise description of what the agent actually does — more precise than the spec's natural language.

---

## Therefore

> **Map every spec constraint and success criterion to at least one test. Boundary constraints get boundary tests. Negative constraints get violation tests. Re-run the full suite on every spec change. New constraints need new tests. Tightened constraints need documented expectation changes. The conformance suite is the executable version of the spec.**

---

## Connections

- [Output Validation Gate](../safety/output-validation-gate.md) — conformance tests are the design-time version of runtime validation
- [Adversarial Input Test](adversarial-input.md) — adversarial tests go beyond conformance to test resilience against hostile input
- [Multi-Agent Integration Test](multi-agent-integration.md) — integration tests verify that conformant individual agents work correctly together
- [The Living Spec](../../sdd/06-living-specs.md) — conformance test failures can reveal spec gaps that feed back into spec evolution
- [Spec Versioning](../deployment/spec-versioning.md) — test sets are versioned alongside specs
- [Canary Deployment](../deployment/canary.md) — canary deploys compare old and new spec versions in production after regression tests pass
- [Evaluation by Judge Agent](judge-agent.md) — for semantic quality tests that can't be checked programmatically
