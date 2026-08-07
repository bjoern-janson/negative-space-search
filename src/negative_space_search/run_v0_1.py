"""Run the minimal v0.1 benchmark and emit JSON.

Usage after an editable install:

    python -m negative_space_search.run_v0_1
"""

from __future__ import annotations

import json

from .baselines import INITIAL_BASELINES
from .evaluation import score_cases, score_hostile_pair
from .simulator import canonical_cases, hostile_equivalence_pair


def run() -> dict[str, object]:
    cases = canonical_cases()
    hostile_i, hostile_s = hostile_equivalence_pair()

    policies: dict[str, object] = {}
    for policy in INITIAL_BASELINES:
        case_scores = score_cases(policy, cases)
        hostile_score = score_hostile_pair(policy, hostile_i, hostile_s)

        policies[policy.name] = {
            "initial_cases": [score.to_dict() for score in case_scores],
            "diagnostic_counts": {
                "action_correct": sum(score.action_correct for score in case_scores),
                "diagnosis_supported": sum(score.diagnosis_supported for score in case_scores),
                "evidence_match": sum(score.evidence_match is True for score in case_scores),
                "healthy_absence_preserved": sum(
                    score.healthy_absence_preserved is True for score in case_scores
                ),
                "n_cases": len(case_scores),
            },
            "hostile_observational_equivalence": hostile_score.to_dict(),
        }

    return {
        "benchmark": "negative-space-search-v0.1",
        "status": "initial executable benchmark; full Q_Psi vector not yet implemented",
        "canonical_case_ids": [case.case_id for case in cases],
        "policies": policies,
    }


def main() -> None:
    print(json.dumps(run(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
