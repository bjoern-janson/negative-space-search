"""Execute the preregistered v0.6 construction-language boundary benchmark."""

from __future__ import annotations

import json

from .evaluation_v0_6 import summarize
from .language_boundary_v0_6 import (
    BoundaryAwareLanguageAuditor,
    ConservativeAbstainer,
    CurrentLanguageAssimilator,
    ExpandedLanguageOracle,
    current_language,
    held_out_cases,
    training_episodes,
)


def run() -> dict[str, object]:
    training = training_episodes()
    cases = held_out_cases()
    policies = (
        CurrentLanguageAssimilator(),
        ConservativeAbstainer(),
        BoundaryAwareLanguageAuditor(),
        ExpandedLanguageOracle(),
    )

    results: dict[str, object] = {}
    for policy in policies:
        policy.fit(training)
        decisions, summary = summarize(policy, cases)
        results[policy.name] = {
            "decisions": [decision.to_dict() for decision in decisions],
            "summary": summary.to_dict(),
        }

    return {
        "benchmark": "negative-space-search-v0.6-language-boundary",
        "training_ids": [episode.episode_id for episode in training],
        "held_out_ids": [case.case_id for case in cases],
        "current_language_expression_count": len(current_language()),
        "policies": results,
        "status": "preregistered construction-language boundary test; operator invention not attempted",
    }


def main() -> None:
    print(json.dumps(run(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
