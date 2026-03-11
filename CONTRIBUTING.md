# Contributing to Forge Plugin

Thank you for your interest in contributing to the
Forge Plugin. This document explains the structure
of the repository and how to make changes.

---

## Repository Structure

```
forge-plugin/
  README.md               # project overview
  CONTRIBUTING.md         # this file
  LICENSE                 # Apache 2.0
  docs/
    getting-started.md    # installation walkthrough
    workflow-overview.md  # effort/slice lifecycle
    command-reference.md  # all commands
  forge/                  # the plugin directory
    .claude-plugin/
      plugin.json         # plugin manifest
    commands/             # slash commands
    agents/               # subagent definitions
    skills/               # skill modules
    templates/            # scaffold templates
```

The `forge/` directory is the plugin itself. When
a user installs the plugin, Claude Code reads
everything inside `forge/`.

---

## Plugin Components

### Commands (`forge/commands/`)

Each file is a slash command definition in markdown.
The filename (without `.md`) becomes the command
name. For example, `init.md` defines `/init`.

Commands are the entry points users interact with.
They describe behavior and delegate complex work
to agents.

### Agents (`forge/agents/`)

Agents are subagent definitions that commands
spawn with the Task tool. Each agent file defines
a named agent type with its own workflow phases.

Agents follow specific disciplines:
- Implementation workers follow TDD
- Code reviewers follow a two-stage review process
- Phase completers follow the review artifact model

### Skills (`forge/skills/`)

Skills are reusable knowledge modules loaded by
commands and agents. Each skill lives in its own
directory with a `SKILL.md` file.

Skills are referenced in commands/agents with:
```
See Skill: `skill-name` for details.
```

### Templates (`forge/templates/`)

Templates are markdown files copied to the user's
project by `/init`. They live in:

```
forge/templates/
  overrides/
    terminology.md    # term mapping table
  starter-principles.md
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
```

---

## Making Changes

### Adding a New Command

1. Create `forge/commands/{name}.md`
2. Follow the pattern of existing commands
3. If the command needs complex behavior, create
   a matching agent in `forge/agents/`
4. Add the command to `docs/command-reference.md`
5. Update the command table in `README.md`

### Adding a New Agent

1. Create `forge/agents/{name}.md`
2. Define the agent's phases and behavior
3. Reference any skills the agent uses
4. Update the command that spawns the agent

### Adding a New Skill

1. Create `forge/skills/{name}/SKILL.md`
2. Write the skill as a self-contained reference
3. Reference the skill from agents/commands that
   use it: `See Skill: \`{name}\``

### Updating Templates

Templates in `forge/templates/` are copied to
users' projects during `/init`. Changes
here affect new projects only — existing projects
keep their copies.

---

## Testing Changes Locally

Since Forge Plugin is a Claude Code plugin, you
test changes by using them in Claude Code.

### Install from Local Directory

```bash
claude plugin install --path /path/to/forge-plugin/forge
```

Or, to test the full marketplace flow:

```bash
claude plugin add-marketplace /path/to/forge-plugin
claude plugin install forge
```

### Test in a Sample Project

Create a test project directory:

```bash
mkdir /tmp/test-project
cd /tmp/test-project
git init
echo "# Test Project" > README.md
```

Open Claude Code in that directory and run:

```
/init
```

Then test the specific commands you've changed.

### Reload After Changes

When you modify plugin files, reload the plugin:

```bash
claude plugin reload forge
```

---

## Code Style

All markdown files follow these conventions:

- Line length: 80 characters or fewer
- Semantic line breaks (break at sentence/clause
  boundaries, not at character count)
- Active voice, concise prose
- No Flox-specific references in user-facing content
- Replace "TAO" with "area owner" or "reviewer"
- Replace `.context/` with `.forge-context/`

---

## PR Process

1. Fork the repository
2. Create a feature branch from `main`
3. Make your changes
4. Test locally in a sample project
5. Open a pull request with:
   - What changed and why
   - How you tested it
   - Any limitations or follow-up work

---

## Questions

Open an issue in the repository for questions,
bug reports, or feature requests.
