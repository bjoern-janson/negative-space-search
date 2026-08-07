from __future__ import annotations

import unittest

from negative_space_search.evaluation_v0_6 import summarize
from negative_space_search.language_boundary_v0_6 import (
    LANGUAGE_ADEQUATE,
    LANGUAGE_EXPANSION_PROBE,
    LANGUAGE_INADEQUATE,
    LANGUAGE_UNKNOWN,
    BoundaryAwareLanguageAuditor,
    ConservativeAbstainer,
    CurrentLanguageAssimilator,
    ExpandedLanguageOracle,
    current_language,
    current_language_signature,
    expanded_oracle_signature,
    held_out_cases,
    training_episodes,
)
from negative_space_search.representation_v0_4 import MODEL_DISRUPTING_PROBE


class V06LanguageBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.training = training_episodes()
        self.cases = held_out_cases()
        self.by_training_id = {episode.episode_id: episode for episode in self.training}
        self.by_case_id = {case.case_id: case for case in self.cases}

    def test_frozen_ids(self) -> None:
        self.assertEqual(
            [episode.episode_id for episode in self.training],
            [
                "T_COMP1", "T_COMP2",
                "T_CLOSE1", "T_CLOSE2",
                "T_FAR1", "T_FAR2",
                "T_REF1", "T_REF2",
                "T_UP1", "T_DOWN1", "T_UP2", "T_DOWN2",
            ],
        )
        self.assertEqual(
            [case.case_id for case in self.cases],
            ["H_COMP", "H_REF", "H_ORDER_UP", "H_ORDER_DOWN", "H_UNKNOWN"],
        )

    def test_error_magnitude_is_non_identifying(self) -> None:
        self.assertEqual({round(episode.error, 8) for episode in self.training}, {0.6})
        self.assertEqual({round(case.error, 8) for case in self.cases}, {0.6})

    def test_current_language_is_exactly_v05_expression_family(self) -> None:
        language = current_language()
        self.assertEqual(len(language), 78)
        self.assertTrue(all("trace" not in expression.name for expression in language))

    def test_hostile_training_pairs_are_identical_under_every_current_expression(self) -> None:
        for up_id, down_id in (("T_UP1", "T_DOWN1"), ("T_UP2", "T_DOWN2")):
            up = self.by_training_id[up_id]
            down = self.by_training_id[down_id]
            self.assertNotEqual(up.ordered_trace, down.ordered_trace)
            self.assertEqual(current_language_signature(up), current_language_signature(down))
            self.assertNotEqual(expanded_oracle_signature(up), expanded_oracle_signature(down))

    def test_hostile_held_out_pair_is_language_equivalent_but_raw_trace_differs(self) -> None:
        up = self.by_case_id["H_ORDER_UP"]
        down = self.by_case_id["H_ORDER_DOWN"]
        self.assertNotEqual(up.ordered_trace, down.ordered_trace)
        self.assertEqual(current_language_signature(up), current_language_signature(down))
        self.assertNotEqual(expanded_oracle_signature(up), expanded_oracle_signature(down))

    def test_boundary_signature_maps_to_conflicting_resolved_classes(self) -> None:
        auditor = BoundaryAwareLanguageAuditor()
        auditor.fit(self.training)
        up_decision = auditor.decide(self.by_case_id["H_ORDER_UP"])
        self.assertEqual(
            set(up_decision.matched_resolving_probes),
            {"order_up_probe", "order_down_probe"},
        )

    def test_unknown_case_has_no_supported_current_language_signature(self) -> None:
        training_signatures = {current_language_signature(episode) for episode in self.training}
        self.assertNotIn(current_language_signature(self.by_case_id["H_UNKNOWN"]), training_signatures)

    def test_assimilator_hallucinates_existing_class_on_boundary_pair(self) -> None:
        policy = CurrentLanguageAssimilator()
        policy.fit(self.training)
        decisions, summary = summarize(policy, self.cases)
        boundary = [decision for decision in decisions if decision.case_id.startswith("H_ORDER")]
        self.assertEqual(summary.language_inadequacy_detection_rate, 0.0)
        self.assertEqual(summary.boundary_nonhallucination_rate, 0.0)
        self.assertEqual(summary.language_expansion_request_rate, 0.0)
        self.assertTrue(all(decision.language_status == LANGUAGE_ADEQUATE for decision in boundary))
        self.assertTrue(all(decision.selected_probe in decision.matched_resolving_probes for decision in boundary))

    def test_conservative_abstainer_avoids_guessing_but_does_not_localize_language_failure(self) -> None:
        policy = ConservativeAbstainer()
        policy.fit(self.training)
        decisions, summary = summarize(policy, self.cases)
        boundary = [decision for decision in decisions if decision.case_id.startswith("H_ORDER")]
        self.assertEqual(summary.boundary_nonhallucination_rate, 1.0)
        self.assertEqual(summary.language_inadequacy_detection_rate, 0.0)
        self.assertEqual(summary.language_expansion_request_rate, 0.0)
        self.assertTrue(all(decision.language_status == LANGUAGE_UNKNOWN for decision in boundary))
        self.assertTrue(all(decision.selected_probe == MODEL_DISRUPTING_PROBE for decision in boundary))

    def test_boundary_auditor_localizes_language_failure_and_preserves_unknown(self) -> None:
        policy = BoundaryAwareLanguageAuditor()
        policy.fit(self.training)
        decisions, summary = summarize(policy, self.cases)
        by_id = {decision.case_id: decision for decision in decisions}

        self.assertEqual(summary.language_inadequacy_detection_rate, 1.0)
        self.assertEqual(summary.false_language_inadequacy_rate, 0.0)
        self.assertEqual(summary.boundary_nonhallucination_rate, 1.0)
        self.assertEqual(summary.language_expansion_request_rate, 1.0)
        self.assertEqual(summary.false_language_expansion_request_rate, 0.0)
        self.assertEqual(summary.adequate_case_selection_rate, 1.0)
        self.assertEqual(summary.unknown_calibration_rate, 1.0)

        self.assertEqual(by_id["H_ORDER_UP"].language_status, LANGUAGE_INADEQUATE)
        self.assertEqual(by_id["H_ORDER_DOWN"].language_status, LANGUAGE_INADEQUATE)
        self.assertEqual(by_id["H_ORDER_UP"].selected_probe, LANGUAGE_EXPANSION_PROBE)
        self.assertEqual(by_id["H_ORDER_DOWN"].selected_probe, LANGUAGE_EXPANSION_PROBE)
        self.assertEqual(by_id["H_UNKNOWN"].language_status, LANGUAGE_UNKNOWN)
        self.assertEqual(by_id["H_UNKNOWN"].selected_probe, MODEL_DISRUPTING_PROBE)
        self.assertEqual(by_id["H_COMP"].language_status, LANGUAGE_ADEQUATE)
        self.assertEqual(by_id["H_REF"].language_status, LANGUAGE_ADEQUATE)

    def test_expanded_oracle_recovers_raw_distinction_without_counting_as_discovery(self) -> None:
        oracle = ExpandedLanguageOracle()
        oracle.fit(self.training)
        decisions, summary = summarize(oracle, self.cases)
        by_id = {decision.case_id: decision for decision in decisions}
        self.assertEqual(summary.oracle_recoverability_rate, 1.0)
        self.assertEqual(by_id["H_ORDER_UP"].selected_probe, "order_up_probe")
        self.assertEqual(by_id["H_ORDER_DOWN"].selected_probe, "order_down_probe")
        self.assertEqual(oracle.current_language_expression_count, 80)

    def test_raw_history_contains_no_language_failure_semantic_field(self) -> None:
        fields = set(self.training[0].__dataclass_fields__)
        self.assertNotIn("language_failure", fields)
        self.assertNotIn("language_status", fields)
        self.assertNotIn("missing_operator", fields)
        self.assertNotIn("negative_space", fields)


if __name__ == "__main__":
    unittest.main()
