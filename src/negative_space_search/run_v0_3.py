"""Run the preregistered v0.3 representation-transfer benchmark."""

from __future__ import annotations

import json

from .evaluation_v0_3 import summarize
from .representation_v0_3 import held_out_cases, training_episodes, v0_3_policies


def run() -> dict[str, object]:
    training = training_episodes()
    cases = held_out_cases()
    policies: dict[str, object] = {}

    for policy in v0_3_policies():
        policy.fit(training)
        decisions, summary = summarize(policy, cases)
        policies[policy.name] = {
            "decisions": [decision.to_dict() for decision in decisions],
            "summary": summary.to_dict(),
        }

    return {
        "benchmark": "negative-space-search-v0.3-representation-transfer",
        "training_ids": [episode.episode_id for episode in training],
        "held_out_ids": [case.case_id for case in cases],
        "status": "preregistered representation ablation; no composite score",
        "policies": policies,
    }


def main() -> None:
    print(json.dumps(run(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
