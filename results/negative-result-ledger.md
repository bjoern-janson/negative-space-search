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

**Next discriminator:** vary or hide the escalation signature and test whether the policy can infer when repeated ordinary failures justify testing model adequacy rather than merely matching the exact `ordinary_hypotheses_unresolved` pattern.

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

**v0.1.1 update:** run `31172485528` produced a narrow difference on the model-adequacy evidence-selection task. `causal_negative_space_search` requested `model_disrupting_probe`; `general_causal_reasoner` requested more within-model evidence. When the model-disrupting result was supplied to both, both interpreted the two regimes correctly. This localizes the observed difference to investigative-attention / evidence-selection policy, not post-evidence causal reasoning.

**Claim constraint:** v0.1.1 does not erase the v0.1 null and does not establish general superiority. The new benchmark is deliberately aligned with the hypothesized escalation mechanism and must transfer to held-out surface signatures before stronger authority is warranted.

**Next discriminator:** generate held-out model-adequacy environments where the history pattern, surface fields, noise process, and evidence costs vary, while the strong causal baseline has access to the same history and can adapt its search policy.

**Status:** open.

---

## Ledger rule

A negative result may be closed only by a new experiment that directly discriminates the implicated failure. A code change that makes the old case pass is not sufficient by itself.
