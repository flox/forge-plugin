# /requirements

Run the requirements phase for a slice.

## This Command's Role

Identify the slice, detect if it is effort-sourced or
from-scratch, then gather requirements through guided
conversation.

For the `approach` subcommand, delegate to the `Designer`
agent in approach mode for lightweight design exploration.

## Subcommands

### `approach` - Lightweight Design Exploration

Run lightweight design exploration to populate the
Approach section during requirements phase.

**Usage:** `/requirements approach`

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

## Terminology Awareness

Before producing any user-facing output, read
`.forge-context/overrides/terminology.md`. If the user
has mapped Forge terms to their own vocabulary, use
their terms in all output — menus, status messages,
suggestions, and agent prompts. Pass the mapped terms
to any spawned agents so they also use the user's
language.

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

### Step 3: Gather Requirements

Gather requirements through guided conversation and write
them to `{slice_path}/requirements.md`.

**For effort-sourced slices:**

Read the linked effort's accepted slice candidate to
extract existing content. Ask ≤3 refinement questions:
- Any scope changes since effort review?
- Any additional success criteria?
- Any constraints that emerged?

Draft requirements from the effort content plus
refinements.

**For from-scratch slices:**

Ask the user 3 focused questions:

1. "What are we building? (1-3 sentences)"
2. "What problem does this solve or what value
   does it deliver?"
3. "How will we know it works? (measurable outcomes)"

Draft requirements from the answers.

**After drafting (both modes):**

Present requirements draft to user:
> "Here are the requirements I've captured:
> {requirements summary}
>
> Would you like to:
> 1. Accept as-is
> 2. Edit a section
> 3. Add more detail"

Write final requirements to `requirements.md`.

**About Approach section:**

After requirements are accepted, ask:
> "Would you like to include an approach section?"
> 1. Skip — leave blank, proceed to review
> 2. Manual — you'll write the approach yourself
> 3. Collaborative — use `/requirements approach`

### Step 3b: Approach Mode (for `approach` subcommand)

**Prerequisites check:**
1. Verify slice directory exists
2. Verify `requirements.md` exists with:
   - Summary section populated
   - Success Criteria section populated
   - Scope section populated

If prerequisites not met:
> "Requirements basics not yet captured. Please run
> `/requirements` first, then run
> `/requirements approach` for the Approach
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
User: /requirements

Agent: Working on `.forge-context/slices/202601-cuda-build/`.
       This slice came from effort: CUDA Ecosystem.

       I'll consolidate requirements from the effort...

       Here's what I pulled from the effort:
       - Summary: Enable CUDA builds in environments
       - Success criteria: 3 items from stories
       - Scope: From slice candidate SL-001

       Any changes since the effort review?

User: looks good

Agent: Requirements consolidated. Ready for: /design
```

### From-Scratch
```
User: /requirements

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
       Ready for: /design
```
