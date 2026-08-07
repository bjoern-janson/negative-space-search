# Negative-Result Ledger

This ledger preserves failures that constrain the search architecture. Entries are not bugs to erase automatically; they are evidence about which claims or mechanisms have not earned authority.

## NR-001 — model-inadequacy localization failed

**Run:** GitHub Actions `31171905710`

**Observed:** `causal_negative_space_search` selected the expected conservative action on `E_model_inadequate` but failed both:

```text
diagnosis_supported = false
evidence_match = false
```

It abstained without correctly identifying causal-vocabulary inadequacy or requesting `cross_interface_probe`.

**What this identifies:** the current policy does not yet demonstrate the claimed ability to distinguish ordinary unresolved uncertainty from inadequacy of its causal vocabulary from the original `E_model_inadequate` observation.

**What this does not identify:** failure of the full negative-space-search hypothesis, failure of the frozen core, or failure of abstention as a decision primitive.

**v0.1.1 update:** run `31172485528` showed that, when the shared observable history explicitly contains repeated inconclusive ordinary probes, the negative-space policy selects a `model_disrupting_probe` and correctly separates within-model uncertainty from model inadequacy after that evidence arrives. This is a partial discriminator, not closure: the original `E_model_inadequate` trigger remains unsolved and the escalation behavior has not transferred to held-out signatures.

**v0.2 update:** run `31173078806` showed that a history-aware policy can distinguish systematic residual structure from noise-compatible uncertainty on the frozen v0.2 surface split. This still does not close NR-001: the capability was implemented through an explicit standardized-residual rule rather than discovered from the original unresolved observation.

**Next discriminator:** test whether the search process can learn when model-adequacy checks are warranted from attributed prior failures, including a held-out failure structure not represented by residual persistence.

**Status:** open.

---

## NR-002 — no incremental advantage over general causal reasoning on hostile equivalence

**Run:** GitHub Actions `31171905710`

**Observed:** both policies passed the hostile observational-equivalence test:

```text
general_causal_reasoner: pass
causal_negative_space_search: pass
```

Both avoided guessing and requested `controlled_external_value_test` for the identical underinvestment / justified-selection observations.

**What this identifies:** the hostile pair distinguishes causal evidence-seeking from naive gap/opportunity search, but does not distinguish explicit causal negative-space search from a strong general causal reasoner.

**What this does not identify:** equivalence across richer negative-space tasks, model-inadequacy tests, counterfactual causal fidelity, durability, or history-based search adaptation.

**v0.1.1 update:** run `31172485528` produced a narrow difference on the model-adequacy evidence-selection task. `causal_negative_space_search` requested `model_disrupting_probe`; `general_causal_reasoner` requested more within-model evidence. When the model-disrupting result was supplied to both, both interpreted the two regimes correctly. This localized the observed difference to investigative-attention / evidence-selection policy, not post-evidence causal reasoning.

**v0.2 update:** run `31173078806` removed that narrow advantage once the strong causal baseline received the same history-sensitive escalation competence. `history_aware_general_causal_reasoner` and `history_aware_negative_space_search` were identical on true escalation, false escalation, overall and held-out evidence selection, post-evidence interpretation, and evidence cost.

**Claim constraint:** the current evidence supports history-sensitive selective escalation as a useful search-control capability. It does not support a distinct performance advantage for explicit negative-space framing over a matched strong causal reasoner.

**Next discriminator:** compare learnability and transfer of search-control updates, not hand-coded framing, on a novel failure structure.

**Status:** open.

---

## NR-003 — v0.2 does not show incremental value beyond history-aware causal search

**Run:** GitHub Actions `31173078806`

**Observed:** both history-aware strong policies achieved:

```text
true_escalation_rate = 1.0
false_escalation_rate = 0.0
correct_evidence_selection_rate = 1.0
held_out_correct_evidence_selection_rate = 1.0
post_evidence_regime_interpretation_rate = 1.0
evidence_cost = 2.0
```

The frozen v0.1.1 controls failed in opposite directions: the negative-space policy escalated every unresolved case, while the general causal policy never escalated.

**What this identifies:** structured failure history can support selective escalation and prevent both automatic escalation and automatic within-model persistence.

**What this does not identify:** any incremental value attributable specifically to negative-space framing. The matched history-aware general causal reasoner achieved the same result using the same observable history, residual summary, threshold, evidence affordances, and costs.

**Claim constraint:** do not cite v0.2 as evidence that `Psi_NS` outperforms strong adaptive causal search.

**Next discriminator:** allow both search processes to update from prior diagnostic outcomes and evaluate transfer to a held-out failure structure that is not reducible to the v0.2 standardized-residual signature.

**Status:** open.

---

## Ledger rule

A negative result may be closed only by a new experiment that directly discriminates the implicated failure. A code change that makes the old case pass is not sufficient by itself.
