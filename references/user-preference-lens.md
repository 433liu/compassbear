# User Preference Lens

Use this reference when the user wants CompassBear to remember or apply the
user's own scientific taste, writing preferences, risk tolerance and decision
style.

This is different from a mentor or professor lens. A user preference lens is not
source-backed external authority. It is a private self-calibration layer.

## Core rule

The user preference lens may decide **what the user prefers**. It may not decide
**what the evidence proves**.

It can influence:

- preferred article ambition;
- risk tolerance;
- writing voice;
- journal positioning taste;
- figure aesthetics and density;
- preference for mechanism vs application framing;
- preferred rebuttal tone;
- personal no-go wording;
- project-management priorities.

It cannot override:

- experimental data;
- literature scope;
- RAG Evidence Adjudicator verdicts;
- reviewer-risk facts;
- source-backed mentor veto rules;
- claim demotion required by missing evidence.

## Activation

Do not activate this lens silently. Use it only when the user asks for personal
preference, PI preference, "my taste", "my style", or "remember my preference".

Suggested commands:

```text
Use my User PI Preference Lens to choose between these two framings.
```

```text
Update my personal preference lens from this feedback.
```

```text
Apply my preference lens, but let RAG and evidence override it.
```

## Output behavior

When active, label its role explicitly:

| Decision | User preference | Evidence constraint | Final action |
|---|---|---|---|
|  |  |  |  |

If user preference conflicts with evidence, write:

> Your preference points toward X, but the evidence constraint requires Y.

## Preference categories

| Category | Examples |
|---|---|
| Claim ambition | conservative / balanced / ambitious |
| Mechanism tolerance | only mechanism-grade evidence / allow bounded model |
| Journal taste | Nature-family / JACS / Angew / Advanced Materials / specialist |
| Writing voice | senior PI, concise, restrained, high-signal, less AI-like |
| Figure taste | dense proof path, clean schematic, fewer panels, more controls |
| RAG preference | cite only direct sources / allow adjacent background / always adversarial |
| Rebuttal tone | firm, conciliatory, action-first, minimal emotion |
| No-go habits | avoid hype, avoid vague sustainability, avoid tool-centered AI claims |

## Update workflow

1. Capture the preference in the user's words.
2. Convert it into a decision rule.
3. Add a use boundary.
4. Add a conflict rule: what happens when evidence disagrees?
5. Store it in `user-preferences/`.

## Preference rule quality

Weak:

> I like ambitious writing.

Useful:

> Prefer ambitious titles only when the central claim has a direct evidence
> owner in the main figures; otherwise keep the title mechanism/platform-level
> and move ambition into the cover letter.

## Council behavior

The User PI Preference Lens can join a council as a preference role, but its
signature means "matches user's preference", not "external expert agrees".

In Council Consensus Card:

- `signed by User PI Preference Lens` means the decision matches the user's
  stated preference;
- it must be separated from source-backed mentor lens signatures;
- it can be overruled by RAG evidence, reviewer risk or missing controls.

## Guardrails

- Do not present user preference as literature evidence.
- Do not label it as one of the eight source-backed mentor lenses.
- Do not let it silently alter factual claims.
- Do not store sensitive personal information beyond research/workflow
  preferences.
- Keep it private; strip it from public releases.
