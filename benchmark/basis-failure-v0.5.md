# v0.5 Basis-Failure Benchmark

Status: preregistered before learner implementation.

## Question

Can a learner distinguish:

1. a failure that can still be expressed by its current relation basis; from
2. a failure for which no supplied single relation is adequate,

and conditionally expand the basis by constructing a more complex relation from primitive relations?

The primary target is **basis inadequacy detection plus selective basis repair**, not unrestricted invention of representational primitives.

## Frozen boundary

v0.4 showed representation selection and repair inside a supplied single-relation library. v0.5 withholds the relation required by one probe from that library.

The withheld relation is a conjunction of two primitive relations:

```text
pair0_close AND pair1_far
```

`AND` is available only to the expansion procedure. It is not in the initial basis.

Therefore a positive v0.5 result would establish composition-based basis expansion, not invention of the Boolean composition operator itself.

## Raw episode interface

Each resolved episode exposes only:

```text
episode_id
paired_measurements
surface_hint
prediction
outcome
selected_action
timestamp
cost
resolving_probe
```

No episode contains labels such as:

```text
basis failure
interaction
conjunction required
model inadequacy
negative space
```

The resolving-probe identifier is an observed outcome of the completed search process, not a causal-class label.

## Initial basis

The initial basis is the frozen v0.4 relation family:

```text
hint_high
hint_low
hint_near_zero
pair{i}_close
pair{i}_far
pair{i}_sign_disagree
```

for `i in {0,1,2}`.

No conjunction is present.

## Expansion basis

If and only if a probe's best single relation fails the frozen adequacy threshold, an adaptive learner may evaluate pairwise conjunctions:

```text
relation_a AND relation_b
```

where both operands come from the initial basis and are distinct.

No deeper nesting, OR, XOR, negation, arithmetic synthesis, learned neural representation, or free-form code generation is allowed in v0.5.

## Adequacy rule

For each resolving probe, score candidate relations using balanced accuracy over resolved history.

Frozen threshold:

```text
BASIS_ADEQUACY_THRESHOLD = 0.90
```

A probe is diagnosed as **basis-inadequate under the current single-relation basis** when:

```text
max_single_relation_balanced_accuracy < 0.90
```

This is an evaluation/algorithmic diagnosis, not a new ontology primitive.

## Complexity and search cost

Representation complexity:

```text
single relation: relation complexity
conjunction: complexity(left) + complexity(right) + 1
```

Search cost is the number of candidate relations evaluated during fit.

The gated learner pays composition-search cost only for probes that fail the adequacy test.

The always-compose control evaluates the same conjunction search space for every probe.

## Probe families

Four resolved probe families are present:

```text
independence_probe
payoff_regime_probe
topology_probe
interaction_probe
```

The first three are expressible by one supplied relation.

`interaction_probe` is not. Its stable discriminating relation is:

```text
pair0_close AND pair1_far
```

Each constituent is deliberately non-identifying by itself because other probe families activate exactly one constituent.

## Systems

### 1. Fixed single-basis selector

May fit only supplied single relations.

If its best relation is below the adequacy threshold, it may record the inadequacy but cannot construct a new relation.

This separates **detection** from **repair**.

### 2. Gated basis-repair learner

Uses the same initial basis.

It may search conjunctions only for a probe whose best single relation is below threshold.

Primary candidate.

### 3. Always-compose learner

Searches the identical single + conjunction candidate space for every probe regardless of adequacy.

This is an adversarial control for brute-force basis expansion. It can match evidence-selection performance while paying unnecessary search cost.

### 4. Fixed composition oracle

Upper-bound control supplied with the stable relations, including the withheld conjunction.

It does not count as learned basis repair.

## Held-out cases

Held-out cases preserve the relation structure while perturbing all numeric measurements and surface hints.

They include:

- conjunction-active interaction cases;
- `pair0_close` without `pair1_far`;
- `pair1_far` without `pair0_close`;
- all three known single-relation families;
- a no-match case whose correct action is `model_disrupting_probe`.

The single-constituent cases are essential: a learner that promotes either constituent to the interaction relation should fail them.

## Metrics

Report separately:

```text
basis_inadequacy_detection_rate
false_basis_inadequacy_rate
basis_expansion_rate
construction_success_rate
held_out_evidence_selection_rate
interaction_transfer_rate
constituent_false_positive_rate
novel_model_check_rate
search_cost
representation_cost
```

No composite score.

## Primary success condition

The gated basis-repair learner must:

1. mark `interaction_probe` as inadequate under the initial basis;
2. not mark the three supplied-basis probes inadequate;
3. construct the withheld conjunction;
4. improve held-out evidence selection over the fixed single-basis selector;
5. avoid false interaction attribution on constituent-only held-out cases;
6. match the always-compose learner on held-out selection while using strictly lower search cost.

## Primary failure conditions

v0.5 fails the basis-repair claim if any of the following occur:

- a supplied single relation already reaches the adequacy threshold for `interaction_probe`;
- the gated learner does not identify the basis insufficiency;
- it expands indiscriminately across all probes;
- it fails to construct a relation that transfers to held-out interaction cases;
- the result depends on semantic causal labels not present in raw episodes;
- the always-compose learner is cheaper under the frozen cost accounting;
- prior benchmark tests regress.

## Claim boundary

A positive result licenses only:

> In this controlled benchmark, a learner can detect that its supplied single-relation basis is insufficient for one evidence-selection class and conditionally construct a useful conjunction from supplied primitive relations, improving held-out search while avoiding the cost of global brute-force composition.

It does **not** establish:

- autonomous invention of primitive relation operators;
- discovery of the raw measurement interface;
- unique value of negative-space terminology;
- superiority over generic program synthesis or representation learning;
- real-world interface invention.
