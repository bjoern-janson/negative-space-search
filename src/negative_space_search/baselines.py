"""Baseline search policies for the initial benchmark.

All policies receive the same observable state. The causal negative-space policy is
not granted privileged evidence or actions.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Protocol

from .environments import EcologyObservation


class Action(str, Enum):
    INTERVENE = "intervene"
    PRESERVE = "preserve"
    INVESTIGATE = "investigate"
    ABSTAIN = "abstain"


@dataclass(frozen=True)
class Decision:
    action: Action
    diagnosis: Mapping[str, float]
    confidence: float
    requested_evidence: str | None = None
    intervention: str | None = None
    predicted_outcome: str | None = None


class SearchPolicy(Protocol):
    name: str

    def decide(self, observation: EcologyObservation) -> Decision:
        """Return the next epistemic action from the matched observable state."""
        ...


class RandomAction:
    """Seeded sanity baseline."""

    name = "random_action"

    def __init__(self, seed: int = 0) -> None:
        self._rng = random.Random(seed)

    def decide(self, observation: EcologyObservation) -> Decision:
        action = self._rng.choice(tuple(Action))
        return Decision(action, {"random": 1.0}, confidence=0.25)


class GapHeuristic:
    name = "gap_heuristic"

    def decide(self, observation: EcologyObservation) -> Decision:
        if observation.prevalence < 0.25:
            return Decision(
                Action.INTERVENE,
                {"unspecified_gap": 1.0},
                confidence=0.60,
                intervention="increase_adoption",
                predicted_outcome="the missing capability becomes more prevalent",
            )
        return Decision(Action.PRESERVE, {"no_gap": 1.0}, confidence=0.60)


class NoveltyHeuristic:
    name = "novelty_heuristic"

    def decide(self, observation: EcologyObservation) -> Decision:
        novelty = 1.0 - max(0.0, min(1.0, observation.prevalence))
        if novelty >= 0.70:
            return Decision(
                Action.INVESTIGATE,
                {"novelty": novelty},
                confidence=novelty,
                requested_evidence="test low-prevalence capability under matched external conditions",
                predicted_outcome="rare capability may reveal unmeasured value",
            )
        return Decision(Action.PRESERVE, {"novelty": novelty}, confidence=0.55)


class PerformanceHeuristic:
    """Optimizes the currently visible short-term external performance signal."""

    name = "performance_heuristic"

    def decide(self, observation: EcologyObservation) -> Decision:
        if observation.external_performance is None:
            return Decision(
                Action.INVESTIGATE,
                {"performance_unknown": 1.0},
                confidence=0.50,
                requested_evidence="measure_external_performance",
                predicted_outcome="external measurement resolves short-term value",
            )
        if observation.external_performance > 0:
            return Decision(
                Action.INTERVENE,
                {"positive_external_performance": 1.0},
                confidence=0.70,
                intervention="increase_adoption",
                predicted_outcome="short-term external performance improves",
            )
        return Decision(
            Action.PRESERVE,
            {"nonpositive_external_performance": 1.0},
            confidence=0.70,
        )


class SelfConfirmingOpportunitySearch:
    """Adversarial baseline: low prevalence is treated as evidence of opportunity."""

    name = "self_confirming_opportunity_search"

    def decide(self, observation: EcologyObservation) -> Decision:
        opportunity = 1.0 - max(0.0, min(1.0, observation.prevalence))
        return Decision(
            Action.INTERVENE,
            {"latent_opportunity": opportunity},
            confidence=max(0.50, opportunity),
            intervention="promote_absent_capability",
            predicted_outcome="neglect was masking useful capability",
        )


class GeneralCausalReasoner:
    """Strong matched competitor using ordinary causal decision rules.

    It does not assume that negative space is intrinsically informative. It simply
    reasons over the observable causal features and requests discriminating evidence
    when the available state is not identifying.
    """

    name = "general_causal_reasoner"

    def decide(self, observation: EcologyObservation) -> Decision:
        if observation.metadata.get("current_causal_vocabulary_residual"):
            return Decision(
                Action.ABSTAIN,
                {"model_inadequacy": 0.85},
                confidence=0.85,
                requested_evidence="cross_interface_probe",
                predicted_outcome="additional representation is required before causal action",
            )

        if observation.representation_available is False:
            return Decision(
                Action.INVESTIGATE,
                {"representation_failure": 0.85},
                confidence=0.85,
                requested_evidence="interface_probe",
                predicted_outcome="probe determines which distinction the current interface cannot express",
            )

        if observation.external_performance is not None:
            if observation.external_performance <= 0:
                return Decision(
                    Action.PRESERVE,
                    {"evidence_against_intervention": 0.85},
                    confidence=0.85,
                )
            if observation.coordination_threshold is not None:
                return Decision(
                    Action.INVESTIGATE,
                    {"coordination_or_payoff": 0.70},
                    confidence=0.70,
                    requested_evidence="threshold_test",
                    predicted_outcome="threshold test distinguishes unilateral from coordinated value",
                )
            if observation.local_payoff is not None and observation.local_payoff < 0:
                return Decision(
                    Action.INTERVENE,
                    {"payoff_misalignment": 0.80},
                    confidence=0.80,
                    intervention="change_incentives",
                    predicted_outcome="adoption rises while external value remains positive",
                )

        if observation.coordination_threshold is not None:
            return Decision(
                Action.INVESTIGATE,
                {"coordination_possible": 0.60},
                confidence=0.60,
                requested_evidence="threshold_test",
                predicted_outcome="test reveals whether value depends on coordinated adoption",
            )

        if observation.external_performance is None:
            return Decision(
                Action.INVESTIGATE,
                {"underinvestment": 0.50, "justified_selection": 0.50},
                confidence=0.50,
                requested_evidence="controlled_external_value_test",
                predicted_outcome="matched external test discriminates suppressed value from justified rejection",
            )

        return Decision(Action.ABSTAIN, {"unresolved": 1.0}, confidence=0.35)


class CausalNegativeSpaceSearch:
    """Minimal explicit causal negative-space policy for v0.1.

    This implementation is intentionally inspectable. It treats absence as a causal
    inference problem, preserves healthy absence, requests discriminating evidence
    under observational equivalence, and refuses to turn model inadequacy into an
    ordinary causal bucket.
    """

    name = "causal_negative_space_search"

    def decide(self, observation: EcologyObservation) -> Decision:
        if observation.metadata.get("current_causal_vocabulary_residual"):
            return Decision(
                Action.ABSTAIN,
                {"current_vocabulary_inadequate": 0.90},
                confidence=0.90,
                requested_evidence="cross_interface_probe",
                predicted_outcome="new observations are required before extending the causal vocabulary",
            )

        if observation.representation_available is False:
            return Decision(
                Action.INVESTIGATE,
                {"underrepresentation": 0.85},
                confidence=0.85,
                requested_evidence="interface_probe",
                predicted_outcome="probe identifies the missing representational distinction",
            )

        if observation.external_performance is not None and observation.external_performance <= 0:
            return Decision(
                Action.PRESERVE,
                {"justified_selection": 0.85},
                confidence=0.85,
                predicted_outcome="preserving the absence avoids a low-value intervention",
            )

        if observation.coordination_threshold is not None and observation.coordination_threshold > 0:
            return Decision(
                Action.INVESTIGATE,
                {"coordination_failure": 0.60, "underinvestment": 0.40},
                confidence=0.65,
                requested_evidence="threshold_test",
                predicted_outcome="effect differs between unilateral and coordinated adoption regimes",
            )

        if observation.external_performance is not None and observation.external_performance > 0:
            if observation.local_payoff is not None and observation.local_payoff < 0:
                return Decision(
                    Action.INTERVENE,
                    {"underinvestment": 0.85},
                    confidence=0.85,
                    intervention="change_incentives",
                    predicted_outcome="local adoption rises without losing external value",
                )

        if observation.local_payoff is not None and observation.local_payoff < 0:
            return Decision(
                Action.INVESTIGATE,
                {"underinvestment": 0.50, "justified_selection": 0.50},
                confidence=0.50,
                requested_evidence="controlled_external_value_test",
                predicted_outcome="external value distinguishes suppressed capability from justified rejection",
            )

        return Decision(
            Action.ABSTAIN,
            {"unidentified": 1.0},
            confidence=0.35,
            requested_evidence="seek an observation that discriminates the leading causal explanations",
        )


INITIAL_BASELINES: tuple[SearchPolicy, ...] = (
    RandomAction(seed=0),
    GapHeuristic(),
    NoveltyHeuristic(),
    PerformanceHeuristic(),
    SelfConfirmingOpportunitySearch(),
    GeneralCausalReasoner(),
    CausalNegativeSpaceSearch(),
)
