# Experiment C — preregistration

Frozen before any confirmation output was generated, in the commit that
introduced this file together with `briefs.experiment-c.jsonl`,
`specs/experiment-c.json`, `prompts/scout.md`, and the runtimes
`runtimes/engine-v0.7.0-rc1.md` and `runtimes/engine-v0.7.0-rc3.md`.

## Question

Should the engine give each search pass to a worker with a fresh context?

v0.5.3 runs its three passes (direct, mechanism transfer, premise shift) in
one context. The candidate (`rc1`) keeps the same three passes and the same
cull, comparison, and proof, but tells the host to dispatch each pass to a
separate worker that sees only the brief and that one pass. Nothing else
changes. The harness emulates the dispatch: three separate calls, then a
fourth that receives the runtime, the task, and the pooled rough candidates.

A second runtime (`rc3`) adds one selection rule on top: a mechanism that more
than one worker reached independently counts as common ground, and at most one
such mechanism may survive. It is tested as a possible on-request "bolder"
mode, not as the default.

## What development showed

On eight development briefs (`briefs.b-dev.jsonl`, two runs each):

| Candidate | vs | GPT briefs W–L–T | Claude briefs W–L–T | Note |
|---|---|---|---|---|
| rc1 fan-out | v0.5.3 | 5–1–2 | 4–2–2 | fit +0.59 / +0.44, craft +0.81 / +0.47, surprise +0.16 / +0.09 |
| rc2 common-ground cap | rc1 | 4–0–4 | 0–5–3 | announced a recommended option, fewer ideas |
| rc3 cap, reworded | rc1 | 2–3–3 | 0–5–3 | vs v0.5.3: 5–1–2 and 4–3–1 |
| rc4 farther-reaching passes | rc1 | 2–5–1 | 2–4–2 | |
| rc5 rc4 + rarity tie-break | rc1 | 2–4–2 | 1–4–3 | |

Every variant that pushed selection toward rarer mechanisms produced
mechanisms that a plain prompt had reached less often, and every one of them
lost to rc1 in judged preference. So the default candidate is rc1, and it is
expected to yield better-chosen portfolios, not markedly stranger ones. The
tokens were 3.9× (GPT) and 2.9× (Claude) those of v0.5.3.

## Design

| | |
|---|---|
| Briefs | `briefs.experiment-c.jsonl`: 12 fresh briefs (8 English, 4 Korean), 3 narrative premises, 2 traps where a conventional answer is correct |
| Generators | `gpt-5.5` and `claude-opus-5-5` |
| Arms | `A0` plain prompt · `OLD` v0.5.3 · `NEW` rc1 with fan-out · `BOLD` rc3 over the same worker sketches as `NEW` |
| Runs | 3 per brief × generator × arm |
| Judging | Cross-family, both left/right orders: `NEW`–`OLD` and `BOLD`–`OLD` |
| Coding | One cross-family mechanism coding per brief × generator, arms unlabelled |

`A0` is generated only as the reference for "share of mechanisms the plain
prompt also produced"; it is not judged. `BOLD` reuses `NEW`'s worker sketches
so the two differ only in the selection rule; its cost is therefore reported
as equal to `NEW`'s.

## Decision rule

**Default.** rc1 replaces v0.5.3 only if every gate holds on **both**
generators:

1. **Coverage.** Every planned output and vote exists.
2. **Preference.** `NEW` wins more briefs than it loses against `OLD`.
3. **Fit.** Pooled `NEW` − `OLD` is at least −0.25.
4. **Craft.** Pooled `NEW` − `OLD` is at least −0.25.
5. **Conventional traps.** On the trap briefs `NEW` does not lose more cells
   than it wins, and its fit difference is at least −0.25.
6. **Cost.** `NEW` uses at most 4.5× the tokens of `OLD`.
7. **Breadth.** `NEW` averages no fewer than `OLD`'s ideas per portfolio minus 0.25.
8. **Not less surprising.** Pooled useful-surprise difference is at least −0.10.
9. **Not more repetitive.** `NEW`'s mechanism overlap across runs is at most
   `OLD`'s plus 0.10.

**The word "creative".** Passing the gates above supports "better portfolios
at several times the cost". The result may be described as *more creative*
only if, on both generators, useful surprise rises by at least +0.25 or the
share of `NEW`'s mechanisms that the plain prompt also produced is at least
0.10 below `OLD`'s. This is reported either way and does not affect the
replacement decision.

**Bolder mode.** The rc3 rule ships as a mode the user must ask for only if,
on both generators: `BOLD` wins at least as many briefs as it loses against
`OLD`; its fit difference is at least −0.25; its share of mechanisms the plain
prompt also produced is at least 0.10 below `OLD`'s; and its ideas per
portfolio are no fewer than `OLD`'s minus 0.25.

A gate that fails is reported as a failure, and nothing ships for one
generator alone.

## Known limits, stated before the run

- Three runs on twelve briefs cannot detect a small preference difference.
- The harness emulates sub-agents with separate API calls. Whether a host
  actually dispatches workers when the skill asks is checked separately and
  is not evidence here.
- Preference is judged by the other model family, not by people. Development
  suggests these judges reward fit and polish over rarity.
- The mechanism coding varies between coding passes; in development the same
  outputs gave overlap values that moved by about ±0.07.
- Cost is tokens. Fan-out also takes roughly two to four times the wall-clock
  time when the calls run one after another, as they do in this harness.
