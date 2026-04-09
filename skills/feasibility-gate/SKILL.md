---
description: >
  Pre-execution feasibility check before significant implementation work. FIRES before
  building anything non-trivial: training models, collecting large datasets, writing
  multi-file systems, architectural rewrites, or any task requiring >10 minutes of
  compute or >100 lines of new code. Triggers: 'train', 'model', 'dataset', 'collect
  data', 'build', 'implement', 'create system', 'surrogate', 'pipeline', 'architecture',
  'rewrite', 'migrate', 'deploy', 'scale', 'automate', 'GPU', 'ensemble', 'fine-tune',
  'scrape', 'crawl', 'generate', 'synthesize'.
---

# Feasibility Gate

## The Problem This Solves

LLMs have a bias toward execution. When the user proposes an approach, the model's default is to start building immediately because execution feels productive and refusal feels like failure.

This creates a recurring failure mode:

1. User proposes approach X
2. Model can predict X will likely fail (or could predict it with 30 seconds of reasoning)
3. Model starts building X anyway because stopping feels like disappointing the user
4. X fails after hours of work
5. Model correctly diagnoses why it failed — using reasoning it could have applied before step 2

## The Gate

Before starting any significant implementation work, answer these three questions explicitly.

### 1. What would have to be true for this to work?

List concrete, falsifiable preconditions. Not "it should work if the model is good enough" — specific conditions.

Examples:
- "The training data must contain examples of the target class"
- "The API must support batch requests under 100ms"
- "The success region must be large enough to sample randomly"

### 2. Are those things actually true?

Check each precondition against what you already know. Use math, not vibes. If you don't have enough information, say so — that's a flag, not a blocker.

Examples:
- "500k random samples, zero positive examples. The success region is too small for random sampling." -> FAIL
- "The API docs say batch limit is 10, we need 1000." -> FAIL
- "I don't know the distribution of positive examples in this space." -> FLAG

### 3. What's the cheapest way to verify before committing?

If preconditions are uncertain (FLAG, not FAIL), propose a minimal test — not the full implementation.

Examples:
- "Run 1000 samples and check if ANY are positive before collecting 500k"
- "Hit the API with one batch request before building the pipeline"
- "Train on 1k samples for 2 epochs and check if loss decreases before scaling"

## Decision Rules

- All preconditions TRUE -> Proceed. State them for the record.
- Any precondition FAIL -> Stop. Explain why. Propose alternatives.
- Any precondition FLAG -> Run the minimal test first. Do not scale until verified.

## What Triggers This Gate

**Fires for:**
- Training any model
- Collecting datasets (>1000 samples)
- Writing >100 lines of new code for a new system
- Any task requiring >10 minutes of compute
- Architectural changes affecting multiple files
- Anything the user will wait on and expect results from

**Does NOT fire for:**
- Quick edits to existing code
- Reading files, searching, exploring
- Answering questions
- Small scripts (<50 lines)
- Changes the user can verify in seconds

## Presentation

Keep it light:

> "Before I build this, let me check if the approach is sound.
> - [precondition 1]: [true/false/unknown]
> - [precondition 2]: [true/false/unknown]
> - [conclusion]: [proceed / stop because X / need to verify Y first]"

If the user says "just do it" after seeing a FAIL, push back once with the specific reason. If they insist, proceed but note the risk explicitly.
