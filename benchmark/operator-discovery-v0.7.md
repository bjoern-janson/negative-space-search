# Operator Discovery Benchmark v0.7

## Purpose

Test construction-language repair after v0.6 has established that the current language is non-identifying.

The benchmark does not ask whether a solver can choose a hidden semantic operator from a menu. It asks whether a generic expression generator can construct a useful full predicate from primitive trace operations, and whether boundary detection improves when that synthesis is invoked.

## Frozen transition

```text
current-language collision
-> boundary diagnosis
-> generic expression construction
-> training discrimination
-> held-out transfer
-> retain candidate coordinate
```

The final step does not grant epistemic authority to the abstraction.

## Current language

The pre-repair language is `current_language()` from v0.6: 78 expressions over paired measurements.

## Primitive synthesis grammar

Terminals:

```text
t0 t1 t2 t3
```

Numeric constructors:

```text
ADD(x,y)
SUB(x,y)
```

Boolean constructors:

```text
GT(x,y)
LT(x,y)
```

No numeric constants are supplied. Numeric expression depth is at most one arithmetic constructor. Full predicates are generated programmatically; no target semantic predicate is stored as a candidate list.

## Hostile family requirements

For each hostile family:

1. at least two resolving classes share the same complete pre-repair language signature;
2. their labels conflict within that equivalence class;
3. a predicate generated from the primitive grammar can discriminate the resolved training cases;
4. the retained predicate must transfer to held-out traces with changed numeric values.

Two independent hostile families are required so a single special-case trace rule is insufficient.

## Boundary states

- `adequate`: one resolved class occupies the current-language signature;
- `inadequate`: two or more resolved classes occupy the same current-language signature;
- `unknown`: no resolved historical case occupies the signature.

`unknown` must not trigger synthesis in the boundary-gated system.

## Policies

- `current_language_assimilator`
- `conservative_abstainer`
- `boundary_only_auditor`
- `always_expand_generic_synthesizer`
- `boundary_gated_generic_synthesizer`

The two synthesis systems share the same expression generator and scoring implementation.

## Retention rule

A generated predicate is eligible for retention only if its one-vs-rest balanced accuracy is exactly `1.0` on the resolved training cases inside the implicated equivalence class.

Among eligible predicates, maximize:

```text
balanced_accuracy - 0.002 * complexity
```

then minimize complexity, then use lexical name ordering.

## Evaluation

Report separately:

```text
boundary_detection_rate
construction_success_rate
held_out_repair_selection_rate
multi_family_transfer_rate
false_expansion_rate
adequate_case_preservation_rate
unknown_calibration_rate
search_cost
representation_cost
generated_operator_count
```

No scalar benchmark score.

## Invalid benchmark conditions

The run is invalid if:

- any hostile pair differs under the frozen 78-expression current language;
- a target semantic full operator is supplied directly to the synthesis policy;
- the two synthesis systems use different candidate-generation or scoring rules;
- the unknown control is treated as demonstrated language inadequacy;
- held-out cases duplicate training traces exactly.

## Scope boundary

A positive v0.7 result establishes at most **conditional expression synthesis inside a supplied meta-language**. It does not establish invention of the primitive operations or the generator itself.
