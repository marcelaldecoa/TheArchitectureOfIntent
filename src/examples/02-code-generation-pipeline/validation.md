# Validating Outcomes

**Applied Examples**

---

> *"Validating a pipeline is different from validating a single agent: you are testing not just what was produced, but whether the stages of production connected correctly."*

---

## How Pipeline Validation Differs

In Example 1, acceptance testing asked: given these inputs, did the agent produce the correct output? The test subject was a single agent and the evaluation was against its spec's success criteria.

In this pipeline, there are three agents that must operate correctly *and* connect correctly to each other. A component that passes Standards Guardian validation in isolation may still be wrong if it doesn't import the path that the service-executor produced. An acceptance suite for a pipeline must test at three levels:

1. **Component correctness** — Does each generated file satisfy its spec's success criteria?
2. **Cross-component consistency** — Do the files reference each other correctly?
3. **Pipeline mechanics** — Does the pipeline behave correctly on failures: validation failures, input failures, overwrite conflicts?

---

## Test Inputs

All tests use the same base input set to enable reproducibility:

**Feature intent document (input A — "User Management Service"):**
```markdown
# UserManagement Service

This service manages user accounts for the platform. It provides CRUD operations
for user profile data.

Entities: User  
Operations: list all users, get user by ID, create user, update user, delete user

Business rules:
- Email addresses must be unique across all users
- Users cannot be deleted if they have active subscriptions (returns 409 Conflict)
```

**Data schema (input B):**
```json
{
  "entity": "User",
  "table": "users",
  "fields": [
    { "name": "id", "type": "uuid", "primaryKey": true },
    { "name": "email", "type": "string", "unique": true, "required": true },
    { "name": "displayName", "type": "string", "required": true },
    { "name": "createdAt", "type": "timestamp", "auto": true },
    { "name": "updatedAt", "type": "timestamp", "auto": true }
  ]
}
```

**Output path:** `./test-output/user-management/`  
**Team ID:** `platform-test`

---

## Test Suite

### Test P-01: Happy path — complete valid scaffold
**Spec criterion:** SC1 (complete scaffold delivery), SC5 (catalog registration)  
**Input:** Feature intent document A + schema B, clean output path  
**Expected:** All 7 components generated, all pass Standards Guardian on first or second attempt, scaffold directory assembled, catalog.register() called with correct parameters  
**Observed:** All 7 components generated. 6 passed on first attempt. One (test file) failed first attempt — the Guardian flagged missing error path test. Retry produced a passing file. Scaffold assembled. Catalog registered with service name `user-management`, team ID `platform-test`, OpenAPI path `./test-output/user-management/openapi.yaml`.  
**Result:** ✅ Pass

---

### Test P-02: Cross-component consistency — import paths
**Spec criterion:** SC2 (cross-component consistency)  
**Input:** Same as P-01  
**Verification method:** Static analysis of generated files — parse imports and verify they reference the correct paths and class names from the naming package  
**Checks performed:**
- `controller.ts` imports `UserService` from `./service` ✅
- `service.ts` imports `UserRepository` from `./repository` ✅
- `controller.test.ts` imports `UserController` from `./controller` ✅
- Endpoint paths in `controller.ts` match paths in `openapi.yaml` ✅
- Endpoint paths in `controller.ts` match paths in `controller.test.ts` ✅  
**Result:** ✅ Pass

---

### Test P-03: Input validation — empty feature intent
**Spec criterion:** SC7 (input validation rejection), C1  
**Input:** Empty feature intent document + valid schema B, clean output path  
**Expected:** Pipeline halts before invoking any executor; returns structured error identifying empty intent document; no files written  
**Observed:** Pipeline returned `{ "status": "failed", "stage": "input_validation", "error": "Feature intent document is empty", "files_generated": [] }`. No executor invocations. No files written.  
**Result:** ✅ Pass

---

### Test P-04: Input validation — invalid schema JSON
**Spec criterion:** SC7, C1  
**Input:** Valid feature intent document A + malformed JSON schema  
**Expected:** Pipeline halts; returns structured error with schema parse error; no files written  
**Observed:** `schema.parse()` returned parse error. Pipeline returned structured error at stage `input_validation`. No executors invoked. No files written.  
**Result:** ✅ Pass

---

### Test P-05: Overwrite protection
**Spec criterion:** SC4 (overwrite protection), C6  
**Input:** Same as P-01, but `./test-output/user-management/controller.ts` already exists (pre-created with placeholder content)  
**Expected:** Pipeline halts before writing any file; returns conflict error identifying the existing file; no files written (including files that do not conflict)  
**Observed (first run):** Pipeline attempted to write files in sequence. When it reached `controller.ts`, detected existing file. Halted. Returned `{ "status": "failed", "stage": "file_write", "conflict": "./test-output/user-management/controller.ts", "files_generated": [] }`. No files were written — not even `repository.ts` which would have been written earlier in sequence.  

**Important finding:** The first run exposed an architectural choice that needed clarification. The pipeline generated all components, validated them all, then wrote them. Since the conflict is detected at write time (Step 5 in the Synthesizer instructions), the validation had already run. An alternative sequence (check for conflicts before generating) would save compute but was explicitly rejected: the intent is to fail fast at the conflict rather than fail before doing any work. The spec annotation in §4 explains why.  
**Result:** ✅ Pass

---

### Test P-06: Standards Guardian first-attempt failure, successful retry
**Spec criterion:** SC3 (standards compliance), C5 (retry limit)  
**Input:** Same as P-01  
**Setup:** Standards Guardian configured to return a `console.log` violation on the first `service-executor` invocation (simulated by injecting `console.log(data)` into the service output before Guardian evaluation)  
**Expected:** Guardian returns fail; Synthesizer invokes service-executor again with violation report; second-attempt output passes  
**Observed:** Guardian flagged `console.log` on first attempt with error severity. Synthesizer invoked service-executor with violation report as context. Second service file did not contain `console.log`. Guardian returned pass. Scaffold assembly continued normally.  
**Result:** ✅ Pass

---

### Test P-07: Standards Guardian double failure — pipeline halt
**Spec criterion:** SC6 (failure report on double validation failure)  
**Input:** Same as P-01  
**Setup:** Guardian configured to return error violation on both first and second submission for `controller-executor` (simulating a case where the Generator cannot satisfy the constraint — injected a required pattern that the executor doesn't know about)  
**Expected:** After second failure, pipeline halts; returns structured failure report with both attempts' violation lists; no files written  
**Observed:** First controller generation failed Guardian evaluation (missing required Logger import). Synthesizer retried with violation report. Second generation also failed (Logger was added but as `console.log` alias rather than proper NestJS Logger — the executor misinterpreted the violation description). Pipeline halted with:
```json
{
  "status": "failed",
  "stage": "validation",
  "failed_component": "controller",
  "attempt_1_violations": [{ "rule_id": "CTL-003", "description": "Missing Logger import from @nestjs/common", "severity": "error" }],
  "attempt_2_violations": [{ "rule_id": "CTL-001", "description": "console.log used instead of Logger", "severity": "error" }],
  "files_generated": [],
  "guidance": "Review the violation list and update your feature intent document or schema, then re-run the pipeline."
}
```
No files written.

**Finding from this test:** The violation description in the standards document for Logger usage was insufficiently specific about what "Logger" means — the executor interpreted "add Logger" and added a `console.log` wrapper labeled as a logger. The Standards Guardian rule description was updated to: `"Missing NestJS Logger: import \`Logger\` from \`@nestjs/common\` and use \`this.logger.log()\` — do not use console.log or a custom logger wrapper."` This is a constraint library improvement, not a pipeline code change.  
**Result:** ✅ Pass (pipeline behaved correctly; Guardian rule description was improved)

---

### Test P-08: Catalog registration failure — scaffold delivered, registration note created
**Spec criterion:** SC5 (catalog registration), §3.6 (registration failure behavior)  
**Input:** Same as P-01  
**Setup:** `catalog.register()` configured to return error (service name already registered — simulated duplicate)  
**Expected:** Scaffold delivered successfully; `REGISTRATION_FAILED.txt` created in output directory; no scaffold rollback  
**Observed:** All 7 components generated and written successfully. `catalog.register()` returned error (duplicate service name). Pipeline created `REGISTRATION_FAILED.txt` with the service name, error message, and manual registration command. Returned:
```json
{
  "status": "success",
  "service_name": "user-management",
  "files_generated": ["...7 paths..."],
  "catalog_registered": false
}
```
**Result:** ✅ Pass

---

### Test P-09: Standards compliance rate — 20-input sample
**Spec criterion:** SC3 (≥80% first-attempt pass rate)  
**Input:** 20 different feature intent + schema pairs, prepared by the platform engineering team to represent the range of actual services  
**Observed:** 18 of 20 ran to completion on first attempts for all components (90%). 2 of 20 required one retry on the test-executor (the Guardian found missing error path tests in both cases — a repeating pattern). No double failures.  
**First-attempt pass rate:** 90%  
**Result:** ✅ Pass (exceeds the 80% threshold from SC3)

**Pattern identified:** The test-executor was the component most likely to fail first-attempt validation. The most common violation: missing error path test (endpoint returns 404 when resource not found — the executor generated happy-path tests only). The controller-executor instructions were updated to explicitly provide the entity lookup pattern, so the test-executor would have the `findOne null` case as part of its context. Post-update re-run: all 20 passed on first attempt for test files.

---

## Summary

| Test | Criterion | Result |
|------|-----------|--------|
| P-01: Happy path complete scaffold | SC1, SC5 | ✅ |
| P-02: Cross-component consistency | SC2 | ✅ |
| P-03: Empty feature intent | SC7 | ✅ |
| P-04: Invalid schema | SC7 | ✅ |
| P-05: Overwrite protection | SC4 | ✅ |
| P-06: Guardian fail + retry success | SC3, C5 | ✅ |
| P-07: Guardian double fail halt | SC6 | ✅ |
| P-08: Catalog registration failure | SC5 | ✅ |
| P-09: 20-input standards rate | SC3 | ✅ (90%) |

**All 9 tests passed.** Three findings were logged as improvements:

1. Guardian violation description for Logger usage was ambiguous (P-07) → standards document updated
2. test-executor consistently missed error path tests (P-09) → controller-executor context updated to include null-return case
3. Overwrite detection occurs at write time, not before generation (P-05) → behavior is correct per spec; architectural note added to spec annotation for future revision consideration

---

## What Pipeline Validation Teaches That Single-Agent Validation Does Not

**Cross-component consistency is not automatically inherited from component correctness.** Each Component Executor can produce a file that passes the Standards Guardian individually, but if the naming conventions are not shared consistently, the files will not work together. P-02 (import path consistency) is the test that catches this. It is not derivable from the individual component tests.

**The retry path needs its own test.** P-06 specifically tests the retry path. Without it, the retry logic in the Synthesizer's instructions could be broken and no other test would catch it. In pipeline systems, every branch of the pipeline flow needs an explicit test — including the error and retry branches.

**Pipeline mechanics failures (overwrite, bad input) produce no output to evaluate.** Tests P-03, P-04, and P-05 test for correct *non-action*. The spec says "halt and return an error" — the acceptance test evaluates that the halt occurred correctly and the error report contained the right information. This class of test has no output file to analyze. It requires verifying that the correct thing *did not happen*.

**First-attempt pass rate across a sample reveals systemic patterns.** The individual component tests (P-01, P-06) test specific scenarios. The 20-input sample (P-09) reveals systematic weak points in the generators that cannot be detected from single-scenario tests. Running the full suite against a representative sample is a necessary part of pipeline acceptance.

---

*This concludes Example 2 and Part VIII: Applied Examples.*

*[Return to the book index](../../SUMMARY.md)*


