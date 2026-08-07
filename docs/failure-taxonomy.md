# Failure Taxonomy v0.1

This taxonomy localizes benchmark failures. It is not a claim that all real-world failures fit these labels.

## Search-process failures

| Failure | Description | Primary update target |
| --- | --- | --- |
| `F_q` | Misses a consequential apparent absence or treats irrelevant absence as consequential | attention/search policy |
| `F_n` | Misdiagnoses the causal mechanism generating the absence | causal diagnosis |
| `F_E` | Requests evidence that does not discriminate live explanations | evidence acquisition |
| `F_A` | Chooses an intervention mismatched to the identified cause | intervention policy |
| `F_Y` | Predicts the wrong consequence of evidence acquisition or intervention | outcome model |
| `F_CF` | Intervention succeeds only through an accidental mechanism | causal attribution |
| `F_abstain` | Acts when evidence is non-identifying, or abstains when a warranted decision is available | calibration / decision rule |
| `F_D` | Initial gain disappears after ecological adaptation | durability model |
| `F_I` | Forces a case into the current causal vocabulary when the vocabulary is inadequate | search interface / representation |

## Candidate failure versus diagnostic failure

These must remain separate.

```text
candidate failure: the proposed capability/intervention does not improve outcomes
diagnostic failure: the system was wrong about why the absence existed
```

The same observed outcome may imply different updates depending on what the experiment actually identifies.

## Authority rule for failures

A failed intervention does not automatically falsify:

- the value of the candidate capability;
- the causal diagnosis;
- the evidence-acquisition strategy;
- the negative-space search method as a whole.

Update only the shallowest component identified by the failure plus explicit dependency paths.

## False-opportunity control

An absence that is correctly selected against is a healthy state, not a missed discovery.

A search policy succeeds when it correctly chooses `preserve`.

## Non-identifiability control

If two latent mechanisms generate the same available observation, a forced causal diagnosis is an error.

The appropriate action is `investigate` with discriminating evidence, or `abstain` when no such evidence is available.

## Model inadequacy

`F_I` is not repaired by adding an `other` bucket. Success requires recognizing that residual evidence cannot be represented adequately by the current causal vocabulary.