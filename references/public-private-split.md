# Public / Private Split

CompassBear should stay useful as a public research workflow while preserving a
private layer for project-specific mentor lenses, unpublished notes and personal
reading records.

## Public layer

The public layer may include:

- root `SKILL.md`;
- sub-skill `SKILL.md` files;
- general references and protocols;
- fictional, anonymized or synthetic examples;
- generic role libraries;
- scripts that do not reveal private source packs or project details.

The public layer must not include:

- named private mentor cards;
- internal project strategy memos;
- unpublished manuscript text;
- private reviewer guesses;
- confidential source notes;
- user-specific source-pack exports;
- environment files or API keys.

## Private layer

The private layer may include:

- `expert-lenses/`;
- `source-packs/`;
- `project-rosters/`;
- `council-notes/`;
- project-specific examples and private regression snapshots.

Private files can be opinionated and project-aware, but every named lens still
needs source-grounded, non-impersonating rules.

## Release rule

Before public release:

1. Remove or redact `private/`.
2. Remove generated RAG outputs that contain user projects.
3. Replace real project examples with anonymized examples.
4. Check README and changelog for named private details.
5. Confirm no `.env` or access tokens are packaged.

## Private-to-public promotion

A private pattern can be promoted to the public layer only if it is generalized.

Allowed:

- "mechanism claim demotion ladder";
- "AI-discovery claim passport";
- "figure removal test";
- "source-backed lens protocol".

Not allowed:

- "Professor X always wants...";
- project-specific title strategy;
- unpublished data-dependent figure placement;
- source notes that reveal private reading annotations.

## Documentation rule

When adding a new capability, decide whether it belongs to:

- **public protocol**: reusable across users and fields;
- **private configuration**: user-specific lens, project or source basis;
- **example**: anonymized demonstration;
- **test**: checker that guards the behavior.
