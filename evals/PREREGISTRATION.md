# Experiment A — preregistration

Frozen before any confirmation output was generated. This file, the briefs,
the prompts, the engine runtime, and the harness are identified by the commit
that introduced them; `summary.json` records their hashes.

## Question

Does the divergence runtime (`imagination-engine` v0.5.3) give a better
portfolio than asking the same model plainly — on GPT **and** on Claude — and
is the gain produced by the method rather than by extra effort, by a visible
format, or by a house style?

Earlier confirmations used one generator (`gpt-5.4`) and judges from the same
family. They cannot answer this.

## Design

| | |
|---|---|
| Briefs | `briefs.experiment-a.jsonl`: 12 fresh briefs (7 English, 5 Korean), 3 narrative premises, 2 traps where a conventional answer is correct |
| Generators | `gpt-5.5` (Codex CLI, medium reasoning) and `claude-opus-5-5` (Claude Code headless, no tools) |
| Runs | 5 per brief × generator × arm = 480 generations |
| Judges | Cross-family only: Claude judges GPT outputs, GPT judges Claude outputs |
| Seed | `octo-experiment-a-2026-10` |

Arms:

- **A0** — `prompts/control.md`, the strong plain prompt used in earlier
  confirmations.
- **A1** — A0 plus two sentences asking the model to overgenerate privately
  and cull (`prompts/control-effort.md`). The effort-matched control.
- **A2** — the full runtime with its `## Prove each survivor` section removed.
- **A3** — the full runtime as shipped.

Measures, all from the same outputs:

1. **Blind preference.** Pairs A1–A0, A3–A0, A3–A1, A3–A2 are each judged
   twice, once per left/right order, with `prompts/judge.md`. A *cell* (brief ×
   run) is decided only when both orders agree; otherwise it is a tie. A brief
   is won by the arm with more decided cells across its five runs.
2. **Across-run convergence.** For each brief × generator, a cross-family coder
   assigns mechanism ids to all 20 portfolios at once, unlabelled and shuffled
   (`prompts/coding.md`). *Mechanism overlap* of an arm is the mean, over its
   ten run pairs, of shared ids ÷ the smaller portfolio. Character-trigram
   cosine similarity is reported as a lexical cross-check.
3. **Blinding probe.** On A3–A0 pairs of runs 1–2, a cross-family judge guesses
   which side followed a long instruction (`prompts/probe.md`).
4. **Format audit.** Visible length and structure per arm.
5. **Owner anchor.** The owner blind-judges the 24 run-1 A3–A0 pairs exported
   by `human-packet`.

## Decision rule

Evaluated separately for each generator. The gain **transfers** only when all
seven gates hold:

1. **Coverage.** Every planned output and vote exists. Missing rows fail.
2. **Preference.** A3 beats A0 at brief level with at least 8 decided briefs
   and a one-sided exact sign test of p ≤ 0.05.
3. **Useful surprise.** Pooled A3 − A0 is at least +0.35.
4. **Fit.** Pooled A3 − A0 is at least −0.25 and no brief has a median below
   −1.0.
5. **Craft.** Pooled A3 − A0 is at least −0.25.
6. **Cost.** A3 uses at most 2.0× the tokens and 3.0× the wall time of A0.
7. **Conventional traps.** On the trap briefs A3 does not lose more cells than
   it wins against A0, and its fit difference is at least −0.25.

Consequences, fixed in advance:

- **Blinding broken** — the probe is correct more often than chance at
  p ≤ 0.05. That generator's preference results are void as evidence until the
  outputs are format-normalized and re-judged. Nothing else is claimed from
  them.
- **No transfer on Claude** — the READMEs state that no benefit has been shown
  on Claude, and implicit invocation stays disabled there.
- **Mostly ceremony** — the gain transfers, but A1 reaches at least 80% of
  A3's gain over A0 on both preference (net decided cells) and useful
  surprise, or A3 fails to beat A1 head to head at brief level. The runtime is
  replaced by a roughly 1 KB skill and the rest is deleted.
- **House style** — the gain transfers, it is not ceremony, and A3's mechanism
  overlap across runs is at least A0's. The next intervention targets
  convergence (Experiment B: fresh-context passes, capped at 3× tokens, fit
  non-inferior).
- **Proof section** — if A3 does not beat A2 at brief level, the section is a
  candidate for removal. Informative only.
- **Owner anchor** — if the owner decides fewer than 6 pairs for a generator
  or prefers A3 in half or fewer of them, no public claim is strengthened for
  that generator, whatever the AI judges said.

"Underpowered", "almost passed", or a favourable number outside this list is
not a pass.

## Known limits, stated before the run

- Twelve briefs is a small sample; brief-level tests are deliberately strict.
- The briefs were written by a Claude model, one of the two generator families.
- The Codex CLI adds its own agent instructions to every call and the Claude
  calls use a one-line system prompt, so absolute token counts are not
  comparable across generators. Ratios within a generator are.
- A2 removes one section; it does not isolate every component.
- The lexical cross-check is not an embedding distance.
- AI judges may reward novelty that is legible to models rather than useful to
  people. The owner anchor is the only human signal here.
