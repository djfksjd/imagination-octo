# Experiment C — 12 briefs × 3 runs (2026-10-07)

**Result: the fresh-context candidate (v0.7.0-rc1) replaces v0.5.3.** It passed
all nine gates on both generators. The bolder selection rule (rc3) failed one
gate on GPT and does not ship. Preregistered on commit `b554863`; 288
portfolios, 288 judgments, 24 codings, no missing rows.

`NEW` is the candidate, `OLD` is v0.5.3, `BOLD` is the rc3 rule over the same
worker sketches as `NEW`, and `A0` is the plain prompt.

What the candidate did and did not do:

- It was preferred to v0.5.3 on 11 of 12 briefs with GPT (1 lost) and on 10 of
  12 with Claude (none lost). Useful surprise rose by +0.44 and +0.29, fit by
  +0.42 and +0.15, craft by +0.81 and +0.29.
- It cost 3.9× the tokens on GPT and 3.3× on Claude, and took 3.7× and 3.0× as
  long with the calls run one after another.
- Under the rule fixed in advance the result may be described as more
  creative, because useful surprise rose by at least +0.25 on both generators.
  The other route to that claim was not met: the share of its mechanisms that
  the plain prompt also produced did not fall (0.47 vs 0.49 on GPT, 0.59 vs
  0.55 on Claude). The gain is in which ideas are chosen and how well they are
  worked out, not in rarer mechanisms.
- Separate runs still repeated mechanisms about as often as before (overlap
  0.47 vs 0.46 on GPT, 0.48 vs 0.51 on Claude).
- On Claude it returned slightly more ideas than v0.5.3 (4.31 vs 4.00), still
  fewer than the plain prompt (4.61).

The bolder rule did what it was built for on Claude (plain-prompt share 0.39
vs 0.55, overlap 0.33) while tying v0.5.3 in preference there (5–5–2). On GPT
it won 9–0–3 but barely moved the plain-prompt share (0.45 vs 0.49), so it
failed the gate that defines it.

Limits:

- Sub-agents were emulated with separate calls. Whether a host dispatches
  workers when the skill asks is a separate check, not part of this result.
- Judges were the other model family, not people.
- One deviation from the frozen harness: the per-call timeout was raised from
  600 to 1,800 seconds after 287 of 288 portfolios existed, because one Claude
  call for `BOLD` kept reasoning past ten minutes. No prompt, brief, runtime,
  or rule changed.
- The run was interrupted once by a subscription limit and resumed with the
  same command.

## Host check (not part of the preregistered result)

The experiment emulated sub-agents. With the skill installed in real hosts and
called once per brief:

| Dispatch paragraph | Claude Code | Codex |
|---|---|---|
| As tested (v0.7.0): "or the request is too small to justify them" | workers dispatched in 2 of 4 calls | 0 of 1 |
| Firmer (v0.7.1): "do it for every brief" | 3 of 3 | 1 of 1 |

So v0.7.0's wording let hosts skip the step the experiment had measured.
v0.7.1 changes only that paragraph. These are a handful of calls, enough to
show the difference in behaviour and not a rate.

These briefs are now retired.

## Generator: gpt-5.5 (judged by claude-opus-5-5)

| Pair | Cells W–L–T | Briefs W–L–T | fit | surprise | diversity | craft | trap cells W–L–T | trap fit |
|---|---|---|---|---|---|---|---|---|
| NEW vs OLD | 25–3–8 | 11–1–0 | +0.42 | +0.44 | +0.10 | +0.81 | 4–2–0 | 0.0 |
| BOLD vs OLD | 23–3–10 | 9–0–3 | +0.44 | +0.51 | +0.39 | +0.81 | 3–2–1 | 0.0 |

| Arm | tokens | seconds | chars | ideas | overlap | distinct | also in baseline |
|---|---|---|---|---|---|---|---|
| A0 | 19605.6944 | 17.7717 | 2561.1111 | 5.0 | 0.5819 | 0.5811 | 1.0 |
| OLD | 21045.4444 | 19.5561 | 2871.3056 | 5.0 | 0.4574 | 0.6626 | 0.4922 |
| NEW | 81912.6389 | 71.6978 | 2889.1944 | 4.9722 | 0.4708 | 0.6568 | 0.4657 |
| BOLD | 81912.6389 | 71.6978 | 2911.6944 | 4.9722 | 0.4972 | 0.6334 | 0.4499 |

- Gates: coverage=PASS, preference=PASS, fit_non_inferior=PASS, craft_non_inferior=PASS, conventional_trap=PASS, cost=PASS, breadth=PASS, not_less_surprising=PASS, not_more_repetitive=PASS, claim_more_creative=PASS, bold_preference_not_worse=PASS, bold_fit_non_inferior=PASS, bold_beyond_plain=FAIL, bold_breadth=PASS

## Generator: claude-opus-5-5 (judged by gpt-5.5)

| Pair | Cells W–L–T | Briefs W–L–T | fit | surprise | diversity | craft | trap cells W–L–T | trap fit |
|---|---|---|---|---|---|---|---|---|
| NEW vs OLD | 20–4–12 | 10–0–2 | +0.15 | +0.29 | +0.50 | +0.29 | 5–0–1 | 0.6667 |
| BOLD vs OLD | 11–11–14 | 5–5–2 | -0.08 | -0.01 | +0.18 | +0.03 | 3–0–3 | 0.25 |

| Arm | tokens | seconds | chars | ideas | overlap | distinct | also in baseline |
|---|---|---|---|---|---|---|---|
| A0 | 3917.1111 | 38.5572 | 2823.8611 | 4.6111 | 0.6097 | 0.5649 | 1.0 |
| OLD | 7174.7778 | 53.2106 | 2962.8056 | 4.0 | 0.5074 | 0.6293 | 0.5496 |
| NEW | 23387.9444 | 159.3431 | 3322.3056 | 4.3056 | 0.4792 | 0.6407 | 0.5867 |
| BOLD | 23387.9444 | 159.3431 | 3093.1389 | 4.1667 | 0.3306 | 0.7128 | 0.3909 |

- Gates: coverage=PASS, preference=PASS, fit_non_inferior=PASS, craft_non_inferior=PASS, conventional_trap=PASS, cost=PASS, breadth=PASS, not_less_surprising=PASS, not_more_repetitive=PASS, claim_more_creative=PASS, bold_preference_not_worse=PASS, bold_fit_non_inferior=PASS, bold_beyond_plain=PASS, bold_breadth=PASS

**Replace the shipped runtime: YES**

**Ship the bolder selection rule as an on-request mode: NO**

**May be described as more creative: YES**
