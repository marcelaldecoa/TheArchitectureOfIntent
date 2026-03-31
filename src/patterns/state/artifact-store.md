# Artifact Store

---

> *"Agent outputs that matter should outlive the conversation that produced them."*

---

## Context

Agents produce work products — generated code, reports, analysis documents, test results, configuration files. These are not transient conversation outputs; they are durable artifacts that will be used, reviewed, versioned, and maintained.

---

## Problem

Without a declared artifact store, agent outputs live in conversation history, temporary files, or clipboard pastes. They are hard to find, impossible to version, and lost when the conversation ends. Multiple agents producing related artifacts scatter them across different locations with no coherent organization.

**Concrete scenario:** A code generation pipeline produces three artifacts: a generated microservice, unit tests, and an OpenAPI spec. The microservice is saved to `/tmp/output.go` (lost when the session ends). The tests are quoted in chat history (not versioned). The spec is exported to the user's desktop. Two weeks later, the spec is updated, but there's no way to know if the old microservice and tests match the new spec. A second code generation run produces new artifacts in different locations.

---

## Forces

- **Need durable, discoverable outputs** vs. **overhead of managing an artifact store** (requires infrastructure, naming conventions)
- **Need version history** (each spec change should create new artifacts) vs. **storage costs** (every variation is persisted)
- **Need to link artifacts to specs** (provenance tracking) vs. **metadata management complexity** (who maintains the links?)
- **Need atomic artifact production** (all artifacts of a task succeed or fail together) vs. **partial artifacts being useful** (a broken test suite with working code)

---

## The Solution

Store agent-produced artifacts in a **declared, versioned, retrievable location** — separate from conversation history.

1. **The spec declares where artifacts are stored.** A directory, an object store, a repository. The location is part of the spec, not an afterthought.
2. **Artifacts are named and typed.** Each artifact has a name that reflects its content and a type (code, document, analysis, test result) that determines its handling.
3. **Artifacts are linked to the spec that produced them.** Each artifact carries metadata: the spec_id, the agent that produced it, the timestamp, and the validation status.
4. **Artifacts are versioned.** When a task is re-executed with an updated spec, the new artifacts don't overwrite the old ones — they create a new version.

**Example:** A report-generation agent. The spec declares:
```
artifacts:
  store: "s3://reports-prod/acme-corp/Q1-2026/"
  - name: "executive_summary"
    type: "document"
    format: "markdown"
  - name: "detailed_analysis"
    type: "document"
    format: "html"
  - name: "supporting_data"
    type: "dataset"
    format: "json"
```
On the first run (spec v1.0), artifacts are written to `Q1-2026/v1.0/`. On the second run (spec v1.1, with an updated format), artifacts go to `Q1-2026/v1.1/`. Each artifact carries metadata: `{"spec_id": "spec-q1-2026", "produced_by": "report-gen-v5", "timestamp": "2026-03-15T14:22:00Z", "validation": "passed"}`. The report portal links the artifact to its spec version and shows the lineage.

---

## Resulting Context

- **Artifacts are discoverable and retrievable** by spec version, timestamp, and agent
- **Version history is clear** — no confusion about which artifacts correspond to which spec
- **Artifacts can be reviewed and approved** as a unit before deployment
- **Lineage is auditable** — you can query what artifacts were produced by each agent version

---

## Therefore

> **Store agent-produced artifacts in a declared, versioned location linked to the spec that produced them. Artifacts are organizational assets, not ephemeral conversation byproducts.**

---

## Connections

- [Shared Context Store](shared-context.md) — intermediate pipeline state is stored in the context store; final outputs go to the artifact store
- [Checkpoint and Resume](checkpoint-resume.md) — checkpoints are pipeline state; artifacts are completed outputs
- [Spec Versioning](../deployment/spec-versioning.md) — artifacts are versioned alongside the spec versions that produced them
- [Structured Execution Log](../observability/execution-log.md) — the execution log links each artifact to the execution that created it