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

**What this identifies:** the current policy does not yet demonstrate the claimed ability to distinguish ordinary unresolved uncertainty from inadequacy of its causal vocabulary.

**What this does not identify:** failure of the full negative-space-search hypothesis, failure of the frozen core, or failure of abstention as a decision primitive.

**Next discriminator:** construct a hidden-mechanism case in which ordinary uncertainty and representational inadequacy have similar surface signatures, then test whether the policy requests evidence that separates them.

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

**Claim constraint:** do not cite the hostile-pair result as evidence that explicit `Psi_NS` structure adds value beyond strong causal reasoning.

**Next discriminator:** design a held-out environment where success requires reasoning about why an equilibrium leaves a capability absent, rather than only recognizing ordinary causal non-identifiability.

**Status:** open.

---

## Ledger rule

A negative result may be closed only by a new experiment that directly discriminates the implicated failure. A code change that makes the old case pass is not sufficient by itself.