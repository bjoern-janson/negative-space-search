"""Evaluation for v0.7 construction-language repair."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .language_boundary_v0_6 import LANGUAGE_UNKNOWN
from .operator_discovery_v0_7 import (
    CENTER_EDGE_PROBES,
    DIRECTION_PROBES,
    HOSTILE_PROBES,
    OperatorDecision,
    OperatorPolicy,
)
from .representation_v0_4 import MODEL_DISRUPTING_PROBE


@dataclass(frozen=True)
class OperatorDiscoverySummary:
    policy: str
    boundary_detection_rate: float
    construction_success_rate: float
    held_out_repair_selection_rate: float
    multi_family_transfer_rate: float
    false_assimilation_rate: float
    false_expansion_rate: float
    adequate_case_preservation_rate: float
    unknown_calibration_rate: float
    search_cost: int
    representation_cost: int
    generated_operator_count: int
    q_invention: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _rate(values: list[bool]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def summarize(
    policy: OperatorPolicy,
    cases: tuple,
) -> tuple[tuple[OperatorDecision, ...], OperatorDiscoverySummary]:
    decisions = tuple(policy.decide(case) for case in cases)
    paired = tuple(zip(cases, decisions))

    hostile = [
        (case, decision)
        for case, decision in paired
        if case.true_resolving_probe in HOSTILE_PROBES
    ]
    adequate = [
        (case, decision)
        for case, decision in paired
        if case.case_id in {"H_A", "H_R"}
    ]
    unknown = [
        (case, decision)
        for case, decision in paired
        if case.case_id == "H_UNKNOWN"
    ]

    correct_hostile = {
        case.case_id: decision.selected_probe == case.true_resolving_probe
        for case, decision in hostile
    }
    family_success = [
        all(correct_hostile[case_id] for case_id in ("H_DF", "H_DR")),
        all(correct_hostile[case_id] for case_id in ("H_CH", "H_EH")),
    ]

    false_assimilation = [
        decision.selected_probe in HOSTILE_PROBES
        and decision.selected_probe != case.true_resolving_probe
        for case, decision in hostile
    ]

    true_collisions = policy.true_collision_signature_count
    boundary_detection_rate = (
        policy.detected_collision_signature_count / true_collisions
        if true_collisions else 0.0
    )

    construction_success_rate = len(policy.generated_operators) / len(HOSTILE_PROBES)

    adequate_signature_count = policy.adequate_signature_count
    false_expansions = max(
        0,
        policy.expanded_signature_count - policy.true_collision_signature_count,
    )
    false_expansion_rate = (
        false_expansions / adequate_signature_count
        if adequate_signature_count else 0.0
    )

    generated_hostile_success = [
        decision.selected_probe == case.true_resolving_probe
        and decision.used_generated_operator
        for case, decision in hostile
    ]

    summary = OperatorDiscoverySummary(
        policy=policy.name,
        boundary_detection_rate=boundary_detection_rate,
        construction_success_rate=construction_success_rate,
        held_out_repair_selection_rate=_rate([
            decision.selected_probe == case.true_resolving_probe
            for case, decision in hostile
        ]),
        multi_family_transfer_rate=_rate(family_success),
        false_assimilation_rate=_rate(false_assimilation),
        false_expansion_rate=false_expansion_rate,
        adequate_case_preservation_rate=_rate([
            decision.selected_probe == case.true_resolving_probe
            for case, decision in adequate
        ]),
        unknown_calibration_rate=_rate([
            decision.language_status == LANGUAGE_UNKNOWN
            and decision.selected_probe == MODEL_DISRUPTING_PROBE
            for _, decision in unknown
        ]),
        search_cost=policy.search_cost,
        representation_cost=policy.representation_cost,
        generated_operator_count=len(policy.generated_operators),
        q_invention=_rate(generated_hostile_success),
    )
    return decisions, summary
