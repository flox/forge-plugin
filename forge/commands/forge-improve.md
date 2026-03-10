# /forge-improve

Apply retrospective improvements to Forge workflows and
context.

## This Command's Role

Process pending retrospective notes and summaries, applying
improvements to templates, guidelines, and context documents.

This is separate from auditing because it's an interactive,
improvement-focused workflow rather than a health check.

## Bash Command Guidelines

When using bash commands, follow Skill: `bash-guidelines`:
- Use `test -d` or `[ -d ]` before `cd` or directory ops
- Use `test -f` or `[ -f ]` before file operations
- Avoid commands that error on normal condition checks

## Usage

```
/forge-improve [scope] [options]
```

### Scope

| Scope | Description |
|-------|-------------|
| (none) | Process all pending improvements |
| `notes` | Only process incremental correction notes |
| `summaries` | Only process full retrospective summaries |

### Options

| Option | Description |
|--------|-------------|
| `--auto` | Non-interactive mode: apply all recommendations |

## Behavior

### Step 1: Find Pending Improvements

Scan for unprocessed items:

1. **Incremental notes** in `retrospective-notes.md` files:
   - Look in `.forge-context/efforts/*/artifacts/`
   - Look in `.forge-context/slices/*/artifacts/`
   - Look in `.forge-context/artifacts/`
   - Items with `<!-- STATUS: UNPROCESSED -->` markers

2. **Full retrospective summaries** in
   `retrospective-summary.md` files:
   - Check against retrospective log for unapplied entries

If nothing found:
> "No pending improvements found."
>
> "All retrospective notes have been processed."
>
> "Run `/forge-retro-note` to capture new observations."

### Step 2: Spawn Applier Agent

```
Use Task tool with:
- subagent_type: "Retrospective Applier"
- prompt: |
    ## Inputs
    - scope: "all" | "notes" | "summaries"
    - notes_only: {boolean}
    - summaries_only: {boolean}
    - auto: {boolean from --auto}
    - notes_paths: {list of retrospective-notes.md files}
```

### Step 3: Interactive Processing

For each unprocessed item, the agent presents:

```
UNPROCESSED NOTE: {slice/effort name} / Note {N}
===========================================
**What happened:** {description}
**Recommendation:** {suggested improvement}

Target: {file to modify}

How should this be handled?
```

Options:
- **Apply** — Make the suggested change
- **Skip** — Mark as skipped (won't ask again)
- **Defer** — Leave for later (will ask next time)
- **Edit** — Modify the suggestion before applying

### Step 4: Report Results

```
RETROSPECTIVE IMPROVEMENTS APPLIED
==================================
Incremental Notes:
- Applied: {count}
- Skipped: {count}
- Deferred: {count}

Files Modified:
- .forge-context/context/principles.md
- .forge-context/templates/slice/design.md

Commits: {count}
```

## Examples

### Process All Pending
```
User: /forge-improve

Agent: Found 3 pending improvements...

UNPROCESSED NOTE: env-sboms / Note 1
=====================================
**What happened:** Suggested inline type definitions
**Recommendation:** Add types file pattern to context

Target: .forge-context/context/components.md

How should this be handled?
- Apply (Recommended)
- Skip
- Defer
- Edit

User: [Selects Apply]

Agent: Applied change to .forge-context/context/components.md
       Committed: fix(context): Add types file pattern

[Continues with remaining items...]

RETROSPECTIVE IMPROVEMENTS APPLIED
==================================
Notes: 2 applied, 1 skipped
Files Modified: 2
Commits: 2
```

### Nothing Pending
```
User: /forge-improve

Agent: No pending improvements found.

       All retrospective notes have been processed.
       Run `/forge-retro-note` after encountering issues
       to capture new observations.
```

## What Gets Improved

Retrospective improvements typically update:

| Target | Example Improvements |
|--------|---------------------|
| `.forge-context/context/` | Conventions discovered |
| `.forge-context/templates/` | Missing template sections |
| `.forge-context/context/principles.md` | Process refinements |

## Related Commands

| Command | Purpose |
|---------|---------|
| `/forge-retro-note` | Capture a retrospective note |
| `/forge-audit` | Run health checks |

## CI/Automation Mode

When running with `--auto`:
- Skip all interactive prompts
- Apply all recommended improvements automatically
- Each improvement is committed with a descriptive message

Example:
```bash
/forge-improve --auto
```
