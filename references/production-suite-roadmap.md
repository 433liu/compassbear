# Production Suite Roadmap

CompassBear should stay a claim-first judgment layer while exposing enough structure to be useful as a public project.

## Priority Upgrades

| Shortboard | Public-safe upgrade |
|---|---|
| command maturity | small command wrappers that route to stable protocols |
| literature friction | chat-native RAG first, heavier retrieval only as an optional external bridge |
| figure production | figure logic specs that can hand off to drawing or plotting tools |
| examples | synthetic prompts, anonymized output shapes and benchmark cases |
| packaging | installable repository root with no local paths or private materials |

## Release Gates

A public release should pass:

- install instructions contain no machine-specific paths;
- root README explains the value in the first screen;
- examples are synthetic or anonymized;
- no API keys, local databases, personal lenses, generated outputs or unpublished project notes;
- eval files parse cleanly;
- sensitive-term scan returns no actionable hits.
