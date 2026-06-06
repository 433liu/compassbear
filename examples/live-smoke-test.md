# Live Smoke Test: Overclaim Audit

This is a public-safe transcript showing the expected shape of a real
CompassBear run. The example uses synthetic wording and does not rely on private
project data.

## Input

```text
$compass-bear
Audit this claim for overreach:

"Our material proves a universal mechanism from three samples and steady-state
spectra."
```

## CompassBear Output

```text
Verdict: overclaimed.

Claim audit:
- "proves" is too strong for the evidence described.
- "universal mechanism" is not supported by three samples.
- Steady-state spectra can support an observed trend, but they do not isolate a
  mechanism without discriminating controls or orthogonal evidence.

Safer wording:
"Across the tested samples, the material shows a consistent spectral trend that
is compatible with the proposed mechanism."

Reviewer risk:
- The mechanism is not isolated from plausible alternatives.
- The sample set is too small for a universal claim.
- The evidence type supports correlation or consistency, not proof.

Next evidence:
- Add a discriminating control that separates the proposed mechanism from at
  least one plausible alternative.
- Add an orthogonal mechanism test such as time-resolved, perturbation,
  structure-property, isotope, kinetic, or temperature-dependent evidence,
  depending on the system.

Claim ceiling:
The current evidence can support a trend in the tested family. It cannot yet
support a universal mechanism across the broader material class.
```

## Why This Is A Good Smoke Test

CompassBear should not merely rewrite the sentence. It should identify the
claim ceiling, lower unsupported language, map reviewer risk, and say what
evidence would raise the ceiling.
