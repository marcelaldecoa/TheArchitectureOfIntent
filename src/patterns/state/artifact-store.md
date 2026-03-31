# Artifact Store

---

> *"Agent outputs that matter should outlive the conversation that produced them."*

---

## Context

Agents produce work products — generated code, reports, analysis documents, test results, configuration files. These are not transient conversation outputs; they are durable artifacts that will be used, reviewed, versioned, and maintained.

---

## Problem

Without a declared artifact store, agent outputs live in conversation history, temporary files, or clipboard pastes. They are hard to find, impossible to version, and lost when the conversation ends. Multiple agents producing related artifacts scatter them across different locations with no coherent organization.

---

## The Solution

Store agent-produced artifacts in a **declared, versioned, retrievable location** — separate from conversation history.

1. **The spec declares where artifacts are stored.** A directory, an object store, a repository. The location is part of the spec, not an afterthought.
2. **Artifacts are named and typed.** Each artifact has a name that reflects its content and a type (code, document, analysis, test result) that determines its handling.
3. **Artifacts are linked to the spec that produced them.** Each artifact carries metadata: the spec_id, the agent that produced it, the timestamp, and the validation status.
4. **Artifacts are versioned.** When a task is re-executed with an updated spec, the new artifacts don't overwrite the old ones — they create a new version.

---

## Therefore

> **Store agent-produced artifacts in a declared, versioned location linked to the spec that produced them. Artifacts are organizational assets, not ephemeral conversation byproducts.**

---

## Connections

- [Shared Context Store](shared-context.md) — intermediate pipeline state is stored in the context store; final outputs go to the artifact store
- [Checkpoint and Resume](checkpoint-resume.md) — checkpoints are pipeline state; artifacts are completed outputs
- [Spec Versioning](../deployment/spec-versioning.md) — artifacts are versioned alongside the spec versions that produced them
- [Structured Execution Log](../observability/execution-log.md) — the execution log links each artifact to the execution that created it
