from __future__ import annotations

import unittest

from negative_space_search.basis_v0_5 import (
    BASIS_ADEQUACY_THRESHOLD,
    AlwaysComposeLearner,
    FixedCompositionOracle,
    FixedSingleBasisSelector,
    GatedBasisRepairLearner,
    _conjunction_expressions,
    _single_expressions,
    held_out_cases,
    training_episodes,
)
from negative_space_search.evaluation_v0_5 import TARGET_RELATION, summarize


class V05BasisFailureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.training = training_episodes()
        self.cases = held_out_cases()

    def test_frozen_ids(self) -> None:
        self.assertEqual(
            [episode.episode_id for episode in self.training],
            [
                "T_I1", "T_I2", "T_I3", "T_I4",
                "T_D1", "T_D2", "T_D3",
                "T_P1", "T_P2", "T_P3",
                "T_N1", "T_N2", "T_N3",
            ],
        )
        self.assertEqual(
            [case.case_id for case in self.cases],
            ["H_INT_1", "H_INT_2", "H_DEP_ONLY", "H_PAY_ONLY", "H_TOPOLOGY", "H_NOVEL"],
        )

    def test_error_magnitude_is_non_identifying(self) -> None:
        self.assertEqual({round(episode.error, 8) for episode in self.training}, {0.6})
        self.assertEqual({round(case.error, 8) for case in self.cases}, {0.6})

    def test_initial_basis_contains_no_conjunctions(self) -> None:
        self.assertTrue(all(not expression.name.startswith("AND(") for expression in _single_expressions()))
        self.assertIn(TARGET_RELATION, {expression.name for expression in _conjunction_expressions()})

    def test_single_basis_localizes_only_interaction_as_inadequate(self) -> None:
        policy = FixedSingleBasisSelector()
        policy.fit(self.training)
        audits = {audit.probe: audit for audit in policy.audits}
        self.assertLess(audits["interaction_probe"].best_single_balanced_accuracy, BASIS_ADEQUACY_THRESHOLD)
        self.assertAlmostEqual(audits["interaction_probe"].best_single_balanced_accuracy, 5.0 / 6.0)
        self.assertTrue(audits["interaction_probe"].basis_inadequate)
        for probe in ("independence_probe", "payoff_regime_probe", "topology_probe"):
            self.assertEqual(audits[probe].best_single_balanced_accuracy, 1.0)
            self.assertFalse(audits[probe].basis_inadequate)

    def test_fixed_single_basis_detects_but_cannot_repair(self) -> None:
        policy = FixedSingleBasisSelector()
        policy.fit(self.training)
        _, summary = summarize(policy, self.cases)
        self.assertEqual(summary.basis_inadequacy_detection_rate, 1.0)
        self.assertEqual(summary.basis_expansion_rate, 0.0)
        self.assertEqual(summary.construction_success_rate, 0.0)
        self.assertLess(summary.held_out_evidence_selection_rate, 1.0)

    def test_gated_learner_expands_only_inadequate_probe(self) -> None:
        policy = GatedBasisRepairLearner()
        policy.fit(self.training)
        audits = {audit.probe: audit for audit in policy.audits}
        self.assertEqual(
            {probe for probe, audit in audits.items() if audit.expanded},
            {"interaction_probe"},
        )
        self.assertEqual(audits["interaction_probe"].selected_relation, TARGET_RELATION)
        self.assertEqual(audits["interaction_probe"].selected_balanced_accuracy, 1.0)

    def test_gated_repair_transfers_and_rejects_constituent_false_positives(self) -> None:
        policy = GatedBasisRepairLearner()
        policy.fit(self.training)
        _, summary = summarize(policy, self.cases)
        self.assertEqual(summary.held_out_evidence_selection_rate, 1.0)
        self.assertEqual(summary.interaction_transfer_rate, 1.0)
        self.assertEqual(summary.constituent_false_positive_rate, 0.0)
        self.assertEqual(summary.novel_model_check_rate, 1.0)

    def test_always_compose_matches_transfer_but_costs_more_search(self) -> None:
        gated = GatedBasisRepairLearner()
        brute = AlwaysComposeLearner()
        gated.fit(self.training)
        brute.fit(self.training)
        _, gated_summary = summarize(gated, self.cases)
        _, brute_summary = summarize(brute, self.cases)
        self.assertEqual(gated_summary.held_out_evidence_selection_rate, 1.0)
        self.assertEqual(brute_summary.held_out_evidence_selection_rate, 1.0)
        self.assertLess(gated_summary.search_cost, brute_summary.search_cost)
        self.assertEqual(gated_summary.representation_cost, brute_summary.representation_cost)

    def test_fixed_oracle_is_upper_bound_not_a_learned_repair(self) -> None:
        oracle = FixedCompositionOracle()
        gated = GatedBasisRepairLearner()
        oracle.fit(self.training)
        gated.fit(self.training)
        oracle_decisions, oracle_summary = summarize(oracle, self.cases)
        gated_decisions, gated_summary = summarize(gated, self.cases)
        self.assertEqual(oracle_summary.held_out_evidence_selection_rate, 1.0)
        self.assertEqual(
            [decision.selected_probe for decision in oracle_decisions],
            [decision.selected_probe for decision in gated_decisions],
        )
        self.assertEqual(gated_summary.representation_cost, oracle_summary.representation_cost)

    def test_raw_history_contains_no_basis_failure_semantic_field(self) -> None:
        fields = set(self.training[0].__dataclass_fields__)
        self.assertNotIn("basis_failure", fields)
        self.assertNotIn("interaction", fields)
        self.assertNotIn("negative_space", fields)
        self.assertNotIn("conjunction_required", fields)


if __name__ == "__main__":
    unittest.main()
