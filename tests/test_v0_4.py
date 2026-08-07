from __future__ import annotations

import unittest

from negative_space_search.evaluation_v0_4 import evaluate_stage, representation_change_rate
from negative_space_search.representation_v0_4 import (
    AdaptiveRepresentationLearner,
    CompressedOutcomeMemory,
    FixedTypedOracle,
    RawResolvedEpisode,
    acquisition_episodes,
    candidate_relations,
    held_out_cases,
    repair_episodes,
)


class V04RepresentationAcquisitionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.acquisition = acquisition_episodes()
        self.repair = repair_episodes()
        self.all_history = self.acquisition + self.repair
        self.cases = held_out_cases()

    def test_frozen_ids(self) -> None:
        self.assertEqual(
            [episode.episode_id for episode in self.acquisition],
            ["A_D1", "A_D2", "A_P1", "A_P2", "A_N1", "A_N2"],
        )
        self.assertEqual(
            [episode.episode_id for episode in self.repair],
            ["B_D", "B_P", "B_N"],
        )
        self.assertEqual(
            [case.case_id for case in self.cases],
            ["R_DEP", "R_PAY", "R_NET", "R_NOVEL"],
        )

    def test_raw_history_contains_no_semantic_failure_labels(self) -> None:
        forbidden = {
            "diagnosis",
            "failure_class",
            "dependency_failure",
            "payoff_drift",
            "coordination_failure",
            "model_mismatch",
            "negative_space_class",
        }
        self.assertTrue(forbidden.isdisjoint(RawResolvedEpisode.__dataclass_fields__))

    def test_error_magnitude_is_non_identifying_everywhere(self) -> None:
        values = {
            round(item.error, 8)
            for item in self.acquisition + self.repair + self.cases
        }
        self.assertEqual(values, {0.6})

    def test_candidate_library_is_frozen_and_generic(self) -> None:
        self.assertEqual(
            [relation.name for relation in candidate_relations()],
            [
                "hint_high",
                "hint_low",
                "hint_near_zero",
                "pair0_close",
                "pair0_far",
                "pair0_sign_disagree",
                "pair1_close",
                "pair1_far",
                "pair1_sign_disagree",
                "pair2_close",
                "pair2_far",
                "pair2_sign_disagree",
            ],
        )

    def test_pre_repair_representation_prefers_rewarded_surface_cues(self) -> None:
        learner = AdaptiveRepresentationLearner()
        learner.fit(self.acquisition)
        selected = {item.probe: item.relation_name for item in learner.selections}
        self.assertEqual(
            selected,
            {
                "independence_probe": "hint_high",
                "payoff_regime_probe": "hint_near_zero",
                "topology_probe": "hint_low",
            },
        )

    def test_repair_history_changes_all_three_selected_relations(self) -> None:
        learner = AdaptiveRepresentationLearner()
        learner.fit(self.acquisition)
        before = {item.probe: item.relation_name for item in learner.selections}
        learner.fit(self.all_history)
        after = {item.probe: item.relation_name for item in learner.selections}
        self.assertEqual(
            after,
            {
                "independence_probe": "pair0_close",
                "payoff_regime_probe": "pair1_far",
                "topology_probe": "pair2_sign_disagree",
            },
        )
        self.assertEqual(representation_change_rate(before, after), 1.0)

    def test_adaptive_representation_improves_after_repair(self) -> None:
        learner = AdaptiveRepresentationLearner()
        learner.fit(self.acquisition)
        _, before = evaluate_stage(learner, self.cases, "pre_repair")
        learner.fit(self.all_history)
        _, after = evaluate_stage(learner, self.cases, "post_repair")

        self.assertEqual(before.held_out_selection_rate, 0.0)
        self.assertEqual(after.held_out_selection_rate, 1.0)
        self.assertEqual(after.held_out_selection_rate - before.held_out_selection_rate, 1.0)
        self.assertEqual(after.novel_model_check_rate, 1.0)
        self.assertEqual(after.false_model_check_rate, 0.0)

    def test_compressed_memory_follows_wrong_surface_history_after_repair(self) -> None:
        memory = CompressedOutcomeMemory()
        memory.fit(self.all_history)
        decisions, summary = evaluate_stage(memory, self.cases, "post_repair")
        self.assertEqual(summary.held_out_selection_rate, 0.0)
        self.assertEqual(
            [decision.nearest_history_id for decision in decisions],
            ["B_N", "B_D", "B_P", "A_P1"],
        )

    def test_fixed_typed_oracle_remains_upper_bound(self) -> None:
        oracle = FixedTypedOracle()
        oracle.fit(self.all_history)
        _, summary = evaluate_stage(oracle, self.cases, "post_repair")
        self.assertEqual(summary.held_out_selection_rate, 1.0)
        self.assertEqual(summary.novel_model_check_rate, 1.0)
        self.assertEqual(summary.false_model_check_rate, 0.0)


if __name__ == "__main__":
    unittest.main()
