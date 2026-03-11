"""Tier 1 smoke tests: /init onboarding.

Verifies that the init command creates the expected .forge-context/
directory structure and scaffolds the required context files.

These tests are marked `smoke` and use a $1 budget cap with 20 turns.
Skip automatically when ANTHROPIC_API_KEY is not set.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from scorers.trace import assert_file_exists, assert_tool_called


pytestmark = pytest.mark.smoke


@pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set",
)
async def test_forge_init_produces_output(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """Verify /init produces at least one file write.

    Within the $1/20-turn smoke budget, init should at minimum
    write CLAUDE.md or start scaffolding .forge-context/.
    This test validates that the command runs and produces
    observable file output.
    """
    trace = await run_session(  # type: ignore[operator]
        repo_path=disposable_repo,
        prompts=["/init"],
        max_budget_usd=1.0,
        max_turns=20,
    )

    # Init should produce at least one Write call
    from scorers.trace import extract_tool_calls

    calls = extract_tool_calls(trace)
    write_calls = [c for c in calls if c.name in ("Write", "Edit")]
    assert write_calls, (
        f"No Write or Edit calls found during /init. "
        f"Tools called: {[c.name for c in calls]}"
    )


@pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set",
)
async def test_forge_init_uses_bash_for_scaffold(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """Verify /init uses Bash to create directory structure.

    The init command creates .forge-context/ and subdirectories
    using Bash mkdir commands. This verifies the scaffolding
    step runs.
    """
    trace = await run_session(  # type: ignore[operator]
        repo_path=disposable_repo,
        prompts=["/init"],
        max_budget_usd=1.0,
        max_turns=20,
    )

    # Should use Bash for directory creation
    assert_tool_called(trace, "Bash")


@pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set",
)
async def test_forge_init_writes_claude_md(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """Verify /init writes or updates CLAUDE.md.

    The init command appends Forge command references to the
    project's CLAUDE.md file. This is the most reliable
    artifact produced within the $1/20-turn smoke budget.
    """
    trace = await run_session(  # type: ignore[operator]
        repo_path=disposable_repo,
        prompts=["/init"],
        max_budget_usd=1.0,
        max_turns=20,
    )

    # Should write CLAUDE.md with Forge command references
    assert_file_exists(trace, "CLAUDE.md")
