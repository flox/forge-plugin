# Forge Plugin Eval Harness

Automated self-evaluation for the Forge Claude Code plugin.
Tests that commands trigger the right skills, phase outputs
meet quality thresholds, and the full lifecycle works end-to-end.

## Architecture

Three-tier evaluation pyramid:

```
         E2E (Tier 3)
        ┌─────────────┐  $15/run, 150 turns
        │  Full        │  Full lifecycle: init → explore
        │  Lifecycle   │  → requirements → design
        └─────────────┘

       Integration (Tier 2)
      ┌─────────────────────┐  $5/test, 50 turns
      │  Phase Output        │  Score requirements.md,
      │  Quality             │  design.md, effort.md >= 80%
      └─────────────────────┘

         Smoke (Tier 1)
    ┌─────────────────────────┐  $1/test, 20 turns
    │  Command Triggering      │  Verify skills/agents fire
    └─────────────────────────┘
```

## Setup

The eval harness uses a [Flox](https://flox.dev) environment
that provides Python 3.11, pytest, ruff, mypy, uv, and git.
All Python dependencies are installed automatically on first
activate.

```bash
cd eval/
flox activate
export ANTHROPIC_API_KEY=sk-ant-...
```

On first activation, Flox creates a virtual environment and
installs all Python dependencies via `uv`. Subsequent
activations reuse the cached venv (reinstalls only if
`pyproject.toml` changes).

**SDK Compatibility Note:** The `claude-agent-sdk` API is still
evolving. This harness was written against the documented
`query()` / `ClaudeAgentOptions` / `PreToolUse` / `PostToolUse`
interface. Verify your installed SDK version matches before
running. Check `scorers/trace.py` for the event format this
harness expects.

## Running Tests

All tier-marked tests are automatically skipped when
`ANTHROPIC_API_KEY` is absent.

### Tier 1: Smoke Tests (fast, ~$1 each)

```bash
pytest scenarios/smoke/ -m smoke -v
```

Checks that each command triggers its expected skill. Use this
as a quick sanity check after making changes to commands or
skills.

### Tier 2: Integration Tests (moderate, ~$5 each)

```bash
pytest scenarios/integration/ -m integration -v
```

Runs phase workflows and scores output quality. Use this to
verify that requirements, design, and explore phases produce
acceptable documents.

### Tier 3: E2E Tests (expensive, ~$15 each)

```bash
pytest scenarios/e2e/ -m e2e -v
```

Full lifecycle test. Runs init → explore → work → requirements
→ design in sequence and checks all artifacts. Run before
cutting a release or after large changes.

### Run All Tiers

```bash
pytest -v
```

### Run Specific Test

```bash
pytest scenarios/smoke/test_init.py::test_forge_init_creates_context_directory -v
```

## Cost Expectations

| Tier | Tests | Budget per test | Estimated total |
|------|-------|-----------------|-----------------|
| Smoke | 17 | $1 | $17 |
| Integration | 9 | $5 | $45 |
| E2E | 3 | $15 | $45 |
| **Total** | | | **~$107** |

Run smoke tier frequently. Run integration and E2E before releases.

## Directory Structure

```
eval/
  pyproject.toml          # Python project config
  README.md               # This file
  conftest.py             # Shared pytest fixtures
  scenarios/
    smoke/
      test_commands.py    # Command → skill triggering
      test_init.py        # /forge-init onboarding
    integration/
      test_requirements.py  # requirements phase quality
      test_design.py        # design phase quality
      test_explore.py       # explore/effort quality
    e2e/
      test_full_lifecycle.py  # Full workflow
  fixtures/
    sample_project/       # Minimal FastAPI project
    prompt_scripts/       # Scripted user responses (JSON)
  scorers/
    __init__.py
    document.py           # Rubric-based scoring
    trace.py              # Tool call trace analysis
  baselines/
    scores.json           # Stored quality baselines
```

## Scorers

### Document Scorer (`scorers/document.py`)

Scores markdown artifacts against rubrics:

- `score_requirements(content)` — 100pt rubric covering summary,
  user stories, acceptance criteria, scope, success criteria,
  non-goals
- `score_design(content)` — 100pt rubric covering architecture,
  components, API changes, testing strategy, task breakdown
- `score_effort(content)` — 100pt rubric covering problem statement,
  landscape analysis, open questions, success signals, slice candidates

All return a `Score` object with per-criterion breakdown and a
`percentage` property.

### Trace Analyzer (`scorers/trace.py`)

Inspects claude-agent-sdk session traces:

- `assert_tool_called(trace, tool_name, args=None)` — Assert a tool
  was invoked
- `assert_agent_spawned(trace, agent_type)` — Assert a Task call
  with the given `subagent_type`
- `assert_file_exists(trace, path_pattern)` — Assert a Write/Edit
  call matched a file path
- `assert_skill_triggered(trace, skill_name)` — Assert a Skill call
  was made
- `extract_tool_calls(trace)` — Get all tool calls as `ToolCall` objects

## Updating Baselines

After running a full eval suite, update the baselines:

1. Run integration and E2E tests and collect scores
2. Edit `baselines/scores.json` with mean, stddev, n, and date
3. Commit the updated baselines with the eval run date

Baselines track drift over time. A significant drop in mean score
between releases signals a regression in output quality.

## Adding New Test Scenarios

1. Choose the right tier for your scenario (smoke for routing,
   integration for quality, e2e for lifecycle)
2. Copy a similar test file as a starting point
3. Use the `disposable_repo` and `run_session` fixtures
4. Set the appropriate pytest marker (`@pytest.mark.smoke`, etc.)
5. Set `max_budget_usd` and `max_turns` per tier guidelines
6. Add `@pytest.mark.skipif(not os.environ.get("ANTHROPIC_API_KEY"), ...)`

## Fixture: Sample Project

`fixtures/sample_project/` contains a minimal FastAPI app that
serves as the test project for eval runs. The `disposable_repo`
fixture copies these files into a temp directory with git initialized.

To test with a different project structure, either modify the
sample project files or override the fixture in a local `conftest.py`.

## Scripted Prompts

`fixtures/prompt_scripts/` contains JSON files with scripted
answers for interactive Forge prompts. These document the expected
responses for each scenario and serve as reference for constructing
prompt sequences in tests.

The current eval harness sends full prompts in a single session.
For fully scripted interactive sessions, the SDK's turn-by-turn
API can be used with these response files.
