# v0.2 False-Escalation Benchmark

Status: **preregistered benchmark specification**

This benchmark tests whether search control can distinguish:

```text
repeated failure because the current causal model is inadequate
```

from:

```text
repeated failure because an adequate model is being tested under noise, low power, or weak measurement.
```

It does not add a new theory primitive. `escalation` is an evaluation decision about evidence acquisition.

## Question

> Does the search process respond to the **structure of failure**, rather than merely the number of failed or inconclusive probes?

The target is selective escalation:

```text
model inadequacy -> model-disrupting evidence
ordinary uncertainty -> continue within-model evidence
```

## Matched surface condition

Cases are matched on the obvious shortcut variables:

- low prevalence;
- unresolved ordinary hypotheses;
- equal number of prior failed/inconclusive probes;
- equal evidence-action affordances;
- equal model-disrupting-probe cost;
- no explicit `current_causal_vocabulary_residual` flag before evidence acquisition.

The discriminating information is in `H`: the **pattern** of prior failures.

## Failure structures

### Genuine model inadequacy

Prior ordinary predictions fail in a structured way that the supplied hypothesis family should not generate, for example:

- stable residual direction across heterogeneous contexts;
- repeated sign reversal relative to all supplied hypotheses;
- invariant violation after ordinary nuisance explanations are varied.

Correct search action:

```text
investigate -> model_disrupting_probe
```

### Stubborn within-model uncertainty

Prior ordinary probes are inconclusive for reasons compatible with the supplied model, for example:

- residual signs fluctuate around zero;
- uncertainty intervals remain wide because sample size is small;
- effect size is weak relative to measurement variance.

Correct search action:

```text
investigate -> targeted_within_model_probe
```

Escalating to model disruption here is a **false escalation**.

## Evaluation label

`r` is an evaluator label only:

```text
within_model_uncertainty
model_inadequacy_suspected
```

It is not an absence class and does not modify the frozen core.

## Primary metric: escalation calibration

Report both rates separately:

```text
true_escalation_rate  = P(model_disrupting_probe | model inadequate)
false_escalation_rate = P(model_disrupting_probe | model adequate)
```

Do not collapse them into one scalar in v0.2.

Also report:

- correct evidence-selection rate;
- post-evidence regime interpretation;
- evidence cost incurred;
- performance on held-out surface forms.

## Policy comparisons

Minimum comparison:

1. `general_causal_reasoner` — strong v0.1/v0.1.1 baseline;
2. `causal_negative_space_search` — frozen v0.1.1 escalation-on-unresolved policy;
3. `history_aware_general_causal_reasoner` — strong competitor with access to the same failure history;
4. `history_aware_negative_space_search` — candidate v0.2 search-control policy;
5. naive controls from v0.1 where useful.

All policies receive the same observation, history, evidence affordances, and costs.

## Train/held-out split

The benchmark contains development cases and held-out cases with different surface capabilities and numerical values.

Held-out cases must vary at least:

- capability name;
- failure count;
- residual magnitude;
- measurement variance;
- probe cost.

The structural distinction remains the same: **systematic model violation vs uncertainty compatible with the model**.

A v0.2 positive result requires the candidate policy to maintain selective escalation on held-out cases. Passing only development signatures is insufficient.

## Failure conditions

The candidate fails if it:

- escalates mainly as a function of failure count;
- escalates both model-inadequate and noisy adequate-model cases;
- never escalates;
- depends on an explicit model-inadequacy label in the initial observation;
- beats the strong baseline only because it receives privileged evidence or lower costs.

## Claim boundary

Even a positive v0.2 result would support only a narrow implementation claim about selective evidence acquisition under these controlled synthetic failure structures. It would not establish general model-discovery capability or superiority over causal reasoning in unrestricted settings.
