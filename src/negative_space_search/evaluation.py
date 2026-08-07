"""Minimal evaluators for the first executable benchmark.

These checks intentionally cover only what v0.1 can identify cleanly. They do not
collapse the full Q_Psi metric vector into a single score.
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


def _diagnosis_supported(case: SyntheticCase, decision: Decision) -> bool:
    expected_keys: set[str] = set()
    for cause in case.latent_causes:
        expected_keys.update(DIAGNOSIS_KEYS[cause])
    return bool(expected_keys.intersection(decision.diagnosis))


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
    """Score the observational-equivalence test before any evidence is acquired."""

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
