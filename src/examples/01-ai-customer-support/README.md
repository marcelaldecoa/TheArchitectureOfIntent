# Designing an AI Customer Support System

**Part VIII: Applied Examples** · *Example 1 of 2*

---

> *"The first thing a customer support system needs to do is not solve problems. It is to not make them worse."*

---

## The Scenario

**RetailCo** is a mid-size omnichannel retailer with approximately $1.8B in annual revenue and a significant e-commerce presence. Their customer support organization handles 52,000 tickets per month across chat, email, and phone. Headcount is 52 agents.

An operational analysis found that **71% of incoming tickets are Tier 1**: inquiries that require no judgment, only information lookup or a bounded account action. The breakdown:

| Ticket type | Volume share | Average handle time |
|-------------|-------------|-------------------|
| Order status lookup | 38% | 4 min |
| Return/refund request | 19% | 11 min |
| Shipping address update | 8% | 6 min |
| Account/contact update | 6% | 5 min |
| Policy questions | 9% | 7 min |
| Tier 2+ (escalation required) | 20% | 22 min |

The 80 minutes of handle time that agents spend per hour on Tier 1 tasks is 80 minutes not spent on the Tier 2 cases that actually require human judgment and relationship repair.

**The goal:** Automate 65% of total ticket volume (all Tier 1) with a system that: resolves clearly automatable inquiries without human involvement; routes everything else to the appropriate human agent with full context already captured; never makes the customer's situation worse through an incorrect action; maintains first-contact resolution rate at or above current benchmarks.

---

## The Architecture

Four agents work together in this system. Each maps to one of the five archetypes from Part II.

### Agent 1: Inquiry Orchestrator
**Archetype:** Orchestrator  
**Role:** The entry point for every conversation. Receives the incoming inquiry, classifies the intent, authenticates the customer (via integration with the identity service), and routes to the appropriate specialist agent. Monitors the conversation for escalation signals. Does not itself produce content visible to the customer except the initial acknowledgment.

### Agent 2: Policy Advisor
**Archetype:** Advisor  
**Role:** Handles all information-only inquiries: return policy, shipping policy, warranty information, product specifications, FAQ. Has read access to the knowledge base. Has no account access whatsoever. Always presents information and options; never performs an action. The customer must explicitly request an action, which triggers routing to the Account Executor.

### Agent 3: Account Executor
**Archetype:** Executor  
**Role:** Handles bounded account actions for the authenticated customer: order status retrieval, refund initiation, shipping address update, contact email update. Has write access to specific account systems within tightly defined scope. All actions are logged. Refunds above $150 require routing to human approval workflow — the agent can initiate but not complete them unilaterally. **This agent is the subject of the detailed spec in the next chapter.**

### Agent 4: Compliance Guardian
**Archetype:** Guardian  
**Role:** Monitors all conversations in real time. Evaluates for: PII exposure (the system should never surface payment card data, full SSN, or passwords in the conversation), escalation triggers (customer expresses distress, legal threat, or fraud concern), toxicity and harassment, and agent behavior out of scope. If a trigger fires, the Guardian interrupts the conversation flow and surfaces a flag to the orchestrator. The Guardian never communicates directly with the customer.

---

## What This Example Covers

This example walks through the full design and deployment arc for the Account Executor — the most consequential and most constrained agent in the system. The Policy Advisor is simpler (read-only, no account access, no constraint enforcement needed beyond tone); the Orchestrator and Guardian are coordination and monitoring agents whose design is highly system-specific.

The Account Executor is the interesting case because:
- It has real write access to customer accounts
- It operates under competing pressures (resolve quickly vs. authorize conservatively)
- Its failure modes have direct financial and relationship consequences
- It is the agent most likely to be asked to exceed its authorized scope

**The chapters in this example:**

1. [Selecting the Archetypes](archetypes.md) — How the four-archetype architecture was determined, with the full reasoning and alternatives considered
2. [Writing the Spec](spec.md) — Complete SDD spec for the Account Executor
3. [Agent Instructions](agent-instructions.md) — The actual instructions derived from the spec
4. [Validating Outcomes](validation.md) — Acceptance test suite and results
5. [Post-mortem Through Intent](postmortem.md) — A real incident and its retrospective diagnosis

---

## Design Decisions Made Before the Spec Was Written

Three decisions were made at the architecture level before any spec was written:

**Decision 1: No single agent handles the full conversation.** An Orchestrator-only design where one agent classifies, responds, acts, and monitors is technically possible but creates an agent with too wide a scope, too many tool authorities, and no separation of concerns. The risk posture of combined classification-and-execution is higher than the risk posture of separated agents, and the failure diagnosis when something goes wrong is much harder.

**Decision 2: The Guardian has no conversation channel.** Some designs route all output through a guardian filter. This one runs the guardian in parallel and uses interrupts. The interrupt model allows the guardian to monitor without adding latency to happy-path flows. The tradeoff: the guardian catches things after they are said, not before. The constraint library for the Executor and Advisor is designed to prevent the material that the guardian would otherwise need to intercept.

**Decision 3: Refunds above $150 are not automated.** Early design discussions included full automation of refund processing. The decision to cap at $150 and route approvals to humans was made on risk posture grounds, not technical grounds. The system could technically issue larger refunds. The constraint exists because the failure mode of an incorrect large refund (financial exposure, customer expectation management at scale) was assessed as exceeding the system's oversight model capacity at launch.

---

*Continue to [Selecting the Archetypes](archetypes.md)*


