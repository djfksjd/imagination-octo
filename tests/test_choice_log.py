from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).parents[1]
SCRIPT = REPO / "skills" / "imagination-octo" / "scripts" / "choice_log.py"
CHOICE = {
    "event": "choice",
    "brief": "A quiet bathhouse on weekday afternoons",
    "portfolio": [{"title": "Tide table", "mechanism": "posted heat"}, {"title": "Wash walk"}],
    "pick": 2,
}


def run(tmp_path: Path, *args: str, payload: dict | None = None) -> subprocess.CompletedProcess[str]:
    env = {
        **os.environ,
        "IMAGINATION_OCTO_HOME": str(tmp_path / "state"),
        "CLAUDE_CONFIG_DIR": str(tmp_path / "claude"),
        "CODEX_HOME": str(tmp_path / "codex"),
    }
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        input=json.dumps(payload) if payload is not None else None,
        text=True,
        capture_output=True,
        env=env,
        check=False,
    )


def records(tmp_path: Path) -> list[dict]:
    path = tmp_path / "state" / "choices.jsonl"
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_nothing_is_written_until_the_user_opts_in(tmp_path: Path) -> None:
    result = run(tmp_path, "record", payload=CHOICE)

    assert result.returncode == 0
    assert "disabled" in result.stdout
    assert records(tmp_path) == []


def test_brief_is_hashed_unless_text_storage_is_requested(tmp_path: Path) -> None:
    run(tmp_path, "enable")
    run(tmp_path, "record", payload=CHOICE)
    run(tmp_path, "enable", "--with-brief")
    run(tmp_path, "record", payload=CHOICE)

    hashed, stored = records(tmp_path)
    assert "brief" not in hashed
    assert stored["brief"] == CHOICE["brief"]
    assert hashed["brief_hash"] == stored["brief_hash"]
    assert hashed["portfolio_id"] == stored["portfolio_id"]
    assert hashed["pick"] == 2


def test_malformed_records_are_rejected(tmp_path: Path) -> None:
    run(tmp_path, "enable")

    out_of_range = run(tmp_path, "record", payload={**CHOICE, "pick": 3})
    unknown_event = run(tmp_path, "record", payload={**CHOICE, "event": "upload"})

    assert out_of_range.returncode == 2
    assert unknown_event.returncode == 2
    assert records(tmp_path) == []


def test_rediverge_keeps_the_rejected_mechanisms(tmp_path: Path) -> None:
    run(tmp_path, "enable")
    run(
        tmp_path,
        "record",
        payload={
            "event": "rediverge",
            "brief": "b",
            "rejected_mechanisms": ["anything posted on a wall"],
            "rediverge_reason": "too much writing",
        },
    )

    (record,) = records(tmp_path)
    assert record["rejected_mechanisms"] == ["anything posted on a wall"]
    assert record["rediverge_reason"] == "too much writing"


def test_opt_in_line_is_added_and_removed_without_touching_other_text(
    tmp_path: Path,
) -> None:
    instructions = tmp_path / "claude" / "CLAUDE.md"
    instructions.parent.mkdir()
    instructions.write_text("existing rule\n", encoding="utf-8")

    run(tmp_path, "enable", "--hosts", "claude,codex")
    enabled = instructions.read_text(encoding="utf-8")
    run(tmp_path, "enable", "--hosts", "claude")
    assert instructions.read_text(encoding="utf-8") == enabled
    assert enabled.count("imagination-octo choice log: on") == 1
    assert enabled.startswith("existing rule\n")
    assert "choice log: on" in (tmp_path / "codex" / "AGENTS.md").read_text(encoding="utf-8")

    run(tmp_path, "disable")
    assert instructions.read_text(encoding="utf-8") == "existing rule\n"
    assert (tmp_path / "codex" / "AGENTS.md").read_text(encoding="utf-8") == ""


def test_the_logger_has_no_network_path() -> None:
    source = SCRIPT.read_text(encoding="utf-8")

    for module in ("socket", "urllib", "http", "requests", "subprocess"):
        assert f"import {module}" not in source
