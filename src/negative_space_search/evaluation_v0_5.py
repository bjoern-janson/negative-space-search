"""Evaluation for the v0.5 basis-failure benchmark."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .basis_v0_5 import BasisDecision, BasisPolicy
from .representation_v0_4 import MODEL_DISRUPTING_PROBE, RawHeldOutCase


TARGET_PROBE = "interaction_probe"
TARGET_RELATION = "AND(pair0_close,pair1_far)"
CONTROL_PROBES = {
    "independence_probe",
    "payoff_regime_probe",
    "topology_probe",
}


@dataclass(frozen=True)
class BasisSummary:
    policy: str
    basis_inadequacy_detection_rate: float
    false_basis_inadequacy_rate: float
    basis_expansion_rate: float
    construction_success_rate: float
    held_out_evidence_selection_rate: float
    interaction_transfer_rate: float
    constituent_false_positive_rate: float
    novel_model_check_rate: float
    search_cost: int
    representation_cost: int

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def summarize(
    policy: BasisPolicy,
    cases: tuple[RawHeldOutCase, ...],
) -> tuple[tuple[BasisDecision, ...], BasisSummary]:
    decisions = tuple(policy.decide(case) for case in cases)
    audits = policy.audits
    target_audit = next(audit for audit in audits if audit.probe == TARGET_PROBE)
    control_audits = tuple(audit for audit in audits if audit.probe in CONTROL_PROBES)
    interaction = tuple(decision for decision in decisions if decision.case_id.startswith("H_INT_"))
    constituents = tuple(
        decision for decision in decisions if decision.case_id in {"H_DEP_ONLY", "H_PAY_ONLY"}
    )
    novel = next(decision for decision in decisions if decision.case_id == "H_NOVEL")

    summary = BasisSummary(
        policy=policy.name,
        basis_inadequacy_detection_rate=float(target_audit.basis_inadequate),
        false_basis_inadequacy_rate=sum(audit.basis_inadequate for audit in control_audits) / len(control_audits),
        basis_expansion_rate=sum(audit.expanded for audit in audits) / len(audits),
        construction_success_rate=float(target_audit.selected_relation == TARGET_RELATION),
        held_out_evidence_selection_rate=sum(decision.correct for decision in decisions) / len(decisions),
        interaction_transfer_rate=sum(decision.correct for decision in interaction) / len(interaction),
        constituent_false_positive_rate=sum(
            decision.selected_probe == TARGET_PROBE for decision in constituents
        ) / len(constituents),
        novel_model_check_rate=float(novel.selected_probe == MODEL_DISRUPTING_PROBE),
        search_cost=policy.search_cost,
        representation_cost=policy.representation_cost,
    )
    return decisions, summary
