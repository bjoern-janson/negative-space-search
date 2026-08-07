# negative-space-search

**Negative-Space Search** is an empirical research project on adaptive search governance: when an adaptive system should spend resources challenging the representational/search space it currently uses.

It is the discovery-side counterpart to **Correctable Lineage**:

- Negative-Space Search (`Psi`) governs the scope of exploration / investigative effort.
- Evidence determines epistemic authority through updating (`U`).
- Correctable Lineage governs what remains justified as inherited structure (`L`).

> **Keep possibility open; keep authority earned.**

## Current status

**v0.7 — Search Governance, Not Discovery. Frozen for external evaluation.**

Negative-Space Search does **not** currently demonstrate superior invention.

Its supported contribution is conditional allocation of representational search: determining when existing explanatory structures are demonstrably inadequate and when expansion is unwarranted.

The system governs the cost of challenging its own representational boundaries; it does not determine which new representations are true.

The canonical status document is [`docs/research-status-v0.7.md`](docs/research-status-v0.7.md).

## Central hypothesis

> Explicit representational adequacy diagnosis can improve the efficiency of adaptive search by allocating expansion effort only when current explanatory structures have demonstrably failed.

Primary null:

> Matched general search systems achieve equal or better solution quality at equal or lower cost without explicit adequacy-boundary structure.

The null remains live.

## Frozen core

```text
possibility != authority
candidate != claim
Psi != U
evidence changes only identified scope
```

The operational cycle remains:

```text
L_t -> Psi_t -> C_t -> W/e_t -> U_t -> L_t+1
```

Operationally:

```text
Psi proposes.
evidence authorizes.
```

See [`docs/frozen-core.md`](docs/frozen-core.md).

## Current empirical object

The original intuition:

```text
find what the equilibrium missed
```

has contracted through hostile testing into:

```text
detect when the current search space has become inadequate enough to justify expansion
```

The project is therefore **not** a novelty engine and **not** an established autonomous discovery mechanism.

The current policy shape is:

```text
current structure
-> adequacy test
-> continue | repair | expand | investigate
```

The central object is the **decision boundary around discovery**.

## Empirical progression

| Version | Main result |
| --- | --- |
| v0.1 | causal absence reasoning beats naive gap/opportunity heuristics in controlled cases |
| v0.1.1 | apparent advantage localized to evidence selection rather than evidence interpretation |
| v0.2 | matched history-aware causal reasoning removes the apparent unique advantage |
| v0.3 | typed causal failure history improves transfer; negative-space identity does not |
| v0.4 | failure history can justify representation repair from misleading surface cues |
| v0.5 | basis insufficiency can license local composition inside a supplied language |
| v0.6 | demonstrated construction-language non-identifiability can be distinguished from ordinary unknowns |
| v0.7 | boundary-gated generic synthesis preserves invention quality while reducing unnecessary expansion cost |

Read this as **claim contraction under stronger discrimination**, not as a monotonic intelligence ladder.

## v0.7 result

The matched `always-expand` and `boundary-gated` generic synthesizers constructed the same four abstractions and achieved the same held-out repair, transfer, `Q_invention`, and final representation cost.

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

Thus the supported v0.7 contribution is:

```text
when-to-search / adaptive representational economy
```

not:

```text
superior invention quality
```

See [`results/v0.7-operator-discovery.md`](results/v0.7-operator-discovery.md) and [`results/negative-result-ledger.md`](results/negative-result-ledger.md).

## Benchmark lineage

The initial task is still the root benchmark contract: given an observed absence in a controlled ecology, choose an epistemically appropriate action:

```text
intervene | preserve | investigate | abstain
```

The synthetic benchmark lineage then progressively attacks stronger assumptions about:

- causal attribution;
- evidence acquisition;
- history-sensitive escalation;
- representation quality;
- representation repair;
- basis composition;
- construction-language adequacy;
- conditional generic synthesis.

The repository preserves each negative/null result rather than redefining the framework until it wins.

## Evaluation dimensions

No single score is canonical. Earlier benchmark dimensions include:

```text
Q_Psi = (Q_q, Q_n, Q_E, Q_A, Q_Y, Q_CF, Q_abstain, Q_D)
```

For the frozen external-evaluation phase, report quality and cost separately:

```text
Q_eval = (
  task_quality,
  search_cost,
  representation_cost,
  evidence_cost,
  latency
)
```

The key contest is whether explicit adequacy-boundary structure improves the Pareto frontier: same-or-better task quality at lower total cost, or better quality at matched total cost.

## Relationship to Correctable Lineage

```text
Correctable Lineage   -> scope of inheritance / authority
Negative-Space Search -> scope of exploration / search effort
```

Their shared rule is:

> **Expand only when justified. Preserve only when justified.**

No additional bridge object is required.

## What is not established

The current experiments do **not** establish:

- superior invention relative to matched generic synthesis;
- a uniquely negative-space algorithm;
- autonomous invention of primitive operations or the synthesis generator;
- causal truth of synthesized representations;
- open-ended interface invention;
- robustness to corrupted or misattributed resolution labels;
- superiority to neural representation learning, Bayesian structure discovery, causal discovery, AutoML/program synthesis, or a real language-model abstraction baseline;
- transfer of the search-economy result to non-synthetic ecologies.

## Reopening conditions

There is **no automatic v0.8**.

Internal architecture development should reopen only when external pressure identifies a recurring failure the current system cannot discriminate, for example:

1. a stronger matched baseline defeats or matches the claimed search economy;
2. uncertain expansion payoff or realistic costs break the current gating policy;
3. a non-synthetic task reveals a new failure structure;
4. an independent reproduction contradicts the internal results.

Until then, this repository should remain an attackable empirical research object rather than keep climbing an internally generated benchmark staircase.

## Reproduction

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

GitHub Actions runs the benchmark test suite on `main` and pull requests. Individual benchmark runners live under `src/negative_space_search/` and their executed summaries under `results/`.

## Research-status compression

> **Negative-Space Search does not determine what new representations are true. It determines when existing representations have earned the right to be challenged.**

```text
research progress != maximizing claims
research progress  = maximizing justified claims
```
