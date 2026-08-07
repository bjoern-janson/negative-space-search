from __future__ import annotations

import unittest
from collections import defaultdict

from negative_space_search.evaluation_v0_7 import summarize
from negative_space_search.language_boundary_v0_6 import current_language_signature
from negative_space_search.operator_discovery_v0_7 import (
    AlwaysExpandGenericSynthesizer,
    BoundaryGatedGenericSynthesizer,
    BoundaryOnlyAuditorV07,
    ConservativeAbstainerV07,
    CurrentLanguageAssimilatorV07,
    current_language_expression_count,
    generated_predicates,
    held_out_cases,
    numeric_expressions,
    training_episodes,
)


class V07OperatorDiscoveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.training = training_episodes()
        self.cases = held_out_cases()

    def test_frozen_ids(self) -> None:
        self.assertEqual(len(self.training), 20)
        self.assertEqual(
            [case.case_id for case in self.cases],
            ["H_A", "H_R", "H_DF", "H_DR", "H_CH", "H_EH", "H_UNKNOWN"],
        )

    def test_error_magnitude_is_non_identifying(self) -> None:
        self.assertEqual({round(episode.error, 8) for episode in self.training}, {0.6})
        self.assertEqual({round(case.error, 8) for case in self.cases}, {0.6})

    def test_current_language_remains_frozen_v06_language(self) -> None:
        self.assertEqual(current_language_expression_count(), 78)

    def test_generic_meta_language_has_no_constants_or_semantic_target_names(self) -> None:
        numeric = numeric_expressions()
        predicates = generated_predicates()
        self.assertEqual(len(numeric), 26)
        self.assertEqual(len(predicates), 1300)
        joined = " ".join(expression.name for expression in predicates)
        for forbidden in (
            "direction", "center", "edge", "trace", "increasing", "decreasing",
            "frequency", "phase", "dependency", "0.5", "1.0",
        ):
            self.assertNotIn(forbidden, joined)

    def test_two_independent_current_language_collisions_are_frozen(self) -> None:
        grouped: dict[tuple[bool, ...], set[str]] = defaultdict(set)
        ids_by_signature: dict[tuple[bool, ...], list[str]] = defaultdict(list)
        for episode in self.training:
            signature = current_language_signature(episode)
            grouped[signature].add(episode.resolving_probe)
            ids_by_signature[signature].append(episode.episode_id)

        collisions = [labels for labels in grouped.values() if len(labels) > 1]
        self.assertEqual(len(collisions), 2)
        self.assertIn(
            {"direction_forward_probe", "direction_reverse_probe"},
            collisions,
        )
        self.assertIn(
            {"center_heavy_probe", "edge_heavy_probe"},
            collisions,
        )

        direction_signature = next(
            signature for signature, ids in ids_by_signature.items()
            if "T_DF1" in ids
        )
        center_signature = next(
            signature for signature, ids in ids_by_signature.items()
            if "T_CH1" in ids
        )
        self.assertNotEqual(direction_signature, center_signature)

    def test_hostile_heldouts_preserve_current_language_collisions(self) -> None:
        by_id = {case.case_id: case for case in self.cases}
        self.assertEqual(
            current_language_signature(by_id["H_DF"]),
            current_language_signature(by_id["H_DR"]),
        )
        self.assertEqual(
            current_language_signature(by_id["H_CH"]),
            current_language_signature(by_id["H_EH"]),
        )
        self.assertNotEqual(
            current_language_signature(by_id["H_DF"]),
            current_language_signature(by_id["H_CH"]),
        )

    def test_heldout_hostile_traces_are_not_training_duplicates(self) -> None:
        training_traces = {episode.ordered_trace for episode in self.training}
        for case in self.cases:
            if case.case_id in {"H_DF", "H_DR", "H_CH", "H_EH"}:
                self.assertNotIn(case.ordered_trace, training_traces)

    def test_gated_synthesizer_constructs_two_distinct_abstraction_families(self) -> None:
        policy = BoundaryGatedGenericSynthesizer()
        policy.fit(self.training)
        operators = {probe: op.name for probe, op in policy.generated_operators.items()}
        self.assertEqual(
            operators["direction_forward_probe"],
            "GT(t3,t0)",
        )
        self.assertEqual(
            operators["direction_reverse_probe"],
            "GT(t0,t3)",
        )
        self.assertEqual(
            operators["center_heavy_probe"],
            "GT(ADD(t1,t2),ADD(t0,t3))",
        )
        self.assertEqual(
            operators["edge_heavy_probe"],
            "GT(ADD(t0,t3),ADD(t1,t2))",
        )

    def test_boundary_gated_repair_transfers_on_both_families(self) -> None:
        policy = BoundaryGatedGenericSynthesizer()
        policy.fit(self.training)
        _, summary = summarize(policy, self.cases)
        self.assertEqual(summary.boundary_detection_rate, 1.0)
        self.assertEqual(summary.construction_success_rate, 1.0)
        self.assertEqual(summary.held_out_repair_selection_rate, 1.0)
        self.assertEqual(summary.multi_family_transfer_rate, 1.0)
        self.assertEqual(summary.q_invention, 1.0)
        self.assertEqual(summary.false_expansion_rate, 0.0)
        self.assertEqual(summary.adequate_case_preservation_rate, 1.0)
        self.assertEqual(summary.unknown_calibration_rate, 1.0)

    def test_always_expand_matches_repair_but_costs_more_search(self) -> None:
        gated = BoundaryGatedGenericSynthesizer()
        always = AlwaysExpandGenericSynthesizer()
        gated.fit(self.training)
        always.fit(self.training)
        _, gated_summary = summarize(gated, self.cases)
        _, always_summary = summarize(always, self.cases)

        self.assertEqual(gated_summary.held_out_repair_selection_rate, 1.0)
        self.assertEqual(always_summary.held_out_repair_selection_rate, 1.0)
        self.assertEqual(gated.generated_operators, always.generated_operators)
        self.assertEqual(gated_summary.representation_cost, always_summary.representation_cost)
        self.assertEqual(gated_summary.search_cost, 5200)
        self.assertEqual(always_summary.search_cost, 7800)
        self.assertLess(gated_summary.search_cost, always_summary.search_cost)
        self.assertEqual(gated_summary.false_expansion_rate, 0.0)
        self.assertEqual(always_summary.false_expansion_rate, 1.0)

    def test_controls_separate_assimilation_abstention_boundary_and_repair(self) -> None:
        assimilator = CurrentLanguageAssimilatorV07()
        abstainer = ConservativeAbstainerV07()
        boundary = BoundaryOnlyAuditorV07()
        for policy in (assimilator, abstainer, boundary):
            policy.fit(self.training)

        _, assimilator_summary = summarize(assimilator, self.cases)
        _, abstainer_summary = summarize(abstainer, self.cases)
        _, boundary_summary = summarize(boundary, self.cases)

        self.assertGreater(assimilator_summary.false_assimilation_rate, 0.0)
        self.assertEqual(abstainer_summary.false_assimilation_rate, 0.0)
        self.assertEqual(boundary_summary.false_assimilation_rate, 0.0)
        self.assertEqual(abstainer_summary.held_out_repair_selection_rate, 0.0)
        self.assertEqual(boundary_summary.held_out_repair_selection_rate, 0.0)
        self.assertEqual(boundary_summary.boundary_detection_rate, 1.0)
        self.assertEqual(boundary_summary.construction_success_rate, 0.0)

    def test_unknown_does_not_trigger_gated_synthesis(self) -> None:
        policy = BoundaryGatedGenericSynthesizer()
        policy.fit(self.training)
        decisions, summary = summarize(policy, self.cases)
        unknown = next(decision for decision in decisions if decision.case_id == "H_UNKNOWN")
        self.assertEqual(unknown.language_status, "unknown")
        self.assertEqual(unknown.selected_probe, "model_disrupting_probe")
        self.assertFalse(unknown.used_generated_operator)
        self.assertEqual(summary.unknown_calibration_rate, 1.0)


if __name__ == "__main__":
    unittest.main()
