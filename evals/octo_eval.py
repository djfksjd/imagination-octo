#!/usr/bin/env python3
"""Cross-model evaluation harness for Imagination Octo.

`run` executes Experiment A (four arms, two generator families, cross-family
blind judging, across-run convergence, blinding probe) and is resumable: every
model call is appended to a JSONL file and skipped on the next invocation.
`router` runs the two-turn regression suite. `human-packet` exports the owner's
blind sanity pairs. See PREREGISTRATION.md for the frozen decision rule.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import math
import statistics
import subprocess
import sys
import tempfile
import threading
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable, Iterable


EVALS = Path(__file__).resolve().parent
REPO = EVALS.parent
PROMPTS = EVALS / "prompts"
ENGINE_SKILL = REPO / "skills" / "imagination-engine" / "SKILL.md"
ROUTER_FILES = (
    "skills/imagination-octo/SKILL.md",
    "skills/imagination-engine/SKILL.md",
    "skills/imagination-brainstorming/SKILL.md",
)

SEED = "octo-experiment-a-2026-10"
ARMS = ("A0", "A1", "A2", "A3")
PAIRS = (("A1", "A0"), ("A3", "A0"), ("A3", "A1"), ("A3", "A2"))
METRICS = ("fit", "useful_surprise", "set_diversity", "craft")
ABLATED_SECTION = "## Prove each survivor"
# Arm definitions: a prompt template, plus an optional runtime injected as a
# skill. `--spec` replaces ARMS, PAIRS, and ARM_DEFS for other experiments.
ARM_DEFS: dict[str, dict[str, Any]] = {
    "A0": {"prompt": "control.md"},
    "A1": {"prompt": "control-effort.md"},
    "A2": {
        "prompt": "treatment.md",
        "skill": "skills/imagination-engine/SKILL.md",
        "ablate": True,
    },
    "A3": {"prompt": "treatment.md", "skill": "skills/imagination-engine/SKILL.md"},
}
FAMILIES: dict[str, dict[str, str]] = {
    "gpt": {"generator": "gpt-5.5", "judge": "gpt-5.5", "reasoning": "medium"},
    "claude": {"generator": "claude-opus-5-5", "judge": "claude-opus-5-5"},
}
OTHER = {"gpt": "claude", "claude": "gpt"}
CLAUDE_SYSTEM = "You are a helpful assistant. Answer the user's request directly."
CLEAN_ROOM = (
    "Do not use tools, browse, inspect files, discuss the evaluation, or reveal "
    "private reasoning. Return only the requested user-facing result.\n\n"
)


# ----------------------------------------------------------------- storage


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{number}: invalid JSON: {exc}") from exc
        rows.append(row)
    return rows


class Store:
    """Append-only JSONL keyed by a tuple of fields, so runs can resume."""

    def __init__(self, path: Path, key: tuple[str, ...]) -> None:
        self.path, self.key = path, key
        self.lock = threading.Lock()
        self.rows = {self.key_of(row): row for row in read_jsonl(path)}

    def key_of(self, row: dict[str, Any]) -> tuple[Any, ...]:
        return tuple(row[field] for field in self.key)

    def has(self, *key: Any) -> bool:
        return tuple(key) in self.rows

    def get(self, *key: Any) -> dict[str, Any] | None:
        return self.rows.get(tuple(key))

    def add(self, row: dict[str, Any]) -> None:
        with self.lock:
            self.rows[self.key_of(row)] = row
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    def values(self) -> list[dict[str, Any]]:
        return list(self.rows.values())


def stable_int(*parts: object) -> int:
    material = "|".join([SEED, *(str(part) for part in parts)])
    return int.from_bytes(hashlib.sha256(material.encode("utf-8")).digest()[:8], "big")


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


# --------------------------------------------------------------- providers


class Breaker:
    """Stop the whole run after repeated failures (rate limits, auth, outage)."""

    def __init__(self, limit: int = 6) -> None:
        self.limit, self.streak, self.lock = limit, 0, threading.Lock()
        self.tripped = threading.Event()

    def report(self, ok: bool) -> None:
        with self.lock:
            self.streak = 0 if ok else self.streak + 1
            if self.streak >= self.limit:
                self.tripped.set()


BREAKER = Breaker()
LIMITS: dict[str, int] = {}  # optional per-provider cap on concurrent calls


class Aborted(RuntimeError):
    """Raised for calls skipped because the breaker has tripped."""


def call_codex(
    prompt: str, model: str, schema: dict[str, Any] | None, timeout: int
) -> tuple[str, dict[str, int]]:
    reasoning = FAMILIES["gpt"]["reasoning"]
    with tempfile.TemporaryDirectory(prefix="octo-eval-") as clean_dir:
        command = [
            "codex", "exec", "--cd", clean_dir, "--ignore-user-config",
            "--ignore-rules", "--ephemeral", "--skip-git-repo-check",
            "--sandbox", "read-only", "--model", model,
            "-c", f'model_reasoning_effort="{reasoning}"', "--json",
        ]  # fmt: skip
        if schema is not None:
            schema_path = Path(clean_dir) / "schema.json"
            schema_path.write_text(json.dumps(schema), encoding="utf-8")
            command += ["--output-schema", str(schema_path)]
        result = subprocess.run(
            [*command, "-"], input=prompt, text=True, capture_output=True,
            timeout=timeout, check=False,
        )  # fmt: skip
    message, failure, usage = "", "", {}
    for raw in result.stdout.splitlines():
        try:
            event = json.loads(raw)
        except json.JSONDecodeError:
            continue
        item = event.get("item", {})
        if event.get("type") == "item.completed" and item.get("type") == "agent_message":
            message = str(item.get("text", "")).strip()
        elif event.get("type") == "turn.completed":
            usage = event.get("usage", {})
        elif event.get("type") == "error":
            failure = str(event.get("message", ""))
    if result.returncode or not message:
        detail = failure or result.stderr[-600:] or result.stdout[-600:]
        raise RuntimeError(f"codex exited {result.returncode}: {detail[:600]}")
    tokens = {
        "input_tokens": int(usage.get("input_tokens", 0)),
        "output_tokens": int(usage.get("output_tokens", 0)),
    }
    return message, tokens


def call_claude(
    prompt: str, model: str, schema: dict[str, Any] | None, timeout: int
) -> tuple[str, dict[str, int]]:
    command = [
        "claude", "-p", "--model", model, "--system-prompt", CLAUDE_SYSTEM,
        "--tools", "", "--setting-sources", "", "--strict-mcp-config",
        "--disable-slash-commands", "--no-session-persistence",
        "--output-format", "json",
    ]  # fmt: skip
    if schema is not None:
        command += ["--json-schema", json.dumps(schema)]
    with tempfile.TemporaryDirectory(prefix="octo-eval-") as clean_dir:
        result = subprocess.run(
            command, input=prompt, text=True, capture_output=True,
            timeout=timeout, check=False, cwd=clean_dir,
        )  # fmt: skip
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        payload = {}
    if result.returncode or payload.get("is_error") or not payload:
        detail = payload.get("result") or result.stderr or result.stdout
        status = payload.get("api_error_status")
        raise RuntimeError(
            f"claude exited {result.returncode} (status {status}): {str(detail)[:600]}"
        )
    structured = payload.get("structured_output")
    message = (
        json.dumps(structured, ensure_ascii=False)
        if schema is not None and structured is not None
        else str(payload.get("result", "")).strip()
    )
    if not message:
        raise RuntimeError("claude returned no message")
    usage = payload.get("usage", {})
    tokens = {
        "input_tokens": sum(
            int(usage.get(field, 0) or 0)
            for field in (
                "input_tokens",
                "cache_creation_input_tokens",
                "cache_read_input_tokens",
            )
        ),
        "output_tokens": int(usage.get("output_tokens", 0) or 0),
    }
    return message, tokens


def parse_json(message: str) -> dict[str, Any]:
    text = message.strip()
    if not text.startswith("{"):
        start, end = text.find("{"), text.rfind("}")
        if start < 0 or end < 0:
            raise ValueError("no JSON object in the reply")
        text = text[start : end + 1]
    value = json.loads(text)
    if not isinstance(value, dict):
        raise ValueError("reply is not a JSON object")
    return value


def call_model(
    family: str,
    role: str,
    prompt: str,
    *,
    schema: dict[str, Any] | None = None,
    check: Callable[[dict[str, Any]], None] | None = None,
    timeout: int = 600,
    attempts: int = 3,
) -> dict[str, Any]:
    """Call one model with retries; returns text, parsed JSON, tokens, seconds."""
    model = FAMILIES[family][role]
    caller = call_codex if family == "gpt" else call_claude
    error: Exception | None = None
    for attempt in range(attempts):
        if BREAKER.tripped.is_set():
            raise Aborted("aborted after repeated failures")
        started = time.monotonic()
        try:
            message, tokens = caller(prompt, model, schema, timeout)
            parsed = parse_json(message) if schema is not None else None
            if check is not None and parsed is not None:
                check(parsed)
        except Aborted:
            raise
        except Exception as exc:  # noqa: BLE001 - every failure is retried
            error = exc
            BREAKER.report(False)
            time.sleep(30 * (attempt + 1))  # rate limits need a real pause
            continue
        BREAKER.report(True)
        return {
            "text": message,
            "json": parsed,
            "model": model,
            "seconds": round(time.monotonic() - started, 2),
            **tokens,
        }
    raise RuntimeError(f"{family}/{role} failed after {attempts} attempts: {error}")


def run_jobs(
    label: str,
    jobs: list[Any],
    worker: Callable[[Any], None],
    family_of: Callable[[Any], str],
    workers: int,
) -> int:
    """Run jobs with `workers` concurrent calls per provider; returns failures."""
    if not jobs:
        print(f"[{label}] nothing to do")
        return 0
    done, failed, lock = 0, 0, threading.Lock()

    def guarded(job: Any) -> None:
        nonlocal done, failed
        try:
            worker(job)
            ok = True
        except Aborted:
            ok = False
        except Exception as exc:  # noqa: BLE001 - keep the other jobs alive
            ok = False
            print(f"[{label}] error: {exc}", flush=True)
        with lock:
            done += 1
            failed += 0 if ok else 1
            if done % 10 == 0 or done == len(jobs):
                print(f"[{label}] {done}/{len(jobs)} ({failed} failed)", flush=True)

    # One pool per provider, so a slow or capped provider cannot starve the other.
    pools = []
    for family in FAMILIES:
        own = [job for job in jobs if family_of(job) == family]
        size = min(workers, LIMITS.get(family, workers))
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=size)
        pools.append((pool, [pool.submit(guarded, job) for job in own]))
    for pool, futures in pools:
        concurrent.futures.wait(futures)
        pool.shutdown()
    return failed


# ------------------------------------------------------------ experiment A


def ablated_skill(skill: str) -> str:
    start = skill.index(ABLATED_SECTION)
    end = skill.index("\n## ", start + 1)
    return skill[:start] + skill[end + 1 :]


def generation_prompt(arm: str, brief: str) -> str:
    spec = ARM_DEFS[arm]
    template = (PROMPTS / spec["prompt"]).read_text(encoding="utf-8")
    task = template.replace("{{BRIEF}}", brief)
    if "skill" not in spec:
        return CLEAN_ROOM + task
    skill = (REPO / spec["skill"]).read_text(encoding="utf-8")
    if spec.get("ablate"):
        skill = ablated_skill(skill)
    return (
        CLEAN_ROOM
        + "Apply the following skill instructions faithfully while solving the task.\n\n"
        + f"<skill>\n{skill.strip()}\n</skill>\n\n"
        + task
    )


DECISION: dict[str, str] = {}  # {"new", "old", "plain"} for a replacement test


def load_spec(path: Path) -> None:
    """Swap in another experiment's arms and comparisons."""
    global ARMS, PAIRS, ARM_DEFS, DECISION
    spec = json.loads(path.read_text(encoding="utf-8"))
    ARM_DEFS = spec["arms"]
    ARMS = tuple(ARM_DEFS)
    PAIRS = tuple((x, y) for x, y in spec["pairs"])
    DECISION = spec.get("decision", {})


def side_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            metric: {"type": "integer", "minimum": 1, "maximum": 7}
            for metric in METRICS
        },
        "required": list(METRICS),
        "additionalProperties": False,
    }


JUDGE_SCHEMA = {
    "type": "object",
    "properties": {
        "ratings": {
            "type": "object",
            "properties": {"left": side_schema(), "right": side_schema()},
            "required": ["left", "right"],
            "additionalProperties": False,
        },
        "want": {"type": "string", "enum": ["left", "right", "tie"]},
    },
    "required": ["ratings", "want"],
    "additionalProperties": False,
}
PROBE_SCHEMA = {
    "type": "object",
    "properties": {
        "guess": {"type": "string", "enum": ["left", "right"]},
        "cue": {"type": "string"},
    },
    "required": ["guess", "cue"],
    "additionalProperties": False,
}
CODING_SCHEMA = {
    "type": "object",
    "properties": {
        "mechanisms": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"id": {"type": "string"}, "label": {"type": "string"}},
                "required": ["id", "label"],
                "additionalProperties": False,
            },
        },
        "portfolios": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "portfolio": {"type": "string"},
                    "mechanism_ids": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["portfolio", "mechanism_ids"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["mechanisms", "portfolios"],
    "additionalProperties": False,
}


class Experiment:
    def __init__(
        self,
        name: str,
        briefs_path: Path,
        runs: int,
        workers: int,
        root: Path | None = None,
    ) -> None:
        self.dir = (root or EVALS / "runs") / name
        self.briefs = read_jsonl(briefs_path)
        self.briefs_path = briefs_path
        self.brief = {brief["id"]: brief for brief in self.briefs}
        self.runs, self.workers = runs, workers
        self.outputs = Store(
            self.dir / "outputs.jsonl", ("brief_id", "family", "arm", "run")
        )
        self.votes = Store(self.dir / "votes.jsonl", ("pair_id", "order"))
        self.probes = Store(self.dir / "probes.jsonl", ("pair_id",))
        self.codings = Store(self.dir / "codings.jsonl", ("brief_id", "family"))

    def cells(self) -> Iterable[tuple[str, str, int]]:
        for brief in self.briefs:
            for family in FAMILIES:
                for run in range(1, self.runs + 1):
                    yield brief["id"], family, run

    # -- generation

    def generate(self) -> int:
        jobs = [
            (brief_id, family, arm, run)
            for brief_id, family, run in self.cells()
            for arm in ARMS
            if not self.outputs.has(brief_id, family, arm, run)
        ]

        def worker(job: tuple[str, str, str, int]) -> None:
            brief_id, family, arm, run = job
            prompt = generation_prompt(arm, self.brief[brief_id]["prompt"])
            reply = call_model(family, "generator", prompt)
            self.outputs.add(
                {
                    "brief_id": brief_id, "family": family, "arm": arm, "run": run,
                    "text": reply["text"], "model": reply["model"],
                    "seconds": reply["seconds"],
                    "input_tokens": reply["input_tokens"],
                    "output_tokens": reply["output_tokens"],
                }  # fmt: skip
            )

        return run_jobs("generate", jobs, worker, lambda job: job[1], self.workers)

    def text(self, brief_id: str, family: str, arm: str, run: int) -> str:
        row = self.outputs.get(brief_id, family, arm, run)
        if row is None:
            raise KeyError(f"missing output {brief_id}/{family}/{arm}/{run}")
        return row["text"]

    # -- blind pairwise judging (cross-family, both left/right orders)

    @staticmethod
    def pair_id(brief_id: str, family: str, run: int, x: str, y: str) -> str:
        return f"{stable_int(brief_id, family, run, x, y):016x}"

    def judge(self) -> int:
        instructions = (PROMPTS / "judge.md").read_text(encoding="utf-8").strip()
        jobs = []
        for brief_id, family, run in self.cells():
            for x, y in PAIRS:
                pair = self.pair_id(brief_id, family, run, x, y)
                for order in (0, 1):
                    if not self.votes.has(pair, order):
                        jobs.append((brief_id, family, run, x, y, pair, order))

        def worker(job: tuple[str, str, int, str, str, str, int]) -> None:
            brief_id, family, run, x, y, pair, order = job
            left, right = (x, y) if order == 0 else (y, x)
            prompt = (
                "Do not use tools, browse, inspect files, or infer the generating "
                "condition. Judge only the delivered texts. Return only JSON "
                "matching the supplied schema.\n\n"
                f"{instructions}\n\nBRIEF:\n{self.brief[brief_id]['prompt']}"
                f"\n\nLEFT:\n{self.text(brief_id, family, left, run)}"
                f"\n\nRIGHT:\n{self.text(brief_id, family, right, run)}"
            )
            judge_family = OTHER[family]
            reply = call_model(judge_family, "judge", prompt, schema=JUDGE_SCHEMA)
            verdict = reply["json"]
            ratings = {
                left: verdict["ratings"]["left"],
                right: verdict["ratings"]["right"],
            }
            want = {"left": left, "right": right, "tie": "tie"}[verdict["want"]]
            self.votes.add(
                {
                    "pair_id": pair, "order": order, "brief_id": brief_id,
                    "family": family, "run": run, "x": x, "y": y,
                    "judge_family": judge_family, "judge_model": reply["model"],
                    "ratings": ratings, "want": want,
                }  # fmt: skip
            )

        return run_jobs("judge", jobs, worker, lambda job: OTHER[job[1]], self.workers)

    # -- blinding probe: can a judge tell which side used the skill?

    def probe(self, probe_runs: int) -> int:
        instructions = (PROMPTS / "probe.md").read_text(encoding="utf-8").strip()
        jobs = []
        for brief_id, family, run in self.cells():
            pair = self.pair_id(brief_id, family, run, "A3", "A0")
            if run <= probe_runs and not self.probes.has(pair):
                jobs.append((brief_id, family, run, pair))

        def worker(job: tuple[str, str, int, str]) -> None:
            brief_id, family, run, pair = job
            order = stable_int("probe", pair) & 1
            left, right = ("A3", "A0") if order == 0 else ("A0", "A3")
            prompt = (
                f"{instructions}\n\nBRIEF:\n{self.brief[brief_id]['prompt']}"
                f"\n\nLEFT:\n{self.text(brief_id, family, left, run)}"
                f"\n\nRIGHT:\n{self.text(brief_id, family, right, run)}"
            )
            reply = call_model(OTHER[family], "judge", prompt, schema=PROBE_SCHEMA)
            guess = {"left": left, "right": right}[reply["json"]["guess"]]
            self.probes.add(
                {
                    "pair_id": pair, "brief_id": brief_id, "family": family,
                    "run": run, "correct": guess == "A3",
                    "cue": reply["json"]["cue"][:300],
                }  # fmt: skip
            )

        return run_jobs("probe", jobs, worker, lambda job: OTHER[job[1]], self.workers)

    # -- across-run convergence: one cross-family coding call per brief × family

    def labels(self, brief_id: str, family: str) -> dict[str, tuple[str, int]]:
        slots = [(arm, run) for arm in ARMS for run in range(1, self.runs + 1)]
        slots.sort(key=lambda slot: stable_int("coding", brief_id, family, *slot))
        return {f"P{index:02d}": slot for index, slot in enumerate(slots, 1)}

    def converge(self) -> int:
        instructions = (PROMPTS / "coding.md").read_text(encoding="utf-8").strip()
        jobs = [
            (brief["id"], family)
            for brief in self.briefs
            for family in FAMILIES
            if not self.codings.has(brief["id"], family)
        ]

        def worker(job: tuple[str, str]) -> None:
            brief_id, family = job
            labels = self.labels(brief_id, family)
            body = "\n\n".join(
                f"=== {label} ===\n{self.text(brief_id, family, arm, run)}"
                for label, (arm, run) in labels.items()
            )

            def check(parsed: dict[str, Any]) -> None:
                seen = {row["portfolio"] for row in parsed["portfolios"]}
                if seen != set(labels):
                    raise ValueError("coding does not cover every portfolio once")
                if any(not row["mechanism_ids"] for row in parsed["portfolios"]):
                    raise ValueError("a portfolio was coded with no mechanism")

            prompt = (
                f"{instructions}\n\nBRIEF:\n{self.brief[brief_id]['prompt']}\n\n{body}"
            )
            reply = call_model(
                OTHER[family], "judge", prompt, schema=CODING_SCHEMA, check=check,
                timeout=900,
            )  # fmt: skip
            self.codings.add(
                {
                    "brief_id": brief_id, "family": family,
                    "coder_model": reply["model"],
                    "mechanisms": reply["json"]["mechanisms"],
                    "portfolios": {
                        row["portfolio"]: row["mechanism_ids"]
                        for row in reply["json"]["portfolios"]
                    },
                }  # fmt: skip
            )

        return run_jobs("converge", jobs, worker, lambda job: OTHER[job[1]], 2)


# ---------------------------------------------------------------- scoring


def mean(values: Iterable[float]) -> float | None:
    values = list(values)
    return round(statistics.fmean(values), 4) if values else None


def sign_test(wins: int, losses: int) -> float:
    """One-sided exact probability of at least `wins` successes at p = 0.5."""
    total = wins + losses
    if total == 0:
        return 1.0
    tail = sum(math.comb(total, k) for k in range(wins, total + 1))
    return round(tail / 2**total, 5)


def trigram_cosine(left: str, right: str) -> float:
    def grams(text: str) -> Counter[str]:
        squashed = " ".join(text.lower().split())
        return Counter(squashed[i : i + 3] for i in range(len(squashed) - 2))

    a, b = grams(left), grams(right)
    dot = sum(count * b[gram] for gram, count in a.items())
    norm = math.sqrt(sum(v * v for v in a.values()) * sum(v * v for v in b.values()))
    return dot / norm if norm else 0.0


def format_stats(text: str) -> dict[str, float]:
    lines = text.splitlines()
    return {
        "chars": len(text),
        "words": len(text.split()),
        "lines": len([line for line in lines if line.strip()]),
        "bullets": len([l for l in lines if l.lstrip()[:2] in ("- ", "* ", "• ")]),
        "headings": len([line for line in lines if line.lstrip().startswith("#")]),
        "bold_labels": text.count("**") // 2,
    }


def pair_outcome(votes: list[dict[str, Any]]) -> str:
    wants = {vote["want"] for vote in votes}
    return wants.pop() if len(wants) == 1 else "tie"


def score_pair(
    exp: Experiment, family: str, x: str, y: str, briefs: list[str]
) -> dict[str, Any]:
    cell: Counter[str] = Counter()
    per_brief: dict[str, Counter[str]] = defaultdict(Counter)
    diffs: dict[str, list[float]] = defaultdict(list)
    fit_by_brief: dict[str, list[float]] = defaultdict(list)
    missing = 0
    for brief_id in briefs:
        for run in range(1, exp.runs + 1):
            pair = exp.pair_id(brief_id, family, run, x, y)
            votes = [exp.votes.get(pair, order) for order in (0, 1)]
            if None in votes:
                missing += 1
                continue
            outcome = pair_outcome(votes)  # type: ignore[arg-type]
            cell[outcome] += 1
            per_brief[brief_id][outcome] += 1
            for vote in votes:
                for metric in METRICS:
                    diff = vote["ratings"][x][metric] - vote["ratings"][y][metric]
                    diffs[metric].append(diff)
                    if metric == "fit":
                        fit_by_brief[brief_id].append(diff)
    brief_level: Counter[str] = Counter()
    for counts in per_brief.values():
        brief_level[
            x if counts[x] > counts[y] else y if counts[y] > counts[x] else "tie"
        ] += 1
    cells = sum(cell.values())
    return {
        "pair": f"{x} vs {y}",
        "cells": {"x": cell[x], "y": cell[y], "tie": cell["tie"], "missing": missing},
        "cell_net": round((cell[x] - cell[y]) / cells, 4) if cells else None,
        "briefs": {"x": brief_level[x], "y": brief_level[y], "tie": brief_level["tie"]},
        "sign_test_p": sign_test(brief_level[x], brief_level[y]),
        "rating_diff": {metric: mean(diffs[metric]) for metric in METRICS},
        "worst_brief_median_fit": min(
            (statistics.median(values) for values in fit_by_brief.values()),
            default=None,
        ),
    }


def convergence(exp: Experiment, family: str) -> dict[str, dict[str, Any]]:
    overlap: dict[str, list[float]] = defaultdict(list)
    distinct: dict[str, list[float]] = defaultdict(list)
    lexical: dict[str, list[float]] = defaultdict(list)
    runs = range(1, exp.runs + 1)
    for brief in exp.briefs:
        coding = exp.codings.get(brief["id"], family)
        by_slot = {}
        if coding is not None:
            labels = exp.labels(brief["id"], family)
            by_slot = {
                labels[label]: set(ids) for label, ids in coding["portfolios"].items()
            }
        for arm in ARMS:
            if by_slot:
                sets = [by_slot[(arm, run)] for run in runs]
                pairs = [
                    len(a & b) / min(len(a), len(b))
                    for i, a in enumerate(sets)
                    for b in sets[i + 1 :]
                ]
                if pairs:
                    overlap[arm].append(statistics.fmean(pairs))
                distinct[arm].append(
                    len(set().union(*sets)) / sum(len(group) for group in sets)
                )
            texts = [
                row["text"]
                for run in runs
                if (row := exp.outputs.get(brief["id"], family, arm, run))
            ]
            similarities = [
                trigram_cosine(a, b)
                for i, a in enumerate(texts)
                for b in texts[i + 1 :]
            ]
            if similarities:
                lexical[arm].append(statistics.fmean(similarities))
    return {
        arm: {
            "mechanism_overlap": mean(overlap[arm]),
            "distinct_mechanism_ratio": mean(distinct[arm]),
            "lexical_similarity": mean(lexical[arm]),
            "briefs_coded": len(overlap[arm]),
        }
        for arm in ARMS
    }


def arm_costs(exp: Experiment, family: str) -> dict[str, dict[str, Any]]:
    result = {}
    for arm in ARMS:
        rows = [
            row
            for row in exp.outputs.values()
            if row["family"] == family and row["arm"] == arm
        ]
        stats = [format_stats(row["text"]) for row in rows]
        result[arm] = {
            "outputs": len(rows),
            "total_tokens": mean(r["input_tokens"] + r["output_tokens"] for r in rows),
            "output_tokens": mean(row["output_tokens"] for row in rows),
            "seconds": mean(row["seconds"] for row in rows),
            **{
                key: mean(stat[key] for stat in stats)
                for key in ("chars", "words", "lines", "bullets", "headings", "bold_labels")
            },
        }
    return result


def ratio(top: float | None, bottom: float | None) -> float | None:
    return round(top / bottom, 3) if top is not None and bottom else None


def decide(family_result: dict[str, Any], human: dict[str, Any] | None) -> dict[str, Any]:
    pairs = family_result["pairs"]
    a3_a0, a1_a0 = pairs["A3 vs A0"], pairs["A1 vs A0"]
    a3_a1, a3_a2 = pairs["A3 vs A1"], pairs["A3 vs A2"]
    costs, trap = family_result["costs"], family_result["trap_A3_vs_A0"]
    conv, probe = family_result["convergence"], family_result["probe"]
    decided = a3_a0["briefs"]["x"] + a3_a0["briefs"]["y"]
    surprise = a3_a0["rating_diff"]["useful_surprise"]
    token_ratio = ratio(costs["A3"]["total_tokens"], costs["A0"]["total_tokens"])
    time_ratio = ratio(costs["A3"]["seconds"], costs["A0"]["seconds"])

    def at_least(value: float | None, floor: float) -> bool:
        return value is not None and value >= floor

    gates = {
        "coverage": all(pair["cells"]["missing"] == 0 for pair in pairs.values())
        and all(arm["outputs"] == family_result["planned_outputs"] for arm in costs.values()),
        "gain_want": decided >= 8 and a3_a0["sign_test_p"] <= 0.05,
        "gain_useful_surprise": at_least(surprise, 0.35),
        "fit_non_inferior": at_least(a3_a0["rating_diff"]["fit"], -0.25)
        and at_least(a3_a0["worst_brief_median_fit"], -1.0),
        "craft_non_inferior": at_least(a3_a0["rating_diff"]["craft"], -0.25),
        "cost_ceiling": token_ratio is not None
        and token_ratio <= 2.0
        and time_ratio is not None
        and time_ratio <= 3.0,
        "conventional_trap": trap["cells"]["x"] >= trap["cells"]["y"]
        and at_least(trap["rating_diff"]["fit"], -0.25),
    }
    passes = all(gates.values())

    shares = None
    ceremony = False
    if gates["gain_want"] and gates["gain_useful_surprise"]:
        shares = {
            "want": ratio(a1_a0["cell_net"], a3_a0["cell_net"]),
            "useful_surprise": ratio(a1_a0["rating_diff"]["useful_surprise"], surprise),
        }
        ceremony = all(share is not None and share >= 0.8 for share in shares.values())
    head_to_head_lost = a3_a1["briefs"]["x"] <= a3_a1["briefs"]["y"]
    overlap_a3 = conv["A3"]["mechanism_overlap"]
    overlap_a0 = conv["A0"]["mechanism_overlap"]
    verdicts = {
        "transfers": passes,
        "blinding_broken": probe["p_value"] is not None and probe["p_value"] <= 0.05,
        "mostly_ceremony": passes and (ceremony or head_to_head_lost),
        "house_style": passes
        and not (ceremony or head_to_head_lost)
        and overlap_a3 is not None
        and overlap_a0 is not None
        and overlap_a3 >= overlap_a0,
        "proof_section_carries_weight": a3_a2["briefs"]["x"] > a3_a2["briefs"]["y"],
    }
    if human is not None:
        verdicts["owner_anchor_holds"] = human["decided"] >= 6 and human["a3_share"] > 0.5
    return {
        "gates": gates,
        "a1_share_of_a3_gain": shares,
        "token_ratio_A3_over_A0": token_ratio,
        "time_ratio_A3_over_A0": time_ratio,
        "visible_length_ratio_A3_over_A0": ratio(
            costs["A3"]["chars"], costs["A0"]["chars"]
        ),
        "verdicts": verdicts,
    }


def human_pairs(exp: Experiment) -> list[dict[str, Any]]:
    pairs = []
    for brief in exp.briefs:
        for family in FAMILIES:
            pair = exp.pair_id(brief["id"], family, 1, "A3", "A0")
            order = stable_int("human", pair) & 1
            left, right = ("A3", "A0") if order == 0 else ("A0", "A3")
            pairs.append(
                {
                    "pair_id": pair, "brief_id": brief["id"], "family": family,
                    "left": left, "right": right,
                }  # fmt: skip
            )
    pairs.sort(key=lambda pair: stable_int("human-order", pair["pair_id"]))
    return pairs


def score_human(exp: Experiment, votes_path: Path) -> dict[str, dict[str, Any]]:
    votes = json.loads(votes_path.read_text(encoding="utf-8"))
    result = {}
    for family in FAMILIES:
        counts: Counter[str] = Counter()
        agree = total = 0
        for pair in human_pairs(exp):
            choice = votes.get(pair["pair_id"])
            if pair["family"] != family or choice not in ("left", "right", "tie"):
                continue
            winner = pair.get(choice, "tie")
            counts[winner] += 1
            ai = [exp.votes.get(pair["pair_id"], order) for order in (0, 1)]
            if None not in ai:
                total += 1
                agree += pair_outcome(ai) == winner  # type: ignore[arg-type]
        decided = counts["A3"] + counts["A0"]
        result[family] = {
            "judged": sum(counts.values()),
            "decided": decided,
            "A3": counts["A3"], "A0": counts["A0"], "tie": counts["tie"],
            "a3_share": round(counts["A3"] / decided, 3) if decided else 0.0,
            "agreement_with_ai_pair_outcome": ratio(agree, total),
        }  # fmt: skip
    return result


def score(exp: Experiment, probe_runs: int, human_votes: Path | None) -> dict[str, Any]:
    all_briefs = [brief["id"] for brief in exp.briefs]
    traps = [brief["id"] for brief in exp.briefs if brief.get("trap")]
    human = score_human(exp, human_votes) if human_votes else None
    summary: dict[str, Any] = {
        "experiment": "A",
        "seed": SEED,
        "runs": exp.runs,
        "briefs": len(exp.briefs),
        "trap_briefs": traps,
        "models": FAMILIES,
        "hashes": {
            "briefs": file_hash(exp.briefs_path),
            "engine_skill": file_hash(ENGINE_SKILL),
            "preregistration": file_hash(EVALS / "PREREGISTRATION.md"),
            **{path.name: file_hash(path) for path in sorted(PROMPTS.glob("*.md"))},
        },
        "families": {},
    }
    for family in FAMILIES:
        probes = [row for row in exp.probes.values() if row["family"] == family]
        correct = sum(row["correct"] for row in probes)
        result: dict[str, Any] = {
            "generator": FAMILIES[family]["generator"],
            "judge": FAMILIES[OTHER[family]]["judge"],
            "planned_outputs": len(exp.briefs) * exp.runs,
            "pairs": {
                f"{x} vs {y}": score_pair(exp, family, x, y, all_briefs)
                for x, y in PAIRS
            },
            "trap_A3_vs_A0": score_pair(exp, family, "A3", "A0", traps),
            "costs": arm_costs(exp, family),
            "convergence": convergence(exp, family),
            "probe": {
                "planned": len(exp.briefs) * min(probe_runs, exp.runs),
                "judged": len(probes),
                "correct": correct,
                "accuracy": ratio(correct, len(probes)),
                "p_value": sign_test(correct, len(probes) - correct) if probes else None,
            },
        }
        if human is not None:
            result["owner"] = human[family]
        result["decision"] = decide(result, human[family] if human else None)
        summary["families"][family] = result
    return summary


def portfolio_shape(exp: Experiment, family: str) -> dict[str, dict[str, Any]]:
    """Ideas per portfolio, and how much of an arm's mechanism set the first arm
    (the plain prompt) had already produced."""
    ideas: dict[str, list[float]] = defaultdict(list)
    contained: dict[str, list[float]] = defaultdict(list)
    baseline = ARMS[0]
    for brief in exp.briefs:
        coding = exp.codings.get(brief["id"], family)
        if coding is None:
            continue
        labels = exp.labels(brief["id"], family)
        union: dict[str, set[str]] = defaultdict(set)
        for label, ids in coding["portfolios"].items():
            arm = labels[label][0]
            ideas[arm].append(len(ids))
            union[arm] |= set(ids)
        for arm in ARMS:
            if union[arm]:
                contained[arm].append(len(union[arm] & union[baseline]) / len(union[arm]))
    return {
        arm: {
            "ideas_per_portfolio": mean(ideas[arm]),
            f"share_also_in_{baseline}": mean(contained[arm]),
        }
        for arm in ARMS
    }


def decide_replacement(result: dict[str, Any], planned: int) -> dict[str, bool]:
    """Gates for replacing the shipped runtime (`old`) with a candidate (`new`)."""
    new, old, plain = DECISION["new"], DECISION["old"], DECISION["plain"]
    versus_old = result["pairs"][f"{new} vs {old}"]
    versus_plain = result["pairs"][f"{new} vs {plain}"]
    trap = result["trap_pairs"][f"{new} vs {old}"]
    diff, costs, conv = versus_old["rating_diff"], result["costs"], result["convergence"]

    def at_least(value: float | None, floor: float) -> bool:
        return value is not None and value >= floor

    overlap_new = conv[new]["mechanism_overlap"]
    overlap_old = conv[old]["mechanism_overlap"]
    tokens = ratio(costs[new]["total_tokens"], costs[old]["total_tokens"])
    return {
        "coverage": all(pair["cells"]["missing"] == 0 for pair in result["pairs"].values())
        and all(arm["outputs"] == planned for arm in costs.values()),
        "preference_not_worse": versus_old["briefs"]["x"] >= versus_old["briefs"]["y"],
        "fit_non_inferior": at_least(diff["fit"], -0.25),
        "craft_non_inferior": at_least(diff["craft"], -0.25),
        "conventional_trap": trap["cells"]["x"] >= trap["cells"]["y"]
        and at_least(trap["rating_diff"]["fit"], -0.25),
        "beats_plain": versus_plain["briefs"]["x"] > versus_plain["briefs"]["y"],
        "cost": tokens is not None and tokens <= 1.10,
        "breadth": at_least(result["shape"][new]["ideas_per_portfolio"], 4.2),
        "improves": (
            overlap_new is not None
            and overlap_old is not None
            and overlap_new <= overlap_old - 0.05
        )
        or at_least(diff["set_diversity"], 0.25),
    }


def score_generic(exp: Experiment) -> dict[str, Any]:
    all_briefs = [brief["id"] for brief in exp.briefs]
    traps = [brief["id"] for brief in exp.briefs if brief.get("trap")]
    summary: dict[str, Any] = {
        "runs": exp.runs,
        "briefs": len(exp.briefs),
        "arms": ARM_DEFS,
        "runtime_hashes": {
            arm: file_hash(REPO / spec["skill"])
            for arm, spec in ARM_DEFS.items()
            if "skill" in spec
        },
        "families": {},
    }
    for family in FAMILIES:
        summary["families"][family] = {
            "generator": FAMILIES[family]["generator"],
            "judge": FAMILIES[OTHER[family]]["judge"],
            "pairs": {
                f"{x} vs {y}": score_pair(exp, family, x, y, all_briefs)
                for x, y in PAIRS
            },
            "trap_pairs": {
                f"{x} vs {y}": score_pair(exp, family, x, y, traps) for x, y in PAIRS
            },
            "costs": arm_costs(exp, family),
            "convergence": convergence(exp, family),
            "shape": portfolio_shape(exp, family),
        }
        if DECISION:
            summary["families"][family]["gates"] = decide_replacement(
                summary["families"][family], len(exp.briefs) * exp.runs
            )
    if DECISION:
        summary["replace"] = all(
            all(result["gates"].values()) for result in summary["families"].values()
        )
    return summary


def report_generic(summary: dict[str, Any]) -> str:
    lines = [f"# {summary['briefs']} briefs × {summary['runs']} runs"]
    for result in summary["families"].values():
        lines += [
            "",
            f"## Generator: {result['generator']} (judged by {result['judge']})",
            "",
            "| Pair | Cells W–L–T | Briefs W–L–T | fit | surprise | diversity | craft | trap cells W–L–T | trap fit |",
            "|---|---|---|---|---|---|---|---|---|",
        ]
        for name, pair in result["pairs"].items():
            cells, briefs, diff = pair["cells"], pair["briefs"], pair["rating_diff"]
            trap = result["trap_pairs"][name]
            lines.append(
                f"| {name} | {cells['x']}–{cells['y']}–{cells['tie']} | "
                f"{briefs['x']}–{briefs['y']}–{briefs['tie']} | "
                + " | ".join(f"{diff[m]:+.2f}" if diff[m] is not None else "–" for m in METRICS)
                + f" | {trap['cells']['x']}–{trap['cells']['y']}–{trap['cells']['tie']} | "
                f"{trap['rating_diff']['fit']} |"
            )
        lines += [
            "",
            "| Arm | tokens | seconds | chars | ideas | overlap | distinct | also in baseline |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for arm in ARMS:
            cost, conv = result["costs"][arm], result["convergence"][arm]
            shape = list(result["shape"][arm].values())
            lines.append(
                f"| {arm} | {cost['total_tokens']} | {cost['seconds']} | {cost['chars']} | "
                f"{shape[0]} | {conv['mechanism_overlap']} | "
                f"{conv['distinct_mechanism_ratio']} | {shape[1]} |"
            )
        if "gates" in result:
            lines += [
                "",
                "- Gates: "
                + ", ".join(f"{k}={'PASS' if v else 'FAIL'}" for k, v in result["gates"].items()),
            ]
    if "replace" in summary:
        lines += ["", f"**Replace the shipped runtime: {'YES' if summary['replace'] else 'NO'}**"]
    return "\n".join(lines) + "\n"


def report(summary: dict[str, Any]) -> str:
    lines = [
        f"# Experiment A — {summary['briefs']} briefs × {summary['runs']} runs",
        "",
        "Cells are brief × run; a cell is decided only when both left/right "
        "orders agree. Brief-level counts take the majority across runs.",
    ]
    for family, result in summary["families"].items():
        decision = result["decision"]
        lines += [
            "",
            f"## Generator: {result['generator']} (judged by {result['judge']})",
            "",
            "| Pair | Cells W–L–T | Briefs W–L–T | Sign p | fit | surprise | diversity | craft |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for name, pair in result["pairs"].items():
            cells, briefs, diff = pair["cells"], pair["briefs"], pair["rating_diff"]
            lines.append(
                f"| {name} | {cells['x']}–{cells['y']}–{cells['tie']} | "
                f"{briefs['x']}–{briefs['y']}–{briefs['tie']} | {pair['sign_test_p']} | "
                + " | ".join(f"{diff[m]:+.2f}" if diff[m] is not None else "–" for m in METRICS)
                + " |"
            )
        lines += [
            "",
            "| Arm | tokens | seconds | chars | mechanism overlap | distinct ratio | lexical sim |",
            "|---|---|---|---|---|---|---|",
        ]
        for arm in ARMS:
            cost, conv = result["costs"][arm], result["convergence"][arm]
            lines.append(
                f"| {arm} | {cost['total_tokens']} | {cost['seconds']} | {cost['chars']} | "
                f"{conv['mechanism_overlap']} | {conv['distinct_mechanism_ratio']} | "
                f"{conv['lexical_similarity']} |"
            )
        probe = result["probe"]
        lines += [
            "",
            f"- Blinding probe: {probe['correct']}/{probe['judged']} correct "
            f"(p = {probe['p_value']}).",
            f"- A1 share of A3 gain: {decision['a1_share_of_a3_gain']}.",
            f"- Token ratio A3/A0: {decision['token_ratio_A3_over_A0']}; visible length "
            f"ratio: {decision['visible_length_ratio_A3_over_A0']}.",
            "- Gates: "
            + ", ".join(f"{k}={'PASS' if v else 'FAIL'}" for k, v in decision["gates"].items()),
            "- Verdicts: "
            + ", ".join(f"{k}={v}" for k, v in decision["verdicts"].items()),
        ]
        if "owner" in result:
            lines.append(f"- Owner anchor: {result['owner']}")
    return "\n".join(lines) + "\n"


# -------------------------------------------------------- human sanity packet


PACKET_PAGE = """<!doctype html><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Octo blind pairs</title>
<style>
body{font:16px/1.55 system-ui,sans-serif;margin:0;background:#f6f7f9;color:#14181f}
main{max-width:1200px;margin:auto;padding:16px}
.brief{background:#fff;border:1px solid #d8dce3;border-radius:10px;padding:14px;white-space:pre-wrap}
.sides{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:12px 0}
.side{background:#fff;border:1px solid #d8dce3;border-radius:10px;padding:14px;white-space:pre-wrap;overflow-wrap:anywhere}
button{font:inherit;padding:10px 16px;border-radius:8px;border:1px solid #9aa3b2;background:#fff;cursor:pointer}
button.on{background:#1f3a8a;color:#fff;border-color:#1f3a8a}
nav{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:12px 0}
@media(max-width:800px){.sides{grid-template-columns:1fr}}
</style><main>
<h1>Which portfolio would you rather keep developing?</h1>
<p id="where"></p><div class="brief" id="brief"></div>
<div class="sides"><div class="side" id="left"></div><div class="side" id="right"></div></div>
<nav><button data-v="left">Left</button><button data-v="tie">Tie</button>
<button data-v="right">Right</button><span style="flex:1"></span>
<button id="prev">◀ Prev</button><button id="next">Next ▶</button>
<button id="save">Download votes.json</button></nav></main>
<script>
const PAIRS=__PAIRS__;let votes={},i=0;
try{votes=JSON.parse(localStorage.getItem("octo-votes")||"{}")}catch(e){}
function show(){const p=PAIRS[i];
 where.textContent=`Pair ${i+1} of ${PAIRS.length} — ${Object.keys(votes).length} answered`;
 brief.textContent=p.brief;left.textContent=p.left;right.textContent=p.right;
 document.querySelectorAll("button[data-v]").forEach(b=>b.classList.toggle("on",votes[p.id]===b.dataset.v));}
document.querySelectorAll("button[data-v]").forEach(b=>b.onclick=()=>{votes[PAIRS[i].id]=b.dataset.v;
 try{localStorage.setItem("octo-votes",JSON.stringify(votes))}catch(e){}
 if(i<PAIRS.length-1)i++;show();scrollTo(0,0)});
prev.onclick=()=>{if(i>0)i--;show()};next.onclick=()=>{if(i<PAIRS.length-1)i++;show()};
save.onclick=()=>{const a=document.createElement("a");
 a.href=URL.createObjectURL(new Blob([JSON.stringify(votes,null,2)],{type:"application/json"}));
 a.download="votes.json";a.click()};show();
</script>
"""


def human_packet(exp: Experiment) -> Path:
    pairs = [
        {
            "id": pair["pair_id"],
            "brief": exp.brief[pair["brief_id"]]["prompt"],
            "left": exp.text(pair["brief_id"], pair["family"], pair["left"], 1),
            "right": exp.text(pair["brief_id"], pair["family"], pair["right"], 1),
        }
        for pair in human_pairs(exp)
    ]
    payload = json.dumps(pairs, ensure_ascii=False).replace("</", "<\\/")
    path = exp.dir / "human-packet.html"
    path.write_text(PACKET_PAGE.replace("__PAIRS__", payload), encoding="utf-8")
    return path


# ------------------------------------------------------- router regression


GRADE_SCHEMA = {
    "type": "object",
    "properties": {
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "pass": {"type": "boolean"},
                    "evidence": {"type": "string"},
                },
                "required": ["id", "pass", "evidence"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["results"],
    "additionalProperties": False,
}


def transcript(turns: list[dict[str, str]]) -> str:
    return "\n\n".join(f"[{turn['role']}]\n{turn['content']}" for turn in turns)


def router_prompt(case: dict[str, Any]) -> str:
    files = "\n\n".join(
        f'<file path="{path}">\n{(REPO / path).read_text(encoding="utf-8").strip()}\n</file>'
        for path in ROUTER_FILES
    )
    template = (PROMPTS / "router.md").read_text(encoding="utf-8")
    return template.replace("{{FILES}}", files).replace(
        "{{CONVERSATION}}", transcript(case["turns"])
    )


def router(name: str, cases_path: Path, runs: int, workers: int) -> int:
    cases = {case["id"]: case for case in read_jsonl(cases_path)}
    out_dir = EVALS / "runs" / name
    replies = Store(out_dir / "router-replies.jsonl", ("case_id", "family", "run"))
    grades = Store(out_dir / "router-grades.jsonl", ("case_id", "family", "run"))
    grader = (PROMPTS / "router-grader.md").read_text(encoding="utf-8").strip()
    jobs = [
        (case_id, family, run)
        for case_id in cases
        for family in FAMILIES
        for run in range(1, runs + 1)
        if not grades.has(case_id, family, run)
    ]

    def worker(job: tuple[str, str, int]) -> None:
        case_id, family, run = job
        case = cases[case_id]
        reply = replies.get(case_id, family, run)
        if reply is None:
            generated = call_model(family, "generator", router_prompt(case))
            reply = {
                "case_id": case_id, "family": family, "run": run,
                "text": generated["text"], "model": generated["model"],
            }  # fmt: skip
            replies.add(reply)
        criteria = "\n".join(f"- {c['id']}: {c['text']}" for c in case["criteria"])
        wanted = {criterion["id"] for criterion in case["criteria"]}

        def check(parsed: dict[str, Any]) -> None:
            if {row["id"] for row in parsed["results"]} != wanted:
                raise ValueError("grader did not answer every criterion")

        prompt = (
            f"{grader}\n\nCONVERSATION SO FAR:\n{transcript(case['turns'])}"
            f"\n\nASSISTANT REPLY TO GRADE:\n{reply['text']}\n\nCRITERIA:\n{criteria}"
        )
        graded = call_model(
            OTHER[family], "judge", prompt, schema=GRADE_SCHEMA, check=check
        )
        results = graded["json"]["results"]
        grades.add(
            {
                "case_id": case_id, "family": family, "run": run,
                "passed": all(row["pass"] for row in results), "results": results,
            }  # fmt: skip
        )

    failed_calls = run_jobs("router", jobs, worker, lambda job: job[1], workers)
    rows = sorted(grades.values(), key=lambda r: (r["case_id"], r["family"], r["run"]))
    lines = ["| Case | Generator | Run | Result | Failed criteria |", "|---|---|---|---|---|"]
    for row in rows:
        failed = [r["id"] for r in row["results"] if not r["pass"]]
        lines.append(
            f"| {row['case_id']} | {FAMILIES[row['family']]['generator']} | {row['run']} | "
            f"{'PASS' if row['passed'] else 'FAIL'} | {', '.join(failed) or '–'} |"
        )
    passed = sum(row["passed"] for row in rows)
    lines.append(f"\n{passed}/{len(rows)} passed; {failed_calls} call(s) failed.")
    (out_dir / "ROUTER.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 1 if failed_calls or passed < len(rows) else 0


# ---------------------------------------------------------------------- CLI


def command_run(args: argparse.Namespace) -> int:
    if args.spec:
        load_spec(args.spec)
    exp = Experiment(args.name, args.briefs, args.runs, args.workers)
    if args.claude_workers:
        LIMITS["claude"] = args.claude_workers
    stages = [stage.strip() for stage in args.stages.split(",") if stage.strip()]
    actions: dict[str, Callable[[], int]] = {
        "generate": exp.generate,
        "judge": exp.judge,
        "probe": lambda: exp.probe(args.probe_runs),
        "converge": exp.converge,
    }
    for stage in stages:
        if stage == "score":
            continue
        failures = actions[stage]()
        if failures or BREAKER.tripped.is_set():
            print(f"[{stage}] {failures} call(s) failed — re-run the same command to resume")
            return 3
    if "score" in stages:
        if args.spec:
            summary, render = score_generic(exp), report_generic
        else:
            summary, render = score(exp, args.probe_runs, args.human_votes), report
        (exp.dir / "summary.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        text = render(summary)
        (exp.dir / "REPORT.md").write_text(text, encoding="utf-8")
        print(text)
    return 0


def command_human(args: argparse.Namespace) -> int:
    exp = Experiment(args.name, args.briefs, args.runs, 1)
    print(human_packet(exp))
    return 0


def command_router(args: argparse.Namespace) -> int:
    return router(args.name, args.cases, args.runs, args.workers)


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)

    def experiment(name: str, handler: Callable[[argparse.Namespace], int]) -> Any:
        sub = commands.add_parser(name)
        sub.add_argument("--name", required=True, help="folder under evals/runs/")
        sub.add_argument("--briefs", type=Path, default=EVALS / "briefs.experiment-a.jsonl")
        sub.add_argument("--runs", type=int, default=5)
        sub.set_defaults(handler=handler)
        return sub

    run = experiment("run", command_run)
    run.add_argument("--stages", default="generate,judge,probe,converge,score")
    run.add_argument("--workers", type=int, default=3, help="concurrent calls per provider")
    run.add_argument("--probe-runs", type=int, default=2)
    run.add_argument("--claude-workers", type=int, help="lower cap for Claude calls")
    run.add_argument("--human-votes", type=Path)
    run.add_argument("--spec", type=Path, help="arms and pairs for another experiment")
    experiment("human-packet", command_human)

    regression = commands.add_parser("router")
    regression.add_argument("--name", required=True)
    regression.add_argument("--cases", type=Path, default=EVALS / "router" / "cases.jsonl")
    regression.add_argument("--runs", type=int, default=1)
    regression.add_argument("--workers", type=int, default=3)
    regression.set_defaults(handler=command_router)
    return root


def main() -> int:
    args = parser().parse_args()
    return args.handler(args)


if __name__ == "__main__":
    sys.exit(main())
