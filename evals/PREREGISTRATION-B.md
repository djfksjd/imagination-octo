# Experiment B — preregistration

Frozen before any confirmation output was generated, in the commit that
introduced this file together with `briefs.experiment-b.jsonl`,
`specs/experiment-b.json`, and both runtimes under `runtimes/`.

## Question

Should the candidate runtime (`runtimes/engine-v0.6.0-rc2.md`) replace the
shipped one (`runtimes/engine-v0.5.3.md`)?

Experiment A's raw data showed three weaknesses in v0.5.3, all checked
independently by Codex against the same files:

- On Claude it returned fewer ideas than a plain prompt (3.8 vs 4.5 per
  portfolio) and its set diversity fell.
- On Claude, for practical service briefs, every mechanism it produced had
  already been produced by the plain prompt.
- Separate runs still shared 40–50% of their mechanisms, and one brief was lost
  on both generators to a set that repeated a single motif.

The candidate changes three things: a private "modal map" that keeps the
strongest conventional answer as a plainly stated anchor and limits how many
other first-thought mechanisms may survive, a rule that keeps four or five
survivors from different mechanism families, and a shorter stress test in
place of the proof section, which Experiment A did not show to matter.

## Design

| | |
|---|---|
| Briefs | `briefs.experiment-b.jsonl`: 12 fresh briefs (8 English, 4 Korean), 3 narrative premises, 2 traps where a conventional answer is correct |
| Generators | `gpt-5.5` and `claude-opus-5-5`, as in Experiment A |
| Arms | `A0` plain prompt · `OLD` v0.5.3 · `NEW` v0.6.0-rc2 |
| Runs | 4 per brief × generator × arm = 288 generations |
| Judging | Cross-family, both left/right orders: `NEW`–`OLD` and `NEW`–`A0` |
| Coding | One cross-family mechanism coding per brief × generator, arms unlabelled |

Cells, briefs, and mechanism overlap are defined as in
[`PREREGISTRATION.md`](PREREGISTRATION.md). *Ideas* is the mean number of coded
ideas per portfolio.

## Decision rule

The candidate replaces the shipped runtime only if every gate holds on **both**
generators:

1. **Coverage.** Every planned output and vote exists.
2. **Preference not worse.** `NEW` wins at least as many briefs as it loses
   against `OLD`.
3. **Fit.** Pooled `NEW` − `OLD` is at least −0.25.
4. **Craft.** Pooled `NEW` − `OLD` is at least −0.25.
5. **Conventional traps.** On the trap briefs `NEW` does not lose more cells
   than it wins against `OLD`, and its fit difference is at least −0.25.
6. **Still beats plain.** `NEW` wins more briefs than it loses against `A0`.
7. **Cost.** `NEW` uses at most 1.10× the tokens of `OLD`.
8. **Breadth.** `NEW` averages at least 4.2 ideas per portfolio.
9. **Improves.** `NEW`'s mechanism overlap across runs is at least 0.05 below
   `OLD`'s, or its set diversity against `OLD` is at least +0.25.

If any gate fails on either generator, v0.5.3 stays and the failure is
reported as a failure. A candidate that passes on one generator only is not
shipped for that generator alone.

## Known limits, stated before the run

- Gate 2 asks only that the candidate is not worse. Twelve briefs cannot show a
  small preference gain, and this experiment does not try to.
- Both runtimes are skills, so the blinding problem found in Experiment A
  matters less for `NEW`–`OLD`, but `NEW`–`A0` inherits it. Gate 6 is a sanity
  check, not a claim.
- The candidate was developed on eight development briefs
  (`briefs.b-dev.jsonl`), none of which appear here. The diagnosis itself came
  from Experiment A's retired briefs.
- Development did not show a preference gain. Against v0.5.3 on those eight
  briefs, rc1 went 2–4–2 on GPT and 4–2–2 on Claude; rc2, which differs by one
  paragraph, went 5–2–1 and 1–6–1. The only stable effect was more ideas per
  portfolio on Claude (3.96 to about 4.4). This run is expected to be close,
  and a failure is a plausible outcome.
- No human judged anything in this experiment.
