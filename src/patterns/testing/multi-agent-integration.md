# Multi-Agent Integration Test

---

> *"Each agent works correctly alone. Do they work correctly together?"*

---

## Context

Multiple agents are deployed in a pipeline or coordinated system. Each agent passes its conformance tests individually. But the system as a whole has not been tested — agent-to-agent handoffs, shared context consistency, and coordinated failure handling are unverified.

---

## The Solution

Test the **full pipeline end-to-end** with representative inputs, verifying both correctness and coordination.

1. **End-to-end happy path.** Send representative inputs through the full pipeline. Verify the final output is correct and all inter-agent contracts were honored.
2. **Cross-agent consistency.** Verify that what Agent A sends matches what Agent B expects. Naming conventions, data formats, and schema versions must align.
3. **Failure injection at each boundary.** Simulate failure at each agent handoff. Verify the pipeline handles it according to the spec — retry, escalate, or halt.
4. **One test per declared failure mode.** If the pipeline spec declares "if the Guardian rejects the output, return to the Synthesizer with the failure report," test that specific interaction.

---

## Therefore

> **Test multi-agent systems end-to-end. Verify cross-agent contracts at every handoff. Inject failures at each boundary. One integration test per declared failure mode.**

---

## Connections

- [Agent-to-Agent Contract](../coordination/agent-contract.md) — integration tests verify contracts
- [Sequential Pipeline](../coordination/sequential-pipeline.md) — integration tests cover the full pipeline
- [Supervisor Agent](../coordination/supervisor.md) — integration tests verify the supervisor catches coordination failures
- [Spec Conformance Test](spec-conformance.md) — unit-level conformance is a prerequisite for integration testing
