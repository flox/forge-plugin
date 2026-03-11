"""Tier 1 smoke tests: command triggering for all 14 non-init commands.

Each test runs a command in a disposable repo and asserts that the
primary skill was triggered. These are the cheapest validation layer —
they confirm routing works without testing output quality.

Budget: $1 per test, 20 turns max.
Skip automatically when ANTHROPIC_API_KEY is not set.

Command → expected skill mapping:
1.  explore           → "explore"
2.  work              → "work"
3.  requirements      → "requirements"
4.  design            → "design"
5.  implement         → "implement"
6.  investigate       → "investigate" (or "issue-investigator")
7.  start-task        → "start-task"
8.  phase-complete    → "phase-complete"
9.  process-pr-discussions → "process-pr-discussions"
10. reviewable        → "reviewable" (or "commit-restructuring")
11. retro-note        → "retro-note" (or "correction-tracking")
12. improve           → "improve"
13. audit             → "audit"
14. digest            → "digest"
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from scorers.trace import assert_skill_triggered


pytestmark = pytest.mark.smoke


def _skip_if_no_key() -> pytest.MarkDecorator:
    return pytest.mark.skipif(
        not os.environ.get("ANTHROPIC_API_KEY"),
        reason="ANTHROPIC_API_KEY not set",
    )


async def _run_command_test(
    command: str,
    expected_skill: str,
    disposable_repo: Path,
    run_session: object,
    extra_prompt: str = "",
) -> None:
    """Helper to run a command and assert the skill was triggered."""
    prompt = command
    if extra_prompt:
        prompt = f"{command} {extra_prompt}"

    trace = await run_session(  # type: ignore[operator]
        repo_path=disposable_repo,
        prompts=["/init", prompt],
        max_budget_usd=1.0,
        max_turns=20,
    )

    assert_skill_triggered(trace, expected_skill)


# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------


@_skip_if_no_key()
async def test_forge_explore_triggers_skill(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """explore should trigger the explore skill."""
    await _run_command_test(
        "/explore",
        "explore",
        disposable_repo,
        run_session,
        extra_prompt="What should we build for rate limiting?",
    )


@_skip_if_no_key()
async def test_forge_work_triggers_skill(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """work should trigger the work skill."""
    await _run_command_test(
        "/work",
        "work",
        disposable_repo,
        run_session,
        extra_prompt="new",
    )


@_skip_if_no_key()
async def test_forge_requirements_triggers_skill(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """requirements should trigger the requirements skill."""
    await _run_command_test(
        "/requirements",
        "requirements",
        disposable_repo,
        run_session,
    )


@_skip_if_no_key()
async def test_forge_design_triggers_skill(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """design should trigger the design skill."""
    await _run_command_test(
        "/design",
        "design",
        disposable_repo,
        run_session,
    )


@_skip_if_no_key()
async def test_forge_implement_triggers_skill(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """implement should trigger the implement skill."""
    await _run_command_test(
        "/implement",
        "implement",
        disposable_repo,
        run_session,
        extra_prompt="Add a health check endpoint",
    )


@_skip_if_no_key()
async def test_forge_investigate_triggers_skill(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """investigate should trigger the investigate skill."""
    await _run_command_test(
        "/investigate",
        "investigate",
        disposable_repo,
        run_session,
        extra_prompt="Why does the app crash on startup?",
    )


@_skip_if_no_key()
async def test_forge_start_task_triggers_skill(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """start-task should trigger the start-task skill."""
    await _run_command_test(
        "/start-task",
        "start-task",
        disposable_repo,
        run_session,
    )


@_skip_if_no_key()
async def test_forge_phase_complete_triggers_skill(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """phase-complete should trigger the phase-complete skill."""
    await _run_command_test(
        "/phase-complete",
        "phase-complete",
        disposable_repo,
        run_session,
    )


@_skip_if_no_key()
async def test_forge_process_pr_discussions_triggers_skill(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """process-pr-discussions should trigger matching skill."""
    await _run_command_test(
        "/process-pr-discussions",
        "process-pr-discussions",
        disposable_repo,
        run_session,
    )


@_skip_if_no_key()
async def test_forge_reviewable_triggers_skill(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """reviewable should trigger commit-restructuring skill."""
    await _run_command_test(
        "/reviewable",
        "commit-restructuring",
        disposable_repo,
        run_session,
    )


@_skip_if_no_key()
async def test_forge_retro_note_triggers_skill(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """retro-note should trigger correction-tracking skill."""
    await _run_command_test(
        "/retro-note",
        "correction-tracking",
        disposable_repo,
        run_session,
        extra_prompt="The template was missing a section for open questions.",
    )


@_skip_if_no_key()
async def test_forge_improve_triggers_skill(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """improve should trigger the improve skill."""
    await _run_command_test(
        "/improve",
        "improve",
        disposable_repo,
        run_session,
    )


@_skip_if_no_key()
async def test_forge_audit_triggers_skill(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """audit should trigger the audit skill."""
    await _run_command_test(
        "/audit",
        "audit",
        disposable_repo,
        run_session,
    )


@_skip_if_no_key()
async def test_forge_digest_triggers_skill(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """digest should trigger the digest skill."""
    await _run_command_test(
        "/digest",
        "digest",
        disposable_repo,
        run_session,
    )
