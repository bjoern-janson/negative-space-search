# Benchmark Specification — v0.3 Representation Transfer

## Target

Test whether persistent failure representation changes transfer of evidence-selection policies to novel ecologies.

The target is representation dependence, not a new search operator.

## Raw training episode

Every learner initially observes the same fields:

```text
prediction
outcome
selected experiment
assumed absence
causal diagnosis
intervention
challenge channel / dependency relation
payoff regime
coordination topology
classification status
attributed failure mechanism
```

After each training episode, the learner stores a persistent history representation.

## Representation ablation

### Compressed causal history

Stores:

```text
prediction
outcome
absolute error
selected experiment
```

### Typed history

Stores the compressed fields plus:

```text
dependency_overlap
payoff_regime_changed
coordination_topology_changed
unclassified_residual
attributed failure mechanism
successful discriminating probe
```

Two policies use the typed representation:

```text
structured_negative_space_history
typed_general_causal_history
```

Their implementation and decision rule must be identical apart from policy name.

## Learned training map

The training histories expose:

```text
shared dependency -> independence_probe
payoff regime drift -> payoff_regime_probe
coordination topology mismatch -> topology_probe
```

The learner is not given a training example for the held-out unclassified topology.

## Transfer rule

All policies use deterministic nearest-structure retrieval from their own stored representation.

If a typed held-out signature exactly matches an attributed training structure, use its discriminating probe.

If no typed structure matches, request:

```text
model_disrupting_probe
```

The compressed learner performs the same nearest-neighbor procedure in its smaller feature space. It receives no special model-inadequacy rule.

## Held-out cases

```text
H_DEP   -> independence_probe
H_PAY   -> payoff_regime_probe
H_NET   -> topology_probe
H_NOVEL -> model_disrupting_probe
```

Surface names, prediction values, and outcomes differ from training examples.

## Metrics

```text
held_out_evidence_selection_rate
known_topology_transfer_rate
novel_topology_model_check_rate
false_model_check_rate
evidence_cost
```

`false_model_check_rate` is the fraction of the three known-topology held-out cases on which `model_disrupting_probe` is selected.

No composite score.

## Claim boundary

A difference between typed and compressed histories identifies a representation effect under this benchmark.

A tie between the two typed policies means the benchmark supplies no evidence that the effect is uniquely negative-space rather than generally available to any causal learner preserving the same distinctions.
