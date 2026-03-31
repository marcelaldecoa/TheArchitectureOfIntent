# Reading List & References

**Appendices** · *Appendix C*

---

> *"Every book is in conversation with other books. These are the ones this book is most explicitly in debt to."*

---

This appendix has two sections: the **reading list** (books and papers worth reading alongside or after this one, with annotations about why) and the **formal references** (sources cited explicitly in the text).

---

## Reading List

### On Pattern Languages and Design

**Christopher Alexander, Sara Ishikawa, Murray Silverstein** — *A Pattern Language: Towns, Buildings, Construction* (1977)  
The structural ancestor of this book. Alexander's pattern language format — each pattern names a problem, describes its context, offers a solution, and gestures to related patterns — is the direct inspiration for how the Architecture of Intent is organized. Alexander's insight that patterns must address real problems observed in the world rather than invented problems invented for theoretical elegance is a discipline this book tries to honor. Read at least the introduction and Patterns 1–50 before concluding that a "pattern language" is just a list of best practices.

**Christopher Alexander** — *The Timeless Way of Building* (1979)  
The companion volume to A Pattern Language, addressing why the language works and what kind of knowledge it embodies. More philosophical than its partner. The opening section on "the quality without a name" — the felt sense that a design is alive rather than dead — maps imperfectly but meaningfully onto the felt sense that a well-written spec captures something real, where a poorly-written spec merely covers the surface.

**Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides** — *Design Patterns: Elements of Reusable Object-Oriented Software* (1994)  
The software engineering application of Alexander's approach to a specific technical domain. Useful primarily as a calibration for what it means to make a pattern catalog in software: each pattern is a reusable solution to a recurring problem, not a universal principle. The Gang of Four's discipline of naming both the problem and the context before the solution is something many "best practices" documents abandon.

---

### On Software Architecture and Intent

**Frederick P. Brooks Jr.** — *The Mythical Man-Month: Essays on Software Engineering* (1975, Anniversary Edition 1995)  
Still the most honest book about why software development is hard and why the difficulty is not engineering but communication. "No Silver Bullet" (the 1986 essay included in the anniversary edition) is directly relevant — Brooks argues that the accidental complexity of software can be reduced but the essential complexity cannot. Agents reduce accidental complexity significantly. The essential complexity — understanding and precisely encoding what the software must do — does not diminish. SDD is a practice for addressing Brooks's essential complexity.

**Martin Fowler** — *Patterns of Enterprise Application Architecture* (2002)  
Less about the specific patterns (many of which have been superseded) and more about the discipline of naming architectural patterns in a domain — what counts as a pattern, how to scope one, when multiple patterns apply to the same problem. The catalog format is a good reference when designing your own archetype catalog.

**Michael C. Feathers** — *Working Effectively with Legacy Code* (2004)  
Indirectly relevant but important: a book about how to work with systems you didn't design, which did not capture their own intent, and which express accumulated undocumented decisions. The scenarios Feathers describes are precisely the systems that will increasingly exist as the gap between "code that was generated" and "intent that was specified" grows. The antidote to Feathers's problem is not heroic debugging but SDD.

---

### On Agency, Autonomy, and AI Systems

**Stuart Russell** — *Human Compatible: Artificial Intelligence and the Problem of Control* (2019)  
Russell's argument for moving from systems that optimize for a fixed objective to systems that are fundamentally uncertain about human preferences — and which therefore seek human input rather than acting unilaterally on assumed preferences. The alignment problem as stated by Russell is the same problem this book addresses at the organizational practice level: how do you ensure an agent does what you actually want rather than what you literally specified? Russell's answer (preference uncertainty, deference to humans) maps onto the SDD answer (tight specs, validation loops, oversight models).

**Nick Bostrom** — *Superintelligence: Paths, Dangers, Strategies* (2014)  
More speculative and extreme than Russell, and parts of it have aged poorly in the face of how LLMs actually work. Still worth reading as a systematic catalog of ways that capable AI systems can fail to do what their designers intended. The "paperclip maximizer" thought experiment, however cartoonish, is a useful conceptual tool for understanding why Executors with poorly-bounded objectives are dangerous.

**Kate Crawford** — *Atlas of AI: Power, Politics, and the Planetary Costs of Artificial Intelligence* (2021)  
A critical counterweight to the technical optimism that pervades most AI engineering literature. The costs — labor, environmental, political — that AI systems impose on the world do not appear in spec templates or archetype catalogs. They are real, and the architects of AI systems are responsible for them in ways this book touches but does not fully address.

---

### On Specification and Formal Methods

**Michael Jackson** — *Software Requirements & Specifications: A Lexicon of Practice, Principles, and Prejudices* (1995)  
Jackson's *lexicon* is a deliberately opinionated catalog of concepts in requirements engineering, written with unusual clarity and wit. His distinction between "domains" (the real world the software must affect) and "machines" (the implementation) maps directly onto the intent/implementation distinction in this book. His concept of the "problem frame" — the way the world must be divided to understand what the software is supposed to do — is a precursor to what the spec template calls a Problem Statement.

**Bertrand Meyer** — *Object-Oriented Software Construction* (1988, 2nd ed. 1997)  
The origin of Design by Contract — the idea that software components make explicit promises about what they accept and what they guarantee. The constraint sections in SDD specs are Design by Contract formalized for agent behavior. Meyer's argument that correctness assertions should be first-class elements of program text, not documentation afterthoughts, directly anticipates the SDD argument that constraints belong in the spec, not in the implementation's comments.

---

### On AI Tools, MCP, and Modern Agentic Systems

**Anthropic** — *Model Context Protocol Specification*  
The formal specification for MCP: the open standard for how AI models connect to external tools and context sources. The spec is available at [modelcontextprotocol.io](https://modelcontextprotocol.io). Chapter 5.4 of this book provides the conceptual framing; the MCP spec provides the technical reference.

**Lilian Weng** — *LLM Powered Autonomous Agents* (2023)  
A comprehensive technical survey of agentic AI system architectures: planning, memory, tool use, multi-agent coordination. Available at [lilianweng.github.io](https://lilianweng.github.io). Useful as a technical companion to the agent-facing chapters of this book (Parts V and VI).

**Simon Willison** — Writings on prompt injection, LLM security, and agentic system risks  
Willison has been one of the most consistent and technically precise voices on the security implications of giving AI systems tool access. His writing on prompt injection in agentic contexts is directly relevant to Chapter 5.7 (Failure Modes) and the NOT-authorized sections of SDD specs. Available at [simonwillison.net](https://simonwillison.net).

---

### On Organizations and Human Systems

**W. Edwards Deming** — *Out of the Crisis* (1982)  
Deming's argument that quality problems are primarily system problems rather than worker problems is the direct ancestor of the SDD argument that spec gaps are primarily system problems — failures of constraint library, archetype catalog, and review process — rather than spec author failures. His 85/15 rule (85% of quality problems are caused by systems, 15% by individuals) should calibrate how you read the Metrics chapter (7.6).

**Donella Meadows** — *Thinking in Systems: A Primer* (2008)  
The clearest short introduction to systems thinking available. The concept of feedback loops — especially the distinction between balancing loops (self-correcting) and reinforcing loops (self-amplifying) — is directly relevant to understanding how the Spec Gap Log and first-pass validation rate function as balancing feedback in the SDD practice.

**Gene Kim, Patrick Debois, John Willis, Jez Humble** — *The DevOps Handbook* (2016)  
The practical handbook for high-performing engineering organizations. The Three Ways (flow, feedback, continual learning and experimentation) map cleanly onto SDD practice: spec-execute-validate is flow; the Spec Gap Log is feedback; the constraint library update cycle is continual learning. The DevOps transformation patterns (starting with a single value stream, building feedback loops) apply directly to introducing SDD in an organization.

---

## Formal References

These are sources cited specifically within the text of this book.

### Christopher Alexander

- Alexander, C., Ishikawa, S., & Silverstein, M. (1977). *A Pattern Language: Towns, Buildings, Construction.* Oxford University Press. — Referenced in the preface and throughout as the structural model for pattern organization.

### AI and Agent Systems

- Anthropic. (2024). *Model Context Protocol Specification.* Retrieved from https://modelcontextprotocol.io — Referenced in Part V, Chapters 5.4 and the MCP sub-chapters.

- Russell, S. (2019). *Human Compatible: Artificial Intelligence and the Problem of Control.* Viking. — Referenced in Chapter 2.3 (Three Dimensions of Delegation) and Chapter 1.5 (When Power Scales Faster Than Judgment).

- Weng, L. (2023). *LLM Powered Autonomous Agents.* Lil'Log. Retrieved from https://lilianweng.github.io/posts/2023-06-23-agent/ — Referenced in Part V as a technical taxonomy companion.

### Software Engineering

- Brooks, F. P. (1995). *The Mythical Man-Month: Essays on Software Engineering* (Anniversary ed.). Addison-Wesley. — Referenced in Chapter 1.1 (The End of the Human Compiler) for the no-silver-bullet framing.

- Feathers, M. C. (2004). *Working Effectively with Legacy Code.* Prentice Hall. — Referenced in Chapter 4.6 (The Living Spec) as an example of the systems SDD prevents.

- Fowler, M. (2002). *Patterns of Enterprise Application Architecture.* Addison-Wesley. — Referenced in Part VI as a model for catalog-format pattern documentation.

- Jackson, M. (1995). *Software Requirements & Specifications.* Addison-Wesley. — Referenced in Chapter 4.5 (Writing for Machine Execution) for the domain/machine distinction.

- Meyer, B. (1997). *Object-Oriented Software Construction* (2nd ed.). Prentice Hall. — Referenced in Chapter 4.2 (The Spec as Control Surface) for the Design by Contract parallel.

### Organizations and Systems

- Deming, W. E. (1982). *Out of the Crisis.* MIT Press. — Referenced in Chapter 7.6 (Four Signal Metrics) for the systems-vs-individuals framing of quality.

- Kim, G., Debois, P., Willis, J., & Humble, J. (2016). *The DevOps Handbook.* IT Revolution Press. — Referenced in Chapter 7.4 (Proportional Governance) for the Three Ways framework.

- Meadows, D. H. (2008). *Thinking in Systems: A Primer.* Chelsea Green. — Referenced in Chapter 4.6 (The Living Spec) for the feedback loop taxonomy.

---

*This list will be updated as the field develops. The most current version of the reading list is maintained at the book's companion site.*


