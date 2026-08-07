"""v0.6 construction-language boundary benchmark.

The primary systems receive the frozen v0.5 construction language and raw
records that additionally contain an ordered trace. Two resolved classes are
identical under every current-language expression. The benchmark asks whether a
solver can diagnose that non-identifiability without being given replacement
operators to search.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable, Protocol

from .basis_v0_5 import RelationExpression, _conjunction_expressions, _single_expressions
from .representation_v0_4 import MODEL_DISRUPTING_PROBE


LANGUAGE_EXPANSION_PROBE = "language_expansion_probe"
LANGUAGE_ADEQUATE = "adequate"
LANGUAGE_INADEQUATE = "inadequate"
LANGUAGE_UNKNOWN = "unknown"


@dataclass(frozen=True)
class LanguageEpisode:
    episode_id: str
    paired_measurements: tuple[tuple[float, float], ...]
    surface_hint: float
    ordered_trace: tuple[float, ...]
    prediction: float
    outcome: float
    selected_action: str
    timestamp: int
    cost: float
    resolving_probe: str

    @property
    def error(self) -> float:
        return abs(self.prediction - self.outcome)


@dataclass(frozen=True)
class LanguageHeldOutCase:
    case_id: str
    paired_measurements: tuple[tuple[float, float], ...]
    surface_hint: float
    ordered_trace: tuple[float, ...]
    prediction: float
    outcome: float
    timestamp: int
    cost: float
    expected_language_status: str
    expected_selected_probe: str
    true_resolving_probe: str

    @property
    def error(self) -> float:
        return abs(self.prediction - self.outcome)


@dataclass(frozen=True)
class LanguageDecision:
    case_id: str
    policy: str
    language_status: str
    selected_probe: str
    matched_resolving_probes: tuple[str, ...]
    current_language_signature_supported: bool

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class LanguagePolicy(Protocol):
    name: str

    def fit(self, episodes: Iterable[LanguageEpisode]) -> None:
        ...

    def decide(self, case: LanguageHeldOutCase) -> LanguageDecision:
        ...

    @property
    def current_language_expression_count(self) -> int:
        ...


def current_language() -> tuple[RelationExpression, ...]:
    """The frozen v0.5 construction language: singles plus pairwise ANDs."""

    return _single_expressions() + _conjunction_expressions()


def current_language_signature(item: object) -> tuple[bool, ...]:
    return tuple(expression.active(item) for expression in current_language())


def _trace_increasing(trace: tuple[float, ...]) -> bool:
    return len(trace) >= 3 and all(left < right for left, right in zip(trace, trace[1:]))


def _trace_decreasing(trace: tuple[float, ...]) -> bool:
    return len(trace) >= 3 and all(left > right for left, right in zip(trace, trace[1:]))


def expanded_oracle_signature(item: object) -> tuple[bool, ...]:
    trace = getattr(item, "ordered_trace")
    return current_language_signature(item) + (
        _trace_increasing(trace),
        _trace_decreasing(trace),
    )


def _episode(
    episode_id: str,
    resolving_probe: str,
    pairs: tuple[tuple[float, float], ...],
    hint: float,
    trace: tuple[float, ...],
    prediction: float,
    outcome: float,
    timestamp: int,
) -> LanguageEpisode:
    return LanguageEpisode(
        episode_id=episode_id,
        paired_measurements=pairs,
        surface_hint=hint,
        ordered_trace=trace,
        prediction=prediction,
        outcome=outcome,
        selected_action="ordinary_search",
        timestamp=timestamp,
        cost=0.10,
        resolving_probe=resolving_probe,
    )


def training_episodes() -> tuple[LanguageEpisode, ...]:
    return (
        _episode("T_COMP1", "composition_probe", ((0.40, 0.44), (0.10, 0.85), (0.20, 0.40)), 0.20, (0.3, 0.3, 0.3), 0.80, 0.20, 1),
        _episode("T_COMP2", "composition_probe", ((0.31, 0.36), (0.15, 0.84), (0.24, 0.45)), 0.25, (0.4, 0.4, 0.4), 0.70, 0.10, 2),
        _episode("T_CLOSE1", "close_only_probe", ((0.42, 0.47), (0.20, 0.45), (0.18, 0.38)), 0.22, (0.2, 0.2, 0.2), 0.75, 0.15, 3),
        _episode("T_CLOSE2", "close_only_probe", ((0.33, 0.38), (0.25, 0.50), (0.22, 0.43)), 0.26, (0.5, 0.5, 0.5), 0.65, 0.05, 4),
        _episode("T_FAR1", "far_only_probe", ((0.18, 0.40), (0.10, 0.82), (0.25, 0.45)), 0.21, (0.4, 0.4, 0.4), 0.60, 0.00, 5),
        _episode("T_FAR2", "far_only_probe", ((0.22, 0.44), (0.05, 0.75), (0.28, 0.48)), 0.24, (0.3, 0.3, 0.3), 0.50, -0.10, 6),
        _episode("T_REF1", "reference_probe", ((0.15, 0.38), (0.22, 0.44), (0.30, -0.30)), 0.20, (0.4, 0.4, 0.4), 0.55, -0.05, 7),
        _episode("T_REF2", "reference_probe", ((0.18, 0.40), (0.25, 0.47), (0.25, -0.35)), 0.28, (0.2, 0.2, 0.2), 0.45, -0.15, 8),
        _episode("T_UP1", "order_up_probe", ((0.10, 0.80), (0.42, 0.47), (0.20, 0.40)), -0.80, (0.10, 0.40, 0.80), 0.40, -0.20, 9),
        _episode("T_DOWN1", "order_down_probe", ((0.10, 0.80), (0.42, 0.47), (0.20, 0.40)), -0.80, (0.80, 0.40, 0.10), 0.35, -0.25, 10),
        _episode("T_UP2", "order_up_probe", ((0.12, 0.84), (0.35, 0.40), (0.24, 0.44)), -0.75, (0.15, 0.45, 0.85), 0.30, -0.30, 11),
        _episode("T_DOWN2", "order_down_probe", ((0.12, 0.84), (0.35, 0.40), (0.24, 0.44)), -0.75, (0.85, 0.45, 0.15), 0.25, -0.35, 12),
    )


def held_out_cases() -> tuple[LanguageHeldOutCase, ...]:
    rows = (
        (
            "H_COMP", ((0.48, 0.53), (0.08, 0.78), (0.21, 0.41)), 0.23,
            (0.6, 0.6, 0.6), 0.68, 0.08, LANGUAGE_ADEQUATE,
            "composition_probe", "composition_probe",
        ),
        (
            "H_REF", ((0.20, 0.43), (0.28, 0.50), (0.32, -0.28)), 0.27,
            (0.3, 0.3, 0.3), 0.58, -0.02, LANGUAGE_ADEQUATE,
            "reference_probe", "reference_probe",
        ),
        (
            "H_ORDER_UP", ((0.14, 0.82), (0.46, 0.51), (0.26, 0.46)), -0.82,
            (0.12, 0.48, 0.88), 0.48, -0.12, LANGUAGE_INADEQUATE,
            LANGUAGE_EXPANSION_PROBE, "order_up_probe",
        ),
        (
            "H_ORDER_DOWN", ((0.14, 0.82), (0.46, 0.51), (0.26, 0.46)), -0.82,
            (0.88, 0.48, 0.12), 0.43, -0.17, LANGUAGE_INADEQUATE,
            LANGUAGE_EXPANSION_PROBE, "order_down_probe",
        ),
        (
            "H_UNKNOWN", ((0.35, -0.35), (0.40, -0.40), (0.05, 0.80)), 0.82,
            (0.20, 0.50, 0.30), 0.38, -0.22, LANGUAGE_UNKNOWN,
            MODEL_DISRUPTING_PROBE, MODEL_DISRUPTING_PROBE,
        ),
    )
    return tuple(
        LanguageHeldOutCase(
            case_id=case_id,
            paired_measurements=pairs,
            surface_hint=hint,
            ordered_trace=trace,
            prediction=prediction,
            outcome=outcome,
            timestamp=13 + index,
            cost=0.25,
            expected_language_status=status,
            expected_selected_probe=expected_probe,
            true_resolving_probe=true_probe,
        )
        for index, (
            case_id, pairs, hint, trace, prediction, outcome, status,
            expected_probe, true_probe,
        ) in enumerate(rows)
    )


class _SignaturePolicy:
    name = "signature_policy"

    def __init__(self) -> None:
        self._by_signature: dict[tuple[bool, ...], tuple[str, ...]] = {}

    @property
    def current_language_expression_count(self) -> int:
        return len(current_language())

    def fit(self, episodes: Iterable[LanguageEpisode]) -> None:
        grouped: dict[tuple[bool, ...], set[str]] = {}
        for episode in episodes:
            signature = current_language_signature(episode)
            grouped.setdefault(signature, set()).add(episode.resolving_probe)
        self._by_signature = {
            signature: tuple(sorted(labels))
            for signature, labels in grouped.items()
        }

    def _matches(self, case: LanguageHeldOutCase) -> tuple[str, ...]:
        if not self._by_signature:
            raise RuntimeError("fit must be called before decide")
        return self._by_signature.get(current_language_signature(case), ())


class CurrentLanguageAssimilator(_SignaturePolicy):
    """Control that forces an existing class when a current signature is ambiguous."""

    name = "current_language_assimilator"

    def decide(self, case: LanguageHeldOutCase) -> LanguageDecision:
        matches = self._matches(case)
        if matches:
            selected = matches[0]
            status = LANGUAGE_ADEQUATE
        else:
            selected = MODEL_DISRUPTING_PROBE
            status = LANGUAGE_UNKNOWN
        return LanguageDecision(
            case_id=case.case_id,
            policy=self.name,
            language_status=status,
            selected_probe=selected,
            matched_resolving_probes=matches,
            current_language_signature_supported=bool(matches),
        )


class ConservativeAbstainer(_SignaturePolicy):
    """Control that avoids guessing but does not diagnose language inadequacy."""

    name = "conservative_abstainer"

    def decide(self, case: LanguageHeldOutCase) -> LanguageDecision:
        matches = self._matches(case)
        if len(matches) == 1:
            selected = matches[0]
            status = LANGUAGE_ADEQUATE
        else:
            selected = MODEL_DISRUPTING_PROBE
            status = LANGUAGE_UNKNOWN
        return LanguageDecision(
            case_id=case.case_id,
            policy=self.name,
            language_status=status,
            selected_probe=selected,
            matched_resolving_probes=matches,
            current_language_signature_supported=bool(matches),
        )


class BoundaryAwareLanguageAuditor(_SignaturePolicy):
    """Diagnoses conflicting resolved labels inside one language equivalence class."""

    name = "boundary_aware_language_auditor"

    def decide(self, case: LanguageHeldOutCase) -> LanguageDecision:
        matches = self._matches(case)
        if len(matches) == 1:
            selected = matches[0]
            status = LANGUAGE_ADEQUATE
        elif len(matches) > 1:
            selected = LANGUAGE_EXPANSION_PROBE
            status = LANGUAGE_INADEQUATE
        else:
            selected = MODEL_DISRUPTING_PROBE
            status = LANGUAGE_UNKNOWN
        return LanguageDecision(
            case_id=case.case_id,
            policy=self.name,
            language_status=status,
            selected_probe=selected,
            matched_resolving_probes=matches,
            current_language_signature_supported=bool(matches),
        )


class ExpandedLanguageOracle:
    """Recoverability control supplied with trace direction operators."""

    name = "expanded_language_oracle"

    def __init__(self) -> None:
        self._by_signature: dict[tuple[bool, ...], tuple[str, ...]] = {}

    @property
    def current_language_expression_count(self) -> int:
        return len(current_language()) + 2

    def fit(self, episodes: Iterable[LanguageEpisode]) -> None:
        grouped: dict[tuple[bool, ...], set[str]] = {}
        for episode in episodes:
            signature = expanded_oracle_signature(episode)
            grouped.setdefault(signature, set()).add(episode.resolving_probe)
        self._by_signature = {
            signature: tuple(sorted(labels))
            for signature, labels in grouped.items()
        }

    def decide(self, case: LanguageHeldOutCase) -> LanguageDecision:
        if not self._by_signature:
            raise RuntimeError("fit must be called before decide")
        matches = self._by_signature.get(expanded_oracle_signature(case), ())
        if len(matches) == 1:
            selected = matches[0]
            status = LANGUAGE_ADEQUATE
        else:
            selected = MODEL_DISRUPTING_PROBE
            status = LANGUAGE_UNKNOWN
        return LanguageDecision(
            case_id=case.case_id,
            policy=self.name,
            language_status=status,
            selected_probe=selected,
            matched_resolving_probes=matches,
            current_language_signature_supported=bool(matches),
        )
