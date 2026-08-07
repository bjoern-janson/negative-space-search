"""Execute the preregistered v0.4 representation-repair benchmark."""

from __future__ import annotations

import json

from .evaluation_v0_4 import evaluate_stage, representation_change_rate
from .representation_v0_4 import (
    AdaptiveRepresentationLearner,
    CompressedOutcomeMemory,
    FixedTypedOracle,
    acquisition_episodes,
    held_out_cases,
    repair_episodes,
)


def _snapshot(policy: AdaptiveRepresentationLearner) -> dict[str, str]:
    return {selection.probe: selection.relation_name for selection in policy.selections}


def main() -> None:
    acquisition = acquisition_episodes()
    repair = repair_episodes()
    all_history = acquisition + repair
    cases = held_out_cases()

    adaptive = AdaptiveRepresentationLearner()
    adaptive.fit(acquisition)
    pre_representation = _snapshot(adaptive)
    pre_decisions, pre_summary = evaluate_stage(adaptive, cases, "pre_repair")

    adaptive.fit(all_history)
    post_representation = _snapshot(adaptive)
    post_decisions, post_summary = evaluate_stage(adaptive, cases, "post_repair")

    compressed = CompressedOutcomeMemory()
    compressed.fit(acquisition)
    compressed_pre_decisions, compressed_pre_summary = evaluate_stage(
        compressed, cases, "pre_repair"
    )
    compressed.fit(all_history)
    compressed_post_decisions, compressed_post_summary = evaluate_stage(
        compressed, cases, "post_repair"
    )

    oracle = FixedTypedOracle()
    oracle.fit(all_history)
    oracle_decisions, oracle_summary = evaluate_stage(oracle, cases, "post_repair")

    payload = {
        "benchmark": "negative-space-search-v0.4-representation-acquisition",
        "acquisition_ids": [episode.episode_id for episode in acquisition],
        "repair_ids": [episode.episode_id for episode in repair],
        "held_out_ids": [case.case_id for case in cases],
        "adaptive_representation": {
            "pre_selected_relations": pre_representation,
            "post_selected_relations": post_representation,
            "pre_decisions": [decision.to_dict() for decision in pre_decisions],
            "post_decisions": [decision.to_dict() for decision in post_decisions],
            "pre_summary": pre_summary.to_dict(),
            "post_summary": post_summary.to_dict(),
            "Q_repair": post_summary.held_out_selection_rate - pre_summary.held_out_selection_rate,
            "representation_change_rate": representation_change_rate(
                pre_representation, post_representation
            ),
        },
        "compressed_outcome_memory": {
            "pre_decisions": [decision.to_dict() for decision in compressed_pre_decisions],
            "post_decisions": [decision.to_dict() for decision in compressed_post_decisions],
            "pre_summary": compressed_pre_summary.to_dict(),
            "post_summary": compressed_post_summary.to_dict(),
        },
        "fixed_typed_oracle": {
            "decisions": [decision.to_dict() for decision in oracle_decisions],
            "summary": oracle_summary.to_dict(),
        },
        "status": "preregistered representation-repair test; no composite score",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
