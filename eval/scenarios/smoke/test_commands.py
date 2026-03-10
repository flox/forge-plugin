"""Tier 1 smoke tests: command triggering for all 14 non-init commands.

Each test runs a command in a disposable repo and asserts that the
primary skill was triggered. These are the cheapest validation layer —
they confirm routing works without testing output quality.

Budget: $1 per test, 20 turns max.
Skip automatically when ANTHROPIC_API_KEY is not set.

Command → expected skill mapping:
1.  forge-explore           → "forge-explore"
2.  forge-work              → "forge-work"
3.  forge-requirements      → "forge-requirements"
4.  forge-design            → "forge-design"
5.  forge-implement         → "forge-implement"
6.  forge-investigate       → "forge-investigate" (or "issue-investigator")
7.  forge-start-task        → "forge-start-ticket"
8.  forge-phase-complete    → "forge-phase-complete"
9.  forge-process-pr-discussions → "forge-process-pr-discussions"
10. forge-reviewable        → "forge-reviewable" (or "commit-restructuring")
11. forge-retro-note        → "forge-retro-note" (or "correction-tracking")
12. forge-improve           → "forge-maint-improve"
13. forge-audit             → "forge-maint-audit"
14. forge-digest            → "forge-digest"
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
        prompts=["/forge-init", prompt],
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
    """forge-explore should trigger the forge-explore skill."""
    await _run_command_test(
        "/forge-explore",
        "forge-explore",
        disposable_repo,
        run_session,
        extra_prompt="What should we build for rate limiting?",
    )


@_skip_if_no_key()
async def test_forge_work_triggers_skill(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """forge-work should trigger the forge-work skill."""
    await _run_command_test(
        "/forge-work",
        "forge-work",
        disposable_repo,
        run_session,
        extra_prompt="new",
    )


@_skip_if_no_key()
async def test_forge_requirements_triggers_skill(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """forge-requirements should trigger the forge-requirements skill."""
    await _run_command_test(
        "/forge-requirements",
        "forge-requirements",
        disposable_repo,
        run_session,
    )


@_skip_if_no_key()
async def test_forge_design_triggers_skill(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """forge-design should trigger the forge-design skill."""
    await _run_command_test(
        "/forge-design",
        "forge-design",
        disposable_repo,
        run_session,
    )


@_skip_if_no_key()
async def test_forge_implement_triggers_skill(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """forge-implement should trigger the forge-implement skill."""
    await _run_command_test(
        "/forge-implement",
        "forge-implement",
        disposable_repo,
        run_session,
        extra_prompt="Add a health check endpoint",
    )


@_skip_if_no_key()
async def test_forge_investigate_triggers_skill(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """forge-investigate should trigger the forge-investigate skill."""
    await _run_command_test(
        "/forge-investigate",
        "forge-investigate",
        disposable_repo,
        run_session,
        extra_prompt="Why does the app crash on startup?",
    )


@_skip_if_no_key()
async def test_forge_start_task_triggers_skill(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """forge-start-task should trigger the forge-start-ticket skill."""
    await _run_command_test(
        "/forge-start-task",
        "forge-start-ticket",
        disposable_repo,
        run_session,
    )


@_skip_if_no_key()
async def test_forge_phase_complete_triggers_skill(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """forge-phase-complete should trigger the forge-phase-complete skill."""
    await _run_command_test(
        "/forge-phase-complete",
        "forge-phase-complete",
        disposable_repo,
        run_session,
    )


@_skip_if_no_key()
async def test_forge_process_pr_discussions_triggers_skill(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """forge-process-pr-discussions should trigger matching skill."""
    await _run_command_test(
        "/forge-process-pr-discussions",
        "forge-process-pr-discussions",
        disposable_repo,
        run_session,
    )


@_skip_if_no_key()
async def test_forge_reviewable_triggers_skill(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """forge-reviewable should trigger commit-restructuring skill."""
    await _run_command_test(
        "/forge-reviewable",
        "commit-restructuring",
        disposable_repo,
        run_session,
    )


@_skip_if_no_key()
async def test_forge_retro_note_triggers_skill(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """forge-retro-note should trigger correction-tracking skill."""
    await _run_command_test(
        "/forge-retro-note",
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
    """forge-improve should trigger the forge-maint-improve skill."""
    await _run_command_test(
        "/forge-improve",
        "forge-maint-improve",
        disposable_repo,
        run_session,
    )


@_skip_if_no_key()
async def test_forge_audit_triggers_skill(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """forge-audit should trigger the forge-maint-audit skill."""
    await _run_command_test(
        "/forge-audit",
        "forge-maint-audit",
        disposable_repo,
        run_session,
    )


@_skip_if_no_key()
async def test_forge_digest_triggers_skill(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """forge-digest should trigger the forge-digest skill."""
    await _run_command_test(
        "/forge-digest",
        "forge-digest",
        disposable_repo,
        run_session,
    )
