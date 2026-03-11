# /retro-note

Capture a retrospective note about Forge workflows, tools,
or processes.

## This Command's Role

Quick way to capture correction moments and feedback during
development work. Automatically routes notes based on
**where you are working**, not on the content of the note:

- Active slice worktree → that slice's
  `artifacts/retrospective-notes.md`
- Active effort worktree → that effort's
  `artifacts/retrospective-notes.md`
- No active work context → `.forge-context/artifacts/
  retrospective-notes.md`

## Usage

```
/retro-note
```

No arguments — the command will interactively capture
the note.

## Bash Command Guidelines

When using bash commands:
- Use `test -d` or `[ -d ]` before `cd` or directory ops
- Use `test -f` or `[ -f ]` before file operations
- Check branch/worktree existence before operations
- Avoid commands that error on normal condition checks

## When to Use

Capture a note when you encounter:
- **Template gaps**: Agent didn't have the right starting
  structure
- **Context gaps**: Agent didn't have information it
  needed
- **Assumption errors**: Agent assumed something wrong
- **Process gaps**: A step was missing from the workflow
- **Workflow friction**: Something that slowed you down
- **General observations**: Ideas for improvement

## Behavior

### Step 1: Detect Context

Detect location using these checks:

```bash
# Current directory
pwd

# Current branch
git branch --show-current

# List worktrees
git worktree list
```

**Priority order:**

1. **Active slice worktree**: If the current directory
   is within a worktree AND a slice directory exists
   under `.forge-context/slices/YYYYMM-*/`:
   - Target: `{slice_path}/artifacts/retrospective-notes.md`
   - Add note directly — no branch switching needed

2. **Active effort worktree**: If current directory is
   within a worktree AND on an `effort/*` branch:
   - Find the effort dir: `ls {worktree}/.forge-context/efforts/YYYYMM-*/`
   - Target: `{effort_path}/artifacts/retrospective-notes.md`
   - Add note directly — no branch switching needed

3. **Slice directory (not in worktree)**: If cwd matches
   `.forge-context/slices/YYYYMM-*/`:
   - Target: `{slice_path}/artifacts/retrospective-notes.md`

4. **Effort directory**: If cwd matches
   `.forge-context/efforts/YYYYMM-*/`:
   - Target: `{effort_path}/artifacts/retrospective-notes.md`

5. **No context** (on main or elsewhere):
   - Target: `.forge-context/artifacts/retrospective-notes.md`
   - Create the file if it doesn't exist

### Step 2: Gather Information

**1. What happened (REQUIRED):**
- Prompt: "What happened? (describe the issue, error,
  or observation):"
- Capture full details including error messages, commands,
  agent behavior, etc.
- Support multi-line input

**2. Recommendation (optional):**
- Prompt: "What change might improve this?
  (press Enter to skip):"

**3. Additional context (optional):**
- Prompt: "Any additional context? Phase, agent name,
  root cause, etc. (press Enter to skip):"

**Auto-generate title:**
- Extract first 5-10 words from "What happened"
- Lowercase and clean up

### Step 3: Determine Note Number

**REQUIRED GATE: Read the target file before any
modification.** This finds the next note number AND
verifies existing content is present before appending.

Read target `retrospective-notes.md`:
- Parse existing `### Note N:` entries
- Use highest N + 1 for new note
- If file doesn't exist or no notes, start at 1

### Step 4: Format and Append Note

**CRITICAL: Always use the Edit tool to append the note.
Never use the Write tool for existing files — it will
overwrite all existing notes.**

Standard note format:
```markdown
## {YYYY-MM-DD}: General

### Note {N}: {Auto-generated title from "What happened"}
<!-- STATUS: UNPROCESSED -->

**What happened:**
{Full description}

**Recommendation:**
{Recommendation if provided, or "See description"}

**Additional context:**
{Additional context if provided}

---

```

**Field rules:**
- "What happened" is always present (required)
- Title is auto-generated from first 5-10 words
- Recommendation defaults to "See description" if omitted
- Additional context section only included if provided

**Appending with the Edit tool:**
Find the last `---` separator in the file, then append
the new note after it:
```
old_string: "---\n"  (the final separator)
new_string: "---\n\n## {date}: General\n\n### Note {N}:..."
```

If file doesn't exist, create it with a header then add
the note content.

### Step 5: Commit (if in worktree)

If in a worktree, commit the change:

```bash
git add {target_file_path}
git commit -m "docs: Add retrospective note - {brief_title}

Captured correction moment for future workflow improvements.

Co-Authored-By: Claude <noreply@anthropic.com>"
```

For slice/effort directories on main, no separate commit
is needed — the note is added to existing uncommitted work.

### Step 6: Confirm

Show confirmation:
> "Retrospective note added to {context_name}."
>
> "Note #{N}: {title}"
>
> "This note will be processed via `/improve`
> for workflow improvements."
>
> "Location: {file_path}"

If note was committed, offer to push and PR if needed.

## Examples

### Error/Issue Note

```
User: /retro-note

Agent: No active slice/effort context detected.
       Adding note to .forge-context/artifacts/.

       What happened?

User: The designer agent didn't detect our custom
      test runner — it assumed pytest but we use
      cargo nextest.

Agent: What change might improve this?

User: Add a test runner detection step to the
      designer agent.

Agent: Any additional context?

User: This was during implementation phase.

Agent: Retrospective note added.

       Note #1: The designer agent didn t detect
                custom test runner

       Location: .forge-context/artifacts/retrospective-notes.md
```

### Simple Observation

```
User: /retro-note

Agent: Detected active slice: Environment SBOMs

       What happened?

User: Had to look through multiple files to find
      which command to use

Agent: What change might improve this?

User: Add quick command reference to CLAUDE.md

Agent: Any additional context?

User: [presses enter]

Agent: Retrospective note added to Environment SBOMs.
       Note #2: Had to look through multiple files
```

## Related Commands

| Command | Purpose |
|---------|---------|
| `/improve` | Process and apply retrospective notes |
| `/audit` | Check for unprocessed notes |
