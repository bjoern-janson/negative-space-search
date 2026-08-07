# v0.6 Construction-Language Boundary Benchmark

Status: preregistered benchmark contract.

## Question

Can a learner distinguish three states of its current construction language without being given a menu of replacement operators?

1. **adequate** — the current language can express the needed distinction;
2. **inadequate** — different resolved classes are observationally equivalent under every current-language expression;
3. **unknown** — the current language has not been falsified, but the held-out signature is unsupported by resolved history.

The primary target is **boundary recognition**, not operator invention.

## Frozen language

The current construction language is exactly the v0.5 language:

```text
L_t = supplied single relations + all pairwise AND compositions
```

No OR, XOR, NOT, ordering, arithmetic synthesis, learned embeddings, free-form code generation, or additional relation operators are available to the primary systems.

The raw record now includes an `ordered_trace` field. The current language does not inspect that field.

## Evaluation label

v0.6 adds an evaluation-only label:

```text
language_status in {adequate, inadequate, unknown}
```

This is not a new frozen-core primitive and not a fifth absence class. It describes the solver's diagnosis of the adequacy of its current construction language for the present case.

## Non-identifiability criterion

Let `phi_L(x)` be the truth-value signature produced by every expression in the frozen language `L_t`.

Language inadequacy is established when trusted resolved history contains:

```text
phi_L(x_a) = phi_L(x_b)
```

but:

```text
resolving_probe(x_a) != resolving_probe(x_b)
```

Because the primitive truth vectors are identical, no further Boolean composition of those existing truth values can separate the pair. Trying more combinations inside the same language is therefore not a valid repair.

## Layers

### Layer 1 — representation/basis selection

A held-out case matches a unique resolved class under `L_t`.

Correct result:

```text
language_status = adequate
```

and use the current language.

### Layer 2 — language failure

Two resolved classes have identical current-language signatures but different resolving probes. Their raw ordered traces differ, but no operator in `L_t` can express trace direction.

Correct result:

```text
language_status = inadequate
selected_probe = language_expansion_probe
```

The solver must not guess one of the conflicting causal classes.

### Layer 3 — operator invention

Not attempted in v0.6.

An oracle receives a withheld trace-direction operator only to show that the raw data contain a recoverable distinction. The primary learner never receives that operator or a candidate operator library.

## Systems

### Current-language assimilator

Uses the current language but treats an ambiguous matched signature as if one existing class must be correct. This is the false-assimilation control.

### Conservative abstainer

Refuses to choose when a signature maps to conflicting classes, but reports:

```text
language_status = unknown
```

This separates generic non-commitment from explicit language-inadequacy diagnosis.

### Boundary-aware auditor

Maps cases through the full frozen language. It reports:

- `adequate` for a unique supported signature;
- `inadequate` for a signature whose resolved equivalence class contains conflicting probes;
- `unknown` for an unsupported signature not yet shown contradictory.

On `inadequate`, it requests `language_expansion_probe`.

### Expanded-language oracle

Upper bound supplied with trace-direction relations. It is used only to establish that the layer-2 pair is distinguishable from the raw record once the missing operator is available.

It does not count as operator discovery.

## Metrics

Report separately:

```text
language_inadequacy_detection_rate
false_language_inadequacy_rate
boundary_nonhallucination_rate
adequate_case_selection_rate
unknown_calibration_rate
language_expansion_request_rate
false_language_expansion_request_rate
oracle_recoverability_rate
current_language_expression_count
```

No composite score.

## Primary success condition

The boundary-aware auditor must:

1. preserve adequate v0.5-style cases;
2. identify both trace-order cases as `inadequate`;
3. request `language_expansion_probe` on those cases rather than assimilating them into an existing class;
4. report an unseen, non-contradictory held-out signature as `unknown`, not `inadequate`;
5. have zero false language-inadequacy calls on adequate controls;
6. be strictly more informative than the conservative abstainer on the boundary pair;
7. preserve all previous benchmark tests.

The expanded oracle must recover the two trace-order classes from the same raw data, establishing construction-language rather than observation-interface insufficiency.

## Failure conditions

The v0.6 claim fails if:

- any expression in the frozen current language distinguishes the hostile pair;
- the boundary-aware system merely chooses from a supplied list of replacement operators;
- it labels all uncertainty as language inadequacy;
- it hallucinates one of the conflicting classes on the boundary pair;
- the oracle cannot recover the hidden distinction from the supplied raw trace;
- previous benchmark tests regress.

## Allowed claim if positive

> In this controlled benchmark, a system can identify a non-identifiability boundary of its current construction language from resolved failure history, distinguish that boundary from unsupported uncertainty, and request language expansion without being supplied a menu of replacement operators.

## Not established

A positive v0.6 result does **not** establish:

- autonomous operator invention;
- discovery of the raw observation interface;
- superiority over generic identifiability or model-criticism methods;
- unique value of negative-space terminology;
- real-world interface invention.
