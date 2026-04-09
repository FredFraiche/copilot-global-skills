---
description: >
  Anti-lazy-implementation enforcement for plan-driven work. FIRES whenever the agent is
  given a plan, spec, roadmap, or multi-step goal. Triggers: "plan.md", "complete the plan",
  "implement this", "proceed with", "from the plan", "phase", "build this out", "finish this",
  "do everything in", "spec", "roadmap", "task list", "implementation plan", "execute this",
  "carry out the plan", "follow the plan".
---

# Plan Execution — Anti-Lazy Implementation

## What This Prevents

The default failure mode when working from a plan:

- Building correct **structure** with no **substance** (stubs, scaffolding, empty data)
- Implementing what the plan **says** rather than what the user **needs**
- Producing output that looks complete but delivers zero value
- Mistaking "the tool was written" for "it was run and produced output"
- Delivering 10 half-built things when the user needed 3 finished ones

## Phase 0 — Intent Extraction (MANDATORY)

Before writing any code:

### 0.1 Read the plan completely. Extract:

1. **Stated deliverables** — what the plan explicitly says to build
2. **Implied end state** — what a user would experience if this worked perfectly
3. **The gap** — where those two differ

### 0.2 Build a confidence map

For each phase or major component, rate 0-100%:
- **100%** — exact output is clear, zero ambiguity
- **70-99%** — approach is clear but one decision could derail it
- **< 70%** — ambiguous enough that a wrong assumption wastes significant work

### 0.3 Ask the user about every item below 100%

Use multiple choice with a recommended default. Key questions:
- **Depth vs. breadth** — build 3 things completely, or 10 things partially?
- **Real content vs. placeholder** — does the output need real data or is stubbed acceptable?
- **End-to-end vs. wired-up** — should this work fully, or connect to a pipeline the user activates later?
- **Priority** — if this can't all be done, what delivers the most value first?

### 0.4 State the true intent back and get confirmation

> "When I am done, a user who opens [the product] will experience [concrete description].
> The single most important thing to get right is [highest-value deliverable]."

**Get explicit confirmation before writing any code.**

## Phase 1 — Implementation Rules

### The Substance Rule

Every deliverable must contain real content, not structure waiting for content.

- "Populate knowledge blocks" -> output is populated blocks. Not a server that could populate them.
- "Build the pipeline" -> the pipeline runs and produces output. Not a scaffold.

Before marking anything done: **"If the user opened this right now, would they experience value or empty state?"**

### The Execution Rule

Writing a tool is not the same as running it. If the plan calls for a script to produce output — run it and include the output.

### The Honesty Rule

Use these exact labels for deliverable status:

- `DONE` — works end-to-end, contains real content, user can experience it now
- `SCAFFOLDED` — structure exists, requires [specific action] to activate
- `BLOCKED` — cannot complete, reason: [specific explanation]
- `SKIPPED` — not attempted, reason: [explanation]

**Never present `SCAFFOLDED` as `DONE`.**

### The Scope Rule

Build exactly what was agreed. Do not add adjacent features, refactor things that weren't broken, or architect for hypothetical future needs.

## Phase 2 — Completion Verification

Before calling the session complete:

1. Does every deliverable contain real content?
2. Can the user reach it without running steps you didn't mention?
3. Did you run every script and tool you wrote this session?

### Required completion format

```
WHAT WORKS NOW:
  - [feature/content] accessible at [location]

SCAFFOLDED (requires additional steps):
  - [feature] — needs [exact action]

NOT DONE:
  - [item] — reason: [honest explanation]
```

## Anti-patterns — Stop if any of these appear in your output

- "The framework is in place for..."
- "The infrastructure is ready to..."
- "Once populated, this will show..."
- "The tool exists but hasn't been run yet..."
- "This phase is complete pending..."

Each of these is structure without substance.
