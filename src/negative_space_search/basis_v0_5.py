"""v0.5 conditional basis-expansion benchmark.

The initial basis is the frozen v0.4 single-relation library. One probe family
requires a conjunction that is withheld from that initial basis. The benchmark
separates basis-inadequacy detection from conditional relation construction.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import combinations
from typing import Iterable, Protocol

from .representation_v0_4 import (
    MODEL_DISRUPTING_PROBE,
    CandidateRelation,
    RawHeldOutCase,
    RawResolvedEpisode,
    candidate_relations,
)


PROBES = (
    "independence_probe",
    "payoff_regime_probe",
    "topology_probe",
    "interaction_probe",
)
BASIS_ADEQUACY_THRESHOLD = 0.90
COMPLEXITY_PENALTY = 0.01
CONJUNCTION_EXTRA_COMPLEXITY = 1
PROBE_COST = 0.25


@dataclass(frozen=True)
class RelationExpression:
    name: str
    complexity: int
    operands: tuple[str, ...]

    def active(self, item: object) -> bool:
        relations = {relation.name: relation for relation in candidate_relations()}
        if len(self.operands) == 1:
            return relations[self.operands[0]].active(item)  # type: ignore[arg-type]
        if len(self.operands) == 2:
            left, right = self.operands
            return relations[left].active(item) and relations[right].active(item)  # type: ignore[arg-type]
        raise ValueError(f"unsupported expression arity: {self.operands}")


@dataclass(frozen=True)
class ProbeAudit:
    probe: str
    best_single_relation: str
    best_single_balanced_accuracy: float
    basis_inadequate: bool
    expanded: bool
    selected_relation: str
    selected_balanced_accuracy: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class BasisDecision:
    case_id: str
    policy: str
    selected_probe: str
    correct: bool
    model_check: bool
    active_probe_features: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class BasisPolicy(Protocol):
    name: str

    def fit(self, episodes: Iterable[RawResolvedEpisode]) -> None:
        ...

    def decide(self, case: RawHeldOutCase) -> BasisDecision:
        ...

    @property
    def audits(self) -> tuple[ProbeAudit, ...]:
        ...

    @property
    def search_cost(self) -> int:
        ...

    @property
    def representation_cost(self) -> int:
        ...


def _single_expressions() -> tuple[RelationExpression, ...]:
    return tuple(
        RelationExpression(relation.name, relation.complexity, (relation.name,))
        for relation in candidate_relations()
    )


def _conjunction_expressions() -> tuple[RelationExpression, ...]:
    relations = tuple(candidate_relations())
    expressions: list[RelationExpression] = []
    for left, right in combinations(relations, 2):
        operands = tuple(sorted((left.name, right.name)))
        expressions.append(
            RelationExpression(
                name=f"AND({operands[0]},{operands[1]})",
                complexity=left.complexity + right.complexity + CONJUNCTION_EXTRA_COMPLEXITY,
                operands=operands,
            )
        )
    return tuple(expressions)


def _balanced_accuracy(
    expression: RelationExpression,
    episodes: tuple[RawResolvedEpisode, ...],
    target_probe: str,
) -> float:
    positives = tuple(episode for episode in episodes if episode.resolving_probe == target_probe)
    negatives = tuple(episode for episode in episodes if episode.resolving_probe != target_probe)
    if not positives or not negatives:
        raise ValueError("each probe needs positive and negative resolved episodes")
    true_positive_rate = sum(expression.active(episode) for episode in positives) / len(positives)
    true_negative_rate = sum(not expression.active(episode) for episode in negatives) / len(negatives)
    return (true_positive_rate + true_negative_rate) / 2.0


def _best_expression(
    expressions: tuple[RelationExpression, ...],
    episodes: tuple[RawResolvedEpisode, ...],
    probe: str,
) -> tuple[RelationExpression, float]:
    scored: list[tuple[RelationExpression, float, float]] = []
    for expression in expressions:
        accuracy = _balanced_accuracy(expression, episodes, probe)
        objective = accuracy - COMPLEXITY_PENALTY * expression.complexity
        scored.append((expression, accuracy, objective))
    scored.sort(key=lambda item: (-item[2], -item[1], item[0].complexity, item[0].name))
    expression, accuracy, _ = scored[0]
    return expression, accuracy


def _episode(
    episode_id: str,
    resolving_probe: str,
    pairs: tuple[tuple[float, float], ...],
    hint: float,
    prediction: float,
    outcome: float,
    timestamp: int,
) -> RawResolvedEpisode:
    return RawResolvedEpisode(
        episode_id=episode_id,
        paired_measurements=pairs,
        surface_hint=hint,
        prediction=prediction,
        outcome=outcome,
        selected_action="ordinary_search",
        timestamp=timestamp,
        cost=0.10,
        resolving_probe=resolving_probe,
    )


def training_episodes() -> tuple[RawResolvedEpisode, ...]:
    return (
        _episode("T_I1", "interaction_probe", ((0.42, 0.46), (0.10, 0.90), (0.20, 0.42)), 0.80, 0.80, 0.20, 1),
        _episode("T_I2", "interaction_probe", ((0.35, 0.39), (0.15, 0.84), (0.18, 0.40)), -0.75, 0.70, 0.10, 2),
        _episode("T_I3", "interaction_probe", ((0.50, 0.56), (0.05, 0.75), (0.25, 0.44)), 0.05, 0.60, 0.00, 3),
        _episode("T_I4", "interaction_probe", ((0.30, 0.35), (0.20, 0.90), (0.22, 0.41)), 0.65, 0.50, -0.10, 4),
        _episode("T_D1", "independence_probe", ((0.42, 0.46), (0.30, 0.48), (0.50, 0.54)), 0.82, 0.78, 0.18, 5),
        _episode("T_D2", "independence_probe", ((0.35, 0.40), (0.25, 0.43), (0.40, 0.45)), 0.78, 0.68, 0.08, 6),
        _episode("T_D3", "independence_probe", ((0.51, 0.55), (0.33, 0.50), (0.30, 0.37)), -0.70, 0.58, -0.02, 7),
        _episode("T_P1", "payoff_regime_probe", ((0.18, 0.38), (0.10, 0.90), (0.05, 0.80)), 0.00, 0.76, 0.16, 8),
        _episode("T_P2", "payoff_regime_probe", ((0.20, 0.41), (0.12, 0.82), (0.15, 0.88)), 0.05, 0.66, 0.06, 9),
        _episode("T_P3", "payoff_regime_probe", ((0.22, 0.40), (0.05, 0.75), (0.20, 0.90)), 0.75, 0.56, -0.04, 10),
        _episode("T_N1", "topology_probe", ((0.16, 0.35), (0.28, 0.46), (0.32, -0.32)), -0.85, 0.74, 0.14, 11),
        _episode("T_N2", "topology_probe", ((0.20, 0.38), (0.30, 0.50), (0.25, -0.30)), -0.80, 0.64, 0.04, 12),
        _episode("T_N3", "topology_probe", ((0.25, 0.44), (0.35, 0.55), (0.40, -0.20)), 0.02, 0.54, -0.06, 13),
    )


def held_out_cases() -> tuple[RawHeldOutCase, ...]:
    rows = (
        ("H_INT_1", "interaction_probe", ((0.44, 0.49), (0.08, 0.82), (0.24, 0.43)), -0.72, 0.79, 0.19),
        ("H_INT_2", "interaction_probe", ((0.27, 0.33), (0.18, 0.88), (0.31, 0.50)), 0.03, 0.69, 0.09),
        ("H_DEP_ONLY", "independence_probe", ((0.47, 0.52), (0.31, 0.50), (0.43, 0.48)), -0.78, 0.59, -0.01),
        ("H_PAY_ONLY", "payoff_regime_probe", ((0.21, 0.40), (0.07, 0.78), (0.12, 0.82)), 0.81, 0.49, -0.11),
        ("H_TOPOLOGY", "topology_probe", ((0.19, 0.39), (0.32, 0.52), (0.35, -0.25)), 0.00, 0.39, -0.21),
        ("H_NOVEL", MODEL_DISRUPTING_PROBE, ((0.18, 0.39), (0.29, 0.49), (0.22, 0.43)), 0.72, 0.29, -0.31),
    )
    return tuple(
        RawHeldOutCase(
            case_id=case_id,
            paired_measurements=pairs,
            surface_hint=hint,
            prediction=prediction,
            outcome=outcome,
            timestamp=14 + index,
            cost=PROBE_COST,
            correct_probe=probe,
        )
        for index, (case_id, probe, pairs, hint, prediction, outcome) in enumerate(rows)
    )


class _BaseBasisLearner:
    name = "base_basis_learner"

    def __init__(self) -> None:
        self._audits: tuple[ProbeAudit, ...] = ()
        self._expressions: dict[str, RelationExpression] = {}
        self._search_cost = 0

    @property
    def audits(self) -> tuple[ProbeAudit, ...]:
        if not self._audits:
            raise RuntimeError("fit must be called before reading audits")
        return self._audits

    @property
    def search_cost(self) -> int:
        return self._search_cost

    @property
    def representation_cost(self) -> int:
        if not self._expressions:
            raise RuntimeError("fit must be called before reading representation cost")
        return sum(expression.complexity for expression in self._expressions.values())

    def decide(self, case: RawHeldOutCase) -> BasisDecision:
        if not self._expressions:
            raise RuntimeError("fit must be called before decide")
        active = tuple(
            probe for probe in PROBES if self._expressions[probe].active(case)
        )
        selected_probe = active[0] if len(active) == 1 else MODEL_DISRUPTING_PROBE
        return BasisDecision(
            case_id=case.case_id,
            policy=self.name,
            selected_probe=selected_probe,
            correct=selected_probe == case.correct_probe,
            model_check=selected_probe == MODEL_DISRUPTING_PROBE,
            active_probe_features=active,
        )


class FixedSingleBasisSelector(_BaseBasisLearner):
    """Audits single-basis adequacy but cannot construct new relations."""

    name = "fixed_single_basis_selector"

    def fit(self, episodes: Iterable[RawResolvedEpisode]) -> None:
        frozen = tuple(episodes)
        singles = _single_expressions()
        audits: list[ProbeAudit] = []
        expressions: dict[str, RelationExpression] = {}
        self._search_cost = 0
        for probe in PROBES:
            best, accuracy = _best_expression(singles, frozen, probe)
            self._search_cost += len(singles)
            inadequate = accuracy < BASIS_ADEQUACY_THRESHOLD
            expressions[probe] = best
            audits.append(
                ProbeAudit(probe, best.name, accuracy, inadequate, False, best.name, accuracy)
            )
        self._expressions = expressions
        self._audits = tuple(audits)


class GatedBasisRepairLearner(_BaseBasisLearner):
    """Expands the relation basis only after a failed single-basis adequacy test."""

    name = "gated_basis_repair_learner"

    def fit(self, episodes: Iterable[RawResolvedEpisode]) -> None:
        frozen = tuple(episodes)
        singles = _single_expressions()
        conjunctions = _conjunction_expressions()
        audits: list[ProbeAudit] = []
        expressions: dict[str, RelationExpression] = {}
        self._search_cost = 0
        for probe in PROBES:
            best_single, single_accuracy = _best_expression(singles, frozen, probe)
            self._search_cost += len(singles)
            inadequate = single_accuracy < BASIS_ADEQUACY_THRESHOLD
            selected = best_single
            selected_accuracy = single_accuracy
            expanded = False
            if inadequate:
                best_conjunction, conjunction_accuracy = _best_expression(conjunctions, frozen, probe)
                self._search_cost += len(conjunctions)
                selected = best_conjunction
                selected_accuracy = conjunction_accuracy
                expanded = True
            expressions[probe] = selected
            audits.append(
                ProbeAudit(
                    probe,
                    best_single.name,
                    single_accuracy,
                    inadequate,
                    expanded,
                    selected.name,
                    selected_accuracy,
                )
            )
        self._expressions = expressions
        self._audits = tuple(audits)


class AlwaysComposeLearner(_BaseBasisLearner):
    """Brute-force control that evaluates conjunctions for every probe."""

    name = "always_compose_learner"

    def fit(self, episodes: Iterable[RawResolvedEpisode]) -> None:
        frozen = tuple(episodes)
        singles = _single_expressions()
        conjunctions = _conjunction_expressions()
        all_expressions = singles + conjunctions
        audits: list[ProbeAudit] = []
        expressions: dict[str, RelationExpression] = {}
        self._search_cost = 0
        for probe in PROBES:
            best_single, single_accuracy = _best_expression(singles, frozen, probe)
            selected, selected_accuracy = _best_expression(all_expressions, frozen, probe)
            self._search_cost += len(all_expressions)
            expressions[probe] = selected
            audits.append(
                ProbeAudit(
                    probe,
                    best_single.name,
                    single_accuracy,
                    single_accuracy < BASIS_ADEQUACY_THRESHOLD,
                    True,
                    selected.name,
                    selected_accuracy,
                )
            )
        self._expressions = expressions
        self._audits = tuple(audits)


class FixedCompositionOracle(_BaseBasisLearner):
    """Upper bound supplied with the stable single relations and conjunction."""

    name = "fixed_composition_oracle"

    def fit(self, episodes: Iterable[RawResolvedEpisode]) -> None:
        tuple(episodes)
        singles = {expression.name: expression for expression in _single_expressions()}
        conjunctions = {expression.name: expression for expression in _conjunction_expressions()}
        target_name = "AND(pair0_close,pair1_far)"
        self._expressions = {
            "independence_probe": singles["pair2_close"],
            "payoff_regime_probe": singles["pair2_far"],
            "topology_probe": singles["pair2_sign_disagree"],
            "interaction_probe": conjunctions[target_name],
        }
        self._audits = (
            ProbeAudit("independence_probe", "pair2_close", 1.0, False, False, "pair2_close", 1.0),
            ProbeAudit("payoff_regime_probe", "pair2_far", 1.0, False, False, "pair2_far", 1.0),
            ProbeAudit("topology_probe", "pair2_sign_disagree", 1.0, False, False, "pair2_sign_disagree", 1.0),
            ProbeAudit("interaction_probe", "pair0_close", 5.0 / 6.0, True, True, target_name, 1.0),
        )
        self._search_cost = 0


def v0_5_policies() -> tuple[BasisPolicy, ...]:
    return (
        FixedSingleBasisSelector(),
        GatedBasisRepairLearner(),
        AlwaysComposeLearner(),
        FixedCompositionOracle(),
    )
