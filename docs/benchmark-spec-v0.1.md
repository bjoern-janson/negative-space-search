# Frozen Benchmark Specification v0.1

This file freezes the minimal experiment contract. `benchmark/spec.md` may document implementation details, but changes to the task defined here require an explicit v0.1 revision.

## Task

Given an observed absence in a synthetic research ecology, select the epistemically appropriate next action.

Input:

```text
Z_t = (M_t, Pi_t, I_t, H_t)
```

Output:

```text
(n_hat, d, E, c)
```

Decision:

```text
intervene | preserve | investigate | abstain
```

## Five latent environments

### A — underinvestment

A useful, representable capability is suppressed because local incentives make adoption unattractive.

Expected behavior: intervene when the cause is identified; investigate first when it is not.

### B — underrepresentation

A useful capability or distinction cannot be expressed or measured adequately under the current interface.

Expected behavior: investigate the missing distinction / interface expansion before granting authority to the proposed capability.

### C — justified selection

The capability was tested and correctly rejected under the external criterion.

Expected behavior: preserve the absence.

### D — coordination failure

The capability is valuable only when adoption crosses a threshold or shared infrastructure exists. Unilateral adoption is locally unattractive.

Expected behavior: investigate the threshold when needed, then coordinate rather than treat the case as ordinary underinvestment.

### E — model inadequacy

The generating mechanism is intentionally outside the supplied causal vocabulary.

Expected behavior: abstain from forced classification and request evidence capable of exposing model inadequacy.

`E` is not a fifth ordinary absence cause. It is a benchmark condition in which the supplied causal model is inadequate.

## Mandatory hostile pair

Construct two worlds with identical initial observable state:

```text
World I: underinvestment
World S: justified selection
Z_I == Z_S
```

The capability is externally useful in World I and externally non-useful in World S, but that fact is initially hidden.

A policy that guesses `underinvestment` or `justified_selection` from the shared initial observation fails the identifiability test.

The correct initial behavior is:

```text
investigate
```

with a discriminating experiment that reveals external value under matched conditions, or calibrated `abstain` if the experiment is unavailable.

## Baselines

Minimum baselines:

1. random action;
2. gap detector;
3. novelty heuristic;
4. short-term performance optimizer;
5. self-confirming opportunity search;
6. general causal reasoner;
7. causal negative-space search.

All systems receive matched observations, evidence actions, intervention actions, history capacity, and budgets.

## Metrics

Report the vector:

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

No canonical scalar aggregate exists in v0.1.

## Counterfactual validation

A successful intervention does not prove the diagnosis that motivated it. Controlled cases must permit accidental mechanisms to be removed and the intervention retested.

## Search-process learning

History may update `Psi`, but improvement counts only on held-out ecologies:

```text
Q(Psi_t+k, held_out_ecology) > Q(Psi_t, held_out_ecology)
```

Replay improvement alone is insufficient.

## Null hypothesis

```text
H0: Q(Psi_negative_space) <= Q(Psi_baseline)
```

The explicit negative-space architecture earns authority only if it adds measurable value beyond strong matched baselines after accounting for evidence, intervention, and implementation cost.