# Negative-Space Search v0.7: Search Governance, Not Discovery

Status: **frozen empirical research artifact for external evaluation**.

> **Negative-Space Search does not currently demonstrate superior invention. Its supported contribution is conditional allocation of representational search: determining when existing explanatory structures are demonstrably inadequate and when expansion is unwarranted.**

> **Negative-Space Search governs when a representational search space should be challenged. It does not determine which new representation is true.**

The repository preserves the distinction:

```text
Psi allocates attention / search effort.
Evidence allocates authority.
```

The archive must not be interpreted as evidence that the system discovers truth, autonomously invents representations, outperforms generic discovery systems, or solves open-ended interface invention.

## Abstract

Negative-Space Search is an empirical benchmark program studying **adaptive search governance**: when an adaptive system should spend resources challenging the representational/search space it currently uses.

Across v0.1–v0.7, stronger interpretations were progressively narrowed by hostile controls and matched baselines. The surviving v0.7 result is not superior invention. In the frozen synthetic benchmark, a boundary-gated generic synthesizer retained the same invention quality and held-out transfer as an always-expand generic synthesizer while reducing candidate evaluations from `7800` to `5200` and avoiding expansion in already-adequate regions.

The supported contribution is therefore **conditional representational search economy**: detecting demonstrated inadequacy, distinguishing it from ordinary uncertainty, and allocating representational expansion effort only when warranted by the benchmark evidence.

## Research question

> **When should a system spend resources challenging the space of representations it currently uses?**

The project began with a broader intuition about finding what an equilibrium had missed. The executed benchmark sequence contracted that intuition into a narrower systems question:

```text
current structure
-> adequacy test
-> continue | repair | expand | investigate
```

The empirical object is the **decision boundary around discovery**, not discovery quality itself.

## Frozen hypothesis

> **Explicit representational adequacy diagnosis can improve the efficiency of adaptive search by allocating expansion effort only when current explanatory structures have demonstrably failed.**

Primary null:

> **Matched general search systems may achieve equal or better repair quality without explicit adequacy-boundary structure.**

The null remains live.

## Supported findings

The controlled benchmark lineage supports the following narrow findings:

- causal reasoning about why an absence exists can outperform naive gap/novelty heuristics in hostile synthetic cases;
- failed corrections can license representation repair when previously rewarded abstractions stop transferring;
- basis inadequacy can trigger conditional relation composition inside a supplied construction language;
- systems can detect demonstrated non-identifiability of the current construction language and distinguish it from ordinary unsupported uncertainty;
- boundary-gated synthesis can preserve the repair quality of matched generic synthesis while reducing unnecessary expansion effort;
- in v0.7, the supported advantage is **when-to-search / search economy**, not **what-to-invent / invention quality**.

Key v0.7 comparison:

```text
boundary-gated invention quality = 1.0
always-expand invention quality  = 1.0

boundary-gated held-out transfer = 1.0
always-expand held-out transfer  = 1.0

boundary-gated candidate evaluations = 5200
always-expand candidate evaluations  = 7800
```

Detailed summaries:

- [`CLAIMS.md`](CLAIMS.md)
- [`RESULTS.md`](RESULTS.md)
- [`NEGATIVE_RESULTS.md`](NEGATIVE_RESULTS.md)
- [`results/v0.7-operator-discovery.md`](results/v0.7-operator-discovery.md)
- [`results/negative-result-ledger.md`](results/negative-result-ledger.md)

## Unsupported claims

This release does **not** establish:

- autonomous discovery;
- discovery of truth;
- autonomous invention of representational primitives;
- operator invention without supplied primitives or a supplied synthesis generator;
- superiority over strong generic discovery/search systems;
- superiority over neural representation learning, Bayesian structure discovery, causal discovery, AutoML, or generic program synthesis;
- a unique negative-space mechanism;
- open-ended interface invention;
- real-world effectiveness outside the controlled synthetic benchmark sequence;
- causal truth of generated candidate representations.

A candidate coordinate can improve discrimination without earning causal authority.

```text
possibility != authority
candidate != claim
Psi != U
```

## Relationship to Correctable Lineage

Negative-Space Search and Correctable Lineage govern different scopes:

```text
Negative-Space Search -> scope of exploration / attention / search effort
Correctable Lineage   -> scope of inheritance / authority
```

The shared architecture is:

```text
L_t
-> Psi_t
-> candidate
-> evidence / reality
-> U_t
-> L_(t+1)
```

`Psi` proposes where representational search effort should be allocated. Evidence/reality provides the discriminating consequences. `U` updates authority. `L` denotes what remains justified for inheritance.

The shared principle is:

> **Keep possibility open; keep authority earned.**

A compact joint rule is:

> **Expand only when justified. Preserve only when justified.**

No additional bridge object or new primitive is introduced in this archival release.

See [`METHOD.md`](METHOD.md) and [`docs/frozen-core.md`](docs/frozen-core.md).

## Reproducibility instructions

Requirements:

```text
Python >= 3.11
```

Validated v0.7 merge-state environment:

```text
Python 3.11.15
GitHub Actions run 31177528904
job 92862772195
70 / 70 tests passed
```

Install and run the complete test suite:

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

Execute the benchmark lineage:

```bash
python -m negative_space_search.run_v0_1
python -m negative_space_search.run_v0_1_1
python -m negative_space_search.run_v0_2
python -m negative_space_search.run_v0_3
python -m negative_space_search.run_v0_4
python -m negative_space_search.run_v0_5
python -m negative_space_search.run_v0_6
python -m negative_space_search.run_v0_7
```

See [`REPRODUCTION.md`](REPRODUCTION.md) for expected v0.7 outputs and provenance.

## Limitations

The release remains deliberately narrow.

- The benchmark sequence is synthetic and adversarially constructed to isolate specific failure modes.
- v0.7 uses a supplied finite synthesis meta-language (`t0..t3`, `ADD`, `SUB`, `GT`, `LT`) and supplied scoring/retention machinery.
- The project does not demonstrate autonomous invention of the primitive substrate or generator.
- The controlled v0.7 synthesis task guarantees that useful repair expressions exist in the supplied meta-language; real expansion may fail.
- The benchmark does not establish robustness to corrupted or misattributed resolution labels.
- The result has not yet been reproduced by an independent evaluator.
- The result has not yet been compared against a comprehensive set of strong external discovery systems.
- The search-economy effect has not yet been demonstrated in a non-synthetic ecology.

## Future evaluation requirements

There is **no automatic v0.8**.

This repository is frozen so that future work can challenge the current claim rather than extend the ontology by default.

Meaningful reopening pressure should come from one or more of:

1. **External baseline challenge** — a matched strong generic system achieves equal or better quality at equal or lower total cost.
2. **Cost uncertainty** — expansion has uncertain success probability and realistic evidence/compute/opportunity costs.
3. **Real-task transfer** — debugging, experimental design, scientific hypothesis prioritization, engineering diagnosis, or another domain where search cost is measurable.
4. **Independent reproduction** — an external evaluator confirms or contradicts the synthetic benchmark result.
5. **Unclassified failure** — a recurring empirical failure cannot be discriminated by the frozen architecture.

Future evaluation should report quality and cost separately rather than hide tradeoffs in a single scalar:

```text
Q_eval = (
  task_quality,
  search_cost,
  representation_cost,
  evidence_cost,
  latency
)
```

## Empirical progression

| Version | Frozen interpretation |
| --- | --- |
| v0.1 | causal absence reasoning beats naive gap/opportunity search in controlled cases |
| v0.1.1 | apparent advantage localized to evidence selection |
| v0.2 | matched history-aware causal reasoning removes the apparent unique advantage |
| v0.3 | typed causal history, not negative-space identity, drives transfer |
| v0.4 | failed corrections can license representation repair |
| v0.5 | basis inadequacy can trigger conditional composition inside a supplied language |
| v0.6 | construction-language non-identifiability can be detected and separated from ordinary unknowns |
| v0.7 | boundary-gated generic synthesis preserves repair quality while reducing unnecessary expansion |

Read this progression as **claim contraction under stronger discrimination**, not as a monotonic intelligence ladder.

## Citation and archive metadata

- [`CITATION.cff`](CITATION.cff)
- [`.zenodo.json`](.zenodo.json)
- License: [`MIT`](LICENSE)
- Version: `0.7`
- Release date: `2026-08-07`

## Frozen research-status compression

> **Negative-Space Search does not determine what new representations are true. It determines when existing representations have earned the right to be challenged.**

```text
research progress != maximizing claims
research progress  = maximizing justified claims
```
