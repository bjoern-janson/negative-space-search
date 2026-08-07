# Reproduction — Negative-Space Search v0.7

Status: **frozen archival reproduction instructions**.

## Environment

The project declares:

```text
Python >= 3.11
build backend: setuptools
```

The validated v0.7 CI run used:

```text
Python 3.11.15
```

The project does not declare third-party runtime dependencies in `pyproject.toml`; benchmark tests use the standard-library `unittest` runner.

## Installation

From the repository root:

```bash
python -m pip install -e .
```

## Test suite

Run the complete benchmark test suite:

```bash
python -m unittest discover -s tests -v
```

### Expected v0.7 merge-state result

```text
70 / 70 tests passed
```

This result was recorded on the tested v0.7 merge state associated with GitHub Actions run:

```text
run: 31177528904
job: 92862772195
Python: 3.11.15
```

The archival documentation commits made after that validated code state do not alter benchmark source, tests, or synthesis logic.

## Execute benchmark runners

The benchmark lineage can be executed individually:

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

## Expected v0.7 outputs

The v0.7 run should reproduce the qualitative and quantitative comparison recorded in `results/v0.7-operator-discovery.md`.

Key values:

### Boundary-gated generic synthesizer

```text
boundary detection:    1.0
construction:          1.0
held-out repair:       1.0
multi-family transfer: 1.0
false expansion:       0.0
search cost:           5200 candidate evaluations
representation cost:   20
```

### Always-expand generic synthesizer

```text
boundary detection:    1.0
construction:          1.0
held-out repair:       1.0
multi-family transfer: 1.0
false expansion:       1.0
search cost:           7800 candidate evaluations
representation cost:   20
```

Both systems should construct the same retained predicates:

```text
direction_forward_probe -> GT(t3,t0)
direction_reverse_probe -> GT(t0,t3)
center_heavy_probe      -> GT(ADD(t1,t2),ADD(t0,t3))
edge_heavy_probe        -> GT(ADD(t0,t3),ADD(t1,t2))
```

## Expected interpretation

A successful reproduction should preserve the null/localization:

```text
invention quality(boundary-gated) = invention quality(always-expand)
```

and the observed search-economy difference:

```text
search cost(boundary-gated) < search cost(always-expand)
```

Do not reinterpret a passing run as evidence of autonomous discovery or causal truth of the generated predicates.

## CI configuration

GitHub Actions configuration is in:

```text
.github/workflows/ci.yml
```

It runs:

1. editable installation;
2. the full unittest suite;
3. benchmark runners v0.1 through v0.7.

## Detailed provenance

See:

- `results/v0.7-operator-discovery.md`
- `results/negative-result-ledger.md`
- `experiments/v0.7-operator-discovery.md`
- `experiments/v0.7-case-matrix.md`
- `benchmark/operator-discovery-v0.7.md`
