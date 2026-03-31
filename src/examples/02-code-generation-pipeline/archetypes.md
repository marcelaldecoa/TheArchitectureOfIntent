# Selecting the Archetypes

**Applied Examples**

---

## The Governing Constraint: No Live Human in the Loop

Before evaluating archetypes, the design team established one constraint that shaped every selection decision: the pipeline would deliver asynchronously to a technical consumer (the product engineer), and there was no human present to make judgment calls during execution.

This rules out Oversight Model B (human approval per action) and Oversight Model D (human-in-loop for all decisions). The pipeline must run with Oversight Model C (constrained execution with validation gate) or Model A (post-review). The choice between C and A drove the insertion of the Standards Guardian as the validation layer: the team wanted Model C, which requires a mechanism to catch violations before delivery.

That single constraint produced the entire architecture.

---

## The Five Archetypes Evaluated

### Archetype: Executor

**What it does:** Takes bounded, reversible actions. Produces a specific, defined output for a specific, defined input.

**Evaluation for file generation:**

| Dimension | Evaluation |
|-----------|-----------|
| Agency level | 2–3: generates a file from a template and context; determinate output |
| Risk posture | Low: file creation is fully reversible; no side effects on running systems |
| Oversight model | Post-review (or validation-gated) |
| Reversibility | R1: files can be replaced or deleted freely |

**Decision: Adopt** for *individual component generation*. Each file (controller, service layer, repository, tests, manifests) is a bounded Executor task: given a schema, a feature name, a tech stack, and a naming convention document, generate this specific file. The output is deterministic enough to test against specific standards.

**The insight that shaped this decision:** Trying to use an Executor to generate the entire scaffold at once would make the task unbounded — multiple interconnected files, with cross-file consistency requirements, version management, and assembly logic. That is not an Executor task. That is exactly what the Synthesizer archetype is for.

**How many Executors?** One per file type, invoked sequentially by the Synthesizer. Each Executor has exactly one responsibility. This makes each Executor independently testable (can you generate a correct controller file?) and independently replaceable (when the TypeScript standards change, only the affected Executors are updated).

---

### Archetype: Synthesizer

**What it does:** Integrates multiple sources of information to produce a composite output. The output is more than the sum of its parts — the components must be internally consistent with each other.

**Evaluation for scaffold assembly:**

| Dimension | Evaluation |
|-----------|-----------|
| Agency level | 3–4: reads context across sources, decomposes into sub-tasks, assembles results |
| Risk posture | Medium: produces code that will be used in production services |
| Oversight model | Validation-gated (Standards Guardian) before delivery |
| Reversibility | R1: output is files; reversible |

**Decision: Adopt** as the pipeline's primary agent and entry point. The Synthesizer's core capability — integration and consistency — is exactly the problem: the scaffold's seven components come from seven separate generation tasks, and they must refer to each other correctly (the controller imports from the service, the tests import from the controller, the OpenAPI doc reflects the endpoints in the controller). An agent that generates each component in isolation without tracking cross-component references will produce a scaffold whose components don't connect.

**What the Synthesizer does that the Executors cannot:**
1. Reads the feature intent and schema to determine *what* needs to be generated (which entity types, how many endpoints, what naming pattern)
2. Constructs the naming convention package that all Executors share (so `UserController`, `UserService`, `UserRepository` all agree on the entity name)
3. Sequences the generation tasks (repository first, so the service's import path is known; service next; controller last)
4. Assembles the generated files into the scaffold directory structure
5. Handles retry logic for Guardian failures
6. Registers the service in the platform catalog after successful assembly

None of these are single-file Executor operations. They require state and coordination across the full generation sequence. That is the Synthesizer role.

---

### Archetype: Guardian

**What it does:** Monitors and evaluates without taking primary-task action. Outputs are signals (pass/fail/violation report), not work products.

**Evaluation for standards enforcement:**

| Dimension | Evaluation |
|-----------|-----------|
| Agency level | 2: evaluates against criteria; does not produce new content |
| Risk posture | Low for its own actions (cannot cause harmful output, only block it) |
| Oversight model | Automatic; fires on every component before delivery |
| Reversibility | R1: only outputs a report |

**Decision: Adopt** as the validation gate. The Standards Guardian receives each generated component and checks it against the platform's code standards document. It evaluates:

- Naming conventions (class names, method names, file names per platform standard)
- Required import patterns (specific logger, error handling, config loader)
- Required annotations (OpenAPI decorators, DTO validation decorators)
- Prohibited patterns (direct database access from controller layer, console.log statements, hardcoded configuration values)
- Test coverage requirements (at minimum: one test per endpoint, one error path test)

**The Guardian's relationship to the Executors:** The Guardian is not a filter on the Executors' output — it is a peer that receives the same output and produces an evaluation. The Synthesizer decides what to do with the evaluation (deliver, retry, or fail with report). This keeps the evaluation logic separate from the assembly logic and makes it independently updatable: when platform standards change, only the Guardian's evaluation rules are updated.

**Why the Guardian, not the Executor checking its own output:** An Executor with self-evaluation is an Executor doing two jobs. The validation criteria for platform standards are complex enough (150+ checks in the current standards document) that they belong in a dedicated evaluation layer. The Executor's job is to generate correct output; the Guardian's job is to verify that the output is correct. These responsibilities should not be combined in one agent.

---

### Archetype: Orchestrator

**What it does:** Coordinates multiple agents without executing primary tasks itself.

**Evaluation:**

| Dimension | Evaluation |
|-----------|-----------|
| Agency level | 4–5: high coordination responsibility |
| Risk posture | Medium-High: routing failures cascade |
| Oversight model | Human-in-loop for exception handling |

**Decision: Reject** as a separate agent. The Orchestrator archetype is designed for scenarios where the routing logic is independent of the task execution logic — like customer support, where "which agent handles this?" is a policy decision independent of what that agent does.

In this pipeline, the coordination logic (what order to generate components, how to handle Guardian failures, how to assemble the final output) is inextricably bound to the Synthesizer's job. Adding a separate Orchestrator above the Synthesizer would create two agents responsible for the same concern. The Synthesizer *is* the orchestrating layer for this pipeline.

A future version of this system that supported multiple output formats (TypeScript API, Python API, .NET API) with per-format Synthesizers and a routing layer would benefit from an Orchestrator. In the current single-stack version, it adds complexity without value.

---

### Archetype: Advisor

**What it does:** Produces information and recommendations without taking actions.

**Evaluation:**

| Dimension | Evaluation |
|-----------|-----------|
| Agency level | 1–2 |
| Risk posture | Low |
| Oversight model | Post-review |

**Decision: Reject.** This is a code generation pipeline — every agent must produce or evaluate an artifact. There is no advisory function required. The closest advisory function (helping product engineers write better feature intent documents) would be a valuable future investment but is out of scope for this deployment.

---

## The Final Architecture

```
Feature intent doc + Data schema
              │
              ▼
┌─────────────────────────────────────────────┐
│          Scaffold Synthesizer               │
│          (Archetype: Synthesizer)           │
│                                             │
│  1. Parse intent + schema                   │
│  2. Build naming convention package         │
│  3. Invoke Component Executors (×6)         │
│  4. Send each output to Standards Guardian  │
│  5. Retry or fail on Guardian violations    │
│  6. Assemble scaffold directory             │
│  7. Register in service catalog             │
└───────────┬─────────────────────────────────┘
            │  invokes per component
            ▼
┌─────────────────────────────────────────────┐
│      Component Executors (×6 instances)     │
│      (Archetype: Executor)                  │
│                                             │
│  controller-executor → src/controller.ts    │
│  service-executor    → src/service.ts       │
│  repository-executor → src/repository.ts   │
│  openapi-executor    → openapi.yaml         │
│  test-executor       → src/*.test.ts        │
│  manifest-executor   → Dockerfile, k8s/     │
└─────────────────────────────────────────────┘
            │  each output sent for validation
            ▼
┌─────────────────────────────────────────────┐
│          Standards Guardian                 │
│          (Archetype: Guardian)              │
│                                             │
│  Evaluates each component against           │
│  platform code standards                    │
│  Returns: pass | fail + violation report    │
└─────────────────────────────────────────────┘
```

---

## The Retry Decision

One design question required explicit resolution: **what happens when a component fails the Guardian's evaluation?**

Three options were evaluated:

**Option A: Deliver with violation flag** — Send the scaffold with a report of violations. The product engineer decides what to fix. *Rejected:* experience showed that flagged violations in a delivered scaffold were treated as optional — engineers fixed the blocking ones and deferred the rest. Standards drift re-emerged.

**Option B: Block and report** — If any component fails, halt the pipeline, deliver nothing, return the violation report. *Rejected for first-pass:* too aggressive. A minor violation in the test stubs (missing one error path test) blocks the controller, service, and repository — all of which may be fine.

**Option C: Retry once per component, then block if still failing** — Each Component Executor gets one retry attempt when the Guardian reports a violation. The Synthesizer provides the violation report to the Executor as additional context. If the re-generated component still fails, the pipeline halts for that component's file and returns a failure report. *Selected.*

**The retry limit of one:** The decision to allow exactly one retry (not two, not unlimited) was deliberate. A generator that fails two consecutive times on the same component is likely failing because the violation is either in its standard instructions (an instruction update is needed) or because the input schema/intent is ambiguous in a way that produces the violation. In both cases, human judgment is required. Unlimited retries burn compute and obscure the root cause.

---

*Continue to [Writing the Spec](spec.md)*


