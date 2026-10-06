#!/usr/bin/env python3
"""Opt-in, local-only log of which generated direction the user chose.

Nothing is written until `enable` is run, and nothing ever leaves this machine:
the module has no network code. The log is write-only for the skills; it exists
so the owner can later study real choices, not to steer generation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA = 1
EVENTS = ("choice", "rediverge", "outcome")
OUTCOMES = ("accepted", "reworked", "abandoned")
MAX_RECORD_BYTES = 16_384
MAX_TEXT = 600
INSTRUCTION = "imagination-octo choice log: on"
BLOCK_START = "<!-- imagination-octo:choice-log:start -->"
BLOCK_END = "<!-- imagination-octo:choice-log:end -->"
HOST_FILES = {
    "claude": ("CLAUDE_CONFIG_DIR", ".claude", "CLAUDE.md"),
    "codex": ("CODEX_HOME", ".codex", "AGENTS.md"),
}


def state_dir() -> Path:
    override = os.environ.get("IMAGINATION_OCTO_HOME")
    return Path(override) if override else Path.home() / ".imagination-octo"


def config_path() -> Path:
    return state_dir() / "config.json"


def log_path() -> Path:
    return state_dir() / "choices.jsonl"


def load_config() -> dict[str, Any]:
    try:
        config = json.loads(config_path().read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return config if isinstance(config, dict) else {}


def save_config(config: dict[str, Any]) -> None:
    state_dir().mkdir(parents=True, exist_ok=True)
    config_path().write_text(
        json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def host_file(host: str) -> Path:
    variable, folder, name = HOST_FILES[host]
    override = os.environ.get(variable)
    return (Path(override) if override else Path.home() / folder) / name


def strip_block(text: str) -> str:
    while BLOCK_START in text and BLOCK_END in text:
        head, _, rest = text.partition(BLOCK_START)
        _, _, tail = rest.partition(BLOCK_END)
        head, tail = head.rstrip("\n"), tail.strip("\n")
        text = "\n\n".join(part for part in (head, tail) if part)
        text += "\n" if text else ""
    return text


def write_instruction(host: str, enabled: bool) -> Path | None:
    path = host_file(host)
    original = path.read_text(encoding="utf-8") if path.exists() else ""
    text = strip_block(original)
    if enabled:
        body = text.rstrip("\n")
        block = f"{BLOCK_START}\n{INSTRUCTION}\n{BLOCK_END}\n"
        text = (body + "\n\n" if body else "") + block
    if text == original:
        return None
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def digest(*parts: str) -> str:
    normalized = "\n".join(" ".join(part.split()).casefold() for part in parts)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]


def clip(value: Any, field: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field!r} must be text")
    return " ".join(value.split())[:MAX_TEXT]


def clean_portfolio(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not 1 <= len(value) <= 9:
        raise ValueError("'portfolio' must list the one to nine directions shown")
    items = []
    for index, raw in enumerate(value, 1):
        if not isinstance(raw, dict) or "title" not in raw:
            raise ValueError("each portfolio item needs a 'title'")
        item = {"index": index, "title": clip(raw["title"], "title")}
        if raw.get("mechanism"):
            item["mechanism"] = clip(raw["mechanism"], "mechanism")
        items.append(item)
    return items


def build_record(payload: Any, config: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("the record must be a JSON object")
    event = payload.get("event")
    if event not in EVENTS:
        raise ValueError(f"'event' must be one of {', '.join(EVENTS)}")
    brief = clip(payload.get("brief", ""), "brief")
    if not brief:
        raise ValueError("'brief' is required; it is hashed unless text storage is on")

    record: dict[str, Any] = {
        "schema": SCHEMA,
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "event": event,
        "brief_hash": digest(brief),
    }
    if config.get("store_brief"):
        record["brief"] = brief
    for field in ("host", "language", "plugin_version"):
        if payload.get(field):
            record[field] = clip(payload[field], field)[:40]

    if "portfolio" in payload:
        portfolio = clean_portfolio(payload["portfolio"])
        record["portfolio"] = portfolio
        record["portfolio_id"] = digest(brief, *(item["title"] for item in portfolio))

    if event == "choice":
        pick = payload.get("pick")
        size = len(record.get("portfolio", []))
        if not isinstance(pick, int) or isinstance(pick, bool) or pick < 1:
            raise ValueError("'pick' must be the 1-based index of the chosen direction")
        if size and pick > size:
            raise ValueError("'pick' is outside the portfolio")
        record["pick"] = pick
        if payload.get("pick_reason"):
            record["pick_reason"] = clip(payload["pick_reason"], "pick_reason")
    elif event == "rediverge":
        rejected = payload.get("rejected_mechanisms", [])
        if not isinstance(rejected, list):
            raise ValueError("'rejected_mechanisms' must be a list")
        record["rejected_mechanisms"] = [
            clip(item, "rejected_mechanisms") for item in rejected[:9]
        ]
        if payload.get("rediverge_reason"):
            record["rediverge_reason"] = clip(
                payload["rediverge_reason"], "rediverge_reason"
            )
    else:
        outcome = payload.get("outcome")
        if outcome not in OUTCOMES:
            raise ValueError(f"'outcome' must be one of {', '.join(OUTCOMES)}")
        record["outcome"] = outcome
        if payload.get("reworked_part"):
            record["reworked_part"] = clip(payload["reworked_part"], "reworked_part")

    if len(json.dumps(record, ensure_ascii=False).encode("utf-8")) > MAX_RECORD_BYTES:
        raise ValueError("record is too large")
    return record


def read_records() -> list[dict[str, Any]]:
    try:
        lines = log_path().read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    records = []
    for line in lines:
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict):
            records.append(row)
    return records


def command_enable(args: argparse.Namespace) -> int:
    config = load_config()
    config.update(
        enabled=True,
        store_brief=bool(args.with_brief),
        enabled_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )
    save_config(config)
    print(f"Choice log enabled. Records stay in {log_path()}")
    print(
        "Brief text is stored."
        if args.with_brief
        else "Briefs are stored as hashes only (use --with-brief to keep the text)."
    )
    written = [write_instruction(host, True) for host in args.hosts]
    for path in filter(None, written):
        print(f"Added the standing instruction to {path}")
    if not args.hosts:
        print(
            "To let the skill see the opt-in, add this line to your global "
            f"instructions (or re-run with --hosts claude,codex):\n  {INSTRUCTION}"
        )
    return 0


def command_disable(_: argparse.Namespace) -> int:
    config = load_config()
    config["enabled"] = False
    save_config(config)
    for host in HOST_FILES:
        path = write_instruction(host, False)
        if path:
            print(f"Removed the standing instruction from {path}")
    print("Choice log disabled. Existing records are kept; use `purge` to delete them.")
    return 0


def command_status(_: argparse.Namespace) -> int:
    config = load_config()
    print(f"enabled: {bool(config.get('enabled'))}")
    print(f"store_brief: {bool(config.get('store_brief'))}")
    print(f"records: {len(read_records())}")
    print(f"path: {log_path()}")
    return 0


def command_record(_: argparse.Namespace) -> int:
    config = load_config()
    if not config.get("enabled"):
        print("choice log is disabled; nothing was written")
        return 0
    raw = sys.stdin.read(MAX_RECORD_BYTES * 4)
    try:
        record = build_record(json.loads(raw), config)
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"record rejected: {exc}", file=sys.stderr)
        return 2
    state_dir().mkdir(parents=True, exist_ok=True)
    with log_path().open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    print("recorded")
    return 0


def command_show(args: argparse.Namespace) -> int:
    for record in read_records()[-args.last :]:
        print(json.dumps(record, ensure_ascii=False, sort_keys=True))
    return 0


def command_stats(_: argparse.Namespace) -> int:
    records = read_records()
    events = Counter(record.get("event") for record in records)
    positions = Counter(
        record.get("pick") for record in records if record.get("event") == "choice"
    )
    print(
        json.dumps(
            {
                "records": len(records),
                "events": dict(sorted(events.items(), key=str)),
                "pick_position": {
                    str(position): count
                    for position, count in sorted(positions.items(), key=str)
                },
                "briefs": len({record.get("brief_hash") for record in records}),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def command_purge(args: argparse.Namespace) -> int:
    if not args.yes:
        print("Refusing to delete without --yes", file=sys.stderr)
        return 2
    try:
        log_path().unlink()
    except FileNotFoundError:
        pass
    print("Choice log deleted.")
    return 0


def hosts_argument(value: str) -> list[str]:
    hosts = [part.strip() for part in value.split(",") if part.strip()]
    unknown = sorted(set(hosts) - set(HOST_FILES))
    if unknown:
        raise argparse.ArgumentTypeError(f"unknown host(s): {', '.join(unknown)}")
    return hosts


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)

    enable = commands.add_parser("enable", help="turn the log on")
    enable.add_argument(
        "--with-brief", action="store_true", help="store brief text, not only its hash"
    )
    enable.add_argument(
        "--hosts",
        type=hosts_argument,
        default=[],
        help="comma-separated hosts whose global instructions get the opt-in line "
        "(claude, codex)",
    )
    enable.set_defaults(handler=command_enable)

    for name, handler, description in (
        ("disable", command_disable, "turn the log off and remove the opt-in line"),
        ("status", command_status, "show whether the log is on"),
        ("record", command_record, "append one JSON record read from stdin"),
        ("stats", command_stats, "summarize recorded choices"),
    ):
        commands.add_parser(name, help=description).set_defaults(handler=handler)

    show = commands.add_parser("show", help="print recent records")
    show.add_argument("--last", type=int, default=20)
    show.set_defaults(handler=command_show)

    purge = commands.add_parser("purge", help="delete every record")
    purge.add_argument("--yes", action="store_true")
    purge.set_defaults(handler=command_purge)
    return root


def main() -> int:
    args = parser().parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
