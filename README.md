<div align="center">

<img src="assets/brand/imagination-octo-logo.png" alt="IMAGINATION OCTO — Reach wide, choose one" width="380" />

# IMAGINATION OCTO

**REACH WIDE · CHOOSE ONE**

### A human-in-the-loop creative plugin for Claude Code and Codex —<br/>distinct ideas first, your choice second, a pressure-tested concept third

[English](README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português (Brasil)](README.pt-BR.md)

[![Tests](https://img.shields.io/github/actions/workflow/status/djfksjd/imagination-octo/tests.yml?style=flat-square&label=tests)](https://github.com/djfksjd/imagination-octo/actions/workflows/tests.yml)
[![License](https://img.shields.io/badge/license-MIT-1f2937?style=flat-square)](LICENSE)
![Stage](https://img.shields.io/badge/stage-v0.2%20beta-d69526?style=flat-square)
![Skills](https://img.shields.io/badge/skills-3-6d5ef5?style=flat-square)
![Hosts](https://img.shields.io/badge/hosts-Claude%20Code%20%C2%B7%20Codex-0ea5b7?style=flat-square)

</div>

Imagination Octo reaches in several directions at once and then stops. It returns a small portfolio of ideas that differ in mechanism, not in wording, and ends the turn. Only after you pick one does it pressure-test and develop that direction. The decision is the one part it refuses to automate.

**This is `v0.2 beta`.** The measurements below come from one model (`gpt-5.4`) judged by AI calls from the same model family on a small set of briefs. It has not been measured on Claude, and it is not a claim of universal creativity.

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
- **Not measured:** whether separate runs converge on the same ideas, and the full two-turn flow as one product.

Protocols, decision rules and result files: [Imagination Engine](https://github.com/djfksjd/imagination-engine-skill) · [Imagination Brainstorming](https://github.com/djfksjd/imagination-brainstorming-skill).

## When to use it, and when not

**Use it** when you want options that actually differ: concepts, premises, mechanics, products, services, worlds, rituals, or when earlier ideas felt generic.

**Use a plain prompt** for factual questions, routine implementation, naming only, or anything where the conventional answer is the right one.

## Renamed from `imagination`

This plugin and its router skill were called `imagination` up to v0.1.3. GitHub redirects the old repository URL, but the plugin name and the router command changed: remove the old `imagination` plugin, install `imagination-octo`, and call `$imagination-octo`. The two specialist skills keep their names.

## Manual install

```bash
# Claude Code
claude plugin marketplace add djfksjd/imagination-octo
claude plugin install imagination-octo@djfksjd

# Codex
codex plugin marketplace add djfksjd/imagination-octo
codex plugin add imagination-octo@djfksjd
```

## Development

The specialist runtimes are maintained and evaluated in their own repositories. Before a release, synchronize their `SKILL.md` files, validate all three skills, run the repository tests, and forward-test the two-turn boundary.

```bash
python3 -m pytest tests/ -q
bash -n install.sh
```

## License

[MIT](LICENSE).
