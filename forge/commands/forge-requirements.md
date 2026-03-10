# /forge-requirements

Run the requirements phase for a slice.

## This Command's Role

Identify the slice, detect if it is effort-sourced or
from-scratch, then delegate to the `Slice Requirements`
agent.

For the `approach` subcommand, delegate to the `Designer`
agent in approach mode for lightweight design exploration.

## Subcommands

### `approach` - Lightweight Design Exploration

Run lightweight design exploration to populate the
Approach section during requirements phase.

**Usage:** `/forge-requirements approach`

**When to use:**
- During requirements phase
- After capturing basic what/why/scope
- For non-trivial slices needing technical direction
- Before getting requirements reviewed

**Process:**
1. Identify current slice
2. Verify requirements basics exist (Summary, Success
   Criteria, Scope)
3. Spawn Designer agent with `mode: "approach"`
4. Agent explores architecture options and key decisions
5. Agent creates `design-approach.md` with direction

**Output:**
- `design-approach.md` created (~50-100 lines)
- Brief reference added to `requirements.md` Approach
  section
- High-level strategy, key decisions, components, risks

## Behavior

### Step 0: Check for Subcommand

**If subcommand is `approach`:**
Jump to "Step 3b: Approach Mode" below.

**Otherwise:** Continue with Step 1.

### Step 1: Identify Slice

Check current working directory or ask:
> "Which slice are you working on?"

Look for slice directories in
`.forge-context/slices/YYYYMM-*/` and let user select
or confirm.

**CRITICAL: When in a worktree, read all slice files
from the WORKTREE path:**
```
Correct: /path/to/_worktrees/{slug}/.forge-context/slices/{YYYYMM}-{slug}/requirements.md
Wrong:   /path/to/project/.forge-context/slices/{YYYYMM}-{slug}/requirements.md
```

### Step 2: Detect Source

Check if slice was spawned from an effort:

**Check for effort link:**
- Look in `{slice_path}/requirements.md` for existing
  `## Source` section with effort link
- Look in `.forge-context/efforts/` for references to
  this slice

**If effort-sourced:**
> "This slice came from effort: {effort_name}"
> "I'll consolidate requirements from the effort."

Set `effort_path` to the effort directory.

**If from-scratch:**
> "Starting requirements from scratch."
> "Do you have a ticket, discussion, or request link
> for reference?"

Set `effort_path` to `none`.

### Step 3: Spawn Agent

Spawn the `Slice Requirements` agent:

```
Use Task tool with:
- subagent_type: "Slice Requirements"
- prompt: |
    ## Inputs
    - slice_path: {slice_path}
    - slice_name: {slice_name}
    - effort_path: {path to effort or "none"}
    - origin: {ticket/discussion link, for from-scratch}
```

The agent will:
- **Effort-sourced**: Transform content from effort,
  ask ≤3 refinement questions, suggest area owner
  reviewers
- **From-scratch**: Ask 3 questions (what/why/success),
  draft requirements, optionally gather Approach section,
  suggest area owner reviewers

**About Approach section:**
The agent asks if user wants to include it with three
paths:
1. Skip — leave blank, proceed to review
2. Manual — user writes approach themselves
3. Collaborative — use `/forge-requirements approach`

### Step 3b: Approach Mode (for `approach` subcommand)

**Prerequisites check:**
1. Verify slice directory exists
2. Verify `requirements.md` exists with:
   - Summary section populated
   - Success Criteria section populated
   - Scope section populated

If prerequisites not met:
> "Requirements basics not yet captured. Please run
> `/forge-requirements` first, then run
> `/forge-requirements approach` for the Approach
> section."

**Spawn Designer agent in approach mode:**

```
Use Task tool with:
- subagent_type: "Designer"
- prompt: |
    ## Inputs
    - slice_path: {detected slice path}
    - slice_name: {slice name}
    - mode: "approach"
```

The Designer agent will:
- Ask questions about project choices and trade-offs
- Explore options based on user input
- Document chosen approaches from the conversation
- Create `design-approach.md` (~50-100 lines)
- Add brief reference in `requirements.md` Approach section

### Step 4: Report Completion

Display the agent's summary and next steps.

## Context Files to Read

- `.forge-context/slices/` — To identify current slice
- `.forge-context/efforts/` — To detect effort source

**Note:** When working in a worktree, `{slice_path}`
refers to the worktree location, not the main branch.

## Example Interactions

### Effort-Sourced
```
User: /forge-requirements

Agent: Working on `.forge-context/slices/202601-cuda-build/`.
       This slice came from effort: CUDA Ecosystem.

       I'll consolidate requirements from the effort...

       Here's what I pulled from the effort:
       - Summary: Enable CUDA builds in environments
       - Success criteria: 3 items from stories
       - Scope: From slice candidate SL-001

       Any changes since the effort review?

User: looks good

Agent: Requirements consolidated. Ready for: /forge-design
```

### From-Scratch
```
User: /forge-requirements

Agent: Working on `.forge-context/slices/202601-better-errors/`.
       Starting requirements from scratch.

       Do you have a ticket or discussion link for
       reference?

User: https://github.com/org/repo/issues/1234

Agent: Tell me about this slice:
       1. What are we building?
       2. What problem does it solve?
       3. How will we know it works?

User: Better error messages for package conflicts.
      Users get cryptic errors. Success = users
      understand what went wrong and how to fix it.

Agent: Requirements captured.
       Ready for: /forge-design
```
