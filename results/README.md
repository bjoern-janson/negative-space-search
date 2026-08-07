# Results

This directory will contain reproducible summaries of benchmark runs.

Each result record should include:

- experiment identifier;
- code / benchmark commit SHA;
- policy versions;
- environment seeds or generation manifest;
- full metric vector rather than only a composite score;
- per-latent-cause and false-opportunity breakdowns;
- observational-equivalence and model-inadequate performance;
- evidence and intervention cost usage;
- pre-history versus post-history held-out performance;
- counterfactual causal-fidelity results where applicable;
- failures, residuals, and unresolved ambiguities.

Raw artifacts may live outside Git when they become large, but summaries must retain enough provenance to locate and reproduce them.

Do not report only wins. Preserve negative and null results when they constrain the search architecture or its claimed advantage over baselines.
