# Empirical Results — Negative-Space Search v0.7

Status: **frozen archival summary**.

This document summarizes the benchmark progression without converting later capability into authority for stronger earlier interpretations.

## Empirical ladder

### v0.1 — causal absence reasoning versus naive gap search

Controlled hostile cases showed that causal reasoning about why an absence exists can outperform naive gap, novelty, or opportunity heuristics.

Supported interpretation:

> Absence should be treated as a causal inference problem rather than as automatic evidence of opportunity.

Not established:

> A uniquely negative-space discovery mechanism.

### v0.2–v0.3 — contraction toward history and representation

Matched history-aware causal reasoning removed the apparent unique advantage from v0.1.1, and typed general causal history matched structured negative-space history in transfer.

Supported interpretation:

> The useful object is history-sensitive, representation-sensitive search control; negative-space naming itself did not provide a unique mechanism.

### v0.4 — failure-conditioned representation repair

Failed corrections can license representational repair when a previously rewarded abstraction stops transferring.

The adaptive learner moved from misleading surface cues to stable supplied relational features and improved held-out evidence selection from `0.00` to `1.00`.

Supported interpretation:

> Failure history can justify changing which supplied distinctions are preserved and used.

Not established:

> Autonomous invention of new representational primitives.

### v0.5 — conditional basis composition

A supplied single-relation basis was demonstrably inadequate for one class. A gated repair learner conditionally constructed a conjunction inside the supplied construction language and improved held-out selection.

Supported interpretation:

> Basis inadequacy can trigger local relation composition rather than indiscriminate representational expansion.

Not established:

> Invention of the construction language itself.

### v0.6 — construction-language inadequacy detection

Two resolved classes were identical under all 78 expressions in the current construction language but differed in raw ordered trace information.

A boundary-aware auditor distinguished:

```text
adequate
inadequate
unknown
```

and requested language expansion only for a demonstrated non-identifiability collision.

Supported interpretation:

> A system can identify that its current construction language cannot discriminate a resolved distinction, while preserving unsupported cases as ordinary unknowns.

Not established:

> Autonomous generation of the missing operator.

### v0.7 — boundary-gated construction-language repair

Both the always-expand and boundary-gated generic synthesizers used the same supplied primitive meta-language and generated the same four transferable predicates.

#### Gated synthesis

```text
invention quality:      1.0
held-out transfer:      1.0
candidate evaluations:  5200
```

#### Always-expand synthesis

```text
invention quality:      1.0
held-out transfer:      1.0
candidate evaluations:  7800
```

Both systems retained the same final representation quality.

The boundary-gated system avoided expansion in already-adequate regions, while the always-expand system expanded there as well.

## v0.7 interpretation

The advantage is **not** better invention.

The advantage is better control over **when invention search is warranted**.

Formally, the executed result supports:

```text
Q_invention(gated) = Q_invention(always-expand)
C_search(gated)    < C_search(always-expand)
```

within the frozen synthetic benchmark.

The candidate-evaluation reduction was:

```text
7800 -> 5200
```

or one third fewer synthesis evaluations at matched repair quality.

## Surviving empirical claim

> **Negative-Space Search v0.7 supports adaptive search governance: detecting demonstrated representational inadequacy and allocating expansion effort conditionally rather than indiscriminately.**

It does not establish superior discovery or truth-finding.

## Provenance

The detailed executed records remain in `results/`, including:

- `results/v0.1-initial.md`
- `results/v0.1.1-model-adequacy.md`
- `results/v0.2-false-escalation.md`
- `results/v0.3-representation-transfer.md`
- `results/v0.4-representation-acquisition.md`
- `results/v0.5-basis-failure.md`
- `results/v0.6-language-boundary.md`
- `results/v0.7-operator-discovery.md`
- `results/negative-result-ledger.md`
