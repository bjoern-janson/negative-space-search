"""v0.7 construction-language repair by generic expression synthesis.

The frozen v0.6 language cannot discriminate two hostile equivalence classes.
This module adds a generic trace-expression grammar, but does not supply any
ready-made semantic target operator. Boundary-gated and always-expand systems
share the exact same generator and scoring rule.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable, Protocol

from .language_boundary_v0_6 import (
    LANGUAGE_ADEQUATE,
    LANGUAGE_EXPANSION_PROBE,
    LANGUAGE_INADEQUATE,
    LANGUAGE_UNKNOWN,
    LanguageEpisode,
    LanguageHeldOutCase,
    current_language,
    current_language_signature,
)
from .representation_v0_4 import MODEL_DISRUPTING_PROBE


COMPLEXITY_PENALTY = 0.002
REQUIRED_TRAINING_BALANCED_ACCURACY = 1.0

DIRECTION_PROBES = frozenset({"direction_forward_probe", "direction_reverse_probe"})
CENTER_EDGE_PROBES = frozenset({"center_heavy_probe", "edge_heavy_probe"})
HOSTILE_PROBES = DIRECTION_PROBES | CENTER_EDGE_PROBES


@dataclass(frozen=True)
class NumericExpression:
    name: str
    complexity: int
    kind: str
    left: str | None = None
    right: str | None = None

    def value(self, item: object) -> float:
        trace = getattr(item, "ordered_trace")
        if self.kind == "terminal":
            return float(trace[int(self.name.removeprefix("t"))])
        terms = {term.name: term for term in numeric_expressions()}
        if self.left is None or self.right is None:
            raise ValueError("arithmetic expression requires two operands")
        left_value = terms[self.left].value(item)
        right_value = terms[self.right].value(item)
        if self.kind == "add":
            return left_value + right_value
        if self.kind == "sub":
            return left_value - right_value
        raise ValueError(f"unknown numeric expression kind: {self.kind}")


@dataclass(frozen=True)
class GeneratedPredicate:
    name: str
    complexity: int
    comparator: str
    left: str
    right: str

    def active(self, item: object) -> bool:
        terms = {term.name: term for term in numeric_expressions()}
        left_value = terms[self.left].value(item)
        right_value = terms[self.right].value(item)
        if self.comparator == "GT":
            return left_value > right_value
        if self.comparator == "LT":
            return left_value < right_value
        raise ValueError(f"unknown comparator: {self.comparator}")


@dataclass(frozen=True)
class SynthesisSelection:
    target_probe: str
    expression_name: str | None
    complexity: int
    balanced_accuracy: float
    candidate_evaluations: int
    retained: bool

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class OperatorDecision:
    case_id: str
    policy: str
    language_status: str
    selected_probe: str
    current_signature_supported: bool
    collision_detected: bool
    used_generated_operator: bool
    generated_operator: str | None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class OperatorPolicy(Protocol):
    name: str

    def fit(self, episodes: Iterable[LanguageEpisode]) -> None:
        ...

    def decide(self, case: LanguageHeldOutCase) -> OperatorDecision:
        ...

    @property
    def true_collision_signature_count(self) -> int:
        ...

    @property
    def detected_collision_signature_count(self) -> int:
        ...

    @property
    def expanded_signature_count(self) -> int:
        ...

    @property
    def adequate_signature_count(self) -> int:
        ...

    @property
    def search_cost(self) -> int:
        ...

    @property
    def representation_cost(self) -> int:
        ...

    @property
    def generated_operators(self) -> dict[str, GeneratedPredicate]:
        ...


def numeric_expressions() -> tuple[NumericExpression, ...]:
    """Generate the frozen primitive numeric meta-language.

    No numeric constants and no semantic trace features are included.
    """

    terminals = tuple(
        NumericExpression(name=f"t{index}", complexity=1, kind="terminal")
        for index in range(4)
    )
    expressions: list[NumericExpression] = list(terminals)

    for left_index, left in enumerate(terminals):
        for right_index, right in enumerate(terminals):
            if right_index < left_index:
                continue
            expressions.append(
                NumericExpression(
                    name=f"ADD({left.name},{right.name})",
                    complexity=left.complexity + right.complexity + 1,
                    kind="add",
                    left=left.name,
                    right=right.name,
                )
            )

    for left in terminals:
        for right in terminals:
            if left.name == right.name:
                continue
            expressions.append(
                NumericExpression(
                    name=f"SUB({left.name},{right.name})",
                    complexity=left.complexity + right.complexity + 1,
                    kind="sub",
                    left=left.name,
                    right=right.name,
                )
            )

    return tuple(expressions)


def generated_predicates() -> tuple[GeneratedPredicate, ...]:
    """Generate full predicates from primitive syntax rather than a candidate list."""

    terms = numeric_expressions()
    predicates: list[GeneratedPredicate] = []
    for left in terms:
        for right in terms:
            if left.name == right.name:
                continue
            for comparator in ("GT", "LT"):
                predicates.append(
                    GeneratedPredicate(
                        name=f"{comparator}({left.name},{right.name})",
                        complexity=left.complexity + right.complexity + 1,
                        comparator=comparator,
                        left=left.name,
                        right=right.name,
                    )
                )
    return tuple(predicates)


def _balanced_accuracy(
    predicate: GeneratedPredicate,
    episodes: tuple[LanguageEpisode, ...],
    target_probe: str,
) -> float:
    positives = tuple(episode for episode in episodes if episode.resolving_probe == target_probe)
    negatives = tuple(episode for episode in episodes if episode.resolving_probe != target_probe)
    if not positives or not negatives:
        return 0.0
    true_positive_rate = sum(predicate.active(episode) for episode in positives) / len(positives)
    true_negative_rate = sum(not predicate.active(episode) for episode in negatives) / len(negatives)
    return (true_positive_rate + true_negative_rate) / 2.0


def _synthesize(
    episodes: tuple[LanguageEpisode, ...],
    target_probe: str,
) -> tuple[SynthesisSelection, GeneratedPredicate | None]:
    candidates = generated_predicates()
    scored: list[tuple[GeneratedPredicate, float, float]] = []
    for candidate in candidates:
        accuracy = _balanced_accuracy(candidate, episodes, target_probe)
        objective = accuracy - COMPLEXITY_PENALTY * candidate.complexity
        scored.append((candidate, accuracy, objective))

    eligible = [
        item for item in scored
        if item[1] == REQUIRED_TRAINING_BALANCED_ACCURACY
    ]
    if not eligible:
        return (
            SynthesisSelection(
                target_probe=target_probe,
                expression_name=None,
                complexity=0,
                balanced_accuracy=max((accuracy for _, accuracy, _ in scored), default=0.0),
                candidate_evaluations=len(candidates),
                retained=False,
            ),
            None,
        )

    eligible.sort(
        key=lambda item: (
            -item[2],
            -item[1],
            item[0].complexity,
            item[0].name,
        )
    )
    selected, accuracy, _ = eligible[0]
    return (
        SynthesisSelection(
            target_probe=target_probe,
            expression_name=selected.name,
            complexity=selected.complexity,
            balanced_accuracy=accuracy,
            candidate_evaluations=len(candidates),
            retained=True,
        ),
        selected,
    )


def _episode(
    episode_id: str,
    resolving_probe: str,
    pairs: tuple[tuple[float, float], ...],
    hint: float,
    trace: tuple[float, ...],
    index: int,
) -> LanguageEpisode:
    prediction = 0.90 - 0.02 * index
    return LanguageEpisode(
        episode_id=episode_id,
        paired_measurements=pairs,
        surface_hint=hint,
        ordered_trace=trace,
        prediction=prediction,
        outcome=prediction - 0.60,
        selected_action="ordinary_search",
        timestamp=index + 1,
        cost=0.10,
        resolving_probe=resolving_probe,
    )


def training_episodes() -> tuple[LanguageEpisode, ...]:
    s_a = ((0.40, 0.44), (0.10, 0.85), (0.20, 0.40))
    s_r = ((0.15, 0.38), (0.22, 0.44), (0.30, -0.30))
    s_d = ((0.10, 0.80), (0.42, 0.47), (0.20, 0.40))
    s_c = ((0.35, -0.35), (0.10, 0.80), (0.42, 0.47))

    rows = (
        ("T_A1", "composition_probe", s_a, 0.20, (0.30, 0.30, 0.30, 0.30)),
        ("T_A2", "composition_probe", s_a, 0.20, (0.60, 0.20, 0.70, 0.10)),
        ("T_R1", "reference_probe", s_r, 0.20, (0.20, 0.80, 0.10, 0.70)),
        ("T_R2", "reference_probe", s_r, 0.20, (0.75, 0.15, 0.65, 0.25)),
        ("T_DF1", "direction_forward_probe", s_d, -0.80, (0.10, 0.90, 0.05, 0.80)),
        ("T_DF2", "direction_forward_probe", s_d, -0.80, (0.20, 0.10, 0.90, 0.70)),
        ("T_DF3", "direction_forward_probe", s_d, -0.80, (0.40, 0.80, 0.20, 0.60)),
        ("T_DF4", "direction_forward_probe", s_d, -0.80, (0.30, 0.20, 0.10, 0.50)),
        ("T_DR1", "direction_reverse_probe", s_d, -0.80, (0.80, 0.10, 0.90, 0.20)),
        ("T_DR2", "direction_reverse_probe", s_d, -0.80, (0.70, 0.90, 0.10, 0.30)),
        ("T_DR3", "direction_reverse_probe", s_d, -0.80, (0.60, 0.20, 0.80, 0.40)),
        ("T_DR4", "direction_reverse_probe", s_d, -0.80, (0.50, 0.70, 0.30, 0.10)),
        ("T_CH1", "center_heavy_probe", s_c, 0.20, (0.80, 0.70, 0.70, 0.40)),
        ("T_CH2", "center_heavy_probe", s_c, 0.20, (0.20, 0.60, 0.50, 0.70)),
        ("T_CH3", "center_heavy_probe", s_c, 0.20, (0.60, 0.40, 0.80, 0.30)),
        ("T_CH4", "center_heavy_probe", s_c, 0.20, (0.40, 0.80, 0.30, 0.50)),
        ("T_EH1", "edge_heavy_probe", s_c, 0.20, (0.70, 0.60, 0.30, 0.80)),
        ("T_EH2", "edge_heavy_probe", s_c, 0.20, (0.30, 0.70, 0.20, 0.80)),
        ("T_EH3", "edge_heavy_probe", s_c, 0.20, (0.80, 0.30, 0.60, 0.70)),
        ("T_EH4", "edge_heavy_probe", s_c, 0.20, (0.50, 0.20, 0.70, 0.60)),
    )
    return tuple(
        _episode(episode_id, probe, pairs, hint, trace, index)
        for index, (episode_id, probe, pairs, hint, trace) in enumerate(rows)
    )


def held_out_cases() -> tuple[LanguageHeldOutCase, ...]:
    s_a = ((0.40, 0.44), (0.10, 0.85), (0.20, 0.40))
    s_r = ((0.15, 0.38), (0.22, 0.44), (0.30, -0.30))
    s_d = ((0.10, 0.80), (0.42, 0.47), (0.20, 0.40))
    s_c = ((0.35, -0.35), (0.10, 0.80), (0.42, 0.47))
    s_u = ((0.35, -0.35), (0.40, -0.40), (0.05, 0.80))

    rows = (
        ("H_A", s_a, 0.20, (0.55, 0.15, 0.75, 0.25), LANGUAGE_ADEQUATE, "composition_probe"),
        ("H_R", s_r, 0.20, (0.25, 0.85, 0.15, 0.65), LANGUAGE_ADEQUATE, "reference_probe"),
        ("H_DF", s_d, -0.80, (0.25, 0.95, 0.10, 0.65), LANGUAGE_ADEQUATE, "direction_forward_probe"),
        ("H_DR", s_d, -0.80, (0.65, 0.05, 0.90, 0.25), LANGUAGE_ADEQUATE, "direction_reverse_probe"),
        ("H_CH", s_c, 0.20, (0.55, 0.75, 0.65, 0.35), LANGUAGE_ADEQUATE, "center_heavy_probe"),
        ("H_EH", s_c, 0.20, (0.65, 0.25, 0.45, 0.75), LANGUAGE_ADEQUATE, "edge_heavy_probe"),
        ("H_UNKNOWN", s_u, 0.82, (0.20, 0.50, 0.30, 0.40), LANGUAGE_UNKNOWN, MODEL_DISRUPTING_PROBE),
    )
    cases: list[LanguageHeldOutCase] = []
    for index, (case_id, pairs, hint, trace, status, probe) in enumerate(rows):
        prediction = 0.58 - 0.03 * index
        cases.append(
            LanguageHeldOutCase(
                case_id=case_id,
                paired_measurements=pairs,
                surface_hint=hint,
                ordered_trace=trace,
                prediction=prediction,
                outcome=prediction - 0.60,
                timestamp=21 + index,
                cost=0.25,
                expected_language_status=status,
                expected_selected_probe=probe,
                true_resolving_probe=probe,
            )
        )
    return tuple(cases)


class _BaseOperatorPolicy:
    name = "base_operator_policy"

    def __init__(self) -> None:
        self._episodes: tuple[LanguageEpisode, ...] = ()
        self._by_signature: dict[tuple[bool, ...], tuple[LanguageEpisode, ...]] = {}
        self._labels_by_signature: dict[tuple[bool, ...], tuple[str, ...]] = {}
        self._detected_collisions: set[tuple[bool, ...]] = set()
        self._expanded_signatures: set[tuple[bool, ...]] = set()
        self._generated_operators: dict[str, GeneratedPredicate] = {}
        self._selections: dict[str, SynthesisSelection] = {}
        self._search_cost = 0

    def fit(self, episodes: Iterable[LanguageEpisode]) -> None:
        self._episodes = tuple(episodes)
        grouped: dict[tuple[bool, ...], list[LanguageEpisode]] = {}
        for episode in self._episodes:
            grouped.setdefault(current_language_signature(episode), []).append(episode)
        self._by_signature = {
            signature: tuple(items)
            for signature, items in grouped.items()
        }
        self._labels_by_signature = {
            signature: tuple(sorted({item.resolving_probe for item in items}))
            for signature, items in self._by_signature.items()
        }
        self._fit_after_grouping()

    def _fit_after_grouping(self) -> None:
        pass

    @property
    def true_collision_signature_count(self) -> int:
        return sum(len(labels) > 1 for labels in self._labels_by_signature.values())

    @property
    def detected_collision_signature_count(self) -> int:
        return len(self._detected_collisions)

    @property
    def expanded_signature_count(self) -> int:
        return len(self._expanded_signatures)

    @property
    def adequate_signature_count(self) -> int:
        return sum(len(labels) == 1 for labels in self._labels_by_signature.values())

    @property
    def search_cost(self) -> int:
        return self._search_cost

    @property
    def representation_cost(self) -> int:
        return sum(operator.complexity for operator in self._generated_operators.values())

    @property
    def generated_operators(self) -> dict[str, GeneratedPredicate]:
        return dict(self._generated_operators)

    @property
    def selections(self) -> dict[str, SynthesisSelection]:
        return dict(self._selections)

    def _matches(self, case: LanguageHeldOutCase) -> tuple[str, ...]:
        return self._labels_by_signature.get(current_language_signature(case), ())

    def _decision(
        self,
        case: LanguageHeldOutCase,
        status: str,
        selected_probe: str,
        collision_detected: bool,
        generated_operator: str | None = None,
    ) -> OperatorDecision:
        return OperatorDecision(
            case_id=case.case_id,
            policy=self.name,
            language_status=status,
            selected_probe=selected_probe,
            current_signature_supported=bool(self._matches(case)),
            collision_detected=collision_detected,
            used_generated_operator=generated_operator is not None,
            generated_operator=generated_operator,
        )


class CurrentLanguageAssimilatorV07(_BaseOperatorPolicy):
    name = "current_language_assimilator_v0_7"

    def decide(self, case: LanguageHeldOutCase) -> OperatorDecision:
        matches = self._matches(case)
        if matches:
            return self._decision(case, LANGUAGE_ADEQUATE, matches[0], False)
        return self._decision(case, LANGUAGE_UNKNOWN, MODEL_DISRUPTING_PROBE, False)


class ConservativeAbstainerV07(_BaseOperatorPolicy):
    name = "conservative_abstainer_v0_7"

    def decide(self, case: LanguageHeldOutCase) -> OperatorDecision:
        matches = self._matches(case)
        if len(matches) == 1:
            return self._decision(case, LANGUAGE_ADEQUATE, matches[0], False)
        return self._decision(case, LANGUAGE_UNKNOWN, MODEL_DISRUPTING_PROBE, False)


class BoundaryOnlyAuditorV07(_BaseOperatorPolicy):
    name = "boundary_only_auditor_v0_7"

    def _fit_after_grouping(self) -> None:
        self._detected_collisions = {
            signature for signature, labels in self._labels_by_signature.items()
            if len(labels) > 1
        }

    def decide(self, case: LanguageHeldOutCase) -> OperatorDecision:
        signature = current_language_signature(case)
        matches = self._matches(case)
        if len(matches) == 1:
            return self._decision(case, LANGUAGE_ADEQUATE, matches[0], False)
        if len(matches) > 1:
            return self._decision(case, LANGUAGE_INADEQUATE, LANGUAGE_EXPANSION_PROBE, True)
        return self._decision(case, LANGUAGE_UNKNOWN, MODEL_DISRUPTING_PROBE, False)


class _GenericSynthesizer(_BaseOperatorPolicy):
    expand_only_collisions = True

    def _fit_after_grouping(self) -> None:
        predicates_per_search = len(generated_predicates())
        for signature, labels in self._labels_by_signature.items():
            is_collision = len(labels) > 1
            if is_collision:
                self._detected_collisions.add(signature)

            should_expand = is_collision or not self.expand_only_collisions
            if not should_expand:
                continue

            self._expanded_signatures.add(signature)
            group = self._by_signature[signature]
            if not is_collision:
                # Search is invoked but there is no within-signature contrast to repair.
                self._search_cost += predicates_per_search
                continue

            for target_probe in labels:
                selection, predicate = _synthesize(group, target_probe)
                self._search_cost += selection.candidate_evaluations
                self._selections[target_probe] = selection
                if predicate is not None and selection.retained:
                    self._generated_operators[target_probe] = predicate

    def decide(self, case: LanguageHeldOutCase) -> OperatorDecision:
        signature = current_language_signature(case)
        matches = self._matches(case)
        if len(matches) == 1:
            return self._decision(case, LANGUAGE_ADEQUATE, matches[0], False)
        if not matches:
            return self._decision(case, LANGUAGE_UNKNOWN, MODEL_DISRUPTING_PROBE, False)

        active = tuple(
            probe for probe in matches
            if probe in self._generated_operators
            and self._generated_operators[probe].active(case)
        )
        if len(active) == 1:
            probe = active[0]
            return self._decision(
                case,
                LANGUAGE_ADEQUATE,
                probe,
                signature in self._detected_collisions,
                self._generated_operators[probe].name,
            )
        return self._decision(
            case,
            LANGUAGE_INADEQUATE,
            LANGUAGE_EXPANSION_PROBE,
            signature in self._detected_collisions,
        )


class AlwaysExpandGenericSynthesizer(_GenericSynthesizer):
    """Strong generic synthesis control: run the same generator everywhere."""

    name = "always_expand_generic_synthesizer"
    expand_only_collisions = False


class BoundaryGatedGenericSynthesizer(_GenericSynthesizer):
    """Run generic synthesis only after a demonstrated current-language collision."""

    name = "boundary_gated_generic_synthesizer"
    expand_only_collisions = True


def policies() -> tuple[OperatorPolicy, ...]:
    return (
        CurrentLanguageAssimilatorV07(),
        ConservativeAbstainerV07(),
        BoundaryOnlyAuditorV07(),
        AlwaysExpandGenericSynthesizer(),
        BoundaryGatedGenericSynthesizer(),
    )


def current_language_expression_count() -> int:
    return len(current_language())
