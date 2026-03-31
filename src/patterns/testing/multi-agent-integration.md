# Multi-Agent Integration Test

---

> *"Each agent works correctly alone. Do they work correctly together?"*

---

## Context

Multiple agents are deployed in a pipeline or coordinated system. Each agent passes its conformance tests individually. But the system as a whole has not been tested — agent-to-agent handoffs, shared context consistency, and coordinated failure handling are unverified.

---

## Problem

Individual agent correctness does not guarantee system correctness. Agent A may produce well-formed output that perfectly matches its spec. Agent B may be individually correct. But Agent A's output may not match what Agent B expects — schema version mismatch, naming convention difference, missing required fields. These boundary failures only surface under integration.

---

## Forces

- **Test isolation vs. integration testing.** Unit tests are fast and deterministic. They don't catch boundary failures between components. Integration tests are slower and involve more variability (timing, order dependencies). Both are necessary.
- **Contract explicitness vs. implicit coupling.** Explicit contracts (Agent A promises to produce X format; Agent B declares it expects X format) are clear but require discipline to maintain. Implicit coupling (both agents happen to use the same format) is easier to implement but brittle — a refactor in one agent breaks the other silently.
- **Deterministic assertions vs. behavior assertions.** Testing that "pipeline produces output Y given input X" is deterministic. Testing that "the pipeline handles latency correctly, or that two agents enforce ordering" requires scenario-based tests that are more complex to write and maintain.

---

## The Solution

Test the **full pipeline end-to-end** with representative inputs, verifying both correctness and coordination.

1. **End-to-end happy path.** Send representative inputs through the full pipeline. Verify the final output is correct and all inter-agent contracts were honored.
2. **Cross-agent consistency.** Verify that what Agent A sends matches what Agent B expects. Naming conventions, data formats, and schema versions must align.
3. **Failure injection at each boundary.** Simulate failure at each agent handoff. Verify the pipeline handles it according to the spec — retry, escalate, or halt.
4. **One test per declared failure mode.** If the pipeline spec declares "if the Guardian rejects the output, return to the Synthesizer with the failure report," test that specific interaction.

**Example:** Credit approval pipeline: Requester → Analyzer → Guardian → OutputAgent. Test case: Analyzer produces a structured analysis with `{"risk_score": 0.73, "credit_limit": 15000}`. Guardian expects the risk_score to be a float between 0 and 1 and credit_limit to be a positive integer. Happy path passes. Failure injection: Analyzer produces `{"risk_score": "high"}` (string instead of float). Guardian rejects with structured error. OutputAgent receives the rejection and returns it to the user with "Your analysis couldn't be approved. Contact support." This interaction is tested.

---

## Resulting Context

- **Boundary failures are caught before production.** Contract mismatches, format incompatibilities, and handoff failures surface during test, not during deployment.
- **Failure modes are explicit.** Each declared failure mode in the pipeline spec has a test. If the test doesn't exist, the failure mode isn't actually specified.
- **Pipeline changes are safer.** Adding a new agent to the pipeline requires integration tests for its boundaries. Removing an agent requires reviewing all tests that touched it. These requirements naturally surface gaps.
- **Teams can refactor agents independently.** As long as the agent's output contract remains the same (verified by integration tests), internal refactoring is safe.

---

## Therefore

> **Test multi-agent systems end-to-end. Verify cross-agent contracts at every handoff. Inject failures at each boundary. One integration test per declared failure mode.**

---

## Connections

- [Agent-to-Agent Contract](../coordination/agent-contract.md) — integration tests verify contracts
- [Sequential Pipeline](../coordination/sequential-pipeline.md) — integration tests cover the full pipeline
- [Supervisor Agent](../coordination/supervisor.md) — integration tests verify the supervisor catches coordination failures
- [Spec Conformance Test](spec-conformance.md) — unit-level conformance is a prerequisite for integration testing