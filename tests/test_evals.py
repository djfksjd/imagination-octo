from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest


REPO = Path(__file__).parents[1]
sys.path.insert(0, str(REPO / "evals"))

import octo_eval  # noqa: E402


BRIEFS = REPO / "evals" / "briefs.experiment-a.jsonl"
RATING = {"fit": 5, "useful_surprise": 4, "set_diversity": 4, "craft": 5}


def rated(**changes: int) -> dict[str, int]:
    return {**RATING, **changes}


def experiment(tmp_path: Path, preferred: dict[tuple[str, str], str]) -> octo_eval.Experiment:
    """Build a finished two-run experiment whose judges always want `preferred`."""
    exp = octo_eval.Experiment("synthetic", BRIEFS, 2, 1, root=tmp_path)
    for brief_id, family, run in exp.cells():
        for arm in octo_eval.ARMS:
            exp.outputs.add(
                {
                    "brief_id": brief_id, "family": family, "arm": arm, "run": run,
                    "text": f"{arm} portfolio for {brief_id} run {run}",
                    "model": "m", "seconds": 10.0,
                    "input_tokens": 1000 + 200 * (arm == "A3"), "output_tokens": 500,
                }  # fmt: skip
            )
        for x, y in octo_eval.PAIRS:
            want = preferred[(x, y)]
            lift = 1 if want == x else 0
            for order in (0, 1):
                exp.votes.add(
                    {
                        "pair_id": exp.pair_id(brief_id, family, run, x, y),
                        "order": order, "brief_id": brief_id, "family": family,
                        "run": run, "x": x, "y": y, "judge_family": "j",
                        "judge_model": "m", "want": want,
                        "ratings": {
                            x: rated(useful_surprise=4 + lift),
                            y: rated(),
                        },
                    }  # fmt: skip
                )
        if run <= 2:
            pair = exp.pair_id(brief_id, family, run, "A3", "A0")
            exp.probes.add(
                {
                    "pair_id": pair, "brief_id": brief_id, "family": family,
                    "run": run, "correct": run == 1, "cue": "",
                }  # fmt: skip
            )
    for brief in exp.briefs:
        for family in octo_eval.FAMILIES:
            portfolios = {}
            for label, (arm, run) in exp.labels(brief["id"], family).items():
                shared = ["M1", "M2"] if arm == "A0" else [f"{arm}{run}a", "M1"]
                portfolios[label] = shared + [f"{arm}{run}b"]
            exp.codings.add(
                {
                    "brief_id": brief["id"], "family": family, "coder_model": "m",
                    "mechanisms": [], "portfolios": portfolios,
                }  # fmt: skip
            )
    return exp


def test_confirmation_briefs_meet_the_preregistered_mix() -> None:
    briefs = octo_eval.read_jsonl(BRIEFS)

    assert len({brief["id"] for brief in briefs}) == len(briefs) == 12
    assert {brief["language"] for brief in briefs} == {"en", "ko"}
    assert sum("premise" in brief["domain"] for brief in briefs) >= 3
    assert sum(bool(brief.get("trap")) for brief in briefs) >= 2


def test_router_cases_are_well_formed() -> None:
    cases = octo_eval.read_jsonl(REPO / "evals" / "router" / "cases.jsonl")

    assert len(cases) >= 6
    for case in cases:
        assert case["turns"][-1]["role"] == "user"
        assert len({criterion["id"] for criterion in case["criteria"]}) == len(case["criteria"])
        assert "$imagination-octo" in octo_eval.router_prompt(case)


def test_ablation_removes_only_the_proof_section() -> None:
    skill = octo_eval.ENGINE_SKILL.read_text(encoding="utf-8")
    ablated = octo_eval.ablated_skill(skill)

    assert "## Prove each survivor" not in ablated
    assert "## Cull by failure, then compare" in ablated
    assert "## Deliver a portfolio" in ablated
    assert octo_eval.generation_prompt("A3", "B").count("<skill>") == 1
    assert "<skill>" not in octo_eval.generation_prompt("A1", "B")
    assert "privately draft" in octo_eval.generation_prompt("A1", "B")
    assert "privately draft" not in octo_eval.generation_prompt("A0", "B")


def test_sign_test_matches_exact_binomial_tails() -> None:
    assert octo_eval.sign_test(10, 2) == pytest.approx(0.01929, abs=1e-5)
    assert octo_eval.sign_test(9, 3) == pytest.approx(0.07300, abs=1e-5)
    assert octo_eval.sign_test(0, 0) == 1.0


def test_a_split_between_orders_counts_as_a_tie() -> None:
    assert octo_eval.pair_outcome([{"want": "A3"}, {"want": "A3"}]) == "A3"
    assert octo_eval.pair_outcome([{"want": "A3"}, {"want": "A0"}]) == "tie"


def test_a_clean_win_passes_every_gate(tmp_path: Path) -> None:
    exp = experiment(
        tmp_path,
        {("A1", "A0"): "tie", ("A3", "A0"): "A3", ("A3", "A1"): "A3", ("A3", "A2"): "A3"},
    )

    result = octo_eval.score(exp, 2, None)["families"]["claude"]
    decision = result["decision"]

    assert result["pairs"]["A3 vs A0"]["briefs"] == {"x": 12, "y": 0, "tie": 0}
    assert all(decision["gates"].values()), decision["gates"]
    assert decision["verdicts"]["transfers"] is True
    assert decision["verdicts"]["mostly_ceremony"] is False
    assert decision["verdicts"]["blinding_broken"] is False
    assert decision["verdicts"]["house_style"] is False
    assert result["convergence"]["A0"]["mechanism_overlap"] > result["convergence"]["A3"]["mechanism_overlap"]
    assert "A3 vs A0" in octo_eval.report(octo_eval.score(exp, 2, None))


def test_an_effort_matched_control_that_keeps_up_is_called_ceremony(tmp_path: Path) -> None:
    exp = experiment(
        tmp_path,
        {("A1", "A0"): "A1", ("A3", "A0"): "A3", ("A3", "A1"): "tie", ("A3", "A2"): "tie"},
    )

    decision = octo_eval.score(exp, 2, None)["families"]["gpt"]["decision"]

    assert decision["a1_share_of_a3_gain"] == {"want": 1.0, "useful_surprise": 1.0}
    assert decision["verdicts"]["mostly_ceremony"] is True
    assert decision["verdicts"]["proof_section_carries_weight"] is False


def test_no_gain_fails_the_transfer_gate(tmp_path: Path) -> None:
    exp = experiment(
        tmp_path,
        {("A1", "A0"): "tie", ("A3", "A0"): "A0", ("A3", "A1"): "A1", ("A3", "A2"): "tie"},
    )

    decision = octo_eval.score(exp, 2, None)["families"]["claude"]["decision"]

    assert decision["gates"]["gain_want"] is False
    assert decision["verdicts"]["transfers"] is False
    assert decision["verdicts"]["mostly_ceremony"] is False


def test_owner_votes_are_scored_against_the_hidden_sides(tmp_path: Path) -> None:
    exp = experiment(
        tmp_path,
        {("A1", "A0"): "tie", ("A3", "A0"): "A3", ("A3", "A1"): "A3", ("A3", "A2"): "A3"},
    )
    pairs = octo_eval.human_pairs(exp)
    votes = {
        pair["pair_id"]: "left" if pair["left"] == "A3" else "right" for pair in pairs
    }
    votes_path = tmp_path / "votes.json"
    votes_path.write_text(json.dumps(votes), encoding="utf-8")

    assert len(pairs) == 24
    assert {pair["left"] for pair in pairs} == {"A0", "A3"}
    owner = octo_eval.score(exp, 2, votes_path)["families"]["gpt"]
    assert owner["owner"]["A3"] == 12
    assert owner["owner"]["agreement_with_ai_pair_outcome"] == 1.0
    assert owner["decision"]["verdicts"]["owner_anchor_holds"] is True
    assert "A3" not in octo_eval.human_packet(exp).read_text(encoding="utf-8").split("const PAIRS=")[0]


def test_experiment_specs_point_at_existing_prompts_and_runtimes() -> None:
    for path in (REPO / "evals" / "specs").glob("*.json"):
        spec = json.loads(path.read_text(encoding="utf-8"))
        for arm in spec["arms"].values():
            assert (REPO / "evals" / "prompts" / arm["prompt"]).exists()
            assert "skill" not in arm or (REPO / arm["skill"]).exists()
        for x, y in spec["pairs"]:
            assert {x, y} <= set(spec["arms"])


def test_frozen_runtime_copy_matches_the_shipped_engine() -> None:
    frozen = (REPO / "evals" / "runtimes" / "engine-v0.5.3.md").read_text(encoding="utf-8")
    assert "## Prove each survivor" in frozen
    assert "modal map" not in frozen
