# Negative-Space Search v0.7 — Search Governance, Not Discovery

Status: **frozen for external evaluation**.

This document records what the v0.1–v0.7 experiments have earned, what they have not earned, and what can reopen internal architecture development.

## Public claim

Negative-Space Search does not currently demonstrate superior invention.

Its supported contribution is conditional allocation of representational search: determining when existing explanatory structures are demonstrably inadequate and when expansion is unwarranted.

The system governs the cost of challenging its own representational boundaries; it does not determine which new representations are true.

## Central hypothesis

> Explicit representational adequacy diagnosis can improve the efficiency of adaptive search by allocating expansion effort only when current explanatory structures have demonstrably failed.

## Primary null

> Matched general search systems achieve equal or better solution quality at equal or lower cost without explicit adequacy-boundary structure.

The null remains live. v0.7 did not show better invention quality than the matched generic synthesizer.

## Current empirical object

The original intuition:

```text
find what the equilibrium missed
```

has contracted into:

```text
detect when the current search space has become inadequate enough to justify expansion
```

The current object is therefore **adaptive search governance**, not a novelty engine and not an autonomous discovery mechanism.

## Empirical ladder

| Version | Main discriminator | Surviving update |
| --- | --- | --- |
| v0.1 | causal absence reasoning vs naive gap/opportunity search | causal diagnosis beats naive absence-as-opportunity heuristics in controlled cases |
| v0.1.1 | model-disrupting evidence selection | observed difference localized to evidence acquisition, not post-evidence interpretation |
| v0.2 | history-sensitive escalation vs matched causal search | strong history-aware causal reasoning matches the negative-space policy |
| v0.3 | compressed vs typed failure history | typed causal representation improves transfer; negative-space identity adds no unique gain |
| v0.4 | raw-history representation repair | failure history can justify switching from misleading surface cues to useful supplied relations |
| v0.5 | basis insufficiency and conditional composition | a learner can locally construct a missing relation inside a supplied language and avoid indiscriminate composition cost |
| v0.6 | construction-language inadequacy | a learner can distinguish demonstrated non-identifiability from ordinary unsupported uncertainty |
| v0.7 | conditional generic synthesis | boundary gating preserves matched invention quality while reducing unnecessary synthesis cost |

The progression should be read as **claim contraction under stronger discrimination**, not as a monotonic intelligence ladder.

## v0.7 central result

Matched generic synthesizers constructed the same four abstractions and achieved the same held-out repair, transfer, `Q_invention`, and final representation cost.

```text
what-to-invent(boundary-gated) = what-to-invent(always-expand)
```

The observed difference was search allocation:

```text
boundary-gated candidate evaluations = 5200
always-expand candidate evaluations  = 7800
```

and false expansion:

```text
boundary-gated false expansion = 0.0
always-expand false expansion  = 1.0
```

Thus the supported gain is:

```text
when-to-search / representational economy
```

not:

```text
superior invention quality
```

See `results/v0.7-operator-discovery.md` and `results/negative-result-ledger.md`.

## Architecture boundary

The current operational policy can be summarized as:

```text
current structure
-> adequacy test
-> continue | repair | expand | investigate
```

The central decision boundary is around discovery, not discovery itself.

The shared constitutional invariant remains:

> **Keep possibility open; keep authority earned.**

A synthesized representation is a candidate coordinate. It does not become a validated causal claim merely because it improves discrimination.

## Relationship to Correctable Lineage

The projects are complementary scope-control mechanisms:

```text
Correctable Lineage  -> scope of inheritance / authority
Negative-Space Search -> scope of exploration / search effort
```

Their joint rule is:

> **Expand only when justified. Preserve only when justified.**

Negative-Space Search asks when representational search should expand. Correctable Lineage governs what, after evidence arrives, has earned inheritance.

No additional bridge object is required.

## What is not established

The current evidence does **not** establish:

- superior invention relative to matched generic synthesis;
- a uniquely negative-space search algorithm;
- autonomous invention of primitive operations or the synthesis generator;
- causal truth of synthesized representations;
- open-ended interface invention;
- robustness to corrupted or misattributed resolution labels;
- superiority to neural representation learning, Bayesian structure discovery, causal discovery, AutoML/program synthesis, or a real language-model abstraction baseline;
- transfer of the search-economy result to non-synthetic ecologies.

## Evaluation target

Future comparison should emphasize matched quality/cost tradeoffs rather than invention count.

Report at minimum:

```text
Q_eval = (
  task_quality,
  search_cost,
  representation_cost,
  evidence_cost,
  latency
)
```

The key comparison is whether an explicit adequacy-boundary mechanism improves the Pareto frontier:

```text
same-or-better quality at lower total cost
```

or:

```text
better quality at matched total cost
```

A simple improvement/cost ratio may be reported secondarily, but should not replace the multidimensional profile.

## Reopening conditions

There is no automatic v0.8.

Internal architecture development should reopen only after at least one external pressure identifies a recurring failure that the current system cannot discriminate:

1. a stronger matched baseline defeats or matches the claimed search economy;
2. uncertain expansion payoff or realistic costs break the current gating policy;
3. a non-synthetic task reveals a new failure structure;
4. an independent reproduction contradicts the internal results.

Until then, the repository should remain an attackable research object rather than continue expanding because additional synthetic ladder rungs are imaginable.

## Research-status compression

> **Negative-Space Search does not determine what new representations are true. It determines when existing representations have earned the right to be challenged.**

The methodological result is equally important:

```text
research progress != maximizing claims
research progress  = maximizing justified claims
```
