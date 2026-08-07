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

**v0.3 update:** run `31173841990` showed that a typed representation can route an explicitly unclassified held-out residual to a model-disrupting probe. This remains a representation-ablation result, not closure of the original localization failure; the relevant distinction was explicitly preserved in history rather than inferred from the original case.

**Next discriminator:** test whether the system can learn which distinctions deserve preservation and when model-adequacy checks are warranted when those fields are noisy, partial, or not pre-typed.

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

**v0.3 update:** run `31173841990` again found identity once representation was matched: `typed_general_causal_history` and `structured_negative_space_history` produced identical decisions and metrics. The difference was between typed and compressed history, not between negative-space and general causal labels.

**Claim constraint:** the current evidence supports history-sensitive, representation-sensitive search control. It does not support a distinct performance advantage for explicit negative-space framing over a matched strong causal reasoner preserving the same distinctions.

**Next discriminator:** compare learned representation selection under matched raw histories and costs rather than hand-specified typed fields.

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

**v0.3 update:** the next representation-transfer test did not rescue a unique negative-space mechanism. Typed general causal and typed negative-space histories again tied exactly.

**Claim constraint:** do not cite v0.2 or v0.3 as evidence that `Psi_NS` outperforms strong adaptive causal search when relevant history structure is matched.

**Next discriminator:** test whether the negative-space framing helps discover or select useful representations under noise and representation cost, rather than receiving them by construction.

**Status:** open.

---

## NR-004 — v0.3 representation gain is not uniquely negative-space

**Run:** GitHub Actions `31173841990`

**Observed:** the representation ablation produced:

```text
generic_compressed_causal_history:
  held_out_evidence_selection_rate = 0.0
  known_topology_transfer_rate = 0.0
  novel_topology_model_check_rate = 0.0

typed_general_causal_history:
  held_out_evidence_selection_rate = 1.0
  known_topology_transfer_rate = 1.0
  novel_topology_model_check_rate = 1.0

structured_negative_space_history:
  held_out_evidence_selection_rate = 1.0
  known_topology_transfer_rate = 1.0
  novel_topology_model_check_rate = 1.0
```

The two typed systems shared the same representation and decision rule and differed only in name. Their outputs were identical on every held-out case.

**What this identifies:** preserving typed relations can matter substantially when superficial prediction/outcome/error statistics are misleading and the benchmark requires structural transfer.

**What this does not identify:** a unique negative-space algorithm or framing advantage. A generic causal learner with the same typed representation received the full benefit.

**Claim constraint:** attribute the current v0.3 gain to representation quality, not to negative-space identity.

**Additional limitation:** the case matrix was deliberately constructed so compressed surface similarity pointed to the wrong training topology. This is a valid representation ablation but not evidence that compressed causal histories generally fail in natural settings.

**Next discriminator:** force the representation itself to be learned or selected under cost, noise, partial observability, and distractor fields. Include cases where the current typed representation is actively misleading.

**Status:** open.

---

## Ledger rule

A negative result may be closed only by a new experiment that directly discriminates the implicated failure. A code change that makes the old case pass is not sufficient by itself.
