# Writing the Spec

**Applied Examples**

---

> *This chapter contains the complete SDD spec for the Account Executor agent. Annotations in* [brackets] *explain why specific decisions were made — these would not appear in an actual deployed spec.*

---

# SPEC: Account Executor Agent
**Version:** 1.2  
**Date:** 2026-01-14  
**Author:** platform-ai-team  
**Reviewed by:** L. Chen (security), M. Okafor (customer operations), R. Patel (engineering)  
**Status:** Approved

---

## Section 1 — Problem Statement

RetailCo's Tier 1 customer support volume — order lookups, refund requests, address updates, contact updates — requires 52 support agents handling 37,000 tickets per month for inquiries that require no judgment beyond identity verification and scope validation. This consumes approximately 70% of available agent capacity, limiting the time available for Tier 2 cases that require human relationship management and judgment.

The Account Executor is a bounded automation agent that resolves authenticated Tier 1 account actions without human intervention for cases that fall within its authorized scope.

*[Annotation: The problem statement makes the business case explicit — 70% capacity consumption on tasks that don't need human judgment. This is not decoration; it justifies the existence of the spec. If the problem statement were "automate customer support," the scope would be impossible to bound. The specific metrics give the spec reviewers a way to evaluate whether the design is proportionate to the problem.]*

---

## Section 2 — Objective

Resolve authenticated Tier 1 account inquiries (order status, refund initiation ≤$150, shipping address update on unshipped orders, contact email update) without human agent involvement, with a first-contact resolution rate ≥ 90% on in-scope inquiries, while escalating all out-of-scope, ambiguous, or triggering cases to the human escalation queue with full conversation context attached.

*[Annotation: The objective is a single sentence that can be evaluated. Note that it contains a measurable threshold (90%) and defines both the success condition (resolve without human) and the failure handling (escalate with context). A spec that says only "handle customer inquiries automatically" has no evaluable objective.]*

---

## Section 3 — Authorized Scope

**The Account Executor is authorized to perform the following actions for the authenticated customer:**

**3.1 Order status retrieval**
- Look up any order associated with the authenticated customer ID
- Return: order status, estimated delivery date, carrier tracking number if available, items in order
- No modification of order data

**3.2 Refund initiation**
- Initiate a refund request for an order within 90 days of delivery
- Maximum refund amount: $150.00 per request, per 24-hour period
- Eligible conditions: item not received, item damaged in transit, item does not match description
- Required to capture: reason code from the approved list, order ID, item(s) covered by refund
- The action creates a *refund request*; processing to payment is handled by a downstream system, not this agent

**3.3 Shipping address update**
- Update the shipping address on an order with status: "pending" or "processing"
- NOT available if order status is "shipped," "in transit," "delivered," or "cancelled"
- Address must pass validation (deliverable address format for the customer's country)

**3.4 Contact email update**
- Update the contact email address on the customer account
- Requires explicit confirmation from the customer before executing ("Please confirm by replying 'yes' that you want to update your contact email to [new address]")
- The confirmation must occur within the same conversation session

*[Annotation: Section 3 is the most important spec section. It defines what the agent CAN do. Every clause here was discussed in spec review — "within 90 days of delivery" was added in review revision 1.1 after the reviewer asked "what is the age limit on a refund request?" The $150 limit is explicit with the word "per request, per 24-hour period" — the 24-hour period prevents a customer from splitting a larger refund across multiple sessions.]*

---

## Section 4 — NOT-Authorized Scope

**The Account Executor is explicitly NOT authorized to:**

- Cancel any order (cancellation requires human agent review)
- Issue refunds greater than $150 (must route to the human approval workflow)
- Access, display, or discuss payment method details (card numbers, bank accounts, billing address)
- Process chargeback or dispute claims (must escalate with priority: high)
- Create new orders or add items to existing orders
- Modify pricing on any order
- Access the account of any customer other than the currently authenticated customer
- Access accounts without confirmed authentication, including if the customer provides another customer's order number
- Take any action on behalf of a customer who states they are calling on behalf of another person without proper authorization verification
- Interpret a customer's stated intent as implicit authorization for an action not requested explicitly
- Process refunds for orders that predate the 90-day eligibility window, even if the customer provides a compelling reason (must escalate)

*[Annotation: The NOT-authorized list was significantly expanded in spec review. The original draft had 4 items. The reviewers raised: "What if a customer says they're calling on behalf of a family member?" → added the proxy-authorization clause. "What if the customer emotionally explains why they deserve a refund outside the 90-day window?" → added the eligibility window clause with explicit escalation instruction. These are not edge cases. They are the most common manipulation patterns in customer support.]*

---

## Section 5 — Constraints

**C1 — Authentication requirement**  
Every action in Section 3 requires confirmed customer authentication. Authentication is performed by the Inquiry Orchestrator before routing to this agent. The Account Executor must NOT proceed if the `authenticated: true` flag is absent from the session context.

**C2 — Single customer isolation**  
All account actions must be scoped to the `customer_id` passed in the authenticated session context. The agent must not accept an alternative customer ID or order number from the conversation as an override of the session customer ID.

**C3 — Refund dollar limit enforcement**  
The refund amount passed to `refund.initiate()` must be calculated from order data retrieved via `order.lookup()`, not from a customer-stated amount. If the customer states a refund amount, the agent must verify it against the actual order value before initiating.

**C4 — Address update precondition**  
Before calling `address.update()`, the agent must call `order.lookup()` to verify the current order status. If status is not "pending" or "processing," the agent must not attempt the update and must escalate.

**C5 — Email confirmation gate**  
`contact.update()` must be preceded by a confirmation exchange. The agent must present the new email address to the customer and receive explicit confirmation before calling the tool. A follow-up message from the customer saying "yes" or "confirm" or equivalent is required; the agent must not proceed on ambiguous affirmation.

**C6 — Conversation logging**  
Every agent action that calls a write-capable tool must be tagged with the conversation ID from the session context. Tool calls without a conversation ID must not proceed.

**C7 — Escalation attachment**  
When escalating, the agent must call `escalate()` with the full conversation transcript, the customer ID, the identified escalation reason code, and the priority level (see Section 8).

*[Annotation: Constraints convert architectural intent into implementation requirements. C3 is the most important one here and was the source of the postmortem incident (see the postmortem chapter). The original spec did not have C3 explicitly — it was assumed that the agent would use the order lookup value. In the postmortem, we found that the agent used the customer-stated amount when the order lookup returned an ambiguous result. C3 was added in version 1.2 as a direct result.]*

---

## Section 6 — Success Criteria & Acceptance Tests

**SC1 — Happy path resolution**  
Given an authenticated customer with an in-scope request, the agent completes the requested action and presents a confirmation to the customer within 4 agent turns.

**SC2 — Scope boundary behavior**  
Given a request that is explicitly NOT authorized (e.g., cancel an order, request a refund >$150), the agent declines to take the action, explains what it cannot do, and escalates with reason code within 2 agent turns.

**SC3 — Out-of-scope graceful degradation**  
Given a request that is neither in-scope nor in the NOT-authorized list (e.g., a product question, a technical support query), the agent acknowledges the request, explains it cannot help with that directly, and offers to route to the appropriate resource.

**SC4 — Refund amount constraint**  
Given a refund request where the customer states an amount different from the order value, the agent uses the verified order value, not the customer-stated amount.

**SC5 — Address update precondition**  
Given a request to update the shipping address on an order with status "shipped," the agent does not attempt the update, explains why it cannot proceed, and escalates.

**SC6 — Unauthenticated rejection**  
Given a session context where `authenticated: false`, the agent takes no action, returns a message directing the customer to authenticate, and does not attempt any tool call.

**SC7 — PII non-disclosure**  
Given any conversation input, the agent does not surface payment card data, full social security numbers, passwords, or account credentials in its response.

*[Annotation: These seven success criteria map directly to the acceptance tests in the validation chapter. SC4 and the postmortem are directly related: SC4 was the criterion that the original system failed, which is how the incident was detected as a spec gap rather than an edge case.]*

---

## Section 7 — Tool Manifest

**7.1 `order.lookup(order_id: string, customer_id: string) → OrderRecord`**
- Returns: `{ order_id, status, items[], delivery_estimate, tracking_number?, total_value }`
- Authorization: read-only
- Failure behavior: if order not found for customer_id, return not-found error; agent must NOT attempt the action and must escalate

**7.2 `refund.initiate(order_id: string, amount: number, reason_code: ReasonCode, item_ids: string[]) → RefundRequest`**
- Returns: `{ request_id, status: "pending" | "approved" | "requires_review" }`
- Authorization: write; triggers downstream approval workflow for amount > $150 (constraint enforced at API level as a safety net, NOT as the primary enforcement mechanism — the spec constraint C3 is the primary enforcement)
- Failure behavior: if rejected, agent presents the rejection reason and escalates
- Reason codes: `item_not_received`, `damaged_in_transit`, `item_not_as_described`

**7.3 `address.update(order_id: string, new_address: Address) → UpdateConfirmation`**
- Returns: `{ updated: boolean, order_id, new_address }`
- Authorization: write; blocked by API if order status is not "pending" or "processing" (defense-in-depth; spec constraint C4 is the primary enforcement)
- Failure behavior: if blocked, agent presents message and escalates

**7.4 `contact.update(customer_id: string, new_email: string) → UpdateConfirmation`**
- Returns: `{ updated: boolean, customer_id, new_email }`
- Authorization: write
- Failure behavior: if rejected, agent presents message

**7.5 `escalate(customer_id: string, conversation_id: string, reason_code: EscalationReason, priority: "standard" | "high", transcript: string) → EscalationTicket`**
- Returns: `{ ticket_id, queue_position, estimated_wait_minutes? }`
- Authorization: write to escalation queue only
- Reason codes: `out_of_scope`, `refund_over_limit`, `order_cancellation`, `dispute_claim`, `fraud_indicator`, `customer_distress`, `authentication_failed`, `technical_error`

*[Annotation: The tool manifest is the contract between the spec and the implementation. The choice to include API-level enforcement as "defense-in-depth" but explicitly state that the spec constraint is the primary enforcement is important: it prevents the team from treating "the API will catch it" as a substitute for the spec constraint. Defense-in-depth means TWO layers of enforcement, not one with a backup.]*

---

## Section 8 — Oversight Model

**Model: Constrained Execution with Human Escalation (Oversight Model C)**

**Autonomous execution (no human review required):**
- Order status retrieval
- Refund initiation ≤$150 where the order is eligible
- Shipping address update on "pending" or "processing" orders
- Contact email update after confirmation

**Human routing required:**
- Any action outside Section 3 scope
- Refund requests >$150 (route to approval workflow with refund request pre-populated)
- Cancellation requests
- Dispute or fraud claims (priority: high)
- Three or more escalation-worthy signals in a single conversation

**Escalation priority levels:**
- Standard: normal queue, used for out-of-scope routing
- High: bypass standard queue, used for fraud, legal threat, account compromise indicators

**Audit requirements:**
- All write-tool calls logged with conversation ID, customer ID, action type, before/after values
- All escalations logged with reason code and transcript
- Refund initiations aggregated per customer per 24-hour period

---

## Section 9 — Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Customer provides manipulated order data to inflate refund amount | Medium | Financial | C3: amount from order.lookup, not customer input |
| Agent accesses account without auth due to session state bug | Low | High | C1: agent checks authenticated flag; API requires auth token |
| Prompt injection via customer input to override constraints | Medium | High | Constraint statements in system prompt, not user prompt; Guardian monitors |
| Refund amount under limit but for ineligible item/reason | Medium | Financial | Reason code enum limits rationale; SC4 acceptance test |
| Agent updates address on shipped order due to race condition | Low | Medium | C4: pre-action order.lookup; API defense-in-depth |
| Customer attempts to update another customer's contact email | Low | High | C2: customer_id from session context, not conversation |

---

## Section 10 — Spec Gap Log Reference

| Date | Gap description | Section affected | Resolution |
|------|----------------|-----------------|-----------|
| 2026-01-07 | No age limit specified for refund eligibility | §3.2 | Added 90-day delivery window |
| 2026-01-07 | 24-hour refund limit not specified | §3.2 | Added "per 24-hour period" clause |
| 2026-01-07 | Proxy authorization scenario not addressed | §4 | Added explicit NOT-authorized clause |
| 2026-01-12 | Refund amount source not specified (led to postmortem incident) | §5 | Added C3 in v1.2 |

---

## Section 11 — Agent Skills

**Skills to load:**
- `customer-context`: Tone calibration for customer-facing interactions; de-escalation language patterns; confirmation phrasing that minimizes ambiguity
- `retailco-support-constraints`: RetailCo-specific policy constraints, approved reason codes, escalation scripts

**Skills explicitly NOT applicable:**
- Any code generation skill
- Any research or synthesis skill
- Any deployment or infrastructure skill

---

*Continue to [Agent Instructions](agent-instructions.md)*


