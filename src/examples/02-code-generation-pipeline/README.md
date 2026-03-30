# A Code Generation Pipeline

**Part VIII: Applied Examples** · *Example 2 of 2*

---

> *"An agent that generates code for humans is still accountable to human judgment at the end. An agent that generates code for other systems is accountable only to the spec. The spec had better be right."*

---

## The Scenario

**Meridian Software** is a mid-size independent software vendor with product teams building on a shared microservices platform. Their platform engineering team maintains standards for how services are built: TypeScript/Node.js, OpenAPI-documented REST endpoints, PostgreSQL with a standard repository pattern, Kubernetes for deployment.

Every time a product team starts a new microservice, a platform engineer spends approximately 4 hours producing what they call "the scaffold" — the boilerplate structure that must exist before product-specific logic is written:

| Scaffold component | Estimated time |
|-------------------|---------------|
| Controller layer (endpoints, route registration) | 45 min |
| Service layer (business logic shell) | 30 min |
| Repository layer (data access pattern) | 30 min |
| OpenAPI documentation | 45 min |
| Unit test stubs | 30 min |
| Dockerfile and Kubernetes manifests | 30 min |
| Service registry entry | 10 min |
| **Total** | **~4 hours** |

With 12 product teams each launching 1–3 new services per quarter, this consumes significant platform engineering bandwidth. More consequentially: the scaffolds drift. Different engineers produce slightly different patterns, violating the standards that make the platform consistent enough for centralized tooling to work.

**The goal:** A pipeline that accepts a *feature intent document* (a brief markdown description of what a new service must do) and a *data schema* (JSON describing the entities the service manages) — and produces a complete, standards-compliant service scaffold. The pipeline must:

1. Generate all scaffold components consistently
2. Validate every component against current platform standards before delivery
3. Reject or flag any generated component that violates standards rather than delivering non-compliant output
4. Register the new service in the platform service catalog upon successful generation

---

## The Architecture

This pipeline differs structurally from Example 1. There is no human customer on the other end receiving responses in real time. The consumer of this pipeline's output is the product engineering team — and they receive a directory of files, not a conversation. This changes the agent dynamics significantly.

### Agent 1: Scaffold Synthesizer
**Archetype:** Synthesizer  
**Role:** Reads the feature intent document and data schema, decomposes the generation task into components, coordinates the Component Executors for each file type, assembles the results into a coherent scaffold directory, and registers the service. This agent's output is a *composite artifact* — many files that must be internally consistent with each other.

The Synthesizer knows how the components relate. The controller must import from the service layer; the service must import from the repository; the test stubs must reference the controller endpoints. Consistency across the assembled output is the Synthesizer's primary responsibility.

### Agent 2: Component Executor (multiple instances)
**Archetype:** Executor  
**Role:** Generates one scaffold component (one file type) given its specific context. There is one Executor invocation per file type:
- `controller-executor`: generates `src/controller.ts`
- `service-executor`: generates `src/service.ts`
- `repository-executor`: generates `src/repository.ts`
- `openapi-executor`: generates `openapi.yaml`
- `test-executor`: generates `src/controller.test.ts`
- `manifest-executor`: generates `Dockerfile` + `k8s/deployment.yaml`

Each Executor receives exactly what it needs: the schema, the feature intent, and the naming convention package from the Synthesizer. Each Executor is responsible for exactly one file or file pair. **The Executors do not communicate with each other.** Cross-component consistency is the Synthesizer's job.

### Agent 3: Standards Guardian
**Archetype:** Guardian  
**Role:** Receives each generated component and evaluates it against the platform's code standards document. Returns a structured validation report: pass/fail per standard, with specific violations identified and location in the file noted. Does not modify files — only evaluates. If a component fails, the Synthesizer can request a corrected execution from the relevant Executor, up to two retry attempts.

---

## Key Differences from Example 1

Understanding how this pipeline's design differs from the customer support system illuminates why archetype selection and spec decisions are different:

| Dimension | Customer Support | Code Generation Pipeline |
|-----------|-----------------|------------------------|
| Human in real time? | Yes (customer, live) | No (product team receives async output) |
| Primary archetype | Executor (actions) | Synthesizer (composite output) |
| Failure consequence | Customer frustration, financial | Standards drift, blocked development |
| Reversibility | Some actions irreversible | Outputs are files — fully reversible |
| Oversight model | Human-in-loop for escalation | Guardian validation gate |
| Inter-agent communication | Orchestrator routes | Synthesizer coordinates |
| Success criterion | Resolve inquiry without escalation | Deliver complete, passing scaffold |

The most consequential difference: **the pipeline has no human escalation channel.** In customer support, an agent that cannot handle a request escalates to a human. In this pipeline, an output that cannot pass the Standards Guardian's validation is returned to the Synthesizer with a failure report — the human product engineer receives either a complete valid scaffold or a clear error report explaining exactly what failed. There is no middle ground where a partially-correct scaffold is delivered.

This is a design choice, not a technical constraint. Earlier drafts of the system allowed partial scaffolds (some files pass, some fail) to be delivered. The team chose the strict model: all components pass or the delivery is blocked. The reasoning: a partial scaffold silently containing a non-compliant component would likely be used anyway, with the violation only discovered during a later audit. The failure cost is higher than a blocked delivery.

---

## What This Example Covers

This example focuses on the Scaffold Synthesizer — the most architecturally interesting agent in the pipeline — and on the pipeline dynamics that make multi-agent coordination different from single-agent execution.

**The chapters in this example:**

1. [Selecting the Archetypes](archetypes.md) — How the three-archetype pipeline architecture was determined
2. [Writing the Spec](spec.md) — Complete SDD spec for the Scaffold Synthesizer
3. [Agent Instructions](agent-instructions.md) — Instructions for all three agents in the pipeline
4. [Validating Outcomes](validation.md) — How a pipeline is accepted-tested differently from a single agent

---

*Continue to [Selecting the Archetypes](archetypes.md)*


