# Writing the Spec

**Part VIII: Example 2 — Code Generation Pipeline** · *Step 2 of 4*

---

> *This chapter contains the complete SDD spec for the Scaffold Synthesizer — the pipeline's primary agent. Annotations in* [brackets] *explain design decisions. The Component Executor and Standards Guardian specs follow the same template; abbreviated versions are included at the end of this chapter.*

---

# SPEC: Scaffold Synthesizer Agent
**Version:** 1.0  
**Date:** 2026-02-03  
**Author:** platform-eng-team  
**Reviewed by:** A. Vasquez (platform architecture), D. Kim (security), S. Patel (engineering lead)  
**Status:** Approved

---

## Section 1 — Problem Statement

Platform engineering spends 4 hours per new microservice producing scaffolding that should be mechanically consistent across all services. This creates two problems: capacity consumption (time that could be spent on platform improvements) and consistency drift (subtle variations between scaffolds produced by different engineers over time). Drift accumulates until centralized platform tooling breaks because it assumes conventions that some services don't follow.

*[Annotation: Note that the problem statement has two distinct components — capacity and consistency. Both matter. A solution that saves time but produces inconsistent scaffolds would address the capacity problem while worsening the consistency problem. The spec's success criteria (Section 6) must address both.]*

---

## Section 2 — Objective

Generate a complete, standards-compliant TypeScript/Node.js service scaffold for a new microservice given a feature intent document and a data schema, with all generated components passing the platform standards validation in at most two generation attempts per component, and register the new service in the platform service catalog upon successful completion.

*[Annotation: "In at most two generation attempts per component" is in the objective because it connects to the pipeline's failure behavior (if a component fails twice, the pipeline halts). This is the kind of operational constraint that belongs in the objective, not just in the constraints section.]*

---

## Section 3 — Authorized Scope

The Scaffold Synthesizer is authorized to:

**3.1 Parse and decompose inputs**
- Read the feature intent document (markdown format)
- Read the data schema (JSON, following Meridian's entity schema format)
- Extract: service name, entity name(s), endpoint descriptions, relationship dependencies

**3.2 Generate naming conventions**
- Derive and publish the naming convention package: PascalCase class names, camelCase method names, kebab-case file names, per platform naming standard v3.2
- The naming convention package is the sole source of naming for all Component Executors in this pipeline run

**3.3 Invoke Component Executors**
- Invoke each Component Executor with the naming convention package, relevant schema sections, and any file-type-specific context
- Enforce invocation order: repository → service → controller → openapi → tests → manifests
- Pass the Standards Guardian's violation report to the relevant Executor on retry invocations

**3.4 Manage the validation gate**
- Submit each generated component to the Standards Guardian before assembly
- Accept or retry based on the Guardian's pass/fail report
- On second failure: halt pipeline, return structured failure report (see Section 6)

**3.5 Assemble and deliver the scaffold**
- Once all components pass validation, assemble the scaffold directory structure per platform standard
- Deliver to the requesting engineer's designated output location (path provided in the pipeline invocation)

**3.6 Register in service catalog**
- After successful assembly, call `catalog.register()` with the service name, team ID, tech stack, and the generated OpenAPI spec path
- Registration is the final step; failure in registration does not roll back the scaffold delivery but must be reported

---

## Section 4 — NOT-Authorized Scope

The Scaffold Synthesizer is explicitly NOT authorized to:

- Modify existing source files (creation only — if a file at the target path already exists, halt and report; do not overwrite)
- Execute any generated code
- Deploy any generated artifact
- Make any database or infrastructure changes
- Accept or apply custom naming conventions not derived from the platform naming standard v3.2
- Skip the Standards Guardian validation for any component, regardless of invocation parameters
- Register a service that has failed any component validation
- Invoke Component Executors more than twice for any single component
- Access source repositories of existing services
- Generate components for tech stacks other than TypeScript/Node.js (other stack support is not implemented)

*[Annotation: "Cannot overwrite existing files" is critical. The risk of running this pipeline twice on the same service name — once deliberately, once accidentally — is that the second run overwrites customizations the product team added after the initial scaffold. The halt-and-report behavior makes the path safe: the engineer must explicitly acknowledge what's there before proceeding.]*

---

## Section 5 — Constraints

**C1 — Input validation before execution**  
Before invoking any Component Executor, validate that: (a) the feature intent document is non-empty and parseable, (b) the data schema is valid JSON conforming to the entity schema format, (c) the target output path is provided and writable. If any validation fails, halt immediately with a structured error report.

**C2 — Naming convention isolation**  
The naming convention package must be generated once per pipeline run and shared read-only across all Component Executors. No Component Executor may modify or override naming conventions.

**C3 — Invocation order enforcement**  
Component Executors must be invoked in this order: repository → service → controller → openapi → tests → manifests. The controller-executor must receive the actual service interface (output of service-executor) as context, not a generated assumption about it.

**C4 — Validation gate is non-optional**  
No generated component may be assembled into the final scaffold without a `pass` result from the Standards Guardian. This constraint may not be bypassed by invocation parameters, feature flags, or instruction modification.

**C5 — Retry limit**  
If a component fails Standards Guardian validation on the first attempt, the Synthesizer may invoke the relevant Component Executor once more with the violation report appended as context. If the second attempt also fails, the pipeline halts for the entire scaffold (no partial delivery) and returns the failure report.

**C6 — Existing file protection**  
Before writing any file, check whether a file at the target path already exists. If it does, halt the pipeline and return an error: "File [path] already exists. Pipeline halted to prevent overwriting customizations." Do not overwrite. Do not skip the file.

**C7 — Catalog registration dependency**  
`catalog.register()` must be called only after all components have been assembled and the scaffold directory has been delivered successfully. It must not be called if any component failed validation.

*[Annotation: C4 is the most architecturally significant constraint. It lives in the spec because it expresses organizational policy (standards are mandatory, not advisory) rather than just technical mechanics. A team that wants to run the pipeline in "fast mode" without validation is making a different choice about their code standards, not a technical optimization. This constraint makes that conversation explicit.]*

---

## Section 6 — Success Criteria & Acceptance Tests

**SC1 — Complete scaffold delivery**  
Given a valid feature intent document and data schema, the pipeline produces a scaffold directory containing all seven required components, all of which pass Standards Guardian validation.

**SC2 — Cross-component consistency**  
The generated controller imports the service using the exact class name and path produced by the service-executor. The generated tests reference the exact endpoint paths produced by the controller-executor. The OpenAPI document reflects the exact endpoints and request/response shapes in the controller.

**SC3 — Standards compliance**  
All generated components pass the Standards Guardian's validation on their first or second attempt. (First-attempt pass rate ≥ 80% on a representative test set of 20 feature intent + schema pairs.)

**SC4 — Overwrite protection**  
Given an existing file at a target output path, the pipeline halts without writing any file and returns a clear error message identifying the conflicting path.

**SC5 — Catalog registration**  
After successful scaffold delivery, the service appears in the platform service catalog with the correct name, team ID, and OpenAPI spec path.

**SC6 — Failure report on double validation failure**  
Given a component that fails Standards Guardian validation twice, the pipeline returns a structured failure report including: component name, violation list from both attempts, and guidance on what to fix in the input documents.

**SC7 — Input validation rejection**  
Given an invalid or unparseable input document, the pipeline halts before invoking any Executor and returns a clear error identifying the input issue.

---

## Section 7 — Tool Manifest

**7.1 `schema.parse(schema_json: string) → ParsedSchema`**  
Parses and validates the input data schema. Returns structured entity definitions.

**7.2 `naming.derive(entity_name: string, stack: "typescript") → NamingPackage`**  
Derives the full naming convention set from a base entity name. Returns: `{ className, serviceName, repositoryName, controllerName, tableName, fileName }`.

**7.3 `executor.invoke(executor_id: ExecutorId, context: ExecutorContext) → GeneratedComponent`**  
Invokes a specific Component Executor. `ExecutorId` is one of: `controller`, `service`, `repository`, `openapi`, `tests`, `manifests`. `context` includes: naming package, schema sections, feature intent summary, previous violation report (null on first invocation, populated on retry).

**7.4 `guardian.validate(component_id: string, content: string) → ValidationResult`**  
Submits a generated component for standards validation. Returns: `{ pass: boolean, violations: Violation[] }` where each violation includes: rule ID, description, line number, severity (error | warning).

**7.5 `fs.write(path: string, content: string) → WriteResult`**  
Writes a file to the output path. Returns error if file exists (never overwrites). The Synthesizer calls this for each component after validation passes.

**7.6 `catalog.register(service_name: string, team_id: string, stack: string, openapi_path: string) → RegistrationResult`**  
Registers the service in the platform catalog. Called after all files are written successfully.

---

## Section 8 — Oversight Model

**Model: Automated Validation Gate (Oversight Model C, no live human)**

**No human in the pipeline execution path.** The pipeline runs to completion (success or failure) and delivers results asynchronously.

**Guardian validation is the oversight mechanism.** Every generated component passes through the Standards Guardian before delivery. This is the functional equivalent of human review — it evaluates compliance against documented standards.

**Human review is triggered by:**
- Structural pipeline failure (C1 input validation failure)
- Double Guardian failure on any component (policy decision required: does the input need to be rewritten?)
- Catalog registration failure (may indicate service naming conflict)

**Audit trail:**
- Full execution log: every Executor invocation, every Guardian response, every retry, final assembly result
- All logs tagged with pipeline run ID, requesting engineer, input document hashes
- Retention: 90 days

---

## Section 9 — Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Generated code is standards-compliant but semantically wrong (wrong logic for the feature) | Medium | Medium | Pipeline output is a scaffold — no business logic is generated; engineers implement logic manually |
| Pipeline run ID collision produces incorrect catalog entry | Low | Low | catalog.register() returns error on duplicate name; engineer must resolve naming |
| Component Executor produces injection content in generated file | Low | Medium | Standards Guardian checks for prohibited patterns; generated files reviewed by product engineer before use |
| Naming convention drift if platform naming standard is updated without pipeline update | Medium | Medium | naming.derive() tool version-locks to platform standard; update requires pipeline redeployment |
| Feature intent too ambiguous to generate correct endpoint structure | Medium | Medium | SC6 failure report guides engineer to clarify intent; pipeline does not guess |

---

## Section 10 — Spec Gap Log Reference

*(Populated during review and post-deployment)*

| Date | Gap description | Section | Resolution |
|------|----------------|---------|-----------|
| 2026-01-28 | No specification for behavior when output path is not writable | §3, C1 | Added C1 path writability check |
| 2026-01-28 | Retry behavior on catalog registration failure not specified | §3.6 | Added "failure in registration does not roll back scaffold" clause |
| 2026-01-30 | Partial delivery behavior on multi-component failure not specified | §5, C5 | Clarified: no partial delivery; all-or-nothing per run |

---

## Section 11 — Agent Skills

**Skills to load:**
- `meridian-typescript-standards`: Platform code standards v3.2 for TypeScript/Node.js — naming conventions, required patterns, prohibited patterns
- `meridian-scaffold-templates`: Reference implementations of each file type for calibration

---

## Abbreviated Specs: Component Executor and Standards Guardian

The Component Executor and Standards Guardian follow the same spec template. Abbreviated versions are provided here for completeness.

---

### SPEC: Component Executor (per file type)
*Version 1.0 — same date and review as Scaffold Synthesizer*

**Objective:** Given the naming convention package, relevant schema sections, and a feature intent summary, generate a single scaffold file (of the specified type) that complies with platform standards on first or second attempt.

**Authorized scope:** Generate exactly one file. Use only the provided naming conventions. Use only platform-approved patterns for the file type.

**NOT authorized:** Modify any other file. Generate business logic beyond method stubs. Deviate from the naming convention package. Generate code for a tech stack other than TypeScript/Node.js.

**Key constraint — C1:** The file content must be syntactically valid TypeScript (or YAML for manifests/OpenAPI). A file that does not parse is a first-attempt failure by definition, regardless of Standards Guardian evaluation.

**Success criteria:** Generated file passes Standards Guardian validation within two attempts. Generated file is syntactically valid. All imports reference the correct paths from the naming convention package.

---

### SPEC: Standards Guardian
*Version 1.0 — same date and review as Scaffold Synthesizer*

**Objective:** Evaluate a generated scaffold component against the platform's code standards document and return a structured pass/fail report with specific violations identified.

**Authorized scope:** Evaluate a provided file against the standards document. Return structured results. Never modify the file or produce alternative content.

**NOT authorized:** Modify files. Pass a component that violates error-severity rules. Return a pass result without evaluation. Apply different standards for retry attempts.

**Key constraint — C1:** A component with any error-severity violation is always a `fail` result. A component with only warning-severity violations is a `pass` — warnings are included in the report but do not block delivery.

**Success criteria:** Every error-severity rule from the standards document is evaluated on every submission. Evaluation results include line-level citation for each violation. No component with error-severity violations receives a pass result.

---

*Continue to [Agent Instructions](agent-instructions.md)*


