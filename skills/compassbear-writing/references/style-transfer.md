# Style Transfer

Use this reference when the user asks to convert text toward a journal style,
article type, audience or disciplinary register.

Style transfer means changing framing, emphasis, section rhythm and claim
calibration. It does not mean imitating stock phrases or hiding weak evidence.

## Workflow

1. Identify source text type: title, abstract, introduction, Results, Discussion,
   cover letter, figure caption or rebuttal.
2. Identify target: journal, journal family, article type or audience.
3. Check the load-bearing claim and evidence level.
4. Select the target profile from `../../../references/journal-style-profiles.md`
   when available.
5. Rewrite in two passes:
   - **positioning pass**: change hook, audience and claim hierarchy;
   - **voice pass**: tighten rhythm, verbs and transitions.
6. Return a claim-safety note if the target style would tempt overclaiming.

## Default output

1. **Converted text**
2. **What changed**
3. **Claim-safety notes**
4. **Alternative target suggestion** if the requested journal fit is weak

## Target controls

Ask or infer:

- target journal: JACS / Angew / Advanced Materials / Nature-family / other;
- article type: Communication / Article / Research Article / Review /
  Perspective / cover letter;
- desired intensity: conservative / standard / ambitious;
- allowed scope: title-level, abstract-level, Results-level or Discussion-level.

## Rewrite rules

- Preserve data, numbers, mechanisms and limitations.
- Strengthen only the framing, not the evidence.
- Move unsupported journal-style claims into cautious wording.
- Prefer specific scientific nouns and verbs over prestige language.
- If the target journal is a poor fit, give a better framing route instead of
  forcing the prose.

## Common commands

```text
Convert this abstract toward JACS style, but keep mechanism claims bounded.
```

```text
Rewrite this opening for Angew Communication style: compact, urgent, chemistry-first.
```

```text
Convert this abstract toward Advanced Materials: emphasize functional material design and performance, not just synthesis.
```

```text
Compare JACS vs Angew vs Advanced Materials fit for this story, then rewrite the title and abstract opening for the best two.
```
