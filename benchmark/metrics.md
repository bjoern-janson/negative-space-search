# Benchmark Metrics v0.1

The benchmark reports a metric vector. No scalar aggregate is canonical in v0.1.

```text
Q_Psi = (
  Q_q,
  Q_n,
  Q_E,
  Q_A,
  Q_Y,
  Q_CF,
  Q_abstain,
  Q_D
)
```

## Q_q — consequential-absence identification

Measures whether the search process identifies the relevant observed absence without treating every low-prevalence capability as important.

False-positive rate on healthy absences must be reported alongside recall.

## Q_n — causal diagnosis

Measures whether the proposed explanation matches the latent mechanism or causal mixture that generated the absence.

A successful intervention does not by itself establish diagnostic correctness.

## Q_E — evidence acquisition quality

Measures whether `investigate` requests observations that discriminate among live causal hypotheses.

High-quality evidence acquisition should reduce uncertainty or expose non-identifiability efficiently under the evidence budget.

## Q_A — intervention match

Measures whether the selected intervention is appropriate for the identified causal mechanism.

Examples:

- incentive change for underinvestment;
- interface / measurement expansion for underrepresentation;
- preservation for justified selection;
- shared infrastructure or coordinated adoption for coordination failure.

## Q_Y — consequence prediction

Measures calibration and accuracy of predicted intervention or evidence-acquisition outcomes.

## Q_CF — counterfactual causal fidelity

Measures whether the proposed explanation continues to predict outcomes when accidental or correlated mechanisms are removed.

This metric separates causal understanding from lucky exploitation.

## Q_abstain — calibrated non-action

Measures appropriate use of `preserve`, `investigate`, and `abstain` under uncertainty.

This includes at least:

- preserving healthy absences;
- refusing intervention when evidence is insufficient;
- selecting investigation when the cause is identifiable only after additional evidence;
- detecting model inadequacy instead of forcing a familiar diagnosis.

## Q_D — durability after ecological adaptation

Measures whether an intervention's external value persists after the population or payoff landscape responds.

A short-lived counter-meta exploit may score well initially but poorly on durability.

## Required diagnostic views

At minimum, report:

- per-latent-cause performance;
- false-opportunity performance;
- observational-equivalence performance;
- novel/model-inadequate performance;
- cost-normalized evidence use;
- cost-normalized intervention use;
- pre-history versus post-history performance on held-out ecologies.

## Search-process improvement

History-based improvement is valid only when performance increases on held-out environments:

```text
Q(Psi_t+k, novel_ecology) > Q(Psi_t, novel_ecology)
```

Improvement on replayed episodes alone does not establish search-process learning.

## Anti-Goodhart rule

Do not optimize the benchmark around:

- number of discovered opportunities;
- number of interventions;
- novelty rate;
- a single composite score.

A system that intervenes less often but makes better causal decisions may be superior.
