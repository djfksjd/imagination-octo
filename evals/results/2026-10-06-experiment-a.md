# Experiment A — 12 briefs × 5 runs (2026-10-06)

**Status: the preference results below are void under the preregistered rule.**
On both generators the blinding probe identified the skill arm in 22 of 24
pairs (p = 0.00002). `PREREGISTRATION.md` fixes the consequence: nothing is
claimed from these preference numbers until the outputs are format-normalized
and re-judged. The owner's 24 blind pairs have not been judged yet either.

What does not depend on the voided judgments: mechanism overlap across runs
(coded without arm labels), token and time cost, and visible length.

Post-hoc notes, not part of the rule:

- All seven gates passed numerically on both generators, and the
  effort-matched control (A1) reached about 0% of the engine's gain on GPT and
  62–68% on Claude, below the 80% "ceremony" line.
- Most probe cues named content ("more varied, less stock mechanisms") rather
  than layout. The probe cannot separate "recognizable because better" from
  "recognizable because formatted differently", which is a weakness of the
  probe; the rule is applied as written anyway.
- A3 beat A2 (no proof section) on 5–3 and 6–3 briefs, neither significant.
- Preregistered on commit `2032540`. The first launch lost its Claude calls to
  a subscription limit; the run was resumed with harness-only changes
  (error reporting, concurrency), no prompt, brief, or scoring change.
- The generator was `gpt-5.5`, so this is not comparable with the earlier
  `gpt-5.4` confirmations.

Cells are brief × run; a cell is decided only when both left/right orders agree. Brief-level counts take the majority across runs.

## Generator: gpt-5.5 (judged by claude-opus-5-5)

| Pair | Cells W–L–T | Briefs W–L–T | Sign p | fit | surprise | diversity | craft |
|---|---|---|---|---|---|---|---|
| A1 vs A0 | 16–17–27 | 4–5–3 | 0.74609 | +0.01 | +0.01 | -0.12 | +0.07 |
| A3 vs A0 | 47–6–7 | 11–1–0 | 0.00317 | +0.21 | +1.04 | +0.47 | +0.38 |
| A3 vs A1 | 41–5–14 | 11–1–0 | 0.00317 | +0.16 | +0.89 | +0.48 | +0.24 |
| A3 vs A2 | 20–20–20 | 5–3–4 | 0.36328 | -0.03 | +0.02 | +0.06 | +0.03 |

| Arm | tokens | seconds | chars | mechanism overlap | distinct ratio | lexical sim |
|---|---|---|---|---|---|---|
| A0 | 19409.8667 | 18.9807 | 2550.6667 | 0.5406 | 0.4607 | 0.7319 |
| A1 | 19585.8667 | 21.2353 | 3017.9167 | 0.4786 | 0.5003 | 0.8028 |
| A2 | 20610.2333 | 20.9485 | 2915.4333 | 0.4235 | 0.5225 | 0.7997 |
| A3 | 20921.2167 | 21.0067 | 2913.7 | 0.3979 | 0.5509 | 0.7896 |

- Blinding probe: 22/24 correct (p = 2e-05).
- A1 share of A3 gain: {'want': -0.024, 'useful_surprise': 0.008}.
- Token ratio A3/A0: 1.078; visible length ratio: 1.142.
- Gates: coverage=PASS, gain_want=PASS, gain_useful_surprise=PASS, fit_non_inferior=PASS, craft_non_inferior=PASS, cost_ceiling=PASS, conventional_trap=PASS
- Verdicts: transfers=True, blinding_broken=True, mostly_ceremony=False, house_style=False, proof_section_carries_weight=True

## Generator: claude-opus-5-5 (judged by gpt-5.5)

| Pair | Cells W–L–T | Briefs W–L–T | Sign p | fit | surprise | diversity | craft |
|---|---|---|---|---|---|---|---|
| A1 vs A0 | 36–10–14 | 9–1–2 | 0.01074 | +0.28 | +0.44 | -0.03 | +0.18 |
| A3 vs A0 | 47–9–4 | 10–2–0 | 0.01929 | +0.61 | +0.71 | -0.23 | +0.75 |
| A3 vs A1 | 35–9–16 | 10–1–1 | 0.00586 | +0.37 | +0.32 | -0.29 | +0.54 |
| A3 vs A2 | 27–19–14 | 6–3–3 | 0.25391 | +0.12 | -0.13 | -0.19 | +0.19 |

| Arm | tokens | seconds | chars | mechanism overlap | distinct ratio | lexical sim |
|---|---|---|---|---|---|---|
| A0 | 3960.3333 | 37.9467 | 2917.4 | 0.6258 | 0.41 | 0.8338 |
| A1 | 4417.0 | 43.814 | 2881.0667 | 0.6064 | 0.4268 | 0.8308 |
| A2 | 6881.55 | 54.336 | 3035.2 | 0.5154 | 0.4858 | 0.8365 |
| A3 | 7870.6833 | 61.1507 | 3067.5 | 0.5011 | 0.5123 | 0.8297 |

- Blinding probe: 22/24 correct (p = 2e-05).
- A1 share of A3 gain: {'want': 0.684, 'useful_surprise': 0.624}.
- Token ratio A3/A0: 1.987; visible length ratio: 1.051.
- Gates: coverage=PASS, gain_want=PASS, gain_useful_surprise=PASS, fit_non_inferior=PASS, craft_non_inferior=PASS, cost_ceiling=PASS, conventional_trap=PASS
- Verdicts: transfers=True, blinding_broken=True, mostly_ceremony=False, house_style=False, proof_section_carries_weight=True
