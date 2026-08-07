"""v0.4 representation acquisition and repair benchmark.

The learner receives raw resolved histories without semantic causal labels. It may
select from a small frozen library of generic unary and pairwise relations. The
experiment tests whether a previously rewarded surface representation is revised
after diagnostic failures reveal that it does not transfer.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable, Protocol


KNOWN_PROBES = (
    "independence_probe",
    "payoff_regime_probe",
    "topology_probe",
)
MODEL_DISRUPTING_PROBE = "model_disrupting_probe"
COMPLEXITY_PENALTY = 0.01
NEAREST_HISTORY_THRESHOLD = 0.10
PROBE_COST = 0.25


class RawObservable(Protocol):
    paired_measurements: tuple[tuple[float, float], ...]
    surface_hint: float


@dataclass(frozen=True)
class RawResolvedEpisode:
    episode_id: str
    paired_measurements: tuple[tuple[float, float], ...]
    surface_hint: float
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
class RawHeldOutCase:
    case_id: str
    paired_measurements: tuple[tuple[float, float], ...]
    surface_hint: float
    prediction: float
    outcome: float
    timestamp: int
    cost: float
    correct_probe: str

    @property
    def error(self) -> float:
        return abs(self.prediction - self.outcome)


@dataclass(frozen=True)
class CandidateRelation:
    name: str
    complexity: int

    def active(self, item: RawObservable) -> bool:
        if self.name == "hint_high":
            return item.surface_hint >= 0.60
        if self.name == "hint_low":
            return item.surface_hint <= -0.60
        if self.name == "hint_near_zero":
            return abs(item.surface_hint) <= 0.15

        pair_name, relation = self.name.split("_", 1)
        pair_index = int(pair_name.removeprefix("pair"))
        left, right = item.paired_measurements[pair_index]

        if relation == "close":
            return abs(left - right) <= 0.08
        if relation == "far":
            return abs(left - right) >= 0.65
        if relation == "sign_disagree":
            return left * right < 0 and min(abs(left), abs(right)) >= 0.10
        raise ValueError(f"unknown candidate relation: {self.name}")


@dataclass(frozen=True)
class FeatureSelection:
    probe: str
    relation_name: str
    complexity: int
    balanced_accuracy: float
    objective: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class RepresentationDecision:
    case_id: str
    policy: str
    selected_probe: str
    correct: bool
    model_check: bool
    active_probe_features: tuple[str, ...]
    nearest_history_id: str | None = None
    nearest_history_distance: float | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class RepresentationPolicy(Protocol):
    name: str

    def fit(self, episodes: Iterable[RawResolvedEpisode]) -> None:
        ...

    def decide(self, case: RawHeldOutCase) -> RepresentationDecision:
        ...

    @property
    def representation_cost(self) -> int:
        ...


def candidate_relations() -> tuple[CandidateRelation, ...]:
    relations = [
        CandidateRelation("hint_high", 1),
        CandidateRelation("hint_low", 1),
        CandidateRelation("hint_near_zero", 1),
    ]
    for pair_index in range(3):
        relations.extend(
            (
                CandidateRelation(f"pair{pair_index}_close", 2),
                CandidateRelation(f"pair{pair_index}_far", 2),
                CandidateRelation(f"pair{pair_index}_sign_disagree", 2),
            )
        )
    return tuple(relations)


def _relation_by_name(name: str) -> CandidateRelation:
    return next(relation for relation in candidate_relations() if relation.name == name)


def _balanced_accuracy(
    relation: CandidateRelation,
    episodes: tuple[RawResolvedEpisode, ...],
    target_probe: str,
) -> float:
    positives = tuple(episode for episode in episodes if episode.resolving_probe == target_probe)
    negatives = tuple(episode for episode in episodes if episode.resolving_probe != target_probe)
    if not positives or not negatives:
        raise ValueError("each probe requires positive and negative resolved episodes")

    true_positive_rate = sum(relation.active(episode) for episode in positives) / len(positives)
    true_negative_rate = sum(not relation.active(episode) for episode in negatives) / len(negatives)
    return (true_positive_rate + true_negative_rate) / 2.0


def _select_relation(
    episodes: tuple[RawResolvedEpisode, ...],
    target_probe: str,
) -> FeatureSelection:
    scored: list[tuple[CandidateRelation, float, float]] = []
    for relation in candidate_relations():
        accuracy = _balanced_accuracy(relation, episodes, target_probe)
        objective = accuracy - COMPLEXITY_PENALTY * relation.complexity
        scored.append((relation, accuracy, objective))

    scored.sort(
        key=lambda item: (
            -item[2],
            -item[1],
            item[0].complexity,
            item[0].name,
        )
    )
    relation, accuracy, objective = scored[0]
    return FeatureSelection(
        probe=target_probe,
        relation_name=relation.name,
        complexity=relation.complexity,
        balanced_accuracy=accuracy,
        objective=objective,
    )


def _measurement_pairs(kind: str) -> tuple[tuple[float, float], ...]:
    if kind == "dependency":
        return ((0.42, 0.46), (0.30, 0.48), (0.30, 0.46))
    if kind == "payoff":
        return ((0.18, 0.38), (0.10, 0.90), (0.22, 0.43))
    if kind == "topology":
        return ((0.16, 0.35), (0.28, 0.46), (0.32, -0.32))
    if kind == "novel":
        return ((0.20, 0.40), (0.30, 0.50), (0.25, 0.45))
    raise ValueError(kind)


def _episode(
    episode_id: str,
    kind: str,
    surface_hint: float,
    prediction: float,
    outcome: float,
    timestamp: int,
) -> RawResolvedEpisode:
    probe = {
        "dependency": "independence_probe",
        "payoff": "payoff_regime_probe",
        "topology": "topology_probe",
    }[kind]
    return RawResolvedEpisode(
        episode_id=episode_id,
        paired_measurements=_measurement_pairs(kind),
        surface_hint=surface_hint,
        prediction=prediction,
        outcome=outcome,
        selected_action="ordinary_search",
        timestamp=timestamp,
        cost=0.10,
        resolving_probe=probe,
    )


def acquisition_episodes() -> tuple[RawResolvedEpisode, ...]:
    return (
        _episode("A_D1", "dependency", 0.85, 0.80, 0.20, 1),
        _episode("A_D2", "dependency", 0.82, 0.70, 0.10, 2),
        _episode("A_P1", "payoff", 0.02, 0.60, 0.00, 3),
        _episode("A_P2", "payoff", -0.04, 0.50, -0.10, 4),
        _episode("A_N1", "topology", -0.86, 0.40, -0.20, 5),
        _episode("A_N2", "topology", -0.81, 0.30, -0.30, 6),
    )


def repair_episodes() -> tuple[RawResolvedEpisode, ...]:
    return (
        _episode("B_D", "dependency", -0.78, 0.44, -0.16, 7),
        _episode("B_P", "payoff", 0.84, 0.59, -0.01, 8),
        _episode("B_N", "topology", 0.00, 0.79, 0.19, 9),
    )


def held_out_cases() -> tuple[RawHeldOutCase, ...]:
    return (
        RawHeldOutCase(
            case_id="R_DEP",
            paired_measurements=_measurement_pairs("dependency"),
            surface_hint=-0.80,
            prediction=0.78,
            outcome=0.18,
            timestamp=10,
            cost=PROBE_COST,
            correct_probe="independence_probe",
        ),
        RawHeldOutCase(
            case_id="R_PAY",
            paired_measurements=_measurement_pairs("payoff"),
            surface_hint=0.85,
            prediction=0.45,
            outcome=-0.15,
            timestamp=11,
            cost=PROBE_COST,
            correct_probe="payoff_regime_probe",
        ),
        RawHeldOutCase(
            case_id="R_NET",
            paired_measurements=_measurement_pairs("topology"),
            surface_hint=0.00,
            prediction=0.58,
            outcome=-0.02,
            timestamp=12,
            cost=PROBE_COST,
            correct_probe="topology_probe",
        ),
        RawHeldOutCase(
            case_id="R_NOVEL",
            paired_measurements=_measurement_pairs("novel"),
            surface_hint=0.85,
            prediction=0.61,
            outcome=0.01,
            timestamp=13,
            cost=PROBE_COST,
            correct_probe=MODEL_DISRUPTING_PROBE,
        ),
    )


class AdaptiveRepresentationLearner:
    """Learns one probe-specific relation from raw resolved histories."""

    name = "adaptive_representation_learner"

    def __init__(self) -> None:
        self._selections: tuple[FeatureSelection, ...] = ()

    def fit(self, episodes: Iterable[RawResolvedEpisode]) -> None:
        frozen = tuple(episodes)
        self._selections = tuple(_select_relation(frozen, probe) for probe in KNOWN_PROBES)

    @property
    def selections(self) -> tuple[FeatureSelection, ...]:
        if not self._selections:
            raise RuntimeError("fit must be called before reading selections")
        return self._selections

    @property
    def representation_cost(self) -> int:
        return sum(selection.complexity for selection in self.selections)

    def decide(self, case: RawHeldOutCase) -> RepresentationDecision:
        active = tuple(
            selection.probe
            for selection in self.selections
            if _relation_by_name(selection.relation_name).active(case)
        )
        selected_probe = active[0] if len(active) == 1 else MODEL_DISRUPTING_PROBE
        return RepresentationDecision(
            case_id=case.case_id,
            policy=self.name,
            selected_probe=selected_probe,
            correct=selected_probe == case.correct_probe,
            model_check=selected_probe == MODEL_DISRUPTING_PROBE,
            active_probe_features=active,
        )


class FixedTypedOracle:
    """Upper-bound control supplied with the stable relations."""

    name = "fixed_typed_oracle"

    _mapping = (
        FeatureSelection("independence_probe", "pair0_close", 2, 1.0, 1.0),
        FeatureSelection("payoff_regime_probe", "pair1_far", 2, 1.0, 1.0),
        FeatureSelection("topology_probe", "pair2_sign_disagree", 2, 1.0, 1.0),
    )

    def fit(self, episodes: Iterable[RawResolvedEpisode]) -> None:
        tuple(episodes)

    @property
    def selections(self) -> tuple[FeatureSelection, ...]:
        return self._mapping

    @property
    def representation_cost(self) -> int:
        return sum(selection.complexity for selection in self._mapping)

    def decide(self, case: RawHeldOutCase) -> RepresentationDecision:
        active = tuple(
            selection.probe
            for selection in self._mapping
            if _relation_by_name(selection.relation_name).active(case)
        )
        selected_probe = active[0] if len(active) == 1 else MODEL_DISRUPTING_PROBE
        return RepresentationDecision(
            case_id=case.case_id,
            policy=self.name,
            selected_probe=selected_probe,
            correct=selected_probe == case.correct_probe,
            model_check=selected_probe == MODEL_DISRUPTING_PROBE,
            active_probe_features=active,
        )


class CompressedOutcomeMemory:
    """Case-memory control that discards raw relational measurements."""

    name = "compressed_outcome_memory"

    def __init__(self) -> None:
        self._episodes: tuple[RawResolvedEpisode, ...] = ()

    def fit(self, episodes: Iterable[RawResolvedEpisode]) -> None:
        self._episodes = tuple(episodes)

    @property
    def representation_cost(self) -> int:
        return 0

    @staticmethod
    def _distance(episode: RawResolvedEpisode, case: RawHeldOutCase) -> float:
        return (
            abs(episode.prediction - case.prediction)
            + abs(episode.outcome - case.outcome)
            + abs(episode.error - case.error)
        ) / 3.0

    def decide(self, case: RawHeldOutCase) -> RepresentationDecision:
        if not self._episodes:
            raise RuntimeError("fit must be called before decide")
        nearest = min(
            self._episodes,
            key=lambda episode: (self._distance(episode, case), episode.episode_id),
        )
        distance = self._distance(nearest, case)
        selected_probe = (
            MODEL_DISRUPTING_PROBE
            if distance > NEAREST_HISTORY_THRESHOLD
            else nearest.resolving_probe
        )
        return RepresentationDecision(
            case_id=case.case_id,
            policy=self.name,
            selected_probe=selected_probe,
            correct=selected_probe == case.correct_probe,
            model_check=selected_probe == MODEL_DISRUPTING_PROBE,
            active_probe_features=(),
            nearest_history_id=None if distance > NEAREST_HISTORY_THRESHOLD else nearest.episode_id,
            nearest_history_distance=distance,
        )
