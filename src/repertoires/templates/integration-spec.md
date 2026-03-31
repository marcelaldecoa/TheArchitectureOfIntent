# Integration Spec Template

**Repertoire & Reference**

---

> *Use this template when an Executor agent will connect two systems, implement an API, configure an event-driven integration, or build a data pipeline. Every section marked **[REQUIRED]** must be completed. The data contract section must be precise enough that the implementing agent never needs to infer a field's type, name, or optionality.*

---

## How to Use This Template

Integration specs have higher completeness requirements than feature specs because the failure modes are harder to detect and more expensive to reverse. A feature spec with a vague constraint produces code that fails visibly in testing. An integration spec with a vague contract produces a system that works in happy-path tests and fails in production under specific conditions that were never tested.

The data contract section (§6) is the most critical. Every field must be explicitly declared.

---

## Integration Spec

**Spec ID:** `[REQUIRED: INT-YYYY-NNN]`  
**Title:** `[REQUIRED: Source → Target: Purpose]`  
**Template:** `integration-spec-v1.0`  
**Date:** `[REQUIRED]`  
**Author:** `[REQUIRED]`  
**Source System Owner:** `[REQUIRED]`  
**Target System Owner:** `[REQUIRED]`  
**Spec Status:** `Draft` / `Under Review` / `Approved`

---

### Section 1 — Integration Purpose

**[REQUIRED]**

**Why this integration exists:**  
*One sentence: what business or technical need this connection serves.*

**Trigger:** [What causes data/events to flow — schedule / event / API call / user action]  
**Direction:** [Source → Target / Bidirectional]  
**Expected volume:** [Records per batch / events per second / peak load]  
**Latency requirement:** [Real-time / Near-real-time (< N seconds) / Batch (N minutes/hours)]

---

### Section 2 — Source System

**[REQUIRED]**

**System name:** [Name]  
**System type:** [REST API / GraphQL / Database / Event bus / File system / Queue]  
**Environment:** [Production / Staging / Both — with routing rules]  
**Authentication:** [OAuth2 / API key / mTLS / service account — specify token scope]  
**Rate limits:** [Requests per second / minute / hour before throttling]  
**Versioning:** [API version or schema version being consumed]  
**Guaranteed delivery:** [At-least-once / At-most-once / Exactly-once]

**Source contact / owner:** [Team and escalation path for source system issues]

---

### Section 3 — Target System

**[REQUIRED]**

**System name:** [Name]  
**System type:** [REST API / Database / Event bus / File system / Queue]  
**Environment:** [Production / Staging / Both]  
**Authentication:** [OAuth2 / API key / service account — specify write scope]  
**Idempotency support:** [Supports idempotency key / Requires deduplication logic / N/A]  
**Write semantics:** [Insert / Upsert / Replace — and what happens on conflict]  
**Target contact / owner:** [Team and escalation path for target system issues]

---

### Section 4 — Error Handling

**[REQUIRED]**

| Failure Class | Condition | Action | Retry? | Escalation |
|---------------|-----------|--------|--------|------------|
| Source unavailable | HTTP 5xx / connection timeout | [Pause N minutes; retry M times] | Yes | [Alert after M failures] |
| Auth failure | HTTP 401 / 403 | Stop; do not retry; escalate | No | Immediate |
| Validation failure | Record fails schema check | [Route to dead-letter / skip with log / abort batch] | No | [Alert if DLQ > N records] |
| Target write failure | HTTP 4xx on write | [Inspect payload; log specifics; skip / abort] | Conditional | [Alert if > N in 1 hour] |
| Partial batch failure | N of M records fail | [Complete successful records; route failures to DLQ] | No | [Alert always] |
| Rate limit exceeded | HTTP 429 | Backoff per `Retry-After` header | Yes | [Alert if > N rate-limit hits per hour] |

**Dead letter queue / failure destination:** [Specific location or system]  
**Operator notification:** [PagerDuty policy / Slack channel / email group]

---

### Section 5 — Volume & Rate Limits

**[REQUIRED]**

| Metric | Expected | Peak | Hard Limit |
|--------|----------|------|------------|
| Records per batch | | | |
| Batches per day | | | |
| API calls per minute (source) | | | |
| API calls per minute (target) | | | |
| Data volume per batch (MB) | | | |

**Behavior when hard limit is approached:**  
When volume exceeds [% of hard limit], the integration should [throttle / split into sub-batches / escalate and pause].

---

### Section 6 — Data Contract

**[REQUIRED — every field must be declared]**

#### Source Record Structure

| Field | Type | Required? | Source Path | Notes |
|-------|------|-----------|-------------|-------|
| `[field_name]` | `string` | Yes | `data.field_name` | [Constraints, allowed values, max length] |
| `[field_name]` | `integer` | No | `data.count` | [Default if absent: 0] |
| `[field_name]` | `ISO8601 datetime` | Yes | `metadata.created_at` | [Always UTC] |
| *[add all fields]* | | | | |

#### Target Record Structure

| Field | Type | Mapped From | Transformation | Required? |
|-------|------|-------------|---------------|-----------|
| `[target_field]` | `string` | `source.field_name` | [Exact copy / lowercase / truncate to 255] | Yes |
| `[target_field]` | `string` | *derived* | [concat(source.first, ' ', source.last)] | Yes |
| `[target_field]` | `string` | *constant* | `"IMPORTED"` | Yes |
| *[add all fields]* | | | | |

**Fields present in source but NOT written to target:**  
*[List explicitly — absence of a target mapping for a source field must be intentional, not accidental.]*

---

### Section 7 — Validation

**[REQUIRED]**

*Complete applicable rows from the [API/Integration Validation Template](../05-validation-templates.md).*

| Criterion | Test | Pass Condition |
|-----------|------|----------------|
| Contract compliance | Integration test: valid record | Target receives exactly the declared structure |
| Error behavior | Integration test: inject each error class | Each error class produces the declared response |
| Rate limit behavior | Load test at peak volume | No data loss; back-pressure signals correctly |
| Idempotency | Send same record twice | Target contains exactly one copy |
| Rollback | Inject failure at midpoint | System returns to known state; no partial writes |
| [Task-specific] | | |

**Testing environment requirement:** [Staging with production-equivalent data / production with synthetic data / dedicated integration test environment]

---

### Section 8 — Rollback Plan

**[REQUIRED]**

**Rollback trigger:** [What condition causes a rollback to be initiated]  
**Rollback procedure:**
1. [Step 1]
2. [Step 2]
3. [Verify rollback is complete: how]

**Rollback tested?** [Yes — tested on staging / No — procedure documented but untested]  
**Rollback window:** [How long after deployment rollback is viable]

---

### Section 9 — Agent Execution Instructions

**[REQUIRED]**

**Skills to load** *(if applicable)*
- `rest-api-standards`: applies if implementing REST endpoints
- `[other relevant skill]`

**Authorized actions:**
- Read from: [source system as declared in §2]
- Write to: [target system as declared in §3]
- Write to: [dead letter queue if declared in §4]
- NOT authorized: schema changes to either system
- NOT authorized: routing data to any destination not declared in §6
- NOT authorized: contacting system owners directly

**Completion signal:** *When all records are processed (success or DLQ) and the validation criteria in §7 are met, produce a summary report to [location].*

---

### Spec Approval

| | Name | Date |
|-|------|------|
| Author | | |
| Source system owner | | |
| Target system owner | | |
| Technical reviewer | | |
| Approved for execution | | |

---

*Back to: [Spec Template Library](../03-spec-template-library.md)*

