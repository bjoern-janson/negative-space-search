"""Minimal v0.1 synthetic ecologies.

The simulator is intentionally small. It supplies controlled ground truth, evidence
acquisition, and simple intervention outcomes so the search process can be attacked
without importing real-world ambiguity prematurely.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from .environments import EcologyObservation, LatentCause, SyntheticCase


@dataclass(frozen=True)
class EvidenceResult:
    name: str
    observation: EcologyObservation
    note: str


@dataclass(frozen=True)
class InterventionResult:
    intervention: str
    immediate_external_effect: float
    post_adaptation_external_effect: float
    mechanism: str
    note: str


def canonical_cases() -> tuple[SyntheticCase, ...]:
    """Return exactly the five frozen v0.1 environment families."""

    return (
        SyntheticCase(
            case_id="A_underinvestment",
            observation=EcologyObservation(
                capability="adversarial_validation",
                prevalence=0.10,
                adoption_cost=0.50,
                local_payoff=-0.30,
                external_performance=0.80,
                representation_available=True,
            ),
            latent_causes=(LatentCause.UNDERINVESTMENT,),
            available_interventions=("change_incentives",),
            post_adaptation_state={"external_effect": 0.65},
        ),
        SyntheticCase(
            case_id="B_underrepresentation",
            observation=EcologyObservation(
                capability="failure_mode_coverage",
                prevalence=0.00,
                external_performance=None,
                representation_available=False,
            ),
            latent_causes=(LatentCause.UNDERREPRESENTATION,),
            available_evidence=("interface_probe",),
            available_interventions=("expand_interface",),
        ),
        SyntheticCase(
            case_id="C_justified_selection",
            observation=EcologyObservation(
                capability="high_cost_replication_variant",
                prevalence=0.05,
                adoption_cost=0.40,
                local_payoff=-0.10,
                external_performance=-0.60,
                representation_available=True,
            ),
            latent_causes=(LatentCause.JUSTIFIED_SELECTION,),
            healthy_absence=True,
        ),
        SyntheticCase(
            case_id="D_coordination_failure",
            observation=EcologyObservation(
                capability="shared_validation_infrastructure",
                prevalence=0.10,
                adoption_cost=0.50,
                local_payoff=-0.25,
                external_performance=0.75,
                representation_available=True,
                coordination_threshold=0.60,
            ),
            latent_causes=(LatentCause.COORDINATION_FAILURE,),
            available_evidence=("threshold_test",),
            available_interventions=("coordinate_adoption",),
            post_adaptation_state={"external_effect": 0.55},
        ),
        SyntheticCase(
            case_id="E_model_inadequate",
            observation=EcologyObservation(
                capability="unresolved_ecology_pattern",
                prevalence=0.10,
                adoption_cost=0.20,
                local_payoff=0.00,
                external_performance=None,
                representation_available=True,
                metadata={"residual_pattern": True},
            ),
            latent_causes=(LatentCause.MODEL_INADEQUATE,),
            available_evidence=("cross_interface_probe",),
        ),
    )


def hostile_equivalence_pair() -> tuple[SyntheticCase, SyntheticCase]:
    """Return two worlds with identical initial observations and different causes."""

    shared = EcologyObservation(
        capability="independent_validation",
        prevalence=0.08,
        adoption_cost=0.45,
        local_payoff=-0.20,
        external_performance=None,
        representation_available=True,
        coordination_threshold=None,
        visible_history=(),
    )

    underinvestment = SyntheticCase(
        case_id="hostile_I_underinvestment",
        observation=shared,
        latent_causes=(LatentCause.UNDERINVESTMENT,),
        available_evidence=("controlled_external_value_test",),
        available_interventions=("change_incentives",),
        observational_equivalence_group="hostile_I_vs_S",
    )
    selection = SyntheticCase(
        case_id="hostile_S_justified_selection",
        observation=shared,
        latent_causes=(LatentCause.JUSTIFIED_SELECTION,),
        healthy_absence=True,
        available_evidence=("controlled_external_value_test",),
        observational_equivalence_group="hostile_I_vs_S",
    )
    return underinvestment, selection


def acquire_evidence(case: SyntheticCase, evidence_name: str) -> EvidenceResult:
    """Apply one controlled evidence action and return the newly observable state."""

    if evidence_name not in case.available_evidence:
        raise ValueError(f"evidence action {evidence_name!r} is not available for {case.case_id}")

    cause = case.latent_causes[0]

    if evidence_name == "controlled_external_value_test":
        if cause is LatentCause.UNDERINVESTMENT:
            value = 0.80
            note = "Matched external test shows positive value despite negative local payoff."
        elif cause is LatentCause.JUSTIFIED_SELECTION:
            value = -0.60
            note = "Matched external test confirms that the absent capability degrades performance."
        else:
            raise ValueError("controlled_external_value_test is only defined for the hostile pair")
        return EvidenceResult(
            evidence_name,
            replace(case.observation, external_performance=value),
            note,
        )

    if evidence_name == "interface_probe":
        return EvidenceResult(
            evidence_name,
            replace(
                case.observation,
                metadata={**case.observation.metadata, "missing_distinction_confirmed": True},
            ),
            "Probe confirms that the current interface cannot express the needed distinction.",
        )

    if evidence_name == "threshold_test":
        return EvidenceResult(
            evidence_name,
            replace(
                case.observation,
                metadata={**case.observation.metadata, "threshold_effect_confirmed": True},
            ),
            "External value appears only when coordinated adoption crosses the threshold.",
        )

    if evidence_name == "cross_interface_probe":
        return EvidenceResult(
            evidence_name,
            replace(
                case.observation,
                metadata={**case.observation.metadata, "current_causal_vocabulary_residual": True},
            ),
            "Observed residual cannot be explained by the supplied four ordinary causal hypotheses.",
        )

    raise ValueError(f"no evidence dynamics implemented for {evidence_name!r}")


def apply_intervention(case: SyntheticCase, intervention: str) -> InterventionResult:
    """Return a controlled intervention outcome for the mechanisms used in v0.1."""

    if intervention not in case.available_interventions:
        raise ValueError(f"intervention {intervention!r} is not available for {case.case_id}")

    cause = case.latent_causes[0]

    if cause is LatentCause.UNDERINVESTMENT and intervention == "change_incentives":
        return InterventionResult(
            intervention,
            immediate_external_effect=0.80,
            post_adaptation_external_effect=0.65,
            mechanism="local payoff aligned with externally useful capability",
            note="Benefit persists after a simple population response.",
        )

    if cause is LatentCause.UNDERREPRESENTATION and intervention == "expand_interface":
        return InterventionResult(
            intervention,
            immediate_external_effect=0.60,
            post_adaptation_external_effect=0.60,
            mechanism="new distinction becomes measurable and testable",
            note="The intervention changes observability, not epistemic authority by itself.",
        )

    if cause is LatentCause.COORDINATION_FAILURE and intervention == "coordinate_adoption":
        return InterventionResult(
            intervention,
            immediate_external_effect=0.75,
            post_adaptation_external_effect=0.55,
            mechanism="adoption crosses the coordination threshold",
            note="Unilateral adoption would not produce this effect.",
        )

    raise ValueError(f"no v0.1 intervention dynamics for {case.case_id}: {intervention}")
