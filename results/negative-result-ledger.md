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

**v0.4 update:** run `31174650351` showed that an adaptive learner can revise from rewarded surface cues to stable pairwise relations using raw resolved histories, and then route `R_NOVEL` to `model_disrupting_probe` because none of the repaired known-probe relations activate. This is stronger than relying on an explicit `unclassified_residual` field, but NR-001 remains open: the relation operators were supplied in a frozen candidate library and the no-match-to-model-check rule was fixed in advance.

**v0.5 update:** run `31175390339` localized a supplied single-relation basis failure for `interaction_probe` and conditionally constructed `AND(pair0_close,pair1_far)`. This is a genuine step beyond selecting a pre-existing complete relation, but it still does not close NR-001. The raw measurement interface, primitive relations, `AND` constructor, adequacy threshold, scoring rule, maximum construction depth, and no-match-to-model-check policy were all supplied. The system repaired a basis *within a supplied construction language*; it did not identify construction-language inadequacy or invent a missing relation operator.

**Next discriminator:** withhold a relation constructor required by the target distinction while retaining more primitive operations, then test whether the system can identify that the construction language itself is inadequate and generate a new operator without globally expanding every representation.

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

**v0.4 update:** a neutrally named `adaptive_representation_learner`, given no negative-space-specific semantic labels, repaired its representation from raw resolved histories and reached the fixed typed oracle on the frozen held-out cases. v0.4 did not include a separate negative-space-labelled learner because the experiment targeted representation acquisition, so it provides no new evidence for a unique negative-space mechanism. If anything, it further supports treating the useful object as adaptive causal representation repair until a matched comparison shows otherwise.

**v0.5 update:** the successful system was again neutrally instantiated as `gated_basis_repair_learner`. It detected basis inadequacy, constructed the withheld conjunction, and matched the brute-force composition learner at lower search cost without using a negative-space-specific algorithm or label. v0.5 therefore adds evidence for selective representation/basis repair, not for a unique negative-space mechanism.

**Claim constraint:** the current evidence supports history-sensitive, representation-sensitive search control and selective basis repair. It does not support a distinct performance advantage for explicit negative-space framing over matched strong causal or representation-learning processes.

**Next discriminator:** only reopen a negative-space-specific mechanism claim under a matched construction-language benchmark with identical raw history, primitive operations, synthesis budget, evidence budget, and representation/search costs.

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

**v0.4 update:** the raw-history adaptive learner successfully repaired its representation without any negative-space-specific mechanism in the learner name or scoring rule. This does not directly test the v0.2 comparison, but it reinforces the current boundary: adaptive search-control competence can be instantiated generically.

**v0.5 update:** conditional basis expansion was also demonstrated by a generic learner. This strengthens the evidence that the empirically useful object is adaptive search/representation repair under failure, not a mechanism so far shown to be unique to negative-space framing.

**Claim constraint:** do not cite v0.2, v0.3, v0.4, or v0.5 as evidence that `Psi_NS` outperforms strong adaptive causal search or generic representation repair when relevant affordances are matched.

**Next discriminator:** only reopen the mechanism-identity question under a matched operator-construction experiment; otherwise treat negative-space as a research interface or search framing rather than an established unique algorithm.

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

**v0.4 update:** run `31174650351` removed one part of the supplied-representation objection. The adaptive learner received raw unlabeled paired measurements and selected useful relations only after a cheaper surface abstraction failed. Its held-out evidence-selection rate improved from `0.0` to `1.0`, with `representation_change_rate = 1.0`. However, the generic relation operators `high/low/near_zero/close/far/sign_disagree` were still supplied, and no negative-space-labelled learner was needed to obtain the repair. The gain therefore belongs to representation selection and repair, not to negative-space identity or unrestricted representation invention.

**v0.5 update:** run `31175390339` attacked the supplied complete-relation objection one level deeper. The useful `interaction_probe` relation was withheld from the initial single-relation basis. The generic gated learner correctly diagnosed that the best single relation had balanced accuracy `0.8333 < 0.90`, searched compositions only for that probe, and constructed `AND(pair0_close,pair1_far)`, reaching held-out evidence selection `1.0` versus `0.8333` for the fixed single basis. However, `AND` and the primitive operands were supplied. The result is therefore basis composition and selective repair, not primitive operator invention or negative-space identity.

**Claim constraint:** attribute the current v0.3-v0.5 gains to representation quality, evidence-conditioned repair, and selective basis expansion under failure—not to negative-space identity.

**Additional limitation:** the benchmark sequence remains synthetic and deliberately adversarial to surface representations. v0.5 includes measurement jitter and misleading surface hints but no corrupted resolving-probe labels; do not generalize it to label-noise robustness.

**Next discriminator:** attack the construction language itself under explicit search cost, representation cost, noisy/ambiguous attribution, and a matched generic program-synthesis baseline. Preserve the null if generic synthesis constructs the required operator at equal or lower cost.

**Status:** open.

---

## Ledger rule

A negative result may be closed only by a new experiment that directly discriminates the implicated failure. A code change that makes the old case pass is not sufficient by itself.
