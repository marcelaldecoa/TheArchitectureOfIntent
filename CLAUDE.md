# CLAUDE.md — context for working in this repo

This file is the handoff between Claude Code sessions. Keep it current.

## What this repo is

Two artifacts in one repo, both about *The Architecture of Intent*:

| Artifact | Path | Format | Purpose |
|---|---|---|---|
| **Book** | `src/` | mdBook (Markdown → HTML) | A practitioner field guide. ~80,000 words. Deploys to GitHub Pages on push to `main`. |
| **Paper** | `paper/` | Pandoc (Markdown → LaTeX → PDF) | The arXiv distillation. ~15,000 words / 34 pages. Position-and-framework paper. |

The paper is the **academic distillation** of the book. They share vocabulary and citations.

## Title and framing

- **Title:** *The Architecture of Intent*
- **Subtitle (book):** *A Field Guide to Designing and Shipping AI Agent Systems*
- **Subtitle (paper):** *A Framework for Designing Delegated Systems*

The framework's central claim: *intent is a primary design surface for any delegated system; AI agents are the most-acute current instance.*

Four load-bearing elements:
1. **Five archetypes** — Advisor, Executor, Guardian, Synthesizer, Orchestrator
2. **Four orthogonal calibration dimensions** — Agency, Autonomy, Responsibility, Reversibility
3. **Seven-category fix-locus failure taxonomy** — Cat 1 (Spec) through Cat 7 (Perceptual Failure)
4. **Spec-Driven Development** as the executable protocol layer

## Honest contribution accounting

The paper claims novelty for **three things only**:
- Cat 7 (Perceptual Failure) — new failure category for perceiving-then-acting agents
- Autonomy-vs-agency *operationalization* (orthogonality argument extending Shavit & Agarwal 2023)
- The *fix-locus* framing of the failure taxonomy

The paper does **not** claim novelty for: SDD (lineage from spec-kit and DevSquad), archetypes-as-concept (Anthropic *Building Effective Agents*), the four dimensions individually (SAE J3016, Shavit & Agarwal), or Cat 1–6.

When making future changes, preserve this accounting. Reviewers reward honest framing; overclaiming gets punished disproportionately.

---

## Repo structure (what to expect where)

```
.
├── CLAUDE.md                          ← you are here
├── README.md                          ← public-facing book overview
├── book.toml                          ← mdBook config
├── src/                               ← the BOOK
│   ├── SUMMARY.md                     ← table of contents (mdBook reads this)
│   ├── introduction.md, prologue.md, how-to-read.md, miniature-pilot.md, cover.md
│   ├── images/                        ← book-side image copies (currently: framework canvas mirror, kept in sync by the GH workflow)
│   ├── foundations/                   ← Part 0: what is AoI, intent vs implementation, calibration, failure modes, what changes for senior engineers, intent design session
│   ├── frame/                         ← Part 1: archetypes (incl. archetype voice files), dimensions, decision tree, composition, multi-agent + frame/scenarios/
│   ├── specify/                       ← Part 2: SDD, spec lifecycle, canonical spec template, ADRs, SpecKit + specify/scenarios/
│   ├── delegate/                      ← Part 3: what agents are, autonomy vs agency, executor model, least capability, skills, agent classes, MCP/ + delegate/scenarios/
│   ├── validate/                      ← Part 4: intent review, signal metrics, evals, red-team + validate/scenarios/
│   ├── evolve/                        ← Part 5 (EVOLVE & OPERATE): Evolution sub-section (closed loop, anti-patterns, framework versioning) + Operations sub-section (governance, cost, cacheable prompts, telemetry, adoption playbook, MVP-AoI, DevSquad mapping, co-adoption) + evolve/scenarios/
│   ├── patterns/                      ← ~50 pattern one-pagers (capability/integration/coordination/safety/observability/testing/state/deployment); referenced from the Part that consumes them
│   ├── repertoires/                   ← spec templates, code standards (referenced from Part 2 and Part 6)
│   ├── examples/                      ← v1.x worked pilots archive (preserved on disk; not listed in SUMMARY; reached via appendices/legacy-pilots.md); superseded by phase scenarios in Parts 1–5
│   └── appendices/                    ← glossary, pattern index, reading paths, companion paper, legacy-pilots archive, references, archetype card, RACI card, MCP & skills card, model-tier card
├── paper/                             ← the PAPER + companion DECKS
│   ├── architecture-of-intent.md      ← Pandoc Markdown source for the paper
│   ├── architecture-of-intent.pdf     ← compiled paper PDF (committed for convenience)
│   ├── architecture-of-intent.pptx    ← teaching-deck PowerPoint (committed)
│   ├── architecture-of-intent.html    ← teaching-deck self-contained HTML (committed)
│   ├── references.bib                 ← BibTeX (~30 entries)
│   ├── figures/
│   │   ├── architecture-of-intent-canvas.svg + .png ← Figure 1 — framework on one page (mirror of PNG also lives in src/images/)
│   │   ├── archetype-decision-tree.svg + .png      ← Figure 2
│   │   └── four-dimensions-orthogonality.svg + .png ← Figure 3
│   ├── presentation_content.py        ← single source of truth for both decks
│   ├── build_presentation.py          ← builds the PPTX from presentation_content.py
│   ├── build_html_presentation.py     ← builds the HTML deck from presentation_content.py
│   ├── check-deck-sync.py             ← deck/paper sync check (see contract below)
│   └── README.md                      ← paper + deck build instructions
├── scripts/                           ← helper scripts (link/orphan checkers)
├── theme/                             ← mdBook custom CSS/JS
└── .github/workflows/
    ├── deploy.yml                     ← publishes book to GitHub Pages on push to main
    └── build-paper.yml                ← "Compile paper & decks" — auto-rebuild artifacts
                                          when paper sources change on main; opens
                                          bot/paper-artifacts PR via peter-evans/create-pull-request
```

## Build & verification commands

### Compile the paper to PDF

```bash
pandoc paper/architecture-of-intent.md \
  --citeproc \
  --bibliography paper/references.bib \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  --output paper/architecture-of-intent.pdf
```

Required tooling: `pandoc`, `texlive-xetex`, `texlive-fonts-recommended`, `texlive-latex-recommended`. SVG figures are pre-rendered to PNG; `librsvg2-bin` is *not* required at compile time.

### Check internal links and orphans (book)

```bash
python3 scripts/check-internal-links.py
python3 scripts/check-orphans.py
```

Both are fast and run before every commit that touches the book or SUMMARY.

### Build the book locally

```bash
mdbook build           # output to ./book/
mdbook serve --open    # live reload at localhost:3000
```

GitHub Actions auto-publishes on push to `main` via `.github/workflows/deploy.yml`.

### Build the teaching decks (PPTX + HTML)

```bash
python3 paper/build_presentation.py        # → paper/architecture-of-intent.pptx
python3 paper/build_html_presentation.py   # → paper/architecture-of-intent.html
```

Both consume `paper/presentation_content.py` as their single source of truth. Edit slide text once, rerun both builders. Requires `python-pptx`, `Pillow`, and `lxml`.

The HTML deck supports arrow-key navigation, an overview grid (`o`/`Esc`), fullscreen (`f`), and print-to-PDF (`p`). Both paper figures are embedded as inline SVG.

### Check deck/paper sync

```bash
python3 paper/check-deck-sync.py
```

Verifies that the small set of load-bearing named facts (5 archetypes, 7 Cat names, 4 Cat 7 sub-categories, 8 DevSquad phases, 3-novel/4-not-claimed honest-accounting cardinality) match between paper source and deck source. Run before committing paper or deck changes. See "Deck / paper sync contract" below.

### Auto-rebuild on main (`.github/workflows/build-paper.yml`)

The "Compile paper & decks" workflow fires on push to `main` when any of these change:
- `paper/architecture-of-intent.md`, `paper/references.bib`
- `paper/figures/**.svg`
- `paper/build_presentation.py`, `paper/build_html_presentation.py`, `paper/presentation_content.py`
- `.github/workflows/build-paper.yml`

It runs the sync check, regenerates figure PNGs, rebuilds the PPTX + HTML decks, recompiles the PDF, uploads everything as workflow artifacts (90-day retention), and opens (or updates) a single `bot/paper-artifacts` PR with the rebuilt artifacts via `peter-evans/create-pull-request@v7`. Uses `GITHUB_TOKEN` only — no PAT required. Loop-safety: trigger watches *source* paths only; the bot's commit only touches *artifact* paths, so it can't retrigger itself.

Required runner packages (already in the workflow): `pandoc`, `texlive-xetex`, `texlive-fonts-recommended`, `texlive-latex-recommended`, `texlive-latex-extra`, `lmodern`, `librsvg2-bin`. The `lmodern` package is required separately on Ubuntu — `lmodern.sty` is not in `texlive-fonts-recommended` there.

---

## Conventions that matter

### Branch naming
`claude/<short-descriptive-name>` — e.g., `claude/paper-section-3`, `claude/devsquad-second-pass`. One PR per pass.

### PR descriptions
Verbose by design. Honest accounting matters: what changed, what didn't change, what was deliberately left out, why. Reviewers read these as the change record.

### Citation style in paper
Pandoc `[@key]` inline citations. Bibliography in `paper/references.bib`. Pandoc + `--citeproc` resolves at compile time.

### Citation key convention
`<authorOrOrg><Topic><Year>` — e.g., `@anthropicMCP2024`, `@microsoftDevSquadCopilot2026`, `@cemriMAST2025`.

### "Structural fixes live in spec / manifest / CI / platform — never only in the prompt"
This is a *load-bearing discipline* for the framework. When a Cat 1 / Cat 3 hybrid (e.g., the deleted-tests example) recurs, the fix is structural: NOT-authorized clauses, tool-manifest scope, CI guard. Prompt-level patches don't compound.

### Deck / paper sync contract
Both `paper/architecture-of-intent.md` (the paper) and `paper/presentation_content.py` (the teaching-deck source) reference a small set of load-bearing named facts: the five archetype names, the seven failure category names, the four Cat 7 sub-category names, the eight DevSquad phase names, and the "3 novel / 4 not-claimed" honest-accounting counts.

These are checked by `paper/check-deck-sync.py`. The check runs in the "Compile paper & decks" GH Action *before* any build steps. Run it locally with `python3 paper/check-deck-sync.py` before committing paper or deck changes.

If you intentionally change any of these named facts, update **all three** places:
1. `paper/architecture-of-intent.md`
2. `paper/presentation_content.py`
3. `paper/check-deck-sync.py` — the `CANONICAL_*` lists

The script does NOT enforce prose alignment — only named-fact alignment. Freeform deck narrative can differ from paper prose.

---

## mdBook gotchas

### `SUMMARY.md` parser is strict
**Do not put italic paragraph text between a `##` sub-heading and its bullet list inside a numbered part.** mdBook reports the failure misleadingly as *"Suffix chapters cannot be followed by a list"* but the actual cause is the paragraph between heading and list. Italic descriptions go *only* under top-level `#` headings.

This caused PR #11 (deploy hotfix). The check-orphans script does *not* catch it; only `mdbook build` does. If `deploy.yml` fails, look here first.

### File numbering has gaps
Some directories have non-contiguous file numbers (e.g., `foundations/` has 01, 02, 03, 05, 07, 08 — no 04, 06; `evolve/` has 01, 04, 07, 09–16 — no 02, 03, 05, 06, 08). The gaps correspond to chapters cut/merged earlier. Don't renumber; cross-references rely on stable paths.

### Figures use `.png` not `.svg` in the paper
The paper's Markdown references PNG files (pre-rendered from SVG via `rsvg-convert`). Reasoning: arXiv build environments may not have `librsvg2-bin`; PNG is portable. SVG sources kept as the editable form.

If you edit a figure SVG, regenerate the PNG:
```bash
rsvg-convert --format=png --width=1600 paper/figures/archetype-decision-tree.svg \
  --output=paper/figures/archetype-decision-tree.png
```

### `rsvg-convert` mismeasures Georgia bold
The ORCHESTRATOR label in Figure 1 originally clipped because rsvg-convert's font-width estimate diverged from the SVG author's pixel calculation. Fix was to wrap the label as ORCHESTRA-TOR on two lines. If you add long labels in serif bold to figures, test by rendering at multiple widths.

---

## DevSquad Copilot — terminology to use

DevSquad's own README is sometimes informal; the docs site is more precise. Always use docs-site terminology for paper claims. Verified facts:

- **Released:** 2026 (not 2024–2025)
- **8 phases (exact names):** *envisioning phase → Spec the next slice → Plan only what the current slice needs → Decompose that slice → Implement with TDD discipline → Learn in the open → Review in an independent context → Refine continuously*
- **12 named specialist agents + conductor = 13 total:** *init, envision, kickoff, specify, plan, decompose, implement, review, security, sprint, refine, extend*
- **5 first-party MCP servers:** GitHub, Azure DevOps, Azure, Microsoft Learn, Draw.io
- **3 impact tiers:** low (skip ceremony), medium (plan + comprehension checkpoint + automated review), high (mandatory ADR + explicit approval + full review)
- **Config paths:** `.github/copilot-instructions.md`, `.github/docs/coding-guidelines.md`, `.github/instructions/<role>.instructions.md`
- **Invocation:** `copilot --agent devsquad:devsquad`; `--yolo` flag for unattended mode
- **Other named concepts:** comprehension checkpoint, reasoning log, "loop over ladder", 20-skill catalog (semantic activation)

The book uses paraphrases like "TDD-first" in some chapter bodies; that's an internal vocabulary choice consistent through those chapters. Do not bulk-rewrite. The exact names live in `src/operating/12-devsquad-mapping.md` (phase table), `src/appendices/references.md` (citation), and `src/operating/13-co-adoption-with-devsquad.md` vocabulary translation table.

For paper claims about DevSquad, always use exact names — see `paper/architecture-of-intent.md` Appendix B for the canonical statement.

---

## GitHub & MCP gotchas

### MCP server may disconnect mid-session
If you can't open PRs via `mcp__github__create_pull_request`, the MCP server has dropped. Check with `ToolSearch query "select:mcp__github__create_pull_request"`. If returned `No matching deferred tools found`, the server is gone for the session. Two options:
- User restarts Claude session to reconnect
- User opens PRs manually via `https://github.com/marcelaldecoa/TheArchitectureOfIntent/pull/new/<branch>`

### Sandbox blocks remote branch deletion
`git push --delete <branch>` fails with HTTP 403 from this environment. Local branch deletion works. To clean up merged remote branches, use the GitHub UI: https://github.com/marcelaldecoa/TheArchitectureOfIntent/branches

### GitHub MCP scope
The MCP is restricted to `marcelaldecoa/thearchitectureofintent`. Calls to other repos will be denied.

### Repo name vs. brand name
The repo is `TheArchitectureOfIntent` (preserves the GitHub Pages URL). The book and paper title is *The Architecture of Intent*. Repo name not renamed because the Pages URL `marcelaldecoa.github.io/TheArchitectureOfIntent/` would break for any external links.

---

## Recent meaningful decisions

- **Title:** kept "The Architecture of Intent" after briefly trying "Intent Engineering" (PR #14 → #15 reverted). The original title is more memorable, paper-friendly, and citation-friendly. The subtitle is the practical-signal layer.
- **Position paper, not empirical:** the paper does not claim empirical validation at scale; §6 names this explicitly.
- **arXiv first, workshop later:** the paper is sized for arXiv (no length limit). For workshop submission, a length-cut pass is needed (~34 pages now; most workshops cap at 10–12). Compression strategy documented in earlier PR descriptions.
- **`--yolo`, comprehension checkpoint, config paths:** all *are* documented in DevSquad (just in the docs site, not the README). My earlier review dismissed several as unverified — that was wrong; PR #27 corrected. If you read these things in old session transcripts, the corrections are now in main.
- **Teaching deck shipped (PR #33):** companion 19-slide deck for explaining the framework. Modern aesthetic — off-white + indigo + amber palette, asymmetric layouts, native python-pptx shapes for the data slides, paper figures embedded for the figure slides. Two outputs from one source: PPTX and self-contained HTML. The HTML deck is browser-navigable with keyboard shortcuts and prints to a 13.333×7.5" PDF.
- **Paper figures redesigned (PR #33, #36):** Figure 1 (decision tree) — card-based layout with dark-navy archetype result cards, ORCHESTRATOR no longer wraps; Figure 2 (orthogonality plot) — tinted quadrants, white pill labels with leader lines, no overlap. Pill widths widened in #36 after a font-fallback caused "Autonomous coding agent (Devin-class)" to overflow. If you add long pill labels in future, give them ≥40px of margin so font fallbacks don't bite.
- **Pattern Reference renamed → Cross-Cutting Patterns (PR #32):** the SUMMARY's Part 7 section was misleadingly named — it lists 12 of the 50 patterns (the cross-cutting coordination + state ones); the other 38 live inside Parts 3–5. The new name signals these are cross-cutting patterns, not "the patterns list." Updated in 7 files.
- **Cat 7 backfilled into the book (PR #30):** the paper claimed novelty for a seven-category taxonomy but the book theory chapter still presented six. PR #30 added a full Cat 7 section to `src/foundations/05-failure-as-design-signal.md` and updated 8 other book files from "six" to "seven." Architecture chapter's parallel four-dimensions framing was also disambiguated against the calibration-dials framing in the same PR.
- **GH Action: "Compile paper & decks" (PR #34, #35, #37):** auto-rebuilds paper PDF, PPTX, HTML, and figure PNGs on `main` source changes. Direct push to `main` was the original design (PR #34) but failed at the push step; PR #35 switched to opening a `bot/paper-artifacts` PR via `peter-evans/create-pull-request@v7`, which works regardless of branch protection. PR #37 added `lmodern` and `texlive-latex-extra` to the apt install list (xelatex needed `lmodern.sty` which isn't in `texlive-fonts-recommended` on Ubuntu).
- **Deck/paper sync contract (PR #38):** added `paper/check-deck-sync.py` to enforce that load-bearing named facts (archetypes, Cat names, Cat 7 subs, DevSquad phases, honest-accounting counts) stay aligned between paper and deck. Runs in the GH workflow before any build step. Three-place contract documented below.
- **Single-page framework canvas (current pass):** added `paper/figures/architecture-of-intent-canvas.svg/.png` — a one-page diagram that puts every load-bearing list in the framework (3 questions, 4 activities, 5 archetypes, 4 dimensions, 12 spec sections, 8 pattern categories, 4 oversight models, 7 fix-locus failure categories, 4 signal metrics) in the activity row where it does work. Embedded as Figure 1 in paper §3 (renumbering the prior Fig 1 → Fig 2 and Fig 2 → Fig 3) and as the new "The framework on one page" section in `src/introduction.md`. The book references the PNG from `src/images/architecture-of-intent-canvas.png` (mdBook can only serve files under `src/`); the workflow's `Mirror cross-cutting figures into src/images/` step copies the rebuilt PNG there on every paper rebuild so the SVG in `paper/figures/` remains the single source of truth. The deliverables list in the Introduction was rewired so each item names which canvas row produces it. The glossary's "Architecture of Intent" entry now points at the canvas section anchor instead of the broken `[Introduction]` link.
- **Composition first-class, not a sixth archetype (current pass):** the book and paper now explicitly commit to composition as a *first-class design surface* rather than extending the taxonomy to six archetypes. Reasoning: the three 2026 pressure-point classes (coding agents, deep-research agents, self-improving / training agents) do not have a sixth primary act — coding agents and deep-research agents have several of the existing five used in sequence within a session; self-improving agents are honestly two-system deployments. Adding a "sixth" called "operates in multiple modes" would re-name composition while losing the structural clarity of declared transitions and cross-mode invariants. The framework remains open to extension if a class genuinely demonstrates a governance profile no composition provides; as of 2026, none does. Concrete changes: book chapter `architecture/02-canonical-intent-archetypes.md` "A working taxonomy, not a settled one" subsection rewritten to commit; book chapter `architecture/05-composing-archetypes.md` extended with **Pattern E (mode-switching)** for the three pressure-point classes plus a **Composition Declaration** sub-template fragment; canonical spec template `sdd/07-canonical-spec-template.md` §4 extended with the Composition Declaration sub-block (governing archetype, embedded components or modes, mode transitions, cross-mode invariants, per-component oversight notes); paper §3.2 gains a new "Where the taxonomy is under pressure, and why composition is the answer" paragraph after "Why five." This pass preserves the 5-archetype cardinality the deck/paper sync check enforces; the honest accounting in §1.3 ("3 novel / 4 not claimed") is unchanged because composition-first-class is a sharper commitment to an existing position, not a new claim.
- **Legacy v1.x worked pilots collapsed to single appendix entry (v2.3.1):** the multi-chapter `## Worked Pilots (legacy — superseded by phase scenarios in Parts 1–5)` listing in Part 6 — Reference is replaced by a single bullet *Legacy v1.x Worked Pilots Archive* under Appendices, pointing at a new `src/appendices/legacy-pilots.md` page. The 17 example files are preserved on disk; the new appendix lists every chapter of every pilot, names the v2.0.0 scenario that supersedes each, and gives reading guidance. The orphan checker `scripts/check-orphans.py` now whitelists `examples/` as intentionally-not-in-SUMMARY (the script's job is to catch *forgotten* orphans; intentionally-archived content reachable through the appendix should not trigger an error). Inbound references from `pattern-index`, `references`, `frame/scenarios/customer-support.md`, `frame/scenarios/coding-pipeline.md`, `miniature-pilot`, `evolve/11-adoption-playbook`, `speckit-reference`, and `companion-paper` all continue to resolve. PATCH because no commitment moves.
- **Part 5 split into Evolution / Deployment / Operations (v2.3.0):** renamed book Part 5 from "EVOLVE" to "EVOLVE & OPERATE" and reorganized its 11 chapters plus 5 deployment patterns into three reader-facing sub-sections (Evolution = closed loop, anti-patterns, framework versioning; Deployment Patterns = canary/rollback/spec versioning/model upgrade/deprecation; Operations = governance, cost, cacheable prompts, telemetry, adoption playbook, MVP-AoI, DevSquad mapping, co-adoption). The framework retains five activities (Frame, Specify, Delegate, Validate, Evolve); the rename acknowledges that *Evolve* in operation has an inseparable ongoing-ops slice the book treats together. Chapter subtitles, scenario subtitles, scenario H1s, and reading-path tables across Parts 1–5 updated for consistency; deck/paper sync clean (the activity count is unchanged). MINOR rather than MAJOR because no load-bearing commitment moves: Operate is treated as a slice of Evolve, not promoted to a sixth peer activity.
- **`src/theory/` → `src/foundations/` (v2.2.3):** completed the filesystem cleanup begun in v2.2.2 by renaming the Part 0 directory to match its Part label. After v2.2.2 the five Part directories (`frame/`, `specify/`, `delegate/`, `validate/`, `evolve/`) already matched their labels; `theory/` was the one explicitly deferred outlier. v2.2.3 closes the gap. ~170 cross-references swept across 57 files; 0 broken links; paper unchanged (it cites the book by repo URL, not by source-tree path). The CLAUDE.md repo-structure tree was also refreshed in the same pass — it had been stale beyond just `theory/`, still listing `architecture/`, `sdd/`, `agents/`, `operating/` from before v2.2.2's directory renames. Trade-off: bookmarks to `src/theory/...` URLs break; SUMMARY navigation is identical.
- **Framework versioning + reading guide (earlier pass):** introduced framework-level versioning so the discipline can evolve visibly. New `CHANGELOG.md` at repo root documents semver-ish convention (MAJOR breaks specs/sync; MINOR adds; PATCH refines) and seeds **v1.0.0 (2026-05-10)** as the first stable release. The book and paper move together — load-bearing commitments (5 archetypes, 4 dimensions, 7 Cats, 4 oversight models, 4 metrics, 4 activities, composition first-class) bump the framework version regardless of which artifact changes. README.md, paper status header, and a new **Framework Version** glossary entry surface the version. PR descriptions should name the bump and update CHANGELOG in the same commit. The companion paper now has bidirectional discoverability: paper Appendix A refreshed with the new content (canvas, IDS, composition declaration, anti-patterns) and explicitly cross-references the book; new book appendix `src/appendices/companion-paper.md` gives the inverse paper→book mapping with reading-mode guidance ("read paper first if evaluating; read book first if adopting; read both if rolling out organizationally"). Two new pattern-index By-Problem entries: "I'm evaluating the framework, not yet adopting it" and an updated "introducing to my team" pointing at both the miniature pilot and the paper.

---

## Open work / candidates for next sessions

### Paper
- **arXiv submission** (mechanical from current PDF). Action is on the human, not on Claude.
- **Length-cut version for workshop submission** (10–12 pages). Strategy: collapse §2's eight subsections into 4–5 thematic paragraphs; trim §3.3 (orthogonality argument) and §3.4 (Cat 7 sub-categories) where they ran longest.
- **HiL-Bench / Karpathy citations** — if the user has verifiable sources for the "judgment gap" empirical claim in §1.1–§1.2, swap the current "emerging 2026 evaluations" framing for proper citations.
- **Empirical validation** — future-work track. Surveying practitioner adoption across deployments for a "v2" empirical paper.

### Book
- **Multi-tenant fleet governance** — chapter the framework currently doesn't have; identified as a 2026 gap in the introduction's honest-scope section. Hard to write well without case studies.
- **Computer-use agent worked example** — the pattern index notes "no worked example yet" for computer-use. Cat 7 lands in concept but not in concrete pilot.
- **Pattern audit (item 9 from earlier review)** — already done in PR #13, finding was that the pattern library was sturdier than my own review claimed. Could be revisited if specific patterns surface as filler in practice.

### General
- **Bulk-delete merged remote branches** — sandbox can't do remote ref deletion; needs the GitHub UI.
- **Optional CI workflow** — currently `deploy.yml` runs `mdbook build` only on push to main, not on PRs. A PR-time mdBook build check would catch SUMMARY parse errors before merge.
- **Teaching deck refresh cadence** — when the paper acquires new claims or examples, walk the deck slide-by-slide to keep it representative. The sync check covers the named facts; prose alignment is on you.
- **Bot/paper-artifacts PR queue** — the auto-PR keeps reusing the same `bot/paper-artifacts` branch, so it shouldn't pile up. If you don't merge it for a long time and it goes stale, just close it; the bot reopens on the next source change.

---

## Session continuation playbook

When opening this repo in a new Claude session:

1. **Read this file first.** It's the registry.
2. **Check `git log --oneline -10`** to see recent merged PRs.
3. **Run the link/orphan checkers** before making any book changes:
   ```bash
   python3 scripts/check-internal-links.py && python3 scripts/check-orphans.py
   ```
4. **For deck or paper changes**, run the sync check:
   ```bash
   python3 paper/check-deck-sync.py
   ```
5. **Branch as `claude/<descriptive-name>`** for any non-trivial change.
6. **One PR per pass.** Verbose PR descriptions; honest accounting.
7. **For paper changes:** verify the PDF still compiles cleanly (`pandoc` command above) before committing the .md so the committed PDF stays current. The "Compile paper & decks" workflow will rebuild on merge to main, but local verification catches errors faster.
8. **For deck changes:** edit `paper/presentation_content.py` (the shared content), then rebuild both decks via `build_presentation.py` and `build_html_presentation.py`.
9. **For DevSquad-related changes:** verify against the docs site, not just the README. Always.
