"""
Single source of truth for the teaching deck content.

Both build_presentation.py (PPTX) and build_html_presentation.py
consume this. Edit content here, rerun both builders.
"""

# ========================================================================
# Modern palette
# ========================================================================
PALETTE = {
    "bg":          "#FAFAF7",
    "bg_dark":     "#0F1729",
    "ink":         "#0F1729",
    "ink_light":   "#FFFFFF",
    "muted":       "#64748B",
    "muted_2":     "#94A3B8",
    "rule":        "#E2E8F0",
    "card":        "#FFFFFF",
    "indigo":      "#6366F1",
    "indigo_dark": "#4338CA",
    "amber":       "#F59E0B",
    "amber_pale":  "#FEF3C7",
    "amber_dark":  "#92400E",
    "emerald":     "#10B981",
    "emerald_dark":"#166534",
    "rose":        "#E11D48",
    "rose_dark":   "#9F1239",
}

# ========================================================================
# Slide content
# ========================================================================
TITLE        = "The Architecture of Intent"
SUBTITLE     = "A Framework for Designing Delegated Systems"
AUTHOR       = "Marcel Aldecoa"
YEAR         = "2026"
PAPER_KIND   = "Position-and-framework paper · ~15,000 words / 34 pages"

# Each slide: { "kind": "...", **fields }

SLIDES = [
    # --------------------------------------------------------------- 1
    {
        "kind": "cover",
        "eyebrow": "TEACHING DECK",
        "title":   TITLE,
        "subtitle": SUBTITLE,
        "author":  AUTHOR,
        "year":    YEAR,
        "note":    PAPER_KIND,
    },
    # --------------------------------------------------------------- 2
    {
        "kind": "roadmap",
        "section": "ROADMAP",
        "title":   "What we'll cover",
        "items": [
            ("01", "The problem",
             "Why intent is a design surface, and the judgment gap of 2024–2026"),
            ("02", "The framework",
             "Five archetypes · four dimensions · seven failures · spec-driven development"),
            ("03", "Application",
             "Coding agents, computer-use agents, composition with DevSquad Copilot"),
            ("04", "Honest accounting",
             "What is novel, what is borrowed, what we deliberately don't claim"),
            ("05", "Take-homes",
             "Limitations, where the framework breaks, what to try Monday morning"),
        ],
    },
    # --------------------------------------------------------------- 3
    {
        "kind": "quote",
        "section": "01 · THE PROBLEM",
        "headline":  "Delegation is a structural problem.",
        "body": [
            "Humans must express intent precisely enough that a non-human",
            "executor can act on it without supervisory rescue.",
        ],
        "footnote": "The framework's central claim is that intent is a primary design artifact distinct from implementation. AI agents are the class where this becomes load-bearing — because the executor is probabilistic.",
    },
    # --------------------------------------------------------------- 4
    {
        "kind": "compare",
        "section": "01 · THE PROBLEM",
        "title":   "The judgment gap",
        "tagline": "An execution-first bias in current agent harnesses",
        "left": {
            "label":  "SENIOR ENGINEER",
            "color":  "indigo",
            "items": [
                "Surfaces ambiguity before acting",
                "Asks \"is this what you mean?\"",
                "Refuses ill-posed work",
                "Treats clarification as load-bearing",
            ],
        },
        "right": {
            "label":  "LLM AGENT (with AskUserQuestion)",
            "color":  "amber",
            "items": [
                "Executes first, even on under-specified work",
                "Pauses rarely, even when tools exist",
                "Reaches for action before reaching for clarification",
                "Tool exists; judgment to use it is not yet calibrated",
            ],
        },
    },
    # --------------------------------------------------------------- 5
    {
        "kind": "compare",
        "section": "01 · HONEST ACCOUNTING",
        "title":   "What we claim, what we don't",
        "tagline": "Reviewers reward narrow novelty claims. Overclaiming gets punished.",
        "left": {
            "label":  "CLAIMED AS NOVEL  ·  3",
            "color":  "emerald",
            "items": [
                "Cat 7 (Perceptual Failure) for perceiving-then-acting agents",
                "Orthogonality of agency × autonomy (extends Shavit & Agarwal 2023)",
                "Fix-locus framing of the failure taxonomy",
            ],
        },
        "right": {
            "label":  "EXPLICITLY NOT CLAIMED",
            "color":  "muted",
            "items": [
                "SDD as a discipline  —  lineage: spec-kit, DevSquad",
                "Archetypes as concept  —  lineage: Anthropic Building Effective Agents",
                "Four dimensions individually  —  lineage: SAE J3016, Shavit & Agarwal",
                "Cat 1–6 as categories  —  synthesis from common practice",
            ],
        },
    },
    # --------------------------------------------------------------- 6
    {
        "kind": "table",
        "section": "02 · ACTIVITIES",
        "title":   "Five activities, one canvas",
        "tagline": "The framework is organized along an activity spine. Each activity binds a specific load-bearing list; reading the framework along the spine makes the rest fit together.",
        "headers": ["Activity", "Binds", "Output"],
        "rows": [
            ["Frame",     "5 archetypes · 4 dimensions",            "Archetype + calibration"],
            ["Specify",   "12 spec sections · sub-blocks",          "The canonical spec"],
            ["Delegate",  "8 pattern categories · 4 oversight",     "Bound agent + oversight"],
            ["Validate",  "7 failure cats · 4 signal metrics",      "Diagnosed failures, fix-locus"],
            ["Evolve",    "Closed loop · audit · versioning",       "Structural amendments"],
        ],
    },
    # --------------------------------------------------------------- 7
    {
        "kind": "cards4",
        "section": "02 · THE FRAMEWORK",
        "title":   "Four load-bearing elements bound to the spine",
        "tagline": "The synthesis is the larger contribution. The four bind into a framework you can apply in design, in spec review, and in post-incident diagnosis.",
        "cards": [
            ("01", "ARCHETYPES",
             "Five canonical delegation shapes",
             "Advisor · Executor · Guardian · Synthesizer · Orchestrator", "indigo"),
            ("02", "DIMENSIONS",
             "Four orthogonal calibration dials",
             "Agency · Autonomy · Responsibility · Reversibility", "indigo"),
            ("03", "FAILURE TAXONOMY",
             "Seven categories by fix locus",
             "Cat 1 (Spec) → Cat 6 (Model) · Cat 7 (Perceptual) — NOVEL", "amber"),
            ("04", "PROTOCOL",
             "Spec-Driven Development",
             "An executable spec the agent runs and a human validates", "indigo"),
        ],
    },
    # --------------------------------------------------------------- 7
    {
        "kind": "table",
        "section": "02.1 · ARCHETYPES",
        "title":   "Five canonical delegation shapes",
        "tagline": "Pre-commit a system to one shape before design begins. Composition is permitted.",
        "headers": ["Archetype", "Primary intent", "Examples"],
        "rows": [
            ["Advisor",      "Surfaces options; the human acts",  "Code-review suggester · search agent"],
            ["Executor",     "Acts within a defined scope",       "CI/CD pipeline · deploy agent"],
            ["Guardian",     "Vetoes; protects a boundary",        "Compliance gate · safety filter"],
            ["Synthesizer",  "Combines inputs into a new whole",   "Research summarizer · report generator"],
            ["Orchestrator", "Coordinates other agents/services",  "Multi-agent supervisor · planner"],
        ],
    },
    # --------------------------------------------------------------- 8
    {
        "kind": "figure",
        "section": "02.1 · ARCHETYPES",
        "title":   "The selection tree",
        "tagline": "Apply each question in order. Stop at the first match. Risk-override applies.",
        "image":   "archetype-decision-tree.png",
        "svg":     "archetype-decision-tree.svg",
        "caption": "Figure 1. Composition is permitted: a deployment may host multiple archetypes.",
    },
    # --------------------------------------------------------------- 9
    {
        "kind": "cards4",
        "section": "02.2 · DIMENSIONS",
        "title":   "Four orthogonal dials, set deliberately in the spec",
        "tagline": "Most teams collapse these into \"how autonomous is the agent?\" — the intuition hides the calibration work.",
        "cards": [
            ("AGENCY",        "discretion",      "How much judgment when instructions don't fully cover the situation", "", "indigo"),
            ("AUTONOMY",      "operation",       "How much of the work runs without human intervention at each step", "", "indigo"),
            ("RESPONSIBILITY","accountability",  "How accountability is distributed across the humans around the agent", "", "indigo"),
            ("REVERSIBILITY", "consequence",     "How easy or hard it is to undo what the agent did", "", "indigo"),
        ],
    },
    # --------------------------------------------------------------- 10
    {
        "kind": "figure",
        "section": "02.2 · DIMENSIONS",
        "title":   "Agency × Autonomy: orthogonal, not collinear",
        "tagline": "Treating both as a single \"automation level\" (e.g., SAE J3016) collapses the design space onto a diagonal. Real systems sit in all four quadrants.",
        "image":   "four-dimensions-orthogonality.png",
        "svg":     "four-dimensions-orthogonality.svg",
        "caption": "Figure 2. The other two dimensions (Responsibility, Reversibility) are similarly orthogonal.",
    },
    # --------------------------------------------------------------- 11
    {
        "kind": "taxonomy",
        "section": "02.3 · FAILURE TAXONOMY",
        "title":   "Seven categories, organized by fix locus",
        "tagline": "Diagnostic test: \"If a competent agent had executed this spec as written, would the outcome have been correct?\"",
        "rows": [
            ("Cat 1", "Spec",        "Spec was incomplete, ambiguous, or wrong",      "Update the spec",                                  False),
            ("Cat 2", "Capability",  "Agent lacked or misused a tool",                "Add or fix the tool / manifest",                   False),
            ("Cat 3", "Scope creep", "Agent did adjacent work it wasn't authorized",  "Tighten NOT-authorized clauses",                   False),
            ("Cat 4", "Oversight",   "Error escaped the review checkpoint",            "Redesign the oversight model",                     False),
            ("Cat 5", "Compounding", "Early error cascaded through later steps",       "Checkpoint at the handoff",                        False),
            ("Cat 6", "Model-level", "Model failed despite a correct spec",            "Narrow scope, switch model, or accept residual",   False),
            ("Cat 7", "Perceptual",  "Perception diverged from environment state",     "Structural controls + verification step",          True),
        ],
    },
    # --------------------------------------------------------------- 12
    {
        "kind": "cat7",
        "section": "02.3 · THE NOVEL CATEGORY",
        "title":   "Cat 7  —  Perceptual Failure",
        "tagline": "The system's perception of the environment diverged from the actual state, and the system acted on the wrong perception.",
        "subs": [
            ("Misidentification",     "Confirmation gate before high-consequence actions"),
            ("Missed element",        "Screenshot-then-verify before consequential action"),
            ("Hallucinated element",  "Element-allowlist + DOM-grounded verification"),
            ("State miscount",        "Re-verify position-based facts at action time"),
        ],
        "why": [
            "Prior taxonomies don't partition this — MAST, hallucination survey, OWASP LLM Top 10",
            "Applies only to perceiving-then-acting systems — computer-use · browser-use · robotic",
            "The fixes don't live in the prompt — they live in the spec, manifest, and verification step",
            "Smallest contribution that gives the taxonomy a slot for a class already observed",
        ],
    },
    # --------------------------------------------------------------- 13
    {
        "kind": "split_list",
        "section": "02.4 · SPEC-DRIVEN DEVELOPMENT",
        "title":   "SDD: the executable protocol layer",
        "tagline": "A spec the agent can run and a human can validate. Lineage: spec-kit (GitHub), DevSquad (Microsoft).",
        "left_title":  "13 canonical sections",
        "left_items":  [
            "1. Problem statement", "2. Objective",
            "3. Authorized scope",  "4. NOT-authorized scope",
            "5. Tool manifest",     "6. Invariants",
            "7. Non-functional",    "8. Acceptance criteria",
            "9. Execution instructions", "10. Oversight model",
            "11. Validation",       "12. Spec evolution log",
            "13. Spec gap log",
        ],
        "right_title": "How the framework maps in",
        "right_items": [
            ("Agency",          "lives in §3 (scope) and §4 (NOT-authorized)"),
            ("Autonomy",        "lives in §10 (oversight model)"),
            ("Responsibility",  "lives in §1 (problem) and §11 (validation)"),
            ("Reversibility",   "lives in §5 (manifest) and §6 (invariants)"),
            ("Each failure cat","maps to a specific update site"),
        ],
    },
    # --------------------------------------------------------------- 14
    {
        "kind": "callout_list",
        "section": "03 · APPLICATION  ·  CODING AGENTS",
        "title":   "Coding agents — where structural fixes compound",
        "tagline": "Most coding-agent failures look novel; nearly all map to a Cat 1–6 fix-locus.",
        "items": [
            ("The deleted-tests failure",
             "Cat 1 / Cat 3 hybrid. Fix in the spec (§4 NOT-authorized) and in CI (test-skip set monotonic) — never only in the prompt."),
            ("Three structural controls",
             "(1) PR-only branch protection. (2) Tool manifest excludes unrestricted shell. (3) Test-suite invariant in CI."),
            ("The discipline",
             "Structural fixes live in spec / manifest / CI / platform. Prompt-level patches don't compound."),
            ("What Cat 7 does NOT do here",
             "Coding agents are text-only. They have no perception–action interface that can diverge from environment state."),
        ],
    },
    # --------------------------------------------------------------- 15
    {
        "kind": "split_list",
        "section": "03 · APPLICATION  ·  COMPUTER-USE",
        "title":   "Computer-use — where Cat 7 becomes load-bearing",
        "tagline": "Anthropic Computer Use · OpenAI Operator · Gemini computer use — vision-then-action systems.",
        "left_title":  "New failure surfaces",
        "left_items":  [
            ("Lookalike-domain navigation", "homoglyph · typo · subdomain confusion"),
            ("Visual instruction injection", "rendered text treated as authoritative"),
            ("Modal popup interception",     "adversarial dialog read as legitimate prompt"),
        ],
        "right_title": "Four structural controls",
        "right_items": [
            ("Sandboxed environment",          "no host credentials, files, extensions"),
            ("Auth-scope minimization",        "redirects don't carry session cookies"),
            ("Domain allowlist",               "non-allowlisted redirect halts and surfaces"),
            ("High-consequence gates",         "irreversible-action class always gates"),
        ],
        "use_amber": True,
    },
    # --------------------------------------------------------------- 16
    {
        "kind": "table",
        "section": "03 · APPLICATION  ·  DEVSQUAD",
        "title":   "Composition with Microsoft DevSquad Copilot (2026)",
        "tagline": "DevSquad provides the cadence; the framework provides the design vocabulary. They compose cleanly when the artifact mapping is explicit.",
        "headers": ["Phase", "DevSquad activity", "Framework artifact"],
        "rows": [
            ["1–2", "Envisioning + Spec the slice",      "Archetype committed; provisional dimensions"],
            ["3",   "Plan only what the slice needs",    "Invariants in §6; ADRs constrain §8"],
            ["4",   "Decompose that slice",              "Least-Capability tool subset per task"],
            ["5",   "Implement with TDD discipline",     "Spec acceptance suite gates each commit"],
            ["6",   "Learn in the open",                 "Categorize Cat 1–7; trace to fix locus"],
            ["7",   "Review in independent context",     "Validation in fresh sub-agent context"],
            ["8",   "Refine continuously",               "Four signal metrics drive next sprint"],
        ],
    },
    # --------------------------------------------------------------- 17
    {
        "kind": "callout_list",
        "section": "04 · LIMITATIONS",
        "title":   "Where this framework breaks",
        "tagline": "Position-and-framework paper. No quantitative validation at scale yet — acknowledged explicitly.",
        "items": [
            ("Position paper, not empirical",
             "Applied across three worked examples. Quantitative validation across many independent deployments is future work."),
            ("Coarse partitions",
             "Five archetypes, four dimensions, seven categories — opinionated rather than derived."),
            ("Multi-tenant fleet governance is missing",
             "The framework currently does not address governance of large fleets of agents at scale."),
            ("Cardinality is judgment, not theorem",
             "Reasonable readers may propose six categories or eight; the framework's working choice is seven."),
            ("Cat 7 sub-categories may evolve",
             "Computer-use is young; the four sub-categories will likely be revised as the deployment surface matures."),
        ],
    },
    # --------------------------------------------------------------- 18
    {
        "kind": "callout_list",
        "section": "05 · TAKE-HOMES",
        "title":   "What to try Monday morning",
        "tagline": "Five concrete experiments any team can run on the system they're building today.",
        "items": [
            ("Pick one agent system you're operating",
             "Run the archetype decision tree against it. Does the result match what you have today?"),
            ("Write the spec for its most consequential action",
             "Use the canonical template. Focus on §3 (scope) and §4 (NOT-authorized). The first draft will feel incomplete — that is the point."),
            ("Categorize the first three failures",
             "Apply the diagnostic test, walk Cat 1–7, trace to the fix locus. How many were spec gaps versus model limits?"),
            ("Surface ambiguity, don't resolve",
             "When the spec is unclear, the agent's job is to surface, not to guess. Wire AskUserQuestion into the harness AND calibrate the judgment to use it."),
            ("Compound the learning",
             "Each diagnosed failure improves a spec or a skill. The improvement is durable and propagates to every future task."),
        ],
    },
    # --------------------------------------------------------------- 19
    {
        "kind": "discussion",
        "section": "DISCUSSION",
        "title":   "Three prompts to start the conversation",
        "questions": [
            "Where in your team is intent currently implicit, and where would making it explicit pay off most?",
            "What's the last agent failure you saw — and which Cat 1–7 was it, really?",
            "Are your structural controls (spec, manifest, CI, platform) doing the work that today still lives in prompts?",
        ],
        "footer": "Paper · marcelaldecoa.github.io/TheArchitectureOfIntent  ·  Companion book at the same site",
    },
]
