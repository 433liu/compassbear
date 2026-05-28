# Visual Generation Boundary

Use image generation tools, including GPT Image or the local `imagegen` skill
when available, only for visual assets that do not pretend to be scientific
measurements.

## Allowed uses

- graphical abstract concept art;
- cover-art style visual explorations;
- iconography and visual metaphors;
- background textures for presentations;
- schematic mood boards;
- non-data illustration of a workflow, material class, device concept or
  application scene.

## Not allowed

- generating spectra, microscopy, gels, plots or other data-looking evidence;
- fabricating experimental images;
- replacing missing controls or replicates;
- producing realistic panels that could be mistaken for measured results;
- creating journal figures that blur the line between illustration and data.

## Workflow

1. Decide whether the requested image is data, schematic, or illustration.
2. If data: do not generate. Ask for real data or design the figure structure.
3. If schematic: prefer editable vector or code-native figure logic.
4. If illustration: call GPT Image / `imagegen` if available, then label it as
   illustrative or conceptual in the deliverable.
5. Keep final scientific claims tied to real evidence, not generated imagery.

## Prompting rule

Prompts for generated scientific visuals should specify:

- "conceptual illustration" or "graphical abstract style";
- no fake axes, labels, measurements, micrographs or spectra;
- visual hierarchy and subject;
- journal-safe, clean composition;
- transparent or simple background when the asset will be composited.
