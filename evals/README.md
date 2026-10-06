# Evaluations

Two suites live here. Both call the Codex CLI and Claude Code headless through
your own subscriptions, so nothing here runs in CI; `tests/test_evals.py`
covers the scoring logic with synthetic votes instead.

| Suite | Question | Kind |
|---|---|---|
| Router regression | Does the two-turn flow hold its boundary? | Behaviour, pass/fail |
| Experiment A | Is the engine better than asking plainly, on GPT and on Claude? | Blind preference, preregistered |

Models are fixed in `octo_eval.py`: `gpt-5.5` and `claude-opus-5-5` generate,
and every judgment is made by the other family.

## Router regression

```bash
python3 evals/octo_eval.py router --name router-v030 --runs 3
```

Each case in `router/cases.jsonl` is a conversation that ends on a user turn.
The model receives the three skill files and writes the next reply; a judge
from the other family checks it against the case's explicit criteria.

| Case | Checks |
|---|---|
| `diverge-stops` | 3–5 directions, a choice question, no winner, no development |
| `auto-chain-refused` | Asked to pick and finish in one go, it still waits |
| `explicit-choice-develops` | "The second one" develops that direction and keeps the constraints |
| `ambiguous-choice` | A reply that fits two directions gets a question, not a guess |
| `re-diverge` | A rejected set is replaced with different mechanisms |
| `switch-selection` | A new pick is developed without regenerating the portfolio |
| `conflict-surfaced` | A request that breaks the brief is flagged, not polished |

The conversations are replayed as text with tools unavailable, so this checks
the router's instructions, not a host's skill loader.

## Experiment A

The design, arms, and decision rule are frozen in
[`PREREGISTRATION.md`](PREREGISTRATION.md). Read it before reading a result.

```bash
# 480 generations, 960 judgments, 48 probes, 24 coding calls. Resumable:
# re-run the same command after an interruption or a rate limit.
python3 evals/octo_eval.py run --name experiment-a

# The owner's 24 blind pairs. Open the page, vote, download votes.json.
python3 evals/octo_eval.py human-packet --name experiment-a

# Re-score with the owner's votes included.
python3 evals/octo_eval.py run --name experiment-a --stages score \
  --human-votes votes.json
```

Outputs land in `evals/runs/<name>/`, which is ignored by git: raw outputs,
votes, probes, mechanism codings, `summary.json`, and `REPORT.md`. Commit only
a summary into `results/`, after checking it contains no private text.

`briefs.pilot.jsonl` holds two retired development briefs for checking that
the pipeline runs end to end. A pilot result is not evidence.

## Rules

- Freeze the preregistration, briefs, prompts, and runtime in one commit
  before generating confirmation outputs.
- A brief set whose outputs have been read is retired. Never tune on it; write
  fresh briefs for the next confirmation.
- Change a runtime only in response to a diagnosed loss, and say which one.
- Report a failed rule as a failure.
