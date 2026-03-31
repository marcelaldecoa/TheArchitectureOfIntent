# How to Read This Book

---

This book supports two reading modes. Choose the one that fits where you are.

---

## Mode 1: Linear (The Book)

Read from beginning to end. Start with [Introduction](introduction.md), proceed through the Foundations, and let the abstraction tighten gradually from philosophy to execution.

This mode is best if:
- You are new to the concepts of spec-driven development or intent engineering
- You are preparing to advocate for this shift within your organization
- You want the full vocabulary before working with the templates and catalogs

Estimated time to read linearly: 8–12 hours. But this book is not meant to be consumed in a sitting. Read a section, put it down, apply it, return.

---

## Mode 2: Non-Linear (The Reference)

Enter from wherever your current work lives. Use the table of contents, the [Pattern Index](appendices/pattern-index.md), or the [Glossary](appendices/glossary.md) as entry points.

Useful entry points by role:

| If you are... | Start here |
|---------------|------------|
| **Writing a spec today** | [The Canonical Spec Template](sdd/07-canonical-spec-template.md) |
| **Choosing how to deploy an agent** | [The Archetype Selection Tree](architecture/04-decision-tree.md) |
| **Designing oversight for an AI system** | [Proportional Oversight](agents/06-human-oversight-models.md) |
| **Restructuring your team's skills** | [The Intent-Era Skill Matrix](operating/01-skill-matrix.md) |
| **Starting an applied example** | [How to Use These Examples](examples/00-how-to-use.md) |
| **Confused about a term** | [Glossary](appendices/glossary.md) |

---

## The Page Format

Each content page follows this structure, inspired by A Pattern Language:

1. **Name and position** — Which part and pattern number this is
2. **Context** — Where this pattern applies and what it assumes
3. **The Problem** — The specific tension this chapter resolves, stated precisely
4. **The Resolution** — The body of the chapter: how this works, why, with examples
5. **Therefore** — A bold summary statement, the way Alexander used *Therefore*, capturing the resolution in one sentence
6. **Connections** — What patterns this assumes; what patterns it enables

Some chapters also include:
- **Code examples** — Concrete, standards-compliant code illustrating the concept
- **Spec examples** — Fragments of real specs showing intent expressed well
- **Anti-patterns** — What failure looks like when this pattern is absent

---

## About the Code Examples

Code in this book is **authoritative by intent, not by completeness**. Snippets are written to patterns described in Part VI, and are meant to serve as anchors for agents — structures that can be extended, not copied verbatim.

Languages covered: C# / .NET, TypeScript / Node, Python, REST API design, infrastructure as code.

Every code example includes:
- A comment naming the pattern it instantiates
- The spec constraint it satisfies
- The boundary it must not cross

---

## About the Archetype Definitions

The Intent Archetypes in Part III and the Catalog in Part VI are the core vocabulary of this book. They appear in specs, in agent instructions, in design reviews, and in governance conversations.

If you encounter a reference to "the Executor archetype" or "the Guardian pattern" and do not recognize it, the [Archetype Quick-Select Card](appendices/archetype-card.md) gives you a one-page summary.

---

*You are ready. Begin with [Part I](foundations/01-end-of-human-compiler.md) or enter anywhere.*
