"""Execute the preregistered v0.2 false-escalation benchmark."""

from __future__ import annotations

import json

from .v0_2 import false_escalation_cases, score_v0_2_cases, summarize_v0_2
from .v0_2_policies import V02_PRIMARY_POLICIES


def run() -> dict[str, object]:
    cases = false_escalation_cases()
    policies: dict[str, object] = {}

    for policy in V02_PRIMARY_POLICIES:
        scores = score_v0_2_cases(policy, cases)
        policies[policy.name] = {
            "summary": summarize_v0_2(scores),
            "cases": [score.to_dict() for score in scores],
        }

    return {
        "benchmark": "negative-space-search-v0.2-false-escalation",
        "status": "preregistered selective-escalation test; no composite score",
        "case_ids": [case.case_id for case in cases],
        "splits": {
            "development": [
                case.case_id for case in cases if case.observation.metadata["split"] == "development"
            ],
            "held_out": [
                case.case_id for case in cases if case.observation.metadata["split"] == "held_out"
            ],
        },
        "policies": policies,
    }


def main() -> None:
    print(json.dumps(run(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
