"""Minimal evaluators for the executable benchmark line.

These checks intentionally cover only what the current toy environments identify
cleanly. They do not collapse the full Q_Psi metric vector into a single score.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

from .baselines import Action, Decision, SearchPolicy
from .environments import LatentCause, SyntheticCase


EXPECTED_ACTION = {
    "A_underinvestment": Action.INTERVENE,
    "B_underrepresentation": Action.INVESTIGATE,
    "C_justified_selection": Action.PRESERVE,
    "D_coordination_failure": Action.INVESTIGATE,
    "E_model_inadequate": Action.ABSTAIN,
}

EXPECTED_EVIDENCE = {
    "B_underrepresentation": "interface_probe",
    "D_coordination_failure": "threshold_test",
    "E_model_inadequate": "cross_interface_probe",
}

DIAGNOSIS_KEYS = {
    LatentCause.UNDERINVESTMENT: {"underinvestment", "payoff_misalignment"},
    LatentCause.UNDERREPRESENTATION: {"underrepresentation", "representation_failure"},
    LatentCause.JUSTIFIED_SELECTION: {"justified_selection", "evidence_against_intervention"},
    LatentCause.COORDINATION_FAILURE: {"coordination_failure", "coordination_or_payoff", "coordination_possible"},
    LatentCause.MODEL_INADEQUATE: {"current_vocabulary_inadequate", "model_inadequacy"},
}


@dataclass(frozen=True)
class InitialCaseScore:
    case_id: str
    policy: str
    action_correct: bool
    diagnosis_supported: bool
    evidence_match: bool | None
    healthy_absence_preserved: bool | None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class HostilePairScore:
    policy: str
    non_guessing_action: bool
    discriminating_evidence_requested: bool
    same_action_on_same_observation: bool
    passed: bool

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class ModelAdequacyScore:
    """v0.1.1: separate search for evidence from interpretation of evidence."""

    policy: str
    same_initial_observation: bool
    initial_non_guessing_action: bool
    model_adequacy_probe_requested: bool
    within_model_after_probe_correct: bool
    model_inadequacy_after_probe_correct: bool
    passed: bool

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _diagnosis_supported(case: SyntheticCase, decision: Decision) -> bool:
    expected_keys: set[str] = set()
    for cause in case.latent_causes:
        expected_keys.update(DIAGNOSIS_KEYS[cause])
    return bool(expected_keys.intersection(decision.diagnosis))


def _regime_label(decision: Decision) -> str | None:
    keys = set(decision.diagnosis)
    if keys.intersection({"current_vocabulary_inadequate", "model_inadequacy"}):
        return "model_inadequacy_suspected"
    if "within_model_uncertainty" in keys:
        return "within_model_uncertainty"
    return None


def score_initial_case(policy: SearchPolicy, case: SyntheticCase) -> InitialCaseScore:
    decision = policy.decide(case.observation)
    expected_action = EXPECTED_ACTION[case.case_id]
    expected_evidence = EXPECTED_EVIDENCE.get(case.case_id)

    evidence_match: bool | None
    if expected_evidence is None:
        evidence_match = None
    else:
        evidence_match = decision.requested_evidence == expected_evidence

    healthy_absence_preserved: bool | None
    if case.healthy_absence:
        healthy_absence_preserved = decision.action is Action.PRESERVE
    else:
        healthy_absence_preserved = None

    return InitialCaseScore(
        case_id=case.case_id,
        policy=policy.name,
        action_correct=decision.action is expected_action,
        diagnosis_supported=_diagnosis_supported(case, decision),
        evidence_match=evidence_match,
        healthy_absence_preserved=healthy_absence_preserved,
    )


def score_cases(policy: SearchPolicy, cases: Iterable[SyntheticCase]) -> tuple[InitialCaseScore, ...]:
    return tuple(score_initial_case(policy, case) for case in cases)


def score_hostile_pair(
    policy: SearchPolicy,
    underinvestment_case: SyntheticCase,
    selection_case: SyntheticCase,
) -> HostilePairScore:
    """Score the v0.1 observational-equivalence test before evidence acquisition."""

    first = policy.decide(underinvestment_case.observation)
    second = policy.decide(selection_case.observation)

    allowed = {Action.INVESTIGATE, Action.ABSTAIN}
    non_guessing_action = first.action in allowed and second.action in allowed
    discriminating_evidence_requested = (
        first.requested_evidence == "controlled_external_value_test"
        and second.requested_evidence == "controlled_external_value_test"
    )
    same_action_on_same_observation = first.action is second.action

    return HostilePairScore(
        policy=policy.name,
        non_guessing_action=non_guessing_action,
        discriminating_evidence_requested=discriminating_evidence_requested,
        same_action_on_same_observation=same_action_on_same_observation,
        passed=non_guessing_action and discriminating_evidence_requested and same_action_on_same_observation,
    )


def score_model_adequacy_pair(
    policy: SearchPolicy,
    within_model_case: SyntheticCase,
    model_inadequate_case: SyntheticCase,
) -> ModelAdequacyScore:
    """Score whether a policy asks 'more data or a better question?'

    The initial observations are identical. Evidence-selection quality is scored from
    the policy's own choice. Evidence-interpretation quality is scored separately by
    supplying the same model-disrupting probe to every policy. This preserves the
    distinction between Psi (where to look) and U-like interpretation (what evidence
    warrants after it arrives).
    """

    from .simulator import acquire_evidence

    first = policy.decide(within_model_case.observation)
    second = policy.decide(model_inadequate_case.observation)

    same_initial_observation = within_model_case.observation == model_inadequate_case.observation
    allowed = {Action.INVESTIGATE, Action.ABSTAIN}
    initial_non_guessing_action = first.action in allowed and second.action in allowed
    model_adequacy_probe_requested = (
        first.requested_evidence == "model_disrupting_probe"
        and second.requested_evidence == "model_disrupting_probe"
    )

    within_observation = acquire_evidence(within_model_case, "model_disrupting_probe").observation
    inadequate_observation = acquire_evidence(model_inadequate_case, "model_disrupting_probe").observation
    within_after = policy.decide(within_observation)
    inadequate_after = policy.decide(inadequate_observation)

    within_model_after_probe_correct = (
        _regime_label(within_after) == "within_model_uncertainty"
        and within_after.action is Action.INVESTIGATE
    )
    model_inadequacy_after_probe_correct = (
        _regime_label(inadequate_after) == "model_inadequacy_suspected"
        and inadequate_after.action is Action.ABSTAIN
    )

    return ModelAdequacyScore(
        policy=policy.name,
        same_initial_observation=same_initial_observation,
        initial_non_guessing_action=initial_non_guessing_action,
        model_adequacy_probe_requested=model_adequacy_probe_requested,
        within_model_after_probe_correct=within_model_after_probe_correct,
        model_inadequacy_after_probe_correct=model_inadequacy_after_probe_correct,
        passed=(
            same_initial_observation
            and initial_non_guessing_action
            and model_adequacy_probe_requested
            and within_model_after_probe_correct
            and model_inadequacy_after_probe_correct
        ),
    )
