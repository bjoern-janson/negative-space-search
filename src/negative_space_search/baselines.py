"""Minimal baseline policies for the initial benchmark.

These implementations are intentionally simple. Their purpose is to make the first
comparison executable without hiding complexity inside a framework abstraction.
"""

from __future__ import annotations

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


class GapHeuristic:
    name = "gap_heuristic"

    def decide(self, observation: EcologyObservation) -> Decision:
        if observation.prevalence < 0.25:
            return Decision(
                Action.INTERVENE,
                {"unspecified_gap": 1.0},
                confidence=0.60,
                intervention="increase adoption",
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
                requested_evidence="test the low-prevalence capability under matched external conditions",
                predicted_outcome="novel capability may reveal unmeasured value",
            )
        return Decision(Action.PRESERVE, {"novelty": novelty}, confidence=0.55)


class PerformanceHeuristic:
    name = "performance_heuristic"

    def decide(self, observation: EcologyObservation) -> Decision:
        if observation.external_performance is None:
            return Decision(
                Action.INVESTIGATE,
                {"performance_unknown": 1.0},
                confidence=0.50,
                requested_evidence="measure external performance of the absent capability",
            )
        if observation.external_performance > 0:
            return Decision(
                Action.INTERVENE,
                {"positive_external_performance": 1.0},
                confidence=0.70,
                intervention="increase adoption",
                predicted_outcome="external performance improves",
            )
        return Decision(
            Action.PRESERVE,
            {"nonpositive_external_performance": 1.0},
            confidence=0.70,
        )


class SelfConfirmingOpportunitySearch:
    """Adversarial baseline: interprets low prevalence as latent opportunity."""

    name = "self_confirming_opportunity_search"

    def decide(self, observation: EcologyObservation) -> Decision:
        opportunity = 1.0 - max(0.0, min(1.0, observation.prevalence))
        return Decision(
            Action.INTERVENE,
            {"latent_opportunity": opportunity},
            confidence=max(0.50, opportunity),
            intervention="promote the absent capability",
            predicted_outcome="neglect was masking useful capability",
        )


class CausalNegativeSpaceSearch:
    """Minimal causal-search baseline for v0.1.

    This is not intended as the final proposed method. It encodes the initial design
    claim in the smallest inspectable policy: distinguish obvious healthy absence,
    detect missing representation, test coordination/incentive ambiguity, and abstain
    when the observable state does not identify a cause.
    """

    name = "causal_negative_space_search"

    def decide(self, observation: EcologyObservation) -> Decision:
        if observation.representation_available is False:
            return Decision(
                Action.INTERVENE,
                {"underrepresentation": 0.85},
                confidence=0.85,
                intervention="expand measurement or representation",
                predicted_outcome="the previously unavailable distinction becomes testable",
            )

        if observation.external_performance is not None and observation.external_performance <= 0:
            return Decision(
                Action.PRESERVE,
                {"justified_selection": 0.80},
                confidence=0.80,
                predicted_outcome="preserving the absence avoids a low-value intervention",
            )

        if observation.coordination_threshold is not None and observation.coordination_threshold > 0:
            return Decision(
                Action.INVESTIGATE,
                {"coordination_failure": 0.55, "underinvestment": 0.45},
                confidence=0.60,
                requested_evidence="compare unilateral adoption with adoption above the coordination threshold",
                predicted_outcome="the intervention effect differs across adoption regimes",
            )

        if observation.local_payoff is not None and observation.local_payoff < 0:
            return Decision(
                Action.INVESTIGATE,
                {"underinvestment": 0.65, "justified_selection": 0.35},
                confidence=0.60,
                requested_evidence="measure external value while holding local adoption cost constant",
                predicted_outcome="external value distinguishes suppressed capability from justified rejection",
            )

        return Decision(
            Action.ABSTAIN,
            {"unidentified": 1.0},
            confidence=0.40,
            requested_evidence="seek an observation that discriminates the leading causal explanations",
        )


INITIAL_BASELINES: tuple[SearchPolicy, ...] = (
    GapHeuristic(),
    NoveltyHeuristic(),
    PerformanceHeuristic(),
    SelfConfirmingOpportunitySearch(),
    CausalNegativeSpaceSearch(),
)
