# Frozen Core v0.1

Status: **frozen for the initial benchmark**.

This document is a specification, not a manifesto. Do not add primitives during v0.1 unless a recurring empirical failure cannot be discriminated with the current structure.

## Objects

```text
U, Phi, Psi, H, Z
```

- `U` — evidence-conditioned update process.
- `Phi` — population selection/adaptation process.
- `Psi` — embedded search process that allocates investigative attention.
- `H` — preserved diagnostic and intervention history.
- `Z` — observable ecology supplied to the search process.

The lineage boundary is represented operationally as:

```text
L_t -> Psi_t -> C_t -> W/e_t -> U_t -> L_t+1
```

`L` and `C` are roles in the experimental loop, not additional theory objects for v0.1.

## Invariants

```text
Psi != U
possibility != authority
candidate != claim
evidence changes only identified scope
```

Operationally:

```text
Psi proposes.
evidence authorizes.
```

A search result may justify investigation. It does not by itself justify belief, adoption, or inheritance.

## Search output

The v0.1 search process returns:

```text
(q, n_hat, d, E, Y_hat, c)
```

Where:

- `q` — observed candidate absence/deficiency under investigation;
- `n_hat` — causal diagnosis or competing diagnoses;
- `d` — `intervene | preserve | investigate | abstain`;
- `E` — requested discriminating evidence when needed;
- `Y_hat` — predicted consequence of evidence acquisition or intervention;
- `c` — calibrated confidence / identifiability assessment.

## Central constraint

```text
absence != opportunity
absence -> causal inference problem
```

The search process must be able to conclude:

- the absence is maladaptive;
- the absence is justified;
- more evidence is required;
- the current evidence is non-identifying;
- the current causal vocabulary is inadequate.

## Constitutional rule

> **Keep possibility open; keep authority earned.**

The v0.1 benchmark exists to attack this specification. Empirical failure should update the smallest component that the failure actually identifies.