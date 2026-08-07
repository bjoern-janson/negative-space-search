"""History-aware policies for the v0.2 false-escalation benchmark.

These are implementation variants, not new theory objects. Both receive exactly the
same failure history, evidence affordances, and costs.
"""

from __future__ import annotations

import math

from .baselines import (
    Action,
    CausalNegativeSpaceSearch,
    Decision,
    GeneralCausalReasoner,
)
from .environments import EcologyObservation
from .v0_2 import MODEL_PROBE, WITHIN_MODEL_PROBE


def _failure_structure(observation: EcologyObservation) -> tuple[float, float]:
    """Return standardized mean residual and dominant-sign fraction.

    This is deliberately a compact summary of failure structure. It is not an
    epistemic primitive and is visible to both history-aware policies.
    """

    residuals = tuple(float(x) for x in observation.metadata.get("failure_residuals", ()))
    sigma = float(observation.metadata.get("measurement_sigma", 0.0) or 0.0)
    if not residuals or sigma <= 0.0:
        return 0.0, 0.0

    mean = sum(residuals) / len(residuals)
    standard_error = sigma / math.sqrt(len(residuals))
    standardized_mean = abs(mean) / standard_error if standard_error > 0 else 0.0

    positive = sum(value > 0 for value in residuals)
    negative = sum(value < 0 for value in residuals)
    dominant_sign_fraction = max(positive, negative) / len(residuals)
    return standardized_mean, dominant_sign_fraction


def _history_supports_model_escalation(observation: EcologyObservation) -> bool:
    standardized_mean, dominant_sign_fraction = _failure_structure(observation)
    return standardized_mean >= 3.0 and dominant_sign_fraction >= 0.80


class HistoryAwareGeneralCausalReasoner:
    """Strong causal baseline that explicitly conditions evidence selection on H.

    The policy treats persistent standardized model misfit as evidence that a model
    check is warranted. Otherwise it continues targeted inference inside the model.
    """

    name = "history_aware_general_causal_reasoner"

    def __init__(self) -> None:
        self._fallback = GeneralCausalReasoner()

    def decide(self, observation: EcologyObservation) -> Decision:
        if observation.metadata.get("current_causal_vocabulary_residual") or observation.metadata.get(
            "model_adequacy_confirmed"
        ):
            return self._fallback.decide(observation)

        available = set(observation.metadata.get("available_evidence", ()))
        if observation.metadata.get("ordinary_hypotheses_unresolved") and {
            WITHIN_MODEL_PROBE,
            MODEL_PROBE,
        }.issubset(available):
            standardized_mean, dominant_sign_fraction = _failure_structure(observation)
            if _history_supports_model_escalation(observation):
                return Decision(
                    Action.INVESTIGATE,
                    {
                        "persistent_model_misfit": 0.85,
                        "standardized_residual": standardized_mean,
                        "sign_persistence": dominant_sign_fraction,
                    },
                    confidence=0.80,
                    requested_evidence=MODEL_PROBE,
                    predicted_outcome="probe tests whether persistent residual structure reflects model misspecification",
                )
            return Decision(
                Action.INVESTIGATE,
                {
                    "noise_compatible_uncertainty": 0.85,
                    "standardized_residual": standardized_mean,
                    "sign_persistence": dominant_sign_fraction,
                },
                confidence=0.80,
                requested_evidence=WITHIN_MODEL_PROBE,
                predicted_outcome="targeted within-model evidence should reduce uncertainty without model expansion",
            )

        return self._fallback.decide(observation)


class HistoryAwareNegativeSpaceSearch:
    """v0.2 candidate: allocate search attention using failure structure, not count.

    The policy asks whether the observed sequence is still plausible under the
    current causal interface before escalating to model-disrupting evidence.
    """

    name = "history_aware_negative_space_search"

    def __init__(self) -> None:
        self._fallback = CausalNegativeSpaceSearch()

    def decide(self, observation: EcologyObservation) -> Decision:
        if observation.metadata.get("current_causal_vocabulary_residual") or observation.metadata.get(
            "model_adequacy_confirmed"
        ):
            return self._fallback.decide(observation)

        available = set(observation.metadata.get("available_evidence", ()))
        if observation.metadata.get("ordinary_hypotheses_unresolved") and {
            WITHIN_MODEL_PROBE,
            MODEL_PROBE,
        }.issubset(available):
            standardized_mean, dominant_sign_fraction = _failure_structure(observation)
            if _history_supports_model_escalation(observation):
                return Decision(
                    Action.INVESTIGATE,
                    {
                        "current_search_interface_suspect": 0.85,
                        "standardized_residual": standardized_mean,
                        "sign_persistence": dominant_sign_fraction,
                    },
                    confidence=0.80,
                    requested_evidence=MODEL_PROBE,
                    predicted_outcome="model-disrupting evidence tests whether the current causal vocabulary omits a needed distinction",
                )
            return Decision(
                Action.INVESTIGATE,
                {
                    "within_model_uncertainty": 0.85,
                    "standardized_residual": standardized_mean,
                    "sign_persistence": dominant_sign_fraction,
                },
                confidence=0.80,
                requested_evidence=WITHIN_MODEL_PROBE,
                predicted_outcome="failure structure remains compatible with the current model, so reduce ordinary uncertainty first",
            )

        return self._fallback.decide(observation)


V02_PRIMARY_POLICIES = (
    GeneralCausalReasoner(),
    CausalNegativeSpaceSearch(),
    HistoryAwareGeneralCausalReasoner(),
    HistoryAwareNegativeSpaceSearch(),
)
