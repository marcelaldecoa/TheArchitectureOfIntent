# Spec Conformance Test

---

> *"For every constraint in the spec, there must be a test that would fail if the constraint were violated."*

---

## Context

You have a spec. The agent has produced output. You need to verify that the agent followed the spec.

---

## Problem

Without conformance tests, validation is subjective — a reviewer reads the output and decides if it "looks right." Different reviewers reach different conclusions. Constraints that were carefully written into the spec are never systematically checked.

---

## The Solution

For each constraint and success criterion in the spec, write a **corresponding test that would fail if the constraint were violated**.

1. **Constraint tests.** For each numbered constraint (C1, C2, ...), one or more tests that verify compliance. C3 says "refund amount must come from order data" → test: provide an order with amount X and verify the refund request uses X, not a user-stated amount.
2. **Success criteria tests.** For each acceptance criterion, a test checking the criterion. "All primary actions complete within 2 seconds" → test: measure execution time.
3. **Boundary tests.** For constraints with numeric limits, test at the boundary. "Max refund $100" → test with $99, $100, $101.
4. **Violation tests.** Submit inputs that should trigger constraint enforcement. Verify the agent refuses or escalates rather than complying.

---

## Therefore

> **Map every spec constraint and success criterion to at least one test. Boundary constraints get boundary tests. Negative constraints get violation tests. The conformance suite is the executable version of the spec.**

---

## Connections

- [Output Validation Gate](../safety/output-validation-gate.md) — conformance tests are the design-time version of runtime validation
- [Adversarial Input Test](adversarial-input.md) — adversarial tests go beyond conformance to test resilience
- [Regression on Spec Change](regression-spec-change.md) — conformance tests are re-run when specs change
- [The Living Spec](../../sdd/06-living-specs.md) — conformance test failures can reveal spec gaps
