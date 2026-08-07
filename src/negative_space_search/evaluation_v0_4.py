"""Evaluation for v0.4 representation acquisition and repair."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .representation_v0_4 import (
    MODEL_DISRUPTING_PROBE,
    PROBE_COST,
    RawHeldOutCase,
    RepresentationDecision,
    RepresentationPolicy,
)


@dataclass(frozen=True)
class StageSummary:
    policy: str
    stage: str
    held_out_selection_rate: float
    known_case_selection_rate: float
    novel_model_check_rate: float
    false_model_check_rate: float
    evidence_cost: float
    representation_cost: int

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def evaluate_stage(
    policy: RepresentationPolicy,
    cases: tuple[RawHeldOutCase, ...],
    stage: str,
) -> tuple[tuple[RepresentationDecision, ...], StageSummary]:
    decisions = tuple(policy.decide(case) for case in cases)
    known = tuple(decision for decision in decisions if decision.case_id != "R_NOVEL")
    novel = next(decision for decision in decisions if decision.case_id == "R_NOVEL")

    summary = StageSummary(
        policy=policy.name,
        stage=stage,
        held_out_selection_rate=sum(decision.correct for decision in decisions) / len(decisions),
        known_case_selection_rate=sum(decision.correct for decision in known) / len(known),
        novel_model_check_rate=float(novel.selected_probe == MODEL_DISRUPTING_PROBE),
        false_model_check_rate=sum(decision.model_check for decision in known) / len(known),
        evidence_cost=len(decisions) * PROBE_COST,
        representation_cost=policy.representation_cost,
    )
    return decisions, summary


def representation_change_rate(
    before: dict[str, str],
    after: dict[str, str],
) -> float:
    if before.keys() != after.keys():
        raise ValueError("representation snapshots must cover the same probes")
    return sum(before[probe] != after[probe] for probe in before) / len(before)
