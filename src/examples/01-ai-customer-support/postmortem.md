# Post-mortem Through Intent

**Applied Examples**

---

> *"A postmortem that ends with 'the agent did something wrong' has not finished. The question is always: what in the system allowed the agent to do this?"*

---

## The Incident

**Date:** 2026-01-12, 14:37 UTC  
**Severity:** Medium (financial impact, customer experience degraded)  
**Detection:** Automated refund reconciliation alert (refund amount $0.00 flagged as anomalous)  
**Customer:** Account C12388, order RC-94721 (replacement laptop stand, $0.00 after promotional discount)

---

### What Happened

A customer contacted support about order RC-94721. The order contained one item: a laptop stand that had been acquired for $0.00 via a 100% promotional discount applied at checkout. The customer reported the stand arrived broken.

The Account Executor was invoked. The agent:

1. Called `order.lookup("RC-94721", "C12388")` → returned `{ status: "delivered", total_value: 0.00, items: [...] }`
2. Determined the refund was eligible: delivered within 90 days, damage reason valid
3. Called `refund.initiate("RC-94721", 0.00, "damaged_in_transit", ["ITEM-4491"])` → returned `{ request_id: "REF-211033", status: "approved" }`
4. Informed the customer: "Your refund of $0.00 has been processed."

The customer replied: "That doesn't help me. I wanted a replacement."

The agent escalated.

**Financial impact:** None from the refund itself ($0.00). Impact was in customer experience (customer felt dismissed) and operational overhead (the escalated ticket required human handling to identify the correct path: a product replacement under warranty, not a cash refund).

---

## Root Cause Analysis

### Step 1: Was this an execution gap or a spec gap?

**The question to answer first:** Did the agent deviate from the spec, or did the agent follow the spec exactly and produce an outcome the spec did not intend?

The agent called `order.lookup`, used the returned `total_value` of $0.00, and initiated a refund for $0.00. This is exactly what Constraint C3 requires: *the refund amount passed to `refund.initiate()` must be calculated from order data retrieved via `order.lookup()`, not from a customer-stated amount*.

The agent followed constraint C3 faithfully. The spec said to use the order data; the order data said $0.00; the agent initiated a $0.00 refund.

**Conclusion: This is a spec gap, not an execution gap.**

---

### Step 2: Which spec section contains the gap?

Review Section 3.2 of the spec (Refund initiation):

> "Initiate a refund request for an order within 90 days of delivery [...] The action creates a refund request; processing to payment is handled by a downstream system."

And Constraint C3:

> "The refund amount passed to `refund.initiate()` must be calculated from order data retrieved via `order.lookup()`, not from a customer-stated amount."

Neither section addresses what the agent should do when `total_value` is $0.00. The spec assumed that refund requests would have a non-zero amount. The $0.00 case is a legitimate order state (promotional discount, gift, B2B bulk arrangement) that the spec did not anticipate.

**Gap located:** Section 3.2 — missing precondition: behavior when `total_value = 0.00`.

---

### Step 3: Why wasn't this caught in spec review or acceptance testing?

The spec review checklist (five questions from Chapter 7.4) was applied. The question "are constraints sufficient to prevent harmful outputs?" was marked as satisfied because reviewers were not prompted to consider $0-value orders.

The acceptance test suite (T-01 through T-14) did not include a test with a $0.00 order. The test inputs were constructed from "typical" orders. The $0.00 case was not in the testers' mental model because promotional discounts to $0 were treated as a billing edge case, not a support edge case.

**Two system failures combined:**
1. The spec reviewer did not ask "what is the minimum value of `total_value` and is that case handled?"
2. The test suite was not generated from the constraint list exhaustively — it was generated from scenarios, which missed cases outside the reviewers' experience.

---

### Step 4: What would have prevented this?

**A stronger constraint C3:** After this incident, C3 was updated:

*Before (v1.1):*  
> "The refund amount passed to `refund.initiate()` must be calculated from order data retrieved via `order.lookup()`, not from a customer-stated amount."

*After (v1.2):*  
> "The refund amount passed to `refund.initiate()` must be calculated from order data retrieved via `order.lookup()`, not from a customer-stated amount. If `total_value` is $0.00, do not initiate a refund. Inform the customer that the order shows no charge and escalate so a human agent can determine if a replacement or other resolution is appropriate."

**A constraint-driven test generation approach:** The test suite was extended with: for every constraint that has a boundary value (amounts, dates, status values), generate at least one test for the boundary and at least one test for the boundary-adjacent cases. The $0.00 value is adjacent to the ≤$150 constraint boundary; it should have been tested.

---

## Spec Gap Log Entry

| Field | Value |
|-------|-------|
| Date | 2026-01-12 |
| Spec | Account Executor v1.1 |
| Section | §3.2, C3 |
| Gap type | Missing precondition: zero-value order |
| Description | Spec did not specify behavior when order.lookup returns total_value = 0.00. Agent faithfully used 0.00 as refund amount. |
| Detected at | Production (post-execution, 14:37 UTC) |
| Caught by intent review? | No |
| Why not caught by intent review? | Reviewers did not consider promotional $0 orders as a distinct case |
| Resolution | C3 updated with explicit zero-value precondition in spec v1.2 |
| Constraint library update | Added to "zero-value order handling" in constraint library under payment/refund domain |
| Test suite update | Added T-15: refund request on $0.00 order |

---

## What This Postmortem Illustrates About the SDD Practice

**The spec constraint worked — and still produced a wrong outcome.** C3 was correctly designed to prevent a customer from inflating a refund amount. It was correctly followed by the agent. The outcome was still wrong. This is the "valid spec, wrong intent" failure category: the spec correctly expressed what the author intended, but the author's mental model was incomplete.

**The fix is always in the spec, not in the agent.** The instinct after an incident is to "fix the agent" — add instructions, add filters, add guardrails. The correct response is to find the spec gap and close it. An agent-side fix without a spec update is undocumented and will not be present in the next generation of the agent or in the test suite. Spec updates are durable; ad hoc agent adjustments are not.

**The Spec Gap Log closes the loop.** The gap log entry above records not just what happened but: which section, why it wasn't caught, what was changed, and what was added to the constraint library. The constraint library update — "zero-value order handling" — means that the next spec written for any agent that touches order refunds will have a constraint template that covers this case. The incident's value compounds across future specs.

**"Was this caught by intent review?" is the postmortem's most important question.** It was not caught. The answer tells us where to invest: not in more intent review sessions, but in the reviewer checklist — specifically, a prompt to review all boundary value cases for constraints that have numeric thresholds.

---

## Changes Made After This Incident

**Spec v1.2 updates:**
- C3 extended with zero-value precondition (see above)
- Section 6 (Success Criteria) added: SC8 — "Given a refund request on an order with total_value = 0.00, the agent does not initiate a refund and escalates."

**Constraint library update:**
- Added "payment/refund" domain entry: "Zero-value orders: orders with total_value = 0.00 may exist due to promotional discounts, gifts, or B2B arrangements. Refund initiation on these orders is not meaningful. Always check for zero-value before initiating any refund."

**Intent review checklist update:**
- Added question: "For each constraint that has a numeric threshold, has the behavior at and below the minimum value been specified?"

**Acceptance test suite — new tests added:**
- T-15: Refund on $0.00 promotional order → should escalate, not initiate $0.00 refund ✅
- T-16: Refund on 90-day boundary order (exactly 90 days since delivery) → should initiate ✅
- T-17: Refund on 91-day order → should escalate with out_of_scope ✅

---

## Summary

| Category | What happened |
|---------|--------------|
| Failure type | Spec gap — missing precondition for zero-value orders |
| Agent behavior | Correct execution of an incomplete spec |
| Detection | Automated reconciliation (not intent review, not output review) |
| Fix location | Spec (C3 extended), not agent instructions |
| Prevention | Constraint library update; reviewer checklist update; 3 new acceptance tests |
| Time to resolution | 4 hours from detection to spec v1.2 approval |

---

*This concludes Example 1. Continue to [A Code Generation Pipeline](../02-code-generation-pipeline/README.md)*


