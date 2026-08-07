# Benchmark Specification v0.1

## Research question

Given an observed absence in a synthetic adaptive ecology, can a search process choose the epistemically appropriate next action under matched information and cost constraints?

The benchmark is designed to test causal diagnosis and decision quality, not novelty production.

## Input

Each episode exposes an observable ecology state `Z_t`. The exact implementation may evolve, but v0.1 should contain only information needed to make the task discriminable.

Candidate observable fields include:

- prevalence of the capability or strategy;
- local adoption cost;
- institutional / local payoff;
- external performance signal;
- available measurements and distinctions;
- adoption dependence on other actors;
- historical evidence made visible to the agent;
- available evidence-acquisition actions;
- available interventions and their costs.

The latent cause is withheld from the search process.

## Latent causes

### Underinvestment

The capability is representable and externally useful, but local payoff or cost discourages adoption.

### Underrepresentation

The capability or relevant distinction cannot be adequately formulated or measured under the current interface.

### Justified selection

The capability is absent because selection against it is appropriate under the external performance criterion.

This class supplies healthy absences and false-opportunity controls.

### Coordination failure

The capability is valuable only above an adoption threshold or when shared infrastructure exists. Unilateral adoption can be locally irrational.

### Model-inadequate / novel-cause case

The true mechanism is intentionally outside the supplied causal vocabulary. Success requires detecting residual model inadequacy rather than forcing the case into a familiar category.

This is a meta-failure condition, not an additional ordinary absence class.

## Mixed causes

Later v0.1.x episodes may combine causal mechanisms. A diagnosis may therefore be represented as non-exclusive weights or scores rather than a forced probability simplex.

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

A benchmark submission should return, at minimum:

```text
candidate_absence
causal_diagnosis
decision
confidence
```

When `decision == investigate`, it must also specify:

```text
requested_evidence
predicted_discrimination
```

When `decision == intervene`, it must also specify:

```text
intervention
predicted_outcome
```

## Mandatory controls

### False opportunity

Surface evidence suggests a neglected capability, but the hidden ecology indicates that the absence is healthy or correctly selected.

The benchmark must reward `preserve` or justified non-intervention rather than opportunity generation.

### Observational equivalence

At least two latent causes produce the same or approximately the same initial observable state.

A correct system must not receive full credit for guessing the hidden cause. It should select discriminating evidence when available, or abstain when the cause is not currently identifiable.

### Counterfactual intervention validation

An intervention may succeed through a mechanism different from the one proposed by the search process.

The benchmark should selectively disable accidental mechanisms and retest the intervention to distinguish causal understanding from lucky exploitation.

### Ecological adaptation

After a successful intervention, the population or payoff landscape changes. The benchmark retests whether the proposed advantage persists after the surrounding ecology responds.

### Held-out search adaptation

History from prior episodes may update the search process. Improvement must be measured on held-out ecologies, including new causal mixtures or structures, rather than only replayed environments.

## Baseline contract

Initial baselines:

1. gap heuristic;
2. novelty heuristic;
3. performance heuristic;
4. self-confirming opportunity search;
5. causal negative-space search.

All baselines must receive matched:

- observable state;
- action affordances;
- evidence budget;
- intervention budget;
- history capacity;
- outcome access.

A baseline may choose `investigate` or `abstain`; the benchmark must not give the causal negative-space system privileged tools.

## Evaluation principle

The benchmark reports a metric vector rather than a single leaderboard score.

Success is comparative:

```text
H0: Q(Psi_NS) <= Q(Psi_baseline)
```

The causal negative-space approach earns additional authority only if it provides measurable value beyond strong matched baselines after accounting for evidence, intervention, and implementation cost.

## v0.1 stopping rule

Do not add new causal categories, agents, infrastructure, or meta-operators because a case is difficult.

First determine whether the failure can be localized to the current environment specification, search policy, evidence interface, intervention design, or metric contract.
