"""Evaluation for v0.3 representation-transfer benchmark."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .representation_v0_3 import PROBE_COST, HeldOutCase, TransferDecision, TransferPolicy


@dataclass(frozen=True)
class TransferSummary:
    policy: str
    held_out_evidence_selection_rate: float
    known_topology_transfer_rate: float
    novel_topology_model_check_rate: float
    false_model_check_rate: float
    evidence_cost: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def summarize(policy: TransferPolicy, cases: tuple[HeldOutCase, ...]) -> tuple[tuple[TransferDecision, ...], TransferSummary]:
    decisions = tuple(policy.decide(case) for case in cases)
    known = tuple(decision for decision in decisions if decision.case_id != "H_NOVEL")
    novel = next(decision for decision in decisions if decision.case_id == "H_NOVEL")

    summary = TransferSummary(
        policy=policy.name,
        held_out_evidence_selection_rate=sum(decision.correct for decision in decisions) / len(decisions),
        known_topology_transfer_rate=sum(decision.correct for decision in known) / len(known),
        novel_topology_model_check_rate=float(novel.selected_probe == "model_disrupting_probe"),
        false_model_check_rate=sum(decision.model_check for decision in known) / len(known),
        evidence_cost=len(decisions) * PROBE_COST,
    )
    return decisions, summary
