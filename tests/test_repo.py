from __future__ import annotations

import json
from pathlib import Path


REPO = Path(__file__).parents[1]
VERSION = "0.1.0"


def test_manifests_are_synchronized() -> None:
    paths = [
        REPO / "plugin.json",
        REPO / ".codex-plugin" / "plugin.json",
        REPO / ".claude-plugin" / "plugin.json",
    ]
    manifests = [json.loads(path.read_text(encoding="utf-8")) for path in paths]

    assert {manifest["name"] for manifest in manifests} == {"imagination"}
    assert {manifest["version"] for manifest in manifests} == {VERSION}
    assert all(manifest["skills"] == "./skills/" for manifest in manifests)


def test_all_three_skills_are_present() -> None:
    expected = {
        "imagination",
        "imagination-engine",
        "imagination-brainstorming",
    }
    actual = {
        path.parent.name
        for path in (REPO / "skills").glob("*/SKILL.md")
    }
    assert actual == expected


def test_router_preserves_user_choice_boundary() -> None:
    text = (REPO / "skills" / "imagination" / "SKILL.md").read_text(
        encoding="utf-8"
    )

    assert "../imagination-engine/SKILL.md" in text
    assert "../imagination-brainstorming/SKILL.md" in text
    assert "select a winner for the user" in text
    assert "wait for the user to confirm" in text
    assert "Never read both specialist skills in the same turn" in text


def test_no_scaffold_placeholders_remain() -> None:
    tracked_text = [
        *REPO.glob("*.md"),
        *REPO.glob("skills/*/SKILL.md"),
        *REPO.glob(".codex-plugin/*.json"),
        *REPO.glob(".claude-plugin/*.json"),
    ]
    for path in tracked_text:
        assert "[TODO:" not in path.read_text(encoding="utf-8")
