# Pattern 5.1 — What Agents Are (and Are Not)

**Part V: Agents & Execution** · *1 of 7*

---

> *"The navigator is not the ship. But the ship goes nowhere without one."*

---

## Context

You have been using AI tools. A colleague proposes "deploying an agent" to handle a workflow your team runs manually. A vendor demonstrates an "AI agent platform." A job posting asks for experience with "agentic systems."

Each of these uses the same word — agent — to describe something materially different in terms of capability, risk, and architectural implication. Without a precise definition, every conversation about agents is secretly a conversation about different things. Every design decision sits on an unstable foundation.

This chapter opens Part V with first principles. It assumes familiarity with the intent vocabulary from Parts I–III and the spec discipline from Part IV.

---

## The Problem

The word *agent* is used to describe:

- A chatbot with memory that persists across conversations
- An automation script triggered on a schedule
- A system that browses the web, runs code, and sends emails without being asked for each step
- A cloud process that coordinates ten other AI systems to complete a multi-day project

These things are not the same. The chatbot has no agency at all in the meaningful sense — it responds to prompts. The automation script executes deterministically — it follows a fixed path. Neither is an agent in the sense this book uses the term.

The conflation matters because it collapses the architecture. If everything is an "agent," nothing useful is said about authorization scope, oversight requirements, failure modes, or design patterns. The vocabulary fails exactly when precision is most needed.

---

## The Resolution

### The Defining Properties of an Agent

An agent, in the sense used throughout this book, is a system with three properties:

**1. Goal persistence.** An agent holds a goal across multiple steps and continues working toward it until the goal is achieved or a limit is reached. A chatbot responds to each message independently. An agent works on a problem — not just the last utterance.

**2. Action-taking.** An agent can take actions in the world: write files, call APIs, execute code, send messages, update databases. It is not confined to producing text that a human then acts upon. The action is direct. This is the property that confers both utility and risk.

**3. Iterative planning.** When an agent's first approach fails or produces unexpected results, it adapts. It re-reads the situation, adjusts its plan, and tries again. This is not a fixed loop — it is judgment under changing conditions. It is what distinguishes an agent from an automation script, which follows a fixed path regardless of outcomes.

These three properties together produce a system that can pursue goals in dynamic environments without step-by-step human instruction. That is the value. Those same properties are what make agent architecture consequential — a system that persists, acts, and adapts can do real damage if its intent is wrong or its boundaries are absent.

### What Agents Are Not

**Not autonomous in the volitional sense.** Agents do not have their own goals. They do not want things. They do not decide what to work on. Every agent in a well-designed system is executing intent that originated with a human. The word "autonomous" means only that the agent can complete multiple steps without human input per step — not that it operates independent of human intention.

**Not self-correcting in the architectural sense.** An agent that produces wrong output and retries is iterating within the same intent frame. It is not correcting a fundamental misunderstanding of what was wanted — it is trying different paths to the same destination. Architectural correction requires human review of the intent, not agent retries.

**Not a decision-maker.** Agents make choices within a defined space. They select which tool to call, which path to take, which phrasing to use. But the consequential decisions — what problem to solve, what constraints are non-negotiable, what success means — those belong to the human who writes the spec. Conflating operational choices with real decisions is a governance failure.

**Not a chatbot.** A chatbot produces output. An agent takes action. The distinction is not semantic — it determines whether human oversight is advisory (review the text before it goes anywhere) or operational (catch the error before the API call is made). Many tools that present as chat interfaces are actually agents, and the misclassification creates false confidence about the oversight required.

**Not a script.** A script executes a predefined sequence of steps. An agent decides at each step what to do next based on its current context, available tools, and the results of previous actions. A script fails deterministically when a step fails. An agent may route around the failure, which is powerful and also unpredictable if the routing takes it outside its intended scope.

### A Practical Taxonomy

| System Type | Goal Persistence | Action-Taking | Iterative Planning | Agent? |
|-------------|:---:|:---:|:---:|:---:|
| Chatbot / assistant | No | No | No | No |
| Automation / script | Fixed | Yes | No | No |
| Tool-augmented LLM | Per-prompt | Sometimes | No | Borderline |
| Reactive agent | Across steps | Yes | Limited | Yes |
| Deliberative agent | Across sessions | Yes | Yes | Yes |
| Multi-agent system | Distributed | Yes | Coordinated | Yes |

This book uses *agent* to mean any system that qualifies as "Yes" in that table — systems with goal persistence, the ability to take actions, and iterative planning capability.

### Why the Definition Matters for Architecture

The moment a system acquires all three properties, a set of architectural obligations follows:

- **A spec is required.** An agent working without a spec is pursuing a goal under unverified intent. The more capable the agent, the worse this gets — it will competently pursue the wrong thing.
- **Capability boundaries matter.** An agent with unrestricted access to tools will, eventually, use capabilities outside the intended scope. Least-capability design is not paranoia; it is routine engineering hygiene.
- **Oversight must be designed, not assumed.** A human watching the screen is not an oversight model. The failure modes of agents do not present as obvious errors requiring immediate response — they often look like correct execution of a subtly wrong intent. Oversight must be proactive and structured.
- **Failure attribution changes.** When a script fails, you debug the script. When an agent fails, the first question is whether the failure is a spec failure, a capability failure, or a scope failure. The debugging process is different. The fix is different.

These obligations are not burdens. They are the price of the capability. Systems that persist, act, and adapt can accomplish extraordinary things. The architecture exists to ensure they accomplish the *right* things.

---

## Therefore

> **An agent is a goal-persistent, action-taking, iteratively planning system — distinct from chatbots, scripts, and tool-augmented assistants. It is not volitionally autonomous; it executes delegated human intent. Accepting this definition makes every architectural question about agents tractable: it tells you what spec is required, what boundaries matter, what oversight is owed, and how to diagnose failure.**

---

## Connections

**This pattern assumes:**
- [What Is Intent Engineering?](../theory/01-what-is-intent-engineering.md)
- [Intent vs. Implementation](../theory/02-intent-vs-implementation.md)
- [The Five Archetypes](../architecture/02-canonical-intent-archetypes.md)

**This pattern enables:**
- [Operational Autonomy vs. Genuine Agency](02-autonomy-vs-agency.md)
- [Agents as Executors of Intent](03-agents-as-executors.md)
- [Human Oversight Models](06-human-oversight-models.md)
- [Failure Modes in Agent Systems](07-failure-modes.md)

---

*Next: [Operational Autonomy vs. Genuine Agency](02-autonomy-vs-agency.md)*


