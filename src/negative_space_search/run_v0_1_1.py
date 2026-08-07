"""Run the v0.1.1 model-adequacy benchmark and emit JSON.

Usage after an editable install:

    python -m negative_space_search.run_v0_1_1
"""

from __future__ import annotations

import json

from .baselines import INITIAL_BASELINES
from .evaluation import score_model_adequacy_pair
from .simulator import model_adequacy_pair


def run() -> dict[str, object]:
    within_model, model_inadequate = model_adequacy_pair()

    policies: dict[str, object] = {}
    for policy in INITIAL_BASELINES:
        score = score_model_adequacy_pair(policy, within_model, model_inadequate)
        policies[policy.name] = score.to_dict()

    return {
        "benchmark": "negative-space-search-v0.1.1-model-adequacy",
        "status": "hostile evidence-selection test; frozen core unchanged",
        "pair": [within_model.case_id, model_inadequate.case_id],
        "initial_observations_equal": within_model.observation == model_inadequate.observation,
        "policies": policies,
    }


def main() -> None:
    print(json.dumps(run(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
