"""Execute the preregistered v0.5 basis-failure benchmark."""

from __future__ import annotations

import json

from .basis_v0_5 import held_out_cases, training_episodes, v0_5_policies
from .evaluation_v0_5 import summarize


def main() -> None:
    training = training_episodes()
    cases = held_out_cases()
    payload: dict[str, object] = {
        "benchmark": "negative-space-search-v0.5-basis-failure",
        "training_ids": [episode.episode_id for episode in training],
        "held_out_ids": [case.case_id for case in cases],
        "policies": {},
        "status": "preregistered conditional basis-expansion test; no composite score",
    }

    policy_payload: dict[str, object] = {}
    for policy in v0_5_policies():
        policy.fit(training)
        decisions, summary = summarize(policy, cases)
        policy_payload[policy.name] = {
            "audits": [audit.to_dict() for audit in policy.audits],
            "decisions": [decision.to_dict() for decision in decisions],
            "summary": summary.to_dict(),
        }
    payload["policies"] = policy_payload
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
