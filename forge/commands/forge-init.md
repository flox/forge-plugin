# /forge-init

Set up Forge planning in a project by scaffolding
`.forge-context/` and capturing project context.

## This Command's Role

This is the entry point for new Forge users. It creates the
`.forge-context/` directory structure, captures project context
(auto-detected or manual), and appends a `CLAUDE.md` section
with command references.

The first impression matters. Default to auto-detection to show
the user that Forge already understands their project.

## Behavior

### Step 1: Check Existing Scaffold

Check if `.forge-context/` already exists:

```bash
test -d ".forge-context"
```

If it exists:
> "Forge planning is already set up in this project."
> ".forge-context/ found with existing configuration."
>
> "What would you like to do?"
> 1. Re-run context detection (update context files)
> 2. Re-run specific section (choose which)
> 3. Exit — setup is already complete

If the user chooses option 2, present the section list and
jump to the appropriate step. If exit, stop.

If `.forge-context/` does not exist, proceed to Step 2.

### Step 2: Choose Onboarding Mode

> "I'll set up Forge planning for this project. I can
> analyze your codebase and suggest context automatically,
> or you can provide it manually."
>
> 1. Auto-detect (Recommended) — I'll scan the project
>    and confirm findings with you
> 2. Manual — answer a few questions
> 3. Selective — choose which areas to auto-detect

Default to option 1. The first wow moment is showing the
user we already understand their project.

### Step 3: Create Directory Structure

Create the following structure:

```
.forge-context/
  context/
  efforts/
  slices/
  artifacts/
  overrides/
    terminology.md
  templates/
    effort/
      effort.md
      decisions.md
      slices.md
      checklist.md
    slice/
      requirements.md
      design.md
      tasks.md
      checklist.md
      decisions.md
    starter-principles.md
```

### Step 4: Copy Templates

Copy templates from the plugin templates directory using
`${CLAUDE_PLUGIN_ROOT}/templates/` as the source path.

Create the directories:
```bash
mkdir -p .forge-context/context
mkdir -p .forge-context/efforts
mkdir -p .forge-context/slices
mkdir -p .forge-context/artifacts
mkdir -p .forge-context/overrides
mkdir -p .forge-context/templates/effort
mkdir -p .forge-context/templates/slice
```

Copy each template file from
`${CLAUDE_PLUGIN_ROOT}/templates/` to the corresponding
location under `.forge-context/templates/`.

Create `.forge-context/overrides/terminology.md` from the
plugin's overrides template if it exists, or create a
minimal file:

```markdown
# Terminology Overrides

Map Forge terms to your team's preferred vocabulary.
When the user uses a team term, understand it as the
Forge term. When producing output, use the team term.

| Forge Term | Your Term |
|------------|-----------|
| effort | (e.g., epic, initiative, theme) |
| slice | (e.g., project, feature, sprint) |
| task | (e.g., ticket, issue, card) |
| area owner | (e.g., domain owner, tech lead) |

Remove rows where you prefer the Forge term.
```

### Step 5: Context Detection (Auto-detect Mode)

Scan the project and draft context files, then present
findings for confirmation.

**Detection sources:**

| Context File | Detection Strategy |
|-------------|-------------------|
| `context/product.md` | README, package.json description, pyproject.toml, Cargo.toml, top-level comments |
| `context/components.md` | Directory structure, module boundaries, package/workspace layout |
| `context/team.md` | git shortlog (recent contributors), CODEOWNERS, commit patterns by directory |
| `context/principles.md` | CONTRIBUTING.md, linter configs (.eslintrc, rustfmt.toml), CLAUDE.md conventions |
| `context/git-workflow.md` | Branch naming patterns (git branch -r), merge commit presence, CI config |

**Run detection:**

```bash
# Product/description
ls README.md package.json pyproject.toml Cargo.toml 2>/dev/null

# Directory structure for components
ls -1

# Recent contributors
git shortlog -sn --since="90 days ago" | head -10

# Branch patterns
git branch -r | head -20

# Check for contribution guidelines
ls CONTRIBUTING.md .eslintrc* .rustfmt.toml 2>/dev/null
```

**Presentation pattern:**

> "I've analyzed the project. Here's what I found:"
>
> **Product:** "A CLI tool for managing reproducible
> development environments, built in Rust."
>
> **Components:**
> - `cli/` — Command-line interface and argument parsing
> - `core/` — Core application logic
> - `tests/` — Test suite
>
> **Team:** 3 active contributors in the last 90 days
> (alice — cli, bob — core, carol — tests)
>
> **Git workflow:** Feature branches, squash merges to main
>
> **Principles:** Starter template (customize after init)
>
> "Does this look right? You can edit any section, skip
> sections, or I can re-detect specific areas."
>
> 1. Accept all — write context files
> 2. Edit a section
> 3. Re-detect a section
> 4. Skip a section (leave empty for later)

Write confirmed context to `.forge-context/context/`.

**Selective mode:** User picks which areas to auto-detect
vs provide manually:

> "Which areas should I auto-detect?"
> - [ ] Product description
> - [ ] Components/modules
> - [ ] Team/contributors
> - [ ] Git workflow
> - [ ] Engineering principles (starter template)

For unchecked areas, fall through to manual questions.

### Step 6: Context Capture (Manual Mode)

Use interactive questions when user chooses manual mode
or when auto-detection cannot determine a section with
reasonable confidence.

| # | Question | Target File |
|---|----------|------------|
| 1 | "What does this project do?" | `context/product.md` |
| 2 | "Main components or modules?" | `context/components.md` |
| 3 | "Who works on this? (names, areas)" | `context/team.md` |
| 4 | "Engineering principles?" | `context/principles.md` |
| 5 | "Git workflow? (trunk, gitflow, etc.)" | `context/git-workflow.md` |

Keep questions brief. Accept free-form answers and format
them into the appropriate file.

### Step 7: Starter Engineering Principles

When auto-detect finds no existing principles (no
CONTRIBUTING.md, no style guides), or when user selects
manual mode, populate `context/principles.md` with a
curated starter template:

```markdown
# Engineering Principles

> Starter principles — edit, remove, or add your own.
> Run `/forge-retro-note` to capture refinements as
> you work.

## KISS: Keep it simple

Prefer the simplest solution that works. Refactor
toward simplicity. Small, focused components over
large, complex ones.

## Do one thing and do it well

Components with limited scope are easier to design,
test, and maintain. Modular designs lead to cleaner
systems.

## Less is more

Do the least you can to get the job done. You can
always do more later. Avoid unnecessary work that
may be thrown away.

## Consistency is key

Reuse well-established idioms. Reduce the learning
curve for others. When approaches differ, converge
on one.

## Good enough is not good enough

Small inefficiencies multiply. Don't poll when you
can subscribe. Cache efficiently. Minimize
duplication. Take pride in optimal solutions.

## Inform intrinsically

Users learn best in context. Surface knowledge when
users are primed with what they are trying to do,
not in docs they won't read.
```

When CONTRIBUTING.md or linter configs exist, the
auto-detected principles supplement the starter template
with project-specific conventions found in those files.

### Step 8: Append CLAUDE.md Section

Check if `CLAUDE.md` exists:

```bash
test -f "CLAUDE.md"
```

If it exists, append to it. If not, create it.

Append the following section:

```markdown
## Forge Planning Context

This project uses Forge for structured planning.
Planning artifacts live in `.forge-context/`.

- `/forge-explore` - Discover and frame problems
- `/forge-work` - Build and deliver solutions
- `/forge-retro-note` - Capture process observations
- `/forge-improve` - Apply notes as improvements
- `/forge-audit` - Verify context accuracy
- `/forge-digest` - Summarize recent planning activity
- `/forge-reviewable` - Restructure commits for review

Context files in `.forge-context/context/` describe
the project, team, and guidelines. Keep these updated
as the project evolves, or run `/forge-audit` to
check for drift.

If `.forge-context/overrides/terminology.md` exists
and has non-empty mappings, use the team's preferred
terms in all output. When the user says their term,
understand it as the Forge term. When producing
output, use their term instead.
```

### Step 9: Suggest First Retro Note for Terminology

> "Forge uses terms like 'effort', 'slice', and 'task'
> for its planning concepts. Your team may use different
> names.
>
> If your team uses different terms (e.g., 'epic' instead
> of 'effort', 'ticket' instead of 'task'), you can
> capture these now with `/forge-retro-note` and they'll
> appear in `.forge-context/overrides/terminology.md`.
>
> Would you like to set up terminology overrides now?"
> 1. Yes — run `/forge-retro-note` to capture terms
> 2. No — I'll use the default Forge terms

If yes, jump to `/forge-retro-note`.

### Step 10: Offer First Action

> "Forge is ready! What would you like to do?"
>
> 1. Explore a problem space (`/forge-explore`)
> 2. Start building something (`/forge-work new`)
> 3. Investigate an issue (`/forge-investigate`)
> 4. Just commit the scaffold — I'll come back later

Route to the chosen command, or proceed to commit.

### Step 11: Commit Scaffold

Commit the scaffold to git:

```bash
git add .forge-context/ CLAUDE.md
git commit -m "chore: Initialize Forge planning scaffold

Sets up .forge-context/ with project context and
planning structure.

Co-Authored-By: Claude <noreply@anthropic.com>"
```

Report results:

> "Forge planning is set up."
>
> Created:
> - `.forge-context/context/` — 5 context files
> - `.forge-context/templates/` — effort and slice templates
> - `.forge-context/overrides/terminology.md`
> - Updated `CLAUDE.md` with Forge command reference
>
> Changes committed. You're ready to start planning.

## Subcommands

None — this command enters interactive mode directly.
