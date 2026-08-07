# Experiments

The v0.1 runner now exists. This directory records experiment hypotheses and protocols **before** results are interpreted.

Keep experiment records small and reconstructible. Each experiment should state:

- research question / hypothesis;
- benchmark version or commit SHA;
- environment generator and seed set;
- policies compared;
- matched information, evidence, and intervention budgets;
- metric dimensions evaluated;
- held-out split definition when applicable;
- counterfactual validation plan when applicable;
- expected discriminating outcome before the run;
- explicit failure interpretation.

The first registered experiment is [`v0.1-hostile-equivalence.md`](v0.1-hostile-equivalence.md).

Run the current executable benchmark with:

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m negative_space_search.run_v0_1
```

Do not add a workflow engine, experiment database, dashboard, or configuration hierarchy until repeated experiments demonstrate that flat files are insufficient.

A negative result is a valid experiment outcome. Preserve failed diagnoses and mismatched interventions when they are informative about the search process.