"""v0.2 false-escalation benchmark.

The benchmark asks whether a search policy responds to the structure of repeated
failure rather than merely its count. It preserves the v0.1/v0.1.1 modules and
adds no new theory primitive.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Iterable

from .baselines import Action, SearchPolicy
from .environments import EcologyObservation, LatentCause, SyntheticCase


MODEL_PROBE = "model_disrupting_probe"
WITHIN_MODEL_PROBE = "ordinary_discriminator"


@dataclass(frozen=True)
class V02EvidenceResult:
    name: str
    observation: EcologyObservation
    cost: float
    note: str


@dataclass(frozen=True)
class V02CaseScore:
    case_id: str
    split: str
    regime: str
    policy: str
    selected_evidence: str | None
    expected_evidence: str
    correct_evidence_selection: bool
    escalated: bool
    false_escalation: bool
    true_escalation: bool
    evidence_cost: float | None
    post_evidence_regime_correct: bool

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _case(
    *,
    case_id: str,
    split: str,
    regime: str,
    capability: str,
    residuals: tuple[float, ...],
    sigma: float,
    probe_cost: float,
    prevalence: float,
    adoption_cost: float,
    local_payoff: float,
) -> SyntheticCase:
    latent = (
        LatentCause.MODEL_INADEQUATE
        if regime == "model_inadequate"
        else LatentCause.UNDERINVESTMENT
    )
    history = tuple(
        f"ordinary_probe_{index + 1}: residual={residual:+.3f}"
        for index, residual in enumerate(residuals)
    )
    return SyntheticCase(
        case_id=case_id,
        observation=EcologyObservation(
            capability=capability,
            prevalence=prevalence,
            adoption_cost=adoption_cost,
            local_payoff=local_payoff,
            external_performance=None,
            representation_available=True,
            visible_history=history,
            metadata={
                "ordinary_hypotheses_unresolved": True,
                "available_evidence": (WITHIN_MODEL_PROBE, MODEL_PROBE),
                "failure_residuals": residuals,
                "measurement_sigma": sigma,
                "evidence_costs": {
                    WITHIN_MODEL_PROBE: 0.10,
                    MODEL_PROBE: probe_cost,
                },
                "split": split,
                "v0_2_pair": case_id.rsplit("_", 1)[-1],
            },
        ),
        latent_causes=(latent,),
        available_evidence=(WITHIN_MODEL_PROBE, MODEL_PROBE),
        observational_equivalence_group=f"v0.2-{split}",
    )


def false_escalation_cases() -> tuple[SyntheticCase, ...]:
    """Return the frozen eight-case v0.2 matrix."""

    return (
        _case(
            case_id="dev_MI_1",
            split="development",
            regime="model_inadequate",
            capability="adversarial_transfer_gap",
            residuals=(0.52, 0.49, 0.55, 0.51),
            sigma=0.12,
            probe_cost=0.35,
            prevalence=0.08,
            adoption_cost=0.40,
            local_payoff=-0.15,
        ),
        _case(
            case_id="dev_U_1",
            split="development",
            regime="within_model_uncertainty",
            capability="noisy_replication_signal",
            residuals=(0.22, -0.18, 0.15, -0.20),
            sigma=0.35,
            probe_cost=0.35,
            prevalence=0.08,
            adoption_cost=0.40,
            local_payoff=-0.15,
        ),
        _case(
            case_id="dev_MI_2",
            split="development",
            regime="model_inadequate",
            capability="cross_context_reversal",
            residuals=(-0.40, -0.44, -0.39, -0.46, -0.42),
            sigma=0.11,
            probe_cost=0.55,
            prevalence=0.12,
            adoption_cost=0.55,
            local_payoff=-0.20,
        ),
        _case(
            case_id="dev_U_2",
            split="development",
            regime="within_model_uncertainty",
            capability="high_variance_measurement",
            residuals=(0.30, -0.26, 0.18, -0.22, 0.10),
            sigma=0.48,
            probe_cost=0.55,
            prevalence=0.12,
            adoption_cost=0.55,
            local_payoff=-0.20,
        ),
        _case(
            case_id="held_MI_1",
            split="held_out",
            regime="model_inadequate",
            capability="validator_domain_shift",
            residuals=(0.14, 0.12, 0.16),
            sigma=0.08,
            probe_cost=0.45,
            prevalence=0.05,
            adoption_cost=0.30,
            local_payoff=-0.10,
        ),
        _case(
            case_id="held_U_1",
            split="held_out",
            regime="within_model_uncertainty",
            capability="weak_signal_assay",
            residuals=(0.10, 0.08, 0.09),
            sigma=0.20,
            probe_cost=0.45,
            prevalence=0.05,
            adoption_cost=0.30,
            local_payoff=-0.10,
        ),
        _case(
            case_id="held_MI_2",
            split="held_out",
            regime="model_inadequate",
            capability="representation_stress_test",
            residuals=(-0.22, -0.19, -0.24, -0.20, -0.23, -0.21),
            sigma=0.15,
            probe_cost=0.25,
            prevalence=0.16,
            adoption_cost=0.65,
            local_payoff=-0.25,
        ),
        _case(
            case_id="held_U_2",
            split="held_out",
            regime="within_model_uncertainty",
            capability="heterogeneous_sampling",
            residuals=(0.26, -0.22, 0.18, -0.20, 0.14, -0.16),
            sigma=0.45,
            probe_cost=0.25,
            prevalence=0.16,
            adoption_cost=0.65,
            local_payoff=-0.25,
        ),
    )


def regime(case: SyntheticCase) -> str:
    return (
        "model_inadequate"
        if LatentCause.MODEL_INADEQUATE in case.latent_causes
        else "within_model_uncertainty"
    )


def expected_evidence(case: SyntheticCase) -> str:
    return MODEL_PROBE if regime(case) == "model_inadequate" else WITHIN_MODEL_PROBE


def acquire_v0_2_evidence(case: SyntheticCase, evidence_name: str) -> V02EvidenceResult:
    if evidence_name not in case.available_evidence:
        raise ValueError(f"evidence action {evidence_name!r} is not available for {case.case_id}")

    costs = case.observation.metadata.get("evidence_costs", {})
    cost = float(costs.get(evidence_name, 0.0))

    if evidence_name == MODEL_PROBE:
        if regime(case) == "model_inadequate":
            metadata = {
                **case.observation.metadata,
                "current_causal_vocabulary_residual": True,
                "model_adequacy_probe": "residual_found",
            }
            note = "Model-disrupting probe exposes a stable residual outside the supplied causal vocabulary."
        else:
            metadata = {
                **case.observation.metadata,
                "model_adequacy_confirmed": True,
                "model_adequacy_probe": "no_residual",
            }
            note = "Model-disrupting probe finds no out-of-model residual; ordinary uncertainty remains sufficient."
        return V02EvidenceResult(
            evidence_name,
            replace(case.observation, metadata=metadata),
            cost,
            note,
        )

    if evidence_name == WITHIN_MODEL_PROBE:
        if regime(case) == "model_inadequate":
            metadata = {
                **case.observation.metadata,
                "ordinary_discriminator_result": "still_systematically_unresolved",
            }
            note = "Additional within-model evidence does not remove the systematic residual structure."
        else:
            metadata = {
                **case.observation.metadata,
                "ordinary_discriminator_result": "variance_reduced",
                "within_model_resolution_supported": True,
            }
            note = "Additional within-model evidence reduces ordinary uncertainty without requiring model expansion."
        return V02EvidenceResult(
            evidence_name,
            replace(case.observation, metadata=metadata),
            cost,
            note,
        )

    raise ValueError(f"unknown v0.2 evidence action: {evidence_name}")


def _post_evidence_regime_correct(policy: SearchPolicy, case: SyntheticCase) -> bool:
    probe = acquire_v0_2_evidence(case, MODEL_PROBE)
    decision = policy.decide(probe.observation)
    if regime(case) == "model_inadequate":
        return (
            decision.action is Action.ABSTAIN
            and bool({"model_inadequacy", "current_vocabulary_inadequate"}.intersection(decision.diagnosis))
        )
    return (
        decision.action is Action.INVESTIGATE
        and decision.requested_evidence == WITHIN_MODEL_PROBE
        and bool({"within_model_uncertainty"}.intersection(decision.diagnosis))
    )


def score_v0_2_case(policy: SearchPolicy, case: SyntheticCase) -> V02CaseScore:
    decision = policy.decide(case.observation)
    expected = expected_evidence(case)
    selected = decision.requested_evidence
    escalated = selected == MODEL_PROBE
    is_inadequate = regime(case) == "model_inadequate"
    costs = case.observation.metadata.get("evidence_costs", {})
    selected_cost = float(costs[selected]) if selected in costs else None

    return V02CaseScore(
        case_id=case.case_id,
        split=str(case.observation.metadata["split"]),
        regime=regime(case),
        policy=policy.name,
        selected_evidence=selected,
        expected_evidence=expected,
        correct_evidence_selection=selected == expected,
        escalated=escalated,
        false_escalation=escalated and not is_inadequate,
        true_escalation=escalated and is_inadequate,
        evidence_cost=selected_cost,
        post_evidence_regime_correct=_post_evidence_regime_correct(policy, case),
    )


def score_v0_2_cases(policy: SearchPolicy, cases: Iterable[SyntheticCase]) -> tuple[V02CaseScore, ...]:
    return tuple(score_v0_2_case(policy, case) for case in cases)


def summarize_v0_2(scores: Iterable[V02CaseScore]) -> dict[str, object]:
    rows = tuple(scores)
    inadequate = tuple(row for row in rows if row.regime == "model_inadequate")
    adequate = tuple(row for row in rows if row.regime == "within_model_uncertainty")
    held = tuple(row for row in rows if row.split == "held_out")

    def rate(num: int, den: int) -> float:
        return num / den if den else 0.0

    return {
        "n_cases": len(rows),
        "true_escalation_rate": rate(sum(row.true_escalation for row in inadequate), len(inadequate)),
        "false_escalation_rate": rate(sum(row.false_escalation for row in adequate), len(adequate)),
        "correct_evidence_selection_rate": rate(sum(row.correct_evidence_selection for row in rows), len(rows)),
        "held_out_correct_evidence_selection_rate": rate(
            sum(row.correct_evidence_selection for row in held), len(held)
        ),
        "post_evidence_regime_interpretation_rate": rate(
            sum(row.post_evidence_regime_correct for row in rows), len(rows)
        ),
        "evidence_cost": sum(row.evidence_cost or 0.0 for row in rows),
    }
