# v0.4 Benchmark — Representation Acquisition and Repair

## Purpose

Test whether resolved correction history can cause a search process to revise the representation it uses for future evidence allocation.

The benchmark distinguishes:

```text
case memory
from
representation repair
```

and keeps the stronger claim deliberately out of scope:

```text
representation repair != unrestricted interface invention
```

## Input

Raw resolved episodes contain:

```text
paired_measurements
surface_hint
prediction
outcome
selected_action
timestamp
cost
resolving_probe
```

No causal-class labels are exposed.

## Output

For each held-out case, a system selects one evidence action:

```text
independence_probe
payoff_regime_probe
topology_probe
model_disrupting_probe
```

The adaptive representation learner additionally exposes its selected candidate relations so representation change can be measured directly.

## Evaluation phases

1. Fit on the six acquisition episodes.
2. Evaluate the four held-out cases without updating from them.
3. Add the three repair episodes whose surface cue contradicts the earlier rewarded representation.
4. Refit under the identical frozen representation-selection rule.
5. Re-evaluate the same held-out cases.

The held-out evaluations do not enter the learner history.

## Controls

### Compressed outcome memory

Nearest-neighbor retrieval over:

```text
prediction
outcome
absolute error
```

using all resolved episodes available at the phase.

### Fixed typed oracle

Uses the correct three stable relations from the start. It measures an upper bound for the supplied typed representation, not learnability.

### Adaptive representation learner

Searches the frozen generic candidate relation library and chooses one feature per known resolving probe using the preregistered balanced-accuracy / complexity objective.

## Representation decision rule

For a held-out case:

- if exactly one learned probe-specific feature activates, request that probe;
- otherwise request `model_disrupting_probe`.

This makes both no-match and conflicting-match states conservative rather than granting a known diagnosis automatically.

## Metrics

No composite score.

```text
pre_repair_held_out_selection_rate
post_repair_held_out_selection_rate
repair_gain
representation_change_rate
post_repair_novel_model_check_rate
post_repair_false_model_check_rate
selected_representation_cost
compressed_baseline_rate
fixed_oracle_rate
```

## Core falsification

The representation-repair hypothesis fails on this benchmark if the adaptive learner does not improve after the repair episodes under the frozen rule.

A positive result does not validate a uniquely negative-space mechanism. It establishes only that preserving raw correction history plus a generic relation-search interface can support representation repair in this controlled setting.
