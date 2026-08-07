from __future__ import annotations

import unittest

from negative_space_search.baselines import CausalNegativeSpaceSearch, GeneralCausalReasoner
from negative_space_search.v0_2 import MODEL_PROBE, false_escalation_cases, score_v0_2_cases, summarize_v0_2
from negative_space_search.v0_2_policies import (
    HistoryAwareGeneralCausalReasoner,
    HistoryAwareNegativeSpaceSearch,
)


class V02EnvironmentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cases = false_escalation_cases()

    def test_case_matrix_has_four_development_and_four_held_out_cases(self) -> None:
        self.assertEqual(len(self.cases), 8)
        self.assertEqual(
            sum(case.observation.metadata["split"] == "development" for case in self.cases),
            4,
        )
        self.assertEqual(
            sum(case.observation.metadata["split"] == "held_out" for case in self.cases),
            4,
        )

    def test_each_matched_pair_has_equal_failure_count_and_probe_cost(self) -> None:
        by_key: dict[tuple[str, str], list] = {}
        for case in self.cases:
            key = (str(case.observation.metadata["split"]), str(case.observation.metadata["v0_2_pair"]))
            by_key.setdefault(key, []).append(case)

        self.assertEqual(len(by_key), 4)
        for pair in by_key.values():
            self.assertEqual(len(pair), 2)
            failure_counts = {len(case.observation.metadata["failure_residuals"]) for case in pair}
            probe_costs = {
                case.observation.metadata["evidence_costs"][MODEL_PROBE] for case in pair
            }
            self.assertEqual(len(failure_counts), 1)
            self.assertEqual(len(probe_costs), 1)


class V02PolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cases = false_escalation_cases()

    def test_frozen_v011_negative_space_policy_false_escalates(self) -> None:
        summary = summarize_v0_2(score_v0_2_cases(CausalNegativeSpaceSearch(), self.cases))
        self.assertEqual(summary["true_escalation_rate"], 1.0)
        self.assertEqual(summary["false_escalation_rate"], 1.0)

    def test_frozen_general_causal_policy_never_escalates(self) -> None:
        summary = summarize_v0_2(score_v0_2_cases(GeneralCausalReasoner(), self.cases))
        self.assertEqual(summary["true_escalation_rate"], 0.0)
        self.assertEqual(summary["false_escalation_rate"], 0.0)

    def test_history_aware_negative_space_policy_is_selective_on_held_out_cases(self) -> None:
        scores = score_v0_2_cases(HistoryAwareNegativeSpaceSearch(), self.cases)
        summary = summarize_v0_2(scores)
        self.assertEqual(summary["true_escalation_rate"], 1.0)
        self.assertEqual(summary["false_escalation_rate"], 0.0)
        self.assertEqual(summary["held_out_correct_evidence_selection_rate"], 1.0)

    def test_same_sign_low_power_case_does_not_trigger_escalation(self) -> None:
        case = next(case for case in self.cases if case.case_id == "held_U_1")
        decision = HistoryAwareNegativeSpaceSearch().decide(case.observation)
        self.assertNotEqual(decision.requested_evidence, MODEL_PROBE)

    def test_history_aware_strong_causal_competitor_gets_same_primary_selection_result(self) -> None:
        ns_summary = summarize_v0_2(
            score_v0_2_cases(HistoryAwareNegativeSpaceSearch(), self.cases)
        )
        causal_summary = summarize_v0_2(
            score_v0_2_cases(HistoryAwareGeneralCausalReasoner(), self.cases)
        )
        for key in (
            "true_escalation_rate",
            "false_escalation_rate",
            "correct_evidence_selection_rate",
            "held_out_correct_evidence_selection_rate",
            "post_evidence_regime_interpretation_rate",
            "evidence_cost",
        ):
            self.assertEqual(ns_summary[key], causal_summary[key])

    def test_post_evidence_interpretation_is_not_the_discriminator(self) -> None:
        for policy in (
            GeneralCausalReasoner(),
            CausalNegativeSpaceSearch(),
            HistoryAwareGeneralCausalReasoner(),
            HistoryAwareNegativeSpaceSearch(),
        ):
            summary = summarize_v0_2(score_v0_2_cases(policy, self.cases))
            self.assertEqual(summary["post_evidence_regime_interpretation_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()
