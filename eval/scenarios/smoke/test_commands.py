"""Tier 1 smoke tests: command triggering for all 14 non-init commands.

Each test runs a command in a disposable repo and asserts that the
command produced tool calls — confirming the command was recognized
and acted upon. These are the cheapest validation layer.

In Claude Code's plugin system, slash commands are loaded as context
(not via a "Skill" tool call), so we verify behavior by checking
that the session produced tool calls characteristic of the command
running (Read, Write, Bash, etc.) rather than checking for a
specific skill trigger.

Budget: $1 per test, 20 turns max.
Skip automatically when ANTHROPIC_API_KEY is not set.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from scorers.trace import assert_tool_called, extract_tool_calls


pytestmark = pytest.mark.smoke


def _skip_if_no_key() -> pytest.MarkDecorator:
    return pytest.mark.skipif(
        not os.environ.get("ANTHROPIC_API_KEY"),
        reason="ANTHROPIC_API_KEY not set",
    )


async def _run_command_test(
    command: str,
    disposable_repo: Path,
    run_session: object,
    extra_prompt: str = "",
    expected_tools: list[str] | None = None,
) -> list:
    """Run a command and assert it produced tool calls.

    Args:
        command: Slash command to send (e.g. "/explore").
        disposable_repo: Path to temp git repo.
        run_session: Async session runner fixture.
        extra_prompt: Additional text appended to command.
        expected_tools: Tool names that should appear in trace.
            Defaults to ["Bash"] if not specified.

    Returns:
        The raw trace for further assertions.
    """
    prompt = command
    if extra_prompt:
        prompt = f"{command} {extra_prompt}"

    trace = await run_session(  # type: ignore[operator]
        repo_path=disposable_repo,
        prompts=["/init", prompt],
        max_budget_usd=1.0,
        max_turns=20,
    )

    # The command should produce tool calls — if it wasn't
    # recognized, the session would produce only text output.
    calls = extract_tool_calls(trace)
    assert calls, (
        f"Command '{command}' produced no tool calls. "
        "The command may not have been recognized."
    )

    # Check for expected tools if specified
    if expected_tools is None:
        expected_tools = ["Bash"]

    for tool in expected_tools:
        assert_tool_called(trace, tool)

    return trace


# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------


@_skip_if_no_key()
async def test_explore_runs(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """explore should read context and create effort structure."""
    await _run_command_test(
        "/explore",
        disposable_repo,
        run_session,
        extra_prompt="What should we build for rate limiting?",
        expected_tools=["Read", "Bash"],
    )


@_skip_if_no_key()
async def test_work_runs(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """work should read context and present options."""
    await _run_command_test(
        "/work",
        disposable_repo,
        run_session,
        extra_prompt="new",
        expected_tools=["Read"],
    )


@_skip_if_no_key()
async def test_requirements_runs(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """requirements should read context files."""
    await _run_command_test(
        "/requirements",
        disposable_repo,
        run_session,
        expected_tools=["Read"],
    )


@_skip_if_no_key()
async def test_design_runs(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """design should read context files."""
    await _run_command_test(
        "/design",
        disposable_repo,
        run_session,
        expected_tools=["Read"],
    )


@_skip_if_no_key()
async def test_implement_runs(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """implement should use Bash for worktree creation."""
    await _run_command_test(
        "/implement",
        disposable_repo,
        run_session,
        extra_prompt="Add a health check endpoint",
        expected_tools=["Bash"],
    )


@_skip_if_no_key()
async def test_investigate_runs(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """investigate should read code and produce findings."""
    await _run_command_test(
        "/investigate",
        disposable_repo,
        run_session,
        extra_prompt="Why does the app crash on startup?",
        expected_tools=["Read"],
    )


@_skip_if_no_key()
async def test_start_task_runs(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """start-task should read context to find tickets."""
    await _run_command_test(
        "/start-task",
        disposable_repo,
        run_session,
        expected_tools=["Read"],
    )


@_skip_if_no_key()
async def test_phase_complete_runs(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """phase-complete should read checklist to identify phase."""
    await _run_command_test(
        "/phase-complete",
        disposable_repo,
        run_session,
        expected_tools=["Read"],
    )


@_skip_if_no_key()
async def test_process_pr_discussions_runs(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """process-pr-discussions should attempt to read PR data."""
    await _run_command_test(
        "/process-pr-discussions",
        disposable_repo,
        run_session,
    )


@_skip_if_no_key()
async def test_reviewable_runs(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """reviewable should use Bash for git operations."""
    await _run_command_test(
        "/reviewable",
        disposable_repo,
        run_session,
        expected_tools=["Bash"],
    )


@_skip_if_no_key()
async def test_retro_note_runs(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """retro-note should write a note file."""
    await _run_command_test(
        "/retro-note",
        disposable_repo,
        run_session,
        extra_prompt="The template was missing a section for open questions.",
        expected_tools=["Write"],
    )


@_skip_if_no_key()
async def test_improve_runs(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """improve should read retro notes."""
    await _run_command_test(
        "/improve",
        disposable_repo,
        run_session,
        expected_tools=["Read"],
    )


@_skip_if_no_key()
async def test_audit_runs(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """audit should read context files for health checks."""
    await _run_command_test(
        "/audit",
        disposable_repo,
        run_session,
        expected_tools=["Read"],
    )


@_skip_if_no_key()
async def test_digest_runs(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """digest should read recent activity."""
    await _run_command_test(
        "/digest",
        disposable_repo,
        run_session,
        expected_tools=["Bash"],
    )
