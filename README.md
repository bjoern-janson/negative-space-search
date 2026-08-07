# negative-space-search

**Negative-Space Search** is an empirical research project on how adaptive systems allocate investigative attention around apparent absences without converting possibility into epistemic authority.

It is the discovery counterpart to **Correctable Lineage**:

- Negative-Space Search (`Psi`) allocates investigative attention.
- Evidence determines epistemic authority through updating (`U`).
- Correctable Lineage governs what remains justified as inherited structure (`L`).

> **Keep possibility open; keep authority earned.**

## Frozen core

```text
possibility != authority
candidate != claim
Psi != U
evidence changes only identified scope
```

The operational cycle is:

```text
L_t -> Psi_t -> C_t -> W/e_t -> U_t -> L_t+1
```

The project treats absence as a causal inference problem:

```text
absence != opportunity
```

A search process must distinguish justified absence, maladaptive absence, uncertainty requiring evidence, and cases where its own causal vocabulary is inadequate.

The normative v0.1 core is frozen in [`docs/frozen-core.md`](docs/frozen-core.md).

## v0.1 benchmark

Task: given an observed absence in a synthetic research ecology, choose:

```text
intervene | preserve | investigate | abstain
```

The five controlled environment families are:

1. underinvestment;
2. underrepresentation;
3. justified selection;
4. coordination failure;
5. model-inadequate / novel-mechanism condition.

The first hostile test constructs an underinvestment world and a justified-selection world with identical initial observations. A policy that guesses the cause fails. It must request the discriminating external-value experiment or abstain if that evidence is unavailable.

See [`docs/benchmark-spec-v0.1.md`](docs/benchmark-spec-v0.1.md) and [`benchmark/spec.md`](benchmark/spec.md).

## Baselines

v0.1 includes:

- seeded random action;
- gap heuristic;
- novelty heuristic;
- short-term performance heuristic;
- self-confirming opportunity search;
- general causal reasoner;
- causal negative-space search.

All policies receive matched observable information and action affordances.

## Metrics

No single score is canonical. The target metric vector is:

```text
Q_Psi = (Q_q, Q_n, Q_E, Q_A, Q_Y, Q_CF, Q_abstain, Q_D)
```

The initial executable evaluator covers only the dimensions that the toy cases identify cleanly. Unimplemented dimensions remain unscored rather than being approximated into a synthetic aggregate.

## Repository structure

```text
negative-space-search/
├── README.md
├── pyproject.toml
├── .github/workflows/ci.yml
├── docs/
│   ├── framework.md
│   ├── frozen-core.md
│   ├── benchmark-spec-v0.1.md
│   └── failure-taxonomy.md
├── benchmark/
│   ├── spec.md
│   └── metrics.md
├── src/negative_space_search/
│   ├── __init__.py
│   ├── environments.py
│   ├── simulator.py
│   ├── baselines.py
│   ├── evaluation.py
│   └── run_v0_1.py
├── tests/
│   └── test_v0_1.py
├── experiments/
│   └── README.md
└── results/
    └── README.md
```

## Run v0.1

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m negative_space_search.run_v0_1
```

CI runs the same commands on pushes to `main` and on pull requests.

## Explicitly not included yet

- a universal theory of adaptation;
- new primitives beyond the frozen v0.1 core;
- a scalar meta-solver or corrigibility leaderboard;
- a claim that the four ordinary absence mechanisms are exhaustive;
- an `N_X` catch-all category masquerading as a solution to model inadequacy;
- real-science case studies before the synthetic benchmark earns them;
- integration with Correctable Lineage before the evidence boundary is tested;
- production ML/agent infrastructure, databases, dashboards, or distributed execution;
- an operator above `Psi`;
- automatic authority updates from search outputs;
- release/archival machinery before a result warrants freezing;
- a license choice made by default rather than deliberately.

## Status

**v0.1 — executable synthetic benchmark scaffold.**

The null hypothesis remains explicit:

```text
H0: Q(Psi_negative_space) <= Q(Psi_baseline)
```

The next conceptual change must be forced by a recurring empirical failure that the frozen structure cannot discriminate. Until then, the project is an experimental object.