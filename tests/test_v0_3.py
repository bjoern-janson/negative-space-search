from __future__ import annotations

import unittest

from negative_space_search.evaluation_v0_3 import summarize
from negative_space_search.representation_v0_3 import (
    GenericCompressedHistoryLearner,
    TypedHistoryLearner,
    held_out_cases,
    training_episodes,
)


class V03RepresentationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.training = training_episodes()
        self.cases = held_out_cases()

    def test_frozen_training_and_held_out_ids(self) -> None:
        self.assertEqual([episode.episode_id for episode in self.training], ["T_DEP", "T_PAY", "T_NET"])
        self.assertEqual([case.case_id for case in self.cases], ["H_DEP", "H_PAY", "H_NET", "H_NOVEL"])

    def test_training_error_magnitude_is_non_identifying(self) -> None:
        self.assertEqual({round(episode.error, 8) for episode in self.training}, {0.6})

    def test_held_out_error_magnitude_is_non_identifying(self) -> None:
        self.assertEqual({round(case.error, 8) for case in self.cases}, {0.6})

    def test_compressed_history_follows_misleading_surface_similarity(self) -> None:
        policy = GenericCompressedHistoryLearner()
        policy.fit(self.training)
        nearest = {case.case_id: policy.decide(case).nearest_training_id for case in self.cases}
        self.assertEqual(
            nearest,
            {
                "H_DEP": "T_NET",
                "H_PAY": "T_DEP",
                "H_NET": "T_PAY",
                "H_NOVEL": "T_PAY",
            },
        )

    def test_typed_history_transfers_known_structures_and_checks_novel_case(self) -> None:
        policy = TypedHistoryLearner("typed_control")
        policy.fit(self.training)
        decisions, summary = summarize(policy, self.cases)
        self.assertEqual(summary.known_topology_transfer_rate, 1.0)
        self.assertEqual(summary.novel_topology_model_check_rate, 1.0)
        self.assertEqual(summary.false_model_check_rate, 0.0)
        self.assertEqual(summary.held_out_evidence_selection_rate, 1.0)
        self.assertEqual(decisions[-1].selected_probe, "model_disrupting_probe")

    def test_negative_space_and_typed_general_control_are_identical(self) -> None:
        general = TypedHistoryLearner("typed_general_causal_history")
        negative = TypedHistoryLearner("structured_negative_space_history")
        general.fit(self.training)
        negative.fit(self.training)

        general_probes = [general.decide(case).selected_probe for case in self.cases]
        negative_probes = [negative.decide(case).selected_probe for case in self.cases]
        self.assertEqual(general_probes, negative_probes)


if __name__ == "__main__":
    unittest.main()
