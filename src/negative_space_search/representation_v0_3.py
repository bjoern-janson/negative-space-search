"""v0.3 representation-transfer benchmark.

The experiment holds raw training data, decision budget, evidence actions, and the
nearest-structure retrieval rule fixed. Learners differ only in what their persistent
history representation preserves.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable, Protocol


PROBE_COST = 0.25
MATCH_THRESHOLD = 0.10


@dataclass(frozen=True)
class RawTrainingEpisode:
    episode_id: str
    prediction: float
    outcome: float
    selected_experiment: str
    assumed_absence: str
    diagnosis: str
    intervention: str
    challenge_channel: str
    dependency_overlap: bool
    payoff_regime: str
    payoff_regime_changed: bool
    coordination_topology: str
    coordination_topology_changed: bool
    unclassified_residual: bool
    attributed_failure: str
    successful_probe: str

    @property
    def error(self) -> float:
        return abs(self.prediction - self.outcome)


@dataclass(frozen=True)
class HeldOutCase:
    case_id: str
    prediction: float
    outcome: float
    dependency_overlap: bool
    payoff_regime_changed: bool
    coordination_topology_changed: bool
    unclassified_residual: bool
    correct_probe: str

    @property
    def error(self) -> float:
        return abs(self.prediction - self.outcome)


@dataclass(frozen=True)
class GenericHistoryRecord:
    source_id: str
    prediction: float
    outcome: float
    error: float
    successful_probe: str


@dataclass(frozen=True)
class TypedHistoryRecord:
    source_id: str
    dependency_overlap: bool
    payoff_regime_changed: bool
    coordination_topology_changed: bool
    unclassified_residual: bool
    successful_probe: str

    @property
    def signature(self) -> tuple[bool, bool, bool, bool]:
        return (
            self.dependency_overlap,
            self.payoff_regime_changed,
            self.coordination_topology_changed,
            self.unclassified_residual,
        )


@dataclass(frozen=True)
class TransferDecision:
    case_id: str
    policy: str
    selected_probe: str
    nearest_training_id: str | None
    nearest_distance: float
    model_check: bool
    correct: bool

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class TransferPolicy(Protocol):
    name: str

    def fit(self, episodes: Iterable[RawTrainingEpisode]) -> None:
        ...

    def decide(self, case: HeldOutCase) -> TransferDecision:
        ...


def training_episodes() -> tuple[RawTrainingEpisode, ...]:
    """Return the three frozen attributed training failures."""

    return (
        RawTrainingEpisode(
            episode_id="T_DEP",
            prediction=0.80,
            outcome=0.20,
            selected_experiment="ordinary_validation",
            assumed_absence="independent challenge channels were sufficiently represented",
            diagnosis="shared challenge dependency",
            intervention="add another nominal validator",
            challenge_channel="registry_alpha",
            dependency_overlap=True,
            payoff_regime="stable_1",
            payoff_regime_changed=False,
            coordination_topology="pairwise",
            coordination_topology_changed=False,
            unclassified_residual=False,
            attributed_failure="shared_challenge_dependence",
            successful_probe="independence_probe",
        ),
        RawTrainingEpisode(
            episode_id="T_PAY",
            prediction=0.60,
            outcome=0.00,
            selected_experiment="ordinary_performance_test",
            assumed_absence="the old payoff function still governed external value",
            diagnosis="payoff regime drift",
            intervention="optimize the previously rewarded target",
            challenge_channel="external_outcome_beta",
            dependency_overlap=False,
            payoff_regime="shifted_2",
            payoff_regime_changed=True,
            coordination_topology="pairwise",
            coordination_topology_changed=False,
            unclassified_residual=False,
            attributed_failure="payoff_regime_drift",
            successful_probe="payoff_regime_probe",
        ),
        RawTrainingEpisode(
            episode_id="T_NET",
            prediction=0.40,
            outcome=-0.20,
            selected_experiment="ordinary_coordination_test",
            assumed_absence="pairwise coordination logic transferred to the new ecology",
            diagnosis="coordination topology mismatch",
            intervention="repeat pairwise adoption incentive",
            challenge_channel="network_outcome_gamma",
            dependency_overlap=False,
            payoff_regime="stable_3",
            payoff_regime_changed=False,
            coordination_topology="network",
            coordination_topology_changed=True,
            unclassified_residual=False,
            attributed_failure="coordination_topology_mismatch",
            successful_probe="topology_probe",
        ),
    )


def held_out_cases() -> tuple[HeldOutCase, ...]:
    """Return the frozen v0.3 held-out case matrix."""

    return (
        HeldOutCase(
            case_id="H_DEP",
            prediction=0.45,
            outcome=-0.15,
            dependency_overlap=True,
            payoff_regime_changed=False,
            coordination_topology_changed=False,
            unclassified_residual=False,
            correct_probe="independence_probe",
        ),
        HeldOutCase(
            case_id="H_PAY",
            prediction=0.79,
            outcome=0.19,
            dependency_overlap=False,
            payoff_regime_changed=True,
            coordination_topology_changed=False,
            unclassified_residual=False,
            correct_probe="payoff_regime_probe",
        ),
        HeldOutCase(
            case_id="H_NET",
            prediction=0.59,
            outcome=-0.01,
            dependency_overlap=False,
            payoff_regime_changed=False,
            coordination_topology_changed=True,
            unclassified_residual=False,
            correct_probe="topology_probe",
        ),
        HeldOutCase(
            case_id="H_NOVEL",
            prediction=0.62,
            outcome=0.02,
            dependency_overlap=False,
            payoff_regime_changed=False,
            coordination_topology_changed=False,
            unclassified_residual=True,
            correct_probe="model_disrupting_probe",
        ),
    )


def _generic_distance(record: GenericHistoryRecord, case: HeldOutCase) -> float:
    """Normalized mean absolute distance in the compressed representation."""

    return (
        abs(record.prediction - case.prediction)
        + abs(record.outcome - case.outcome)
        + abs(record.error - case.error)
    ) / 3.0


def _typed_signature(case: HeldOutCase) -> tuple[bool, bool, bool, bool]:
    return (
        case.dependency_overlap,
        case.payoff_regime_changed,
        case.coordination_topology_changed,
        case.unclassified_residual,
    )


def _typed_distance(record: TypedHistoryRecord, case: HeldOutCase) -> float:
    """Normalized Hamming distance in the typed relational representation."""

    target = _typed_signature(case)
    return sum(a is not b for a, b in zip(record.signature, target, strict=True)) / 4.0


class GenericCompressedHistoryLearner:
    """Adaptive causal learner whose persistent history drops typed relations."""

    name = "generic_compressed_causal_history"

    def __init__(self) -> None:
        self._records: tuple[GenericHistoryRecord, ...] = ()

    def fit(self, episodes: Iterable[RawTrainingEpisode]) -> None:
        self._records = tuple(
            GenericHistoryRecord(
                source_id=episode.episode_id,
                prediction=episode.prediction,
                outcome=episode.outcome,
                error=episode.error,
                successful_probe=episode.successful_probe,
            )
            for episode in episodes
        )

    def decide(self, case: HeldOutCase) -> TransferDecision:
        if not self._records:
            raise RuntimeError("fit must be called before decide")

        nearest = min(self._records, key=lambda record: (_generic_distance(record, case), record.source_id))
        distance = _generic_distance(nearest, case)

        if distance > MATCH_THRESHOLD:
            selected = "model_disrupting_probe"
            nearest_id: str | None = None
        else:
            selected = nearest.successful_probe
            nearest_id = nearest.source_id

        return TransferDecision(
            case_id=case.case_id,
            policy=self.name,
            selected_probe=selected,
            nearest_training_id=nearest_id,
            nearest_distance=distance,
            model_check=selected == "model_disrupting_probe",
            correct=selected == case.correct_probe,
        )


class TypedHistoryLearner:
    """Learner preserving typed failure relations from the same raw episodes."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._records: tuple[TypedHistoryRecord, ...] = ()

    def fit(self, episodes: Iterable[RawTrainingEpisode]) -> None:
        self._records = tuple(
            TypedHistoryRecord(
                source_id=episode.episode_id,
                dependency_overlap=episode.dependency_overlap,
                payoff_regime_changed=episode.payoff_regime_changed,
                coordination_topology_changed=episode.coordination_topology_changed,
                unclassified_residual=episode.unclassified_residual,
                successful_probe=episode.successful_probe,
            )
            for episode in episodes
        )

    def decide(self, case: HeldOutCase) -> TransferDecision:
        if not self._records:
            raise RuntimeError("fit must be called before decide")

        nearest = min(self._records, key=lambda record: (_typed_distance(record, case), record.source_id))
        distance = _typed_distance(nearest, case)

        if distance > MATCH_THRESHOLD:
            selected = "model_disrupting_probe"
            nearest_id: str | None = None
        else:
            selected = nearest.successful_probe
            nearest_id = nearest.source_id

        return TransferDecision(
            case_id=case.case_id,
            policy=self.name,
            selected_probe=selected,
            nearest_training_id=nearest_id,
            nearest_distance=distance,
            model_check=selected == "model_disrupting_probe",
            correct=selected == case.correct_probe,
        )


def v0_3_policies() -> tuple[TransferPolicy, ...]:
    return (
        GenericCompressedHistoryLearner(),
        TypedHistoryLearner("typed_general_causal_history"),
        TypedHistoryLearner("structured_negative_space_history"),
    )
