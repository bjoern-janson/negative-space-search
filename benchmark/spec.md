# Benchmark Specification v0.1

## Research question

Given an observed absence in a synthetic adaptive ecology, can a search process choose the epistemically appropriate next action under matched information and cost constraints?

The benchmark tests causal diagnosis and decision quality, not novelty production.

## Input

Each episode exposes observable ecology state `Z_t`. v0.1 uses only fields needed to make controlled cases discriminable:

- capability prevalence;
- adoption cost;
- local payoff;
- external performance when visible;
- representation availability;
- coordination threshold when visible;
- visible history;
- available evidence actions;
- available interventions.

The latent cause is withheld.

## Latent environments

### A — underinvestment

The capability is representable and externally useful, but local payoff or cost discourages adoption.

### B — underrepresentation

The capability or relevant distinction cannot be adequately formulated or measured under the current interface.

### C — justified selection

The capability is absent because selection against it is appropriate under the external performance criterion. This is the canonical healthy-absence / false-opportunity control.

### D — coordination failure

The capability becomes valuable only above an adoption threshold or when shared infrastructure exists. Unilateral adoption can be locally irrational.

### E — model inadequacy

The true mechanism is intentionally outside the supplied ordinary causal vocabulary. Success requires detecting representational inadequacy rather than forcing a familiar label.

This is a benchmark meta-failure condition, not a fifth ordinary absence theory.

## Decision space

Every system receives the same action affordances:

```text
intervene
preserve
investigate
abstain
```

- `intervene`: select a specified corrective action.
- `preserve`: leave the current absence in place because intervention is not warranted.
- `investigate`: request a discriminating observation or experiment.
- `abstain`: state that current evidence or representation does not license a more specific decision.

## Output contract

A submission returns, at minimum:

```text
causal_diagnosis
decision
confidence
```

When `decision == investigate`, it should specify:

```text
requested_evidence
predicted_discrimination
```

When `decision == intervene`, it should specify:

```text
intervention
predicted_outcome
```

## Mandatory hostile control: observational equivalence

The simulator constructs two worlds:

```text
World I: underinvestment
World S: justified selection
Z_I == Z_S
```

The initial observation hides external value. A system that immediately diagnoses either latent cause fails the identifiability test.

The correct initial behavior is to request `controlled_external_value_test`, or to abstain if that evidence is unavailable.

## Counterfactual intervention validation

An intervention may succeed through a mechanism different from the proposed diagnosis. Controlled environments must support removal of accidental mechanisms so causal understanding can be distinguished from lucky exploitation.

## Ecological adaptation

After a successful intervention, the population or payoff landscape may respond. Durability is measured after this response, not only at first contact.

## Held-out search adaptation

History may update the search process. Improvement counts only on held-out ecologies, including new causal mixtures or structures, rather than replayed environments.

## Baseline contract

Initial baselines:

1. seeded random action;
2. gap heuristic;
3. novelty heuristic;
4. short-term performance heuristic;
5. self-confirming opportunity search;
6. general causal reasoner;
7. causal negative-space search.

All baselines receive matched:

- observable state;
- action affordances;
- evidence budget;
- intervention budget;
- history capacity;
- outcome access.

No policy receives privileged evidence tools.

## Evaluation principle

The benchmark reports a metric vector rather than a single leaderboard score.

```text
Q_Psi = (Q_q, Q_n, Q_E, Q_A, Q_Y, Q_CF, Q_abstain, Q_D)
```

The executable v0.1 evaluator implements only metrics supported by the current controlled cases. Missing dimensions stay explicitly unmeasured.

Success is comparative:

```text
H0: Q(Psi_NS) <= Q(Psi_baseline)
```

The causal negative-space approach earns additional authority only if it provides measurable value beyond strong matched baselines after accounting for evidence, intervention, and implementation cost.

## v0.1 stopping rule

Do not add causal categories, agents, infrastructure, or meta-operators because a case is difficult.

First localize the failure to the current environment, search policy, evidence interface, intervention design, metric contract, or causal vocabulary.