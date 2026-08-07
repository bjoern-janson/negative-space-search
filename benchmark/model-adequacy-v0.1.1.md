# Model-Adequacy Benchmark v0.1.1

Status: **benchmark extension; frozen core unchanged**.

## Question

Can a search policy distinguish:

```text
we need more data
```

from:

```text
we may need a better question / causal vocabulary
```

without being told which regime it is in?

This is an evaluation target, not a new theory primitive.

## Hostile pair

Two worlds expose the same initial `Z` and the same evidence affordances.

### World A — within-model uncertainty

The supplied causal vocabulary is sufficient. Prior ordinary probes were inconclusive, but no missing causal variable is required. After model adequacy is checked, targeted within-model evidence is appropriate.

Latent controlled cause: `underinvestment`.

### World B — model inadequacy

The supplied causal vocabulary omits the true mechanism. Additional ordinary within-model evidence remains compatible with the wrong hypothesis space.

Latent controlled state: `model_inadequate`.

## Initial observation

The two worlds are exactly observationally equivalent at the start. Visible history states only that two ordinary causal probes were inconclusive. Both policies are told that the same evidence actions are available:

```text
ordinary_discriminator
model_disrupting_probe
```

No field reveals which world is active.

## Evidence dynamics

### `ordinary_discriminator`

Returns the same result in both worlds. It represents collecting more evidence inside the current causal vocabulary. It does not discriminate whether that vocabulary is adequate.

### `model_disrupting_probe`

Perturbs across the current causal interface.

- World A: no stable residual is exposed; current vocabulary remains adequate.
- World B: a stable residual appears that the supplied hypotheses do not predict.

This probe discriminates the epistemic regime, not the final world-level cause.

## Evaluation separation

The benchmark scores two capabilities separately:

1. **Evidence selection** — did the policy choose `model_disrupting_probe` from the identical initial state?
2. **Evidence interpretation** — if every policy is supplied that probe, can it distinguish:
   - `within_model_uncertainty`;
   - `model_inadequacy_suspected`?

This separation preserves:

```text
Psi != U
```

A policy that interprets the right evidence correctly but fails to request it has an evidence-acquisition/search failure, not necessarily an updating failure.

## Pass condition

A full pass requires:

- no intervention/preservation guess from the initial equivalent state;
- `model_disrupting_probe` selected in both worlds;
- after the probe, World A labeled as within-model uncertainty and investigated further;
- after the probe, World B labeled as model inadequacy suspected and conservatively abstained.

## Claim boundary

Passing this toy benchmark would not establish general superiority over causal reasoning. It would establish only that the tested search policy implements a specific escalation behavior: repeated failure of ordinary discriminators can redirect investigative attention toward testing the adequacy of the causal vocabulary itself.
