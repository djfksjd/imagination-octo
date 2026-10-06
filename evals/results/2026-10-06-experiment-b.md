# Experiment B — 12 briefs × 4 runs (2026-10-06)

**Result: the candidate (v0.6.0-rc2) does not replace v0.5.3.** It failed two
of nine gates on GPT and three on Claude. Preregistered on commit `1142752`;
288 generations, 384 judgments, 24 codings, no missing rows.

`NEW` is the candidate, `OLD` is v0.5.3, `A0` is the plain prompt.

What the candidate did and did not do:

- It restored breadth on Claude (3.98 to 4.63 ideas per portfolio) and raised
  set diversity there (+0.24), but craft fell (−0.32) and it lost more briefs
  than it won against v0.5.3 (4–6–2).
- On GPT it was indistinguishable from v0.5.3 in preference (5–5–2) and its
  across-run overlap was higher, not lower (0.45 vs 0.38).
- The modal-map rule did not move the runtime out of the plain prompt's
  mechanism set: the share also produced by the plain prompt stayed at 54–57%.
- v0.5.3's narrower portfolios on Claude replicated on fresh briefs (3.98 ideas
  vs 4.35 for the plain prompt).

Not part of the rule: against the plain prompt the candidate won 11–0–1 on GPT
and 8–2–2 on Claude. That comparison inherits the blinding problem found in
Experiment A and is not a claim.

These briefs are now retired.

## Generator: gpt-5.5 (judged by claude-opus-5-5)

| Pair | Cells W–L–T | Briefs W–L–T | fit | surprise | diversity | craft | trap cells W–L–T | trap fit |
|---|---|---|---|---|---|---|---|---|
| NEW vs OLD | 21–18–9 | 5–5–2 | +0.01 | -0.01 | +0.07 | +0.09 | 2–3–3 | 0.0 |
| NEW vs A0 | 33–6–9 | 11–0–1 | +0.12 | +1.09 | +0.59 | +0.46 | 5–1–2 | 0.0 |

| Arm | tokens | seconds | chars | ideas | overlap | distinct | also in baseline |
|---|---|---|---|---|---|---|---|
| A0 | 19448.1042 | 18.3063 | 2432.2708 | 5.0 | 0.4479 | 0.5817 | 1.0 |
| OLD | 20984.1667 | 20.4713 | 2854.5833 | 5.0 | 0.3833 | 0.6164 | 0.5441 |
| NEW | 20883.5625 | 20.1804 | 2873.5 | 5.0 | 0.4488 | 0.5703 | 0.5699 |

- Gates: coverage=PASS, preference_not_worse=PASS, fit_non_inferior=PASS, craft_non_inferior=PASS, conventional_trap=FAIL, beats_plain=PASS, cost=PASS, breadth=PASS, improves=FAIL

## Generator: claude-opus-5-5 (judged by gpt-5.5)

| Pair | Cells W–L–T | Briefs W–L–T | fit | surprise | diversity | craft | trap cells W–L–T | trap fit |
|---|---|---|---|---|---|---|---|---|
| NEW vs OLD | 16–20–12 | 4–6–2 | -0.15 | -0.18 | +0.24 | -0.32 | 3–0–5 | 0.0 |
| NEW vs A0 | 27–9–12 | 8–2–2 | +0.07 | +0.80 | +0.43 | +0.26 | 5–1–2 | 0.125 |

| Arm | tokens | seconds | chars | ideas | overlap | distinct | also in baseline |
|---|---|---|---|---|---|---|---|
| A0 | 3648.7708 | 35.0215 | 2738.0417 | 4.3542 | 0.6944 | 0.4312 | 1.0 |
| OLD | 7385.5 | 56.0304 | 2996.3542 | 3.9792 | 0.5428 | 0.5231 | 0.5657 |
| NEW | 7530.5 | 58.5548 | 3037.7292 | 4.625 | 0.5264 | 0.5323 | 0.5429 |

- Gates: coverage=PASS, preference_not_worse=FAIL, fit_non_inferior=PASS, craft_non_inferior=FAIL, conventional_trap=PASS, beats_plain=PASS, cost=PASS, breadth=PASS, improves=FAIL

**Replace the shipped runtime: NO**
