from __future__ import annotations

import unittest

from negative_space_search.baselines import (
    Action,
    CausalNegativeSpaceSearch,
    GapHeuristic,
    GeneralCausalReasoner,
    SelfConfirmingOpportunitySearch,
)
from negative_space_search.evaluation import score_hostile_pair, score_model_adequacy_pair
from negative_space_search.simulator import (
    acquire_evidence,
    canonical_cases,
    hostile_equivalence_pair,
    model_adequacy_pair,
)


class V01EnvironmentTests(unittest.TestCase):
    def test_exactly_five_canonical_environment_families(self) -> None:
        cases = canonical_cases()
        self.assertEqual(
            [case.case_id for case in cases],
            [
                "A_underinvestment",
                "B_underrepresentation",
                "C_justified_selection",
                "D_coordination_failure",
                "E_model_inadequate",
            ],
        )

    def test_hostile_pair_is_initially_observationally_equivalent(self) -> None:
        underinvestment, selection = hostile_equivalence_pair()
        self.assertEqual(underinvestment.observation, selection.observation)
        self.assertNotEqual(underinvestment.latent_causes, selection.latent_causes)

    def test_hostile_evidence_discriminates_the_two_worlds(self) -> None:
        underinvestment, selection = hostile_equivalence_pair()
        evidence = "controlled_external_value_test"

        observed_i = acquire_evidence(underinvestment, evidence).observation
        observed_s = acquire_evidence(selection, evidence).observation

        self.assertGreater(observed_i.external_performance or 0.0, 0.0)
        self.assertLess(observed_s.external_performance or 0.0, 0.0)


class V011ModelAdequacyEnvironmentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.within_model, self.model_inadequate = model_adequacy_pair()

    def test_model_adequacy_pair_is_initially_observationally_equivalent(self) -> None:
        self.assertEqual(self.within_model.observation, self.model_inadequate.observation)
        self.assertNotEqual(self.within_model.latent_causes, self.model_inadequate.latent_causes)
        self.assertEqual(self.within_model.available_evidence, self.model_inadequate.available_evidence)

    def test_more_ordinary_data_does_not_discriminate_model_adequacy(self) -> None:
        first = acquire_evidence(self.within_model, "ordinary_discriminator").observation
        second = acquire_evidence(self.model_inadequate, "ordinary_discriminator").observation
        self.assertEqual(first, second)

    def test_model_disrupting_probe_discriminates_regime(self) -> None:
        first = acquire_evidence(self.within_model, "model_disrupting_probe").observation
        second = acquire_evidence(self.model_inadequate, "model_disrupting_probe").observation
        self.assertTrue(first.metadata.get("model_adequacy_confirmed"))
        self.assertFalse(first.metadata.get("current_causal_vocabulary_residual", False))
        self.assertTrue(second.metadata.get("current_causal_vocabulary_residual"))
        self.assertNotEqual(first, second)


class V01PolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.underinvestment, self.selection = hostile_equivalence_pair()

    def test_general_causal_reasoner_does_not_guess_hostile_pair(self) -> None:
        score = score_hostile_pair(
            GeneralCausalReasoner(), self.underinvestment, self.selection
        )
        self.assertTrue(score.passed)

    def test_negative_space_search_does_not_guess_hostile_pair(self) -> None:
        score = score_hostile_pair(
            CausalNegativeSpaceSearch(), self.underinvestment, self.selection
        )
        self.assertTrue(score.passed)

    def test_gap_heuristic_fails_hostile_pair_by_intervening(self) -> None:
        score = score_hostile_pair(GapHeuristic(), self.underinvestment, self.selection)
        self.assertFalse(score.passed)

    def test_self_confirming_detector_fails_hostile_pair(self) -> None:
        score = score_hostile_pair(
            SelfConfirmingOpportunitySearch(), self.underinvestment, self.selection
        )
        self.assertFalse(score.passed)

    def test_negative_space_search_preserves_visible_healthy_absence(self) -> None:
        selection_case = canonical_cases()[2]
        decision = CausalNegativeSpaceSearch().decide(selection_case.observation)
        self.assertIs(decision.action, Action.PRESERVE)


class V011ModelAdequacyPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.within_model, self.model_inadequate = model_adequacy_pair()

    def test_negative_space_search_requests_model_adequacy_probe(self) -> None:
        score = score_model_adequacy_pair(
            CausalNegativeSpaceSearch(), self.within_model, self.model_inadequate
        )
        self.assertTrue(score.passed)

    def test_general_causal_reasoner_uses_more_within_model_data(self) -> None:
        score = score_model_adequacy_pair(
            GeneralCausalReasoner(), self.within_model, self.model_inadequate
        )
        self.assertFalse(score.model_adequacy_probe_requested)
        self.assertTrue(score.within_model_after_probe_correct)
        self.assertTrue(score.model_inadequacy_after_probe_correct)
        self.assertFalse(score.passed)


if __name__ == "__main__":
    unittest.main()
