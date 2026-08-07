# Method — Negative-Space Search v0.7

Status: **frozen archival method description**.

This document describes the architecture used to interpret the v0.1–v0.7 benchmark sequence without adding new primitives at release time.

## Architecture

The research loop is represented as:

```text
L_t
-> Psi_t
-> candidate
-> evidence / reality
-> U_t
-> L_(t+1)
```

Equivalently:

```text
L_t -> Psi_t -> C_t -> W/e_t -> U_t -> L_(t+1)
```

where the candidate stage is a search output and the evidence/reality stage is the independent source of epistemic authorization.

## Psi — allocation of representational search effort

`Psi` is the search-governance role.

It allocates investigative attention and representational search effort. In the frozen v0.7 interpretation, its central task is deciding whether the current representational/search structure should be:

```text
continued
repaired
expanded
investigated further
```

`Psi` may propose a candidate coordinate, test, repair, or expansion.

It does **not** grant epistemic authority to that proposal.

```text
Psi proposes.
evidence authorizes.
```

## Evidence and U — authority update

Evidence/reality provides the discriminating consequences by which candidates can earn or lose authority.

`U` is the evidence-conditioned update process.

The central firewall is:

```text
possibility != authority
candidate != claim
Psi != U
```

A generated representation can be useful for discrimination without thereby being a true causal explanation.

## L — inherited justified structure

`L` denotes the structure carried forward after evidence-conditioned correction.

Negative-Space Search does not define unrestricted inheritance. The complementary Correctable Lineage program governs the scope, provenance, defeasibility, and authority of what is retained after evidence arrives.

## Correctable Lineage relationship

The two projects have distinct operational scopes:

```text
Negative-Space Search -> scope of exploration / attention / search effort
Correctable Lineage   -> scope of inheritance / authority
```

The shared principle is:

> **Keep possibility open; keep authority earned.**

A compact joint rule is:

> **Expand only when justified. Preserve only when justified.**

No additional bridge object is introduced in this archival release.

## Adequacy-boundary method

The benchmark progression tests increasingly strong questions about whether the current representational machinery is sufficient.

The frozen decision pattern is:

```text
current structure
-> adequacy test
-> continue | repair | expand | investigate
```

The method distinguishes at least three states relevant to v0.6–v0.7:

### Adequate

Current representational structure can discriminate the relevant resolved distinctions. Additional expansion is not licensed merely because richer representations are imaginable.

### Inadequate

Resolved histories demonstrate a collision: cases requiring different outcomes remain indistinguishable under the current construction language. This can license expansion effort.

### Unknown

The current case is unsupported or unfamiliar, but there is no demonstrated collision proving that the current language is non-identifying. Unknown does not automatically license representational expansion.

## v0.7 synthesis method

v0.7 supplied both the always-expand and boundary-gated systems with the same generic finite synthesis meta-language:

```text
terminals:    t0, t1, t2, t3
constructors: ADD, SUB, GT, LT
```

No ready-made semantic target operators such as `trace_increasing`, `direction`, `center_heavy`, or `edge_heavy` were supplied.

Both synthesis systems used the same generator and scoring/retention machinery. The experimental difference was when synthesis was invoked.

Therefore:

```text
same what-to-invent mechanism
+ different when-to-search policy
```

is the relevant v0.7 comparison.

## Authority limitation

The synthesized predicates earned authority only as candidate coordinates that discriminated the frozen training histories and transferred to frozen held-out synthetic cases.

They did not earn authority as causal truths beyond that evidence footprint.

## Archival constraint

This release does not add ontology, primitives, or a higher-order operator above `Psi`.

Future conceptual expansion must be forced by external evidence or a recurring failure that the current structure cannot discriminate.
