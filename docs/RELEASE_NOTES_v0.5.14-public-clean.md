# compass-bear v0.5.14-public

This is a cleaner public release of CompassBear Academic Compass. It removes the project-specific example claims and domain-specific test prompts that were present in the earlier public-share package.

## What CompassBear is

CompassBear is a claim-first research workflow skill for Codex / Claude Code. It helps researchers turn scattered data, mechanisms, figures and applications into defensible scientific manuscripts, proposals, cover letters, rebuttals and patent-style claim structures.

It is not a phrase-polishing tool. It asks:

> What must the reader believe, and what evidence makes that belief unavoidable?

## Why it is different

Typical academic AI workflows often focus on polishing prose, summarizing papers, formatting documents or simulating expert comments. CompassBear is built around the layer before polishing: whether the scientific story is defensible.

Strengths:

- starts from the central claim rather than sentence style;
- links claims to evidence owners, figures and reviewer risks;
- designs figures as arguments rather than decorations;
- gives demotion language when evidence is suggestive but not decisive;
- separates literature support, project-specific proof and unsupported analogy;
- supports local source-backed expert lenses without impersonating real people.

Trade-offs:

- heavier than a quick writing prompt;
- needs real evidence from the user for high-stakes claims;
- cannot replace literature reading, experimental validation or statistical review;
- local expert lenses are only as good as the source notes used to build them.

## Sanitized / not included

- No `.env`.
- No real API keys.
- No generated outputs.
- No personal project rosters or source notes.
- No personal mentor lens cards.
- No project-specific public examples that reveal the user's manuscript direction.

## Install

Download and unzip the package, then install the extracted folder as `compass-bear`.

```text
$compass-bear
```

See `INSTALL.md` and `USAGE.md` after unzipping.

## Release asset

Attach:

`compass-bear-v0.5.14-public-clean.zip`

SHA256:

`415F67C02009087E70D56DFE764717A06C37F775D2291DD340965927021B7DDC`
