from __future__ import annotations

import json
from pathlib import Path


REPO = Path(__file__).parents[1]
VERSION = "0.2.0"
README_NAMES = {
    "README.md",
    "README.ko.md",
    "README.ja.md",
    "README.zh-CN.md",
    "README.es.md",
    "README.fr.md",
    "README.de.md",
    "README.pt-BR.md",
}


def test_manifests_are_synchronized() -> None:
    paths = [
        REPO / "plugin.json",
        REPO / ".codex-plugin" / "plugin.json",
        REPO / ".claude-plugin" / "plugin.json",
    ]
    manifests = [json.loads(path.read_text(encoding="utf-8")) for path in paths]

    assert {manifest["name"] for manifest in manifests} == {"imagination-octo"}
    assert {manifest["version"] for manifest in manifests} == {VERSION}
    assert all(manifest["skills"] == "./skills/" for manifest in manifests)


def test_all_three_skills_are_present() -> None:
    expected = {
        "imagination-octo",
        "imagination-engine",
        "imagination-brainstorming",
    }
    actual = {
        path.parent.name
        for path in (REPO / "skills").glob("*/SKILL.md")
    }
    assert actual == expected


def test_embedded_engine_contains_the_confirmed_survivor_proof() -> None:
    text = (
        REPO / "skills" / "imagination-engine" / "SKILL.md"
    ).read_text(encoding="utf-8")

    assert "## Prove each survivor" in text
    assert "**Constraint evidence:**" in text
    assert "**Causal chain:**" in text
    assert "**First encounter:**" in text
    assert "**Decisive uncertainty:**" in text
    assert "**Dramatic cause:**" in text
    assert "**Changed next choice:**" in text


def test_embedded_workshop_contains_the_confirmed_proportional_preflight() -> None:
    text = (
        REPO / "skills" / "imagination-brainstorming" / "SKILL.md"
    ).read_text(encoding="utf-8")

    assert "by function, not label" in text
    assert "under another name, owner, location, or scale" in text
    assert "develop a smallest repair conditionally" in text
    assert "keep that component provisional" in text


def test_readmes_cover_all_supported_languages() -> None:
    actual = {path.name for path in REPO.glob("README*.md")}
    assert README_NAMES <= actual

    for name in README_NAMES:
        text = (REPO / name).read_text(encoding="utf-8")
        assert all(f"]({target})" in text for target in README_NAMES)
        assert "djfksjd/imagination-octo" in text
        assert "Engine v0.5.3" in text
        assert "Workshop v0.4.2" in text
        assert "100" in text
        assert "90" in text


def test_router_preserves_user_choice_boundary() -> None:
    text = (REPO / "skills" / "imagination-octo" / "SKILL.md").read_text(
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
