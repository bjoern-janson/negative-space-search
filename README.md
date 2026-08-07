# negative-space-search

**Negative-Space Search** is an empirical research project on how adaptive systems decide whether an observed absence deserves intervention, preservation, further investigation, or abstention.

It is the discovery counterpart to **Correctable Lineage**:

- Negative-Space Search (`Ψ`) allocates investigative attention.
- Evidence determines epistemic authority.
- Correctable Lineage governs what becomes inherited structure.

> **Keep possibility open; keep authority earned.**

## Core constraint

Absence is not evidence of opportunity:

```text
absence ≠ opportunity
absence → causal inference problem
```

The project asks whether an explicit causal negative-space search process can outperform simpler opportunity-generation strategies by distinguishing:

- maladaptive underprovision;
- underrepresentation / missing distinctions;
- justified selection against a capability;
- coordination failures;
- uncertainty requiring discriminating evidence;
- cases where the current causal vocabulary is itself inadequate.

## Minimal architecture

```text
L_t → Ψ_t → C_t → W/e_t → U_t → L_{t+1}
```

Where:

- `L_t` — inherited validated structure;
- `Ψ_t` — causal negative-space search process;
- `C_t` — candidate intervention or distinction;
- `W/e_t` — external consequence and evidence;
- `U_t` — evidence-conditioned update;
- `L_{t+1}` — revised lineage.

The firewall is deliberate:

```text
Ψ proposes.
e authorizes.
```

Candidate generation must not manufacture epistemic authority.

## Initial benchmark

Given an observed absence, select an action:

```text
intervene | preserve | investigate | abstain
```

The first benchmark evaluates a search process on a vector of capabilities rather than a single score:

- consequential-absence identification;
- causal diagnosis;
- evidence acquisition under non-identifiability;
- intervention matching;
- consequence prediction;
- counterfactual causal fidelity;
- calibrated abstention;
- durability after ecological adaptation;
- improvement from preserved diagnostic history on held-out ecologies.

Synthetic environments begin with controlled latent causes:

1. underinvestment;
2. underrepresentation;
3. justified selection;
4. coordination failure;
5. model-inadequate / novel-cause cases.

False opportunities and observationally equivalent cases are mandatory controls.

## Baselines

The initial comparison set is intentionally small:

- gap heuristic;
- novelty heuristic;
- performance heuristic;
- self-confirming opportunity search;
- causal negative-space search.

All baselines should receive matched information, action affordances, evidence budgets, and intervention budgets.

## Repository structure

```text
negative-space-search/
├── README.md
├── pyproject.toml
├── docs/
│   └── framework.md
├── benchmark/
│   ├── spec.md
│   └── metrics.md
├── src/
│   └── negative_space_search/
│       ├── __init__.py
│       ├── environments.py
│       └── baselines.py
├── experiments/
│   └── README.md
└── results/
    └── README.md
```

### Directory purposes

- `docs/` — frozen conceptual constraints needed to interpret experiments; not an expanding ontology.
- `benchmark/` — formal task, latent-state, action, identifiability, and scoring specifications.
- `src/negative_space_search/` — minimal executable interfaces for synthetic ecologies and search baselines.
- `experiments/` — experiment plans/configurations once the benchmark runner exists.
- `results/` — reproducible result summaries and links to raw artifacts.

## Initial files

The first repository version contains exactly ten substantive files:

1. `README.md` — project contract, scope, tree, and exclusions.
2. `pyproject.toml` — minimal Python project metadata.
3. `docs/framework.md` — compact conceptual specification and invariants.
4. `benchmark/spec.md` — v0.1 task and environment contract.
5. `benchmark/metrics.md` — multidimensional evaluation contract.
6. `src/negative_space_search/__init__.py` — package surface.
7. `src/negative_space_search/environments.py` — controlled latent-cause data model.
8. `src/negative_space_search/baselines.py` — baseline policy interfaces.
9. `experiments/README.md` — rules for future experiment records.
10. `results/README.md` — rules for future result records.

## What is explicitly not included yet

This repository intentionally does **not** include:

- a universal theory of adaptation;
- new ontology beyond what the first benchmark requires;
- a scalar “corrigibility” or “meta-solver” leaderboard score;
- claims that the four initial absence mechanisms are exhaustive;
- an `N_X` catch-all category (model inadequacy is a failure of the current vocabulary, not another world-state class);
- production ML infrastructure, agent frameworks, databases, dashboards, or distributed execution;
- real-world science-policy conclusions before synthetic benchmark results exist;
- automatic authority updates from `Ψ` outputs;
- a bridge layer between candidate generation and evidence;
- a new meta-operator above `Ψ`;
- release/archival machinery before a result warrants freezing;
- a license choice until one is selected deliberately.

## Research status

**Status: v0.1 scaffold / pre-experiment.**

The conceptual architecture is treated as frozen for the initial benchmark. New primitives should be added only when a recurring empirical failure cannot be discriminated using the current structure.

The first meaningful result may be negative:

```text
H0: Q(Ψ_negative-space) ≤ Q(Ψ_baseline)
```

If explicit causal negative-space search does not outperform strong matched baselines after accounting for its complexity and evidence cost, the architecture should be revised rather than protected.
