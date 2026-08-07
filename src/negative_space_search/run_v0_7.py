"""Execute the preregistered v0.7 operator-discovery benchmark."""

from __future__ import annotations

import json

from .evaluation_v0_7 import summarize
from .operator_discovery_v0_7 import (
    generated_predicates,
    held_out_cases,
    numeric_expressions,
    policies,
    training_episodes,
)


def main() -> None:
    training = training_episodes()
    cases = held_out_cases()
    payload: dict[str, object] = {
        "benchmark": "negative-space-search-v0.7-operator-discovery",
        "training_ids": [episode.episode_id for episode in training],
        "held_out_ids": [case.case_id for case in cases],
        "numeric_expression_count": len(numeric_expressions()),
        "generated_predicate_count": len(generated_predicates()),
        "policies": {},
        "status": "preregistered construction-language repair test; no composite score",
    }

    policy_results: dict[str, object] = {}
    for policy in policies():
        policy.fit(training)
        decisions, summary = summarize(policy, cases)
        selections = getattr(policy, "selections", {})
        policy_results[policy.name] = {
            "summary": summary.to_dict(),
            "generated_operators": {
                probe: operator.name
                for probe, operator in policy.generated_operators.items()
            },
            "selections": {
                probe: selection.to_dict()
                for probe, selection in selections.items()
            },
            "decisions": [decision.to_dict() for decision in decisions],
        }
    payload["policies"] = policy_results
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
