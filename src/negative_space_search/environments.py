"""Controlled latent-cause records for the initial synthetic benchmark.

This module defines data, not a full simulator. Environment dynamics should be added
only when an experiment requires them.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


class LatentCause(str, Enum):
    """Initial controlled causes of an observed absence."""

    UNDERINVESTMENT = "underinvestment"
    UNDERREPRESENTATION = "underrepresentation"
    JUSTIFIED_SELECTION = "justified_selection"
    COORDINATION_FAILURE = "coordination_failure"
    MODEL_INADEQUATE = "model_inadequate"


@dataclass(frozen=True)
class EcologyObservation:
    """Observable state supplied to every search policy under matched conditions."""

    capability: str
    prevalence: float
    adoption_cost: float | None = None
    local_payoff: float | None = None
    external_performance: float | None = None
    representation_available: bool | None = None
    coordination_threshold: float | None = None
    visible_history: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SyntheticCase:
    """One benchmark case with hidden causal ground truth.

    `latent_causes` may contain multiple ordinary causes. MODEL_INADEQUATE should be
    used only for cases whose generating mechanism is intentionally outside the
    supplied causal vocabulary.
    """

    case_id: str
    observation: EcologyObservation
    latent_causes: tuple[LatentCause, ...]
    healthy_absence: bool = False
    observational_equivalence_group: str | None = None
    available_evidence: tuple[str, ...] = ()
    available_interventions: tuple[str, ...] = ()
    counterfactuals: Mapping[str, Any] = field(default_factory=dict)
    post_adaptation_state: Mapping[str, Any] = field(default_factory=dict)
