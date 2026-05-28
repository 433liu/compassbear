# Figure Production Bridge

Use this protocol when moving from CompassBear figure logic to actual production
assets such as matplotlib plots, SVG schematics, PowerPoint figures or generated
concept art.

The goal is to make figure production more concrete while preserving the rule:
figures are arguments, not decoration.

## Figure production contract

Every figure-production request should return two layers:

1. **Scientific logic layer**
   - figure-level claim;
   - panel-to-claim map;
   - evidence owner;
   - main/Extended/SI placement;
   - reviewer risk.

2. **Production specification layer**
   - asset type;
   - required data inputs;
   - visual encoding;
   - layout;
   - labels and units;
   - export format;
   - what must not be generated.

## Asset routing

| Asset type | Use when | Tool direction |
|---|---|---|
| measured plot | real numeric data exist | matplotlib / spreadsheet chart / existing plotting code |
| schematic | conceptual mechanism or workflow | SVG / PowerPoint / vector editor |
| panel layout | arranging existing panels | PPT / SVG / figure assembly |
| graphical abstract | conceptual visual | imagegen/GPT Image only if non-data illustration |
| microscopy/spectra/data-looking image | real experiment only | do not generate; request real data |

## Production spec template

| Panel | Claim | Data/input required | Visual encoding | Output asset | Risk |
|---|---|---|---|---|---|
| a |  |  |  | plot / schematic / image / layout |  |

Then provide:

- proposed layout;
- color/label rules;
- caption skeleton;
- data files needed;
- forbidden generated elements.

## Matplotlib/SVG handoff

When the user asks for actual figure code:

- require or infer the data table shape;
- define axes, units, normalization and error bars;
- generate code only for real numeric data or clearly fake demo placeholders;
- label placeholder outputs as placeholders;
- avoid fabricating values.

## Graphical abstract handoff

When the user asks for generated visuals:

- use `skills/compassbear-figure-strategy/references/visual-generation-boundary.md`;
- specify "conceptual illustration";
- exclude fake axes, spectra, microscopy, plots or measurement labels;
- keep final manuscript claims tied to real evidence.

## Review checklist

- Does each panel defend a claim?
- Is every data-looking element backed by real data?
- Are control/baseline panels visible where the claim depends on them?
- Does visual hierarchy match evidence hierarchy?
- Would a reviewer accuse the figure of hiding a limitation?
