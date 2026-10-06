<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/brand/imagination-octo-logo-dark.png" />
  <img src="assets/brand/imagination-octo-logo.png" alt="IMAGINATION OCTO — Reach wide, choose one" width="380" />
</picture>

# IMAGINATION OCTO

**REACH WIDE · CHOOSE ONE**

### A human-in-the-loop creative plugin for Claude Code and Codex —<br/>distinct ideas first, your choice second, a pressure-tested concept third

[English](README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português (Brasil)](README.pt-BR.md)

[![Tests](https://img.shields.io/github/actions/workflow/status/djfksjd/imagination-octo/tests.yml?style=flat-square&label=tests)](https://github.com/djfksjd/imagination-octo/actions/workflows/tests.yml)
[![License](https://img.shields.io/badge/license-MIT-1f2937?style=flat-square)](LICENSE)
![Stage](https://img.shields.io/badge/stage-v0.3%20beta-d69526?style=flat-square)
![Skills](https://img.shields.io/badge/skills-3-6d5ef5?style=flat-square)
![Hosts](https://img.shields.io/badge/hosts-Claude%20Code%20%C2%B7%20Codex-0ea5b7?style=flat-square)

</div>

Imagination Octo reaches in several directions at once and then stops. It returns a small portfolio of ideas that differ in mechanism, not in wording, and ends the turn. Only after you pick one does it pressure-test and develop that direction. The decision is the one part it refuses to automate.

**This is `v0.3 beta`.** The table below comes from one model (`gpt-5.4`) judged by AI calls from the same family on a small set of briefs. A later cross-model run on GPT and Claude exists, but its preference result is void until it is re-judged; see *Read these honestly*. None of this is a claim of universal creativity.

## What it does

| | |
|---|---|
| **Divergent portfolio** | 3–5 directions built from three separate passes: direct, mechanism transfer, and premise shift. Variants that differ only in name or theme are culled. |
| **Fit is a veto** | An idea that weakens a non-negotiable is dropped, however surprising it is. A renamed violation still counts as a violation. |
| **You choose** | The router never picks and develops in the same turn. Automatic chaining lowered constraint fit in testing, so the pause is enforced. |
| **Pressure test** | The chosen idea faces its load-bearing assumption, its simpler conventional competitor, and the failure its own mechanism causes. |
| **Honest failure** | If the conventional answer is better, or the direction does not survive, it says so and sends you back to diverge. |
| **Small runtime** | Three plain skill files. No decks, ban lists, gates, or scripts at run time; about 1.1× the tokens of a plain prompt in testing. |

## How it works

```text
 your brief ──► ┌─────────── diverge · imagination-engine ───────────┐
                │  direct pass · mechanism transfer · premise shift  │
                │    cull by failure · private proof per survivor    │
                └──────────────────────────┬─────────────────────────┘
                                           ▼
                               3–5 distinct directions
                                           ▼
                                    ◆ YOU CHOOSE ◆        the turn always ends here
                                           ▼
                ┌─────── develop · imagination-brainstorming ────────┐
                │ load-bearing assumption · conventional competitor  │
                │   native failure mode · boring half · falsifier    │
                └──────────────────────────┬─────────────────────────┘
                                           ▼
                             decision-ready concept memo
```

- The pause between the two halves is part of the method, not a UI detail.
- Search and proof stay private. You get the ideas, not a report that a pipeline ran.
- Nothing is implemented. The output is a concept you can take to planning.

## Quick start

```bash
curl -fsSL https://raw.githubusercontent.com/djfksjd/imagination-octo/main/install.sh | bash
```

Run the same command again to update. If it reports older standalone copies of these skills, end the command with `| bash -s -- --clean-legacy` to move them aside; nothing is deleted.

Then ask:

```text
Use $imagination-octo to invent several negotiation mechanics for a narrative game
without dialogue trees, hidden dice, or a persuasion stat.
```

The first response ends with a choice. Reply with a number or a direction:

```text
Develop option 2.
```

## One plugin, three skills

| Skill | Best for | Returns |
|---|---|---|
| `$imagination-octo` | Most requests | Portfolio → your choice → developed concept |
| `$imagination-engine` | Divergence only | 3–5 useful, non-obvious directions |
| `$imagination-brainstorming` | An idea you already chose | A decision-ready concept memo |

## Measured (2026-07-30)

Preregistered blind comparisons against a strong plain prompt. 10 fresh English and Korean briefs, 5 runs per condition, 5 judges.

| Runtime | Preferred to continue | Largest gains (1–7 scale) | Tokens |
|---|---|---|---|
| Engine v0.5.3 | **50–0 (100.0%)** | useful surprise `+0.97` · diversity `+0.66` · fit `+0.60` | 1.12× |
| Concept Workshop v0.4.2 | **45–5 (90.0%)** | actionability `+1.37` · fit `+0.95` · robustness `+0.82` | 1.14× |

Read these honestly:

- **Only `gpt-5.4` generated and judged.** No Claude runs and no human judges yet. Judges from the same model family may share its taste.
- **Ten briefs is a small distribution.** 95% Wilson intervals: Engine 92.9–100.0%, Workshop 78.6–95.7%.
- **It can lose.** One Workshop brief went unanimously to the plain prompt, and an earlier Engine build lost a drama brief the same way.
- **An earlier design failed outright.** The deck-and-gate pipeline (Engine v0.4.0) lost 0–30 to a plain prompt at 48× the cost and was replaced. That record is kept in the Engine repository.
- **Experiment A (2026-10-06): preference result void for now.** A preregistered cross-model run ([rule](evals/PREREGISTRATION.md), [result](evals/results/2026-10-06-experiment-a.md)) on 12 fresh briefs with `gpt-5.5` and `claude-opus-5-5`, each judged by the other family. The engine was preferred to the plain prompt on 11 of 12 briefs with GPT and 10 of 12 with Claude, and an effort-matched plain prompt did not close the gap. But judges could tell which side used the skill in 22 of 24 probes on each model, so under the rule fixed in advance these preference numbers do not count until the outputs are format-normalized and re-judged. The owner's blind check is also still open. Not affected by that: separate runs repeated the same mechanisms less with the engine (overlap 0.40 vs 0.54 on GPT, 0.50 vs 0.63 on Claude), at 1.08× the tokens on GPT and 1.99× on Claude.
- **A candidate v0.6.0 failed (2026-10-06).** It tried to widen portfolios and cut repetition. On 12 fresh briefs it did not beat v0.5.3 (5–5–2 with GPT, 4–6–2 with Claude) and missed preregistered gates on both, so v0.5.3 stays ([result](evals/results/2026-10-06-experiment-b.md)).
- **Two-turn flow:** checked for behaviour only. A regression suite passed 13 of 14 cases; the failure, a guessed pick when the reply fit two directions, led to a router fix. There is no preference study of the whole flow.

Protocols, decision rules and result files: [Imagination Engine](https://github.com/djfksjd/imagination-engine-skill) · [Imagination Brainstorming](https://github.com/djfksjd/imagination-brainstorming-skill).

## When to use it, and when not

**Use it** when you want options that actually differ: concepts, premises, mechanics, products, services, worlds, rituals, or when earlier ideas felt generic.

**Use a plain prompt** for factual questions, routine implementation, naming only, or anything where the conventional answer is the right one.

## Choice log (opt-in)

Off by default. Once you turn it on, each time you pick a direction or reject a portfolio one line is appended to `~/.imagination-octo/choices.jsonl` on your machine: the directions shown, your pick, and any reason you gave. Briefs are stored as hashes unless you ask for the text. Nothing is uploaded and the skills never read the log; it is there so you can study your own choices. `enable --hosts` adds one marked line to your global `CLAUDE.md` / `AGENTS.md` so the skill can see the opt-in, and `disable` removes it.

```bash
LOG=https://raw.githubusercontent.com/djfksjd/imagination-octo/main/skills/imagination-octo/scripts/choice_log.py
curl -fsSL $LOG | python3 - enable --hosts claude,codex   # --with-brief keeps the brief text
curl -fsSL $LOG | python3 - stats
curl -fsSL $LOG | python3 - disable
```

## Renamed from `imagination`

This plugin and its router skill were called `imagination` up to v0.1.3. GitHub redirects the old repository URL, but the plugin name and the router command changed: remove the old `imagination` plugin, install `imagination-octo`, and call `$imagination-octo`. The two specialist skills keep their names. From v0.3 the marketplace id changed as well, from `djfksjd` to `imagination-octo`, because the old id collided with other plugins by the same author. The install target is now `imagination-octo@imagination-octo`.

## Manual install

```bash
# Claude Code
claude plugin marketplace add djfksjd/imagination-octo
claude plugin install imagination-octo@imagination-octo

# Codex
codex plugin marketplace add djfksjd/imagination-octo
codex plugin add imagination-octo@imagination-octo
```

## Development

The specialist runtimes are maintained and evaluated in their own repositories. Before a release, synchronize their `SKILL.md` files, validate all three skills, run the repository tests, and forward-test the two-turn boundary.

```bash
python3 -m pytest tests/ -q
bash -n install.sh
```

## License

[MIT](LICENSE).
