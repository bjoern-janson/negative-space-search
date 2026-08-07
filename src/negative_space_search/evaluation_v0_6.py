"""Evaluation for the v0.6 construction-language boundary benchmark."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .language_boundary_v0_6 import (
    LANGUAGE_ADEQUATE,
    LANGUAGE_EXPANSION_PROBE,
    LANGUAGE_INADEQUATE,
    LANGUAGE_UNKNOWN,
    LanguageDecision,
    LanguageHeldOutCase,
    LanguagePolicy,
)
from .representation_v0_4 import MODEL_DISRUPTING_PROBE


@dataclass(frozen=True)
class LanguageBoundarySummary:
    policy: str
    language_inadequacy_detection_rate: float
    false_language_inadequacy_rate: float
    boundary_nonhallucination_rate: float
    adequate_case_selection_rate: float
    unknown_calibration_rate: float
    language_expansion_request_rate: float
    false_language_expansion_request_rate: float
    oracle_recoverability_rate: float
    current_language_expression_count: int

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _rate(values: list[bool]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def summarize(
    policy: LanguagePolicy,
    cases: tuple[LanguageHeldOutCase, ...],
) -> tuple[tuple[LanguageDecision, ...], LanguageBoundarySummary]:
    decisions = tuple(policy.decide(case) for case in cases)
    paired = tuple(zip(cases, decisions))

    inadequate = [(case, decision) for case, decision in paired if case.expected_language_status == LANGUAGE_INADEQUATE]
    non_inadequate = [(case, decision) for case, decision in paired if case.expected_language_status != LANGUAGE_INADEQUATE]
    adequate = [(case, decision) for case, decision in paired if case.expected_language_status == LANGUAGE_ADEQUATE]
    unknown = [(case, decision) for case, decision in paired if case.expected_language_status == LANGUAGE_UNKNOWN]

    summary = LanguageBoundarySummary(
        policy=policy.name,
        language_inadequacy_detection_rate=_rate([
            decision.language_status == LANGUAGE_INADEQUATE
            for _, decision in inadequate
        ]),
        false_language_inadequacy_rate=_rate([
            decision.language_status == LANGUAGE_INADEQUATE
            for _, decision in non_inadequate
        ]),
        boundary_nonhallucination_rate=_rate([
            decision.selected_probe == LANGUAGE_EXPANSION_PROBE
            for _, decision in inadequate
        ]),
        adequate_case_selection_rate=_rate([
            decision.language_status == LANGUAGE_ADEQUATE
            and decision.selected_probe == case.expected_selected_probe
            for case, decision in adequate
        ]),
        unknown_calibration_rate=_rate([
            decision.language_status == LANGUAGE_UNKNOWN
            and decision.selected_probe == MODEL_DISRUPTING_PROBE
            for _, decision in unknown
        ]),
        language_expansion_request_rate=_rate([
            decision.selected_probe == LANGUAGE_EXPANSION_PROBE
            for _, decision in inadequate
        ]),
        false_language_expansion_request_rate=_rate([
            decision.selected_probe == LANGUAGE_EXPANSION_PROBE
            for _, decision in non_inadequate
        ]),
        oracle_recoverability_rate=_rate([
            decision.selected_probe == case.true_resolving_probe
            for case, decision in inadequate
        ]),
        current_language_expression_count=policy.current_language_expression_count,
    )
    return decisions, summary
