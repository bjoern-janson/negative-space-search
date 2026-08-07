# Experiments

This directory will contain experiment definitions once the v0.1 runner exists.

Keep experiment records small and reconstructible. Each experiment should state:

- research question / hypothesis;
- benchmark version or commit SHA;
- environment generator and seed set;
- policies compared;
- matched information, evidence, and intervention budgets;
- metric vector evaluated;
- held-out split definition;
- counterfactual validation plan when applicable;
- expected discriminating outcome before the run.

Do not add a workflow engine, experiment database, dashboard, or configuration hierarchy until repeated experiments demonstrate that flat files are insufficient.

A negative result is a valid experiment outcome. Preserve failed diagnoses and mismatched interventions when they are informative about the search process.
