# CompassBear Research Council

A role-based discussion skill for research direction, article framing and project strategy.

It is designed for moments such as:

- "我们这个课题到底应该主打机制、材料平台还是应用？"
- "帮我模拟几个教授互相辩论一下文章思路。"
- "这个故事会不会被桌拒？"
- "这个 claim 应该升主线还是降到 SI？"

## What it returns

- council roster
- debate summary
- recommended paper angle
- claim hierarchy
- evidence gaps
- reviewer-risk forecast
- next action plan

## Key principle

The council is a reasoning device, not a role-play performance. It should produce decisions, not theatrical dialogue.

## Named professor policy

If the user names real professors, treat the names as public expertise lenses only. Do not imitate private voice, fabricate opinions or claim that the real person would endorse any view.

## Local named-lens mode

This public package ships without personal mentor lenses. If a user wants local named-lens behavior, they should create their own source notes and lens cards from public materials, using the templates in `templates/`.

Typical local workflow:

1. Add source notes in `source-packs/`.
2. Build a lens card from `templates/expert-lens-template.md`.
3. Assemble a project roster from `templates/project-roster-template.md`.
4. Run the council and request a decision memo.

