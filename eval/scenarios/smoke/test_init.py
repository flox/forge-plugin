"""Tier 1 smoke tests: /forge-init onboarding.

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
async def test_forge_init_creates_context_directory(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """Verify /forge-init creates .forge-context/ directory structure.

    The init command should scaffold at minimum:
    - .forge-context/
    - .forge-context/context/
    - .forge-context/efforts/
    - .forge-context/slices/
    """
    trace = await run_session(  # type: ignore[operator]
        repo_path=disposable_repo,
        prompts=["/forge-init"],
        max_budget_usd=1.0,
        max_turns=20,
    )

    # At least one Write call should target .forge-context/
    assert_file_exists(trace, ".forge-context")


@pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set",
)
async def test_forge_init_creates_context_files(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """Verify /forge-init writes context files during onboarding.

    After init, at least a product.md or similar context file
    should exist in .forge-context/context/.
    """
    trace = await run_session(  # type: ignore[operator]
        repo_path=disposable_repo,
        prompts=["/forge-init"],
        max_budget_usd=1.0,
        max_turns=20,
    )

    # Should write at least one context file
    assert_file_exists(trace, "context/")


@pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set",
)
async def test_forge_init_copies_templates(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """Verify /forge-init copies templates into the project.

    Templates should land in .forge-context/templates/ so users
    have scaffold documents to start from.
    """
    trace = await run_session(  # type: ignore[operator]
        repo_path=disposable_repo,
        prompts=["/forge-init"],
        max_budget_usd=1.0,
        max_turns=20,
    )

    # Should create a templates directory or at least reference it
    assert_file_exists(trace, "templates")
