# Selecting the Archetypes

**Applied Examples**

---

## Starting Point: What the System Must Do

Before selecting archetypes, the design team enumerated what the system must do — not in technical terms but in behavioral terms. This list became the first filter:

1. Classify an incoming customer inquiry by intent
2. Present policy information accurately and without commitment to action
3. Look up order status for an authenticated customer
4. Initiate a refund request within a defined dollar limit
5. Update shipping address on an unshipped order
6. Update contact email after customer confirmation
7. Route any inquiry outside the defined scope to a human agent
8. Monitor every conversation for PII exposure, legal triggers, fraud signals
9. Never surface payment card data or full account credentials

Each of these has a different risk profile, a different relationship to reversibility, and a different oversight requirement. The key design insight: **no single archetype can correctly represent all nine behaviors**. Forcing them into one agent would require the most permissive risk posture across all behaviors to dominate — which means the low-risk behaviors (policy lookup) inherit the constraints designed for the high-risk ones (refund initiation), and the whole system becomes harder to reason about.

---

## The Five Archetypes Considered

### Archetype: Advisor
**Core characteristic:** Produces information and recommendations. No actions on external systems. All outputs are reversible by definition because they are informational.

**Evaluation for this system:**

| Dimension | Evaluation |
|-----------|-----------|
| Agency level | 1–2: presents options, does not decide |
| Risk posture | Low: incorrect information causes frustration, not account damage |
| Oversight model | Post-review: incorrect outputs visible in conversation logs, correctable |
| Reversibility | R1: fully reversible — information can be corrected |

**Decision: Adopt** for the policy and FAQ scope. RetailCo's return policy, shipping policy, and product information are stable, auditable, and the consequences of an incorrect answer are bounded (customer frustration, possible re-contact). No account access needed. The separation from the Executor archetype means that an Advisor that answers "yes, you can return that item" is making a policy representation, not an account commitment — and the distinction is meaningful to the customer experience and to the incident log if there is a dispute.

**Scope assigned:** Return policy, shipping policy, warranty, product FAQ, promotional terms, store locator.

---

### Archetype: Executor
**Core characteristic:** Takes bounded, reversible actions on external systems. The defining constraint is that each action is clearly defined, scoped, and the boundary between authorized and unauthorized is unambiguous.

**Evaluation for this system:**

| Dimension | Evaluation |
|-----------|-----------|
| Agency level | 3: executes defined actions, no ambiguity about what it will do |
| Risk posture | Medium-High: write access to customer accounts; financial actions |
| Oversight model | Constrained execution: hard limits on dollar amounts, order states, action types |
| Reversibility | R2–R3: address updates reversible; refunds irreversible after processing |

**Decision: Adopt** for the account action scope. The key insight is that the Executor archetype's value is its *predictability*. Because its authorized action set is explicitly bounded, the spec can enumerate exactly what it can do, and the validation suite can test every boundary. An open-ended "customer service" agent that can do anything provides a fundamentally different (and worse) risk guarantee.

**Scope assigned:** Order status lookup, refund initiation (≤$150), shipping address update (unshipped orders only), contact email update.

**Hard limits built into the archetype selection:**
- No access to payment method data
- No order cancellation authority
- No new account creation
- No accessing other customers' accounts
- No refund initiation >$150 (route to human approval workflow)

---

### Archetype: Guardian
**Core characteristic:** Monitors and evaluates; does not act on the primary task. Its output is a signal (flag, interrupt, block) rather than a customer-facing response.

**Evaluation for this system:**

| Dimension | Evaluation |
|-----------|-----------|
| Agency level | 2–3: evaluates and flags; does not execute primary actions |
| Risk posture | Low for its own actions (only outputs flags); protects against high-risk events |
| Oversight model | Continuous monitoring: must operate without human per-event approval |
| Reversibility | R1: flags are informational; no irreversible consequences from the guardian itself |

**Decision: Adopt** as an always-on monitor. Three categories of guardian behavior were identified:

1. **PII Guardian:** Detects if any conversation output contains payment card numbers, full SSNs, passwords, or account credentials. If detected, fires an interrupt immediately and triggers conversation termination with escalation. *Why this is not handled in the Executor spec:* the PII risk exists across all agents (the Advisor could inadvertently surface something from the KB; the Orchestrator could echo back a customer's incorrectly formatted input). The guardian monitoring at the conversation layer covers all agents.

2. **Escalation Trigger Guardian:** Monitors for signals that require human involvement regardless of the inquiry type: customer expresses legal threat, references fraud, expresses significant distress, requests to speak with a human, uses keywords associated with account compromise. These triggers must bypass the routing logic entirely and go directly to a human agent.

3. **Behavior Guardian:** Monitors for the specialist agents behaving outside their authorized scope — examples: the Policy Advisor promising a specific outcome rather than describing a policy, the Account Executor being manipulated into discussing another customer's account.

**An important constraint on the Guardian:** The Guardian monitors and flags but does not directly modify conversation state — only the Orchestrator does. The Guardian fires events; the Orchestrator responds to them. This separation prevents the Guardian from being a point of failure that can silence the whole system.

---

### Archetype: Orchestrator
**Core characteristic:** Coordinates other agents; does not itself execute primary tasks. Manages workflow, state, and routing.

**Evaluation for this system:**

| Dimension | Evaluation |
|-----------|-----------|
| Agency level | 4: coordinates multi-agent sequences; high situational awareness |
| Risk posture | Medium: routing errors can send customers to wrong agents; must handle Guardian interrupts |
| Oversight model | Human-in-the-loop for escalation decisions |
| Reversibility | R1–R2: routing decisions are soft; can re-route |

**Decision: Adopt** as the entry point and conversation coordinator. Every conversation begins with the Orchestrator. It performs:
- Intent classification (what type of inquiry is this?)
- Authentication verification (is this customer authenticated? what is their customer ID?)
- Routing (which specialist agent handles this intent?)
- Context accumulation (builds the conversation summary packet for human escalation)
- Guardian event handling (when the Guardian fires, the Orchestrator decides: re-route, terminate, or escalate)

The Orchestrator has no direct account access. It passes the customer ID and authenticated context to the specialist agents; it does not perform lookups itself. This separation means the routing logic and the action logic are independently testable and independently updatable.

---

### Archetype: Synthesizer
**Core characteristic:** Produces composite outputs from multiple information sources. Best suited when the output requires integration across sources rather than action on systems.

**Evaluation for this system:**

| Dimension | Evaluation |
|-----------|-----------|
| Agency level | 3–4: reads from multiple sources to produce integrated analysis |
| Risk posture | Low-Medium: primarily informational |
| Oversight model | Post-review suitable for most cases |
| Reversibility | R1: outputs are informational |

**Decision: Reject** for this deployment. The Synthesizer's value is in situations where the output requires integrating across many sources to produce something the customer could not easily find themselves — a research summary, a multi-source analysis. RetailCo's support scenarios do not require this. The highest-complexity "synthesis" in this system is the Orchestrator combining the conversation summary for escalation hand-off, which is a much more bounded operation than what the Synthesizer archetype is designed for.

A possible future use: a "case summary" agent that synthesizes a customer's full account history, prior support contacts, and current inquiry into a briefing document for Tier 2 agents. That would be a Synthesizer role. It is not in scope for this deployment.

---

## The Final Architecture

```
Customer inquiry
        │
        ▼
┌─────────────────────────────────────────────┐
│           Inquiry Orchestrator              │
│           (Archetype: Orchestrator)         │
│   • Classifies intent                       │
│   • Verifies authentication                 │
│   • Routes to specialist                    │
│   • Handles Guardian interrupts             │
└───────┬──────────────────────┬──────────────┘
        │                      │
        ▼                      ▼
┌───────────────┐    ┌──────────────────────┐
│ Policy Advisor│    │   Account Executor   │
│ (Advisor)     │    │   (Executor)         │
│               │    │                      │
│ • Policy info │    │ • Order status       │
│ • FAQ         │    │ • Refund initiation  │
│ • Shipping    │    │ • Address update     │
│   information │    │ • Contact update     │
└───────────────┘    └──────────────────────┘

        All conversations monitored by:
┌─────────────────────────────────────────────┐
│           Compliance Guardian               │
│           (Archetype: Guardian)             │
│   • PII detection                           │
│   • Escalation trigger detection            │
│   • Out-of-scope behavior detection         │
└─────────────────────────────────────────────┘
```

---

## The Authority Matrix

What each agent can and cannot access:

| Capability | Orchestrator | Policy Advisor | Account Executor | Guardian |
|-----------|:---:|:---:|:---:|:---:|
| Customer identity service (read) | ✅ | ❌ | ✅ | ❌ |
| Knowledge base (read) | ❌ | ✅ | ❌ | ❌ |
| Order data (read) | ❌ | ❌ | ✅ | ❌ |
| Account data (write) | ❌ | ❌ | ✅ (scoped) | ❌ |
| Conversation stream (read) | ✅ | ❌ | ❌ | ✅ |
| Escalation queue (write) | ✅ | ❌ | ✅ (initiate) | ✅ (initiate) |
| Human agent routing (write) | ✅ | ❌ | ❌ | ❌ |

The most important cell in this table is Account data (write) — only the Account Executor has write access, and that access is scoped to the specific actions in the spec. No other agent in the system can modify customer account data. This is the architectural expression of the minimum authority principle.

---

*Continue to [Writing the Spec](spec.md)*


