---
name: compassbear-wechat-distiller
description: Distill long WeChat chat records exported as notes/text chunks into CompassBear knowledge artifacts: decisions, claims, evidence gaps, action items, User PI Preference updates, mentor-lens candidates and source-note leads.
---

# CompassBear WeChat Distiller

## Inherits from CompassBear

Use the CompassBear north-star: **if forced to choose between sounding impressive and being defensible, choose defensible.**

This skill turns messy chat history into structured research memory. It does not
access or modify the WeChat database.

## Trigger calibration

Trigger on: 微信聊天记录, 微信笔记, 合并转发, chat distillation, distill WeChat,
long chat, 聊天蒸馏, 知识管理, 从聊天记录提炼, 100条上限.

## Input reality

WeChat's forward/notes workflow may force the user to create multiple chunks.
Accept:

- pasted text chunks;
- `.txt` / `.md` files;
- a folder of chunk files;
- WeChat note text copied into the conversation.

Do not require the user to manually reassemble the chunks.

## Output-first contract

Return structured research memory:

- conversation topics;
- project decisions;
- claim candidates;
- evidence gaps;
- figure ideas;
- action items;
- User PI Preference updates;
- mentor-lens candidate rules;
- source-note leads;
- unresolved questions.

## Local command

```bash
python scripts/cb.py wechat --input "path/to/chunks" --project "<project>" --topic "<topic>"
```

Direct helper:

```bash
python scripts/wechat_distill.py --input "path/to/chunks"
```

Outputs land in:

```text
outputs/wechat-distill/
```

## Distillation workflow

1. Merge chunks and remove exact duplicate lines.
2. Preserve chunk boundaries so context is auditable.
3. Segment by topic.
4. Extract only content that changes research decisions or memory:
   - decisions;
   - claims;
   - evidence;
   - experiments;
   - figures;
   - writing preferences;
   - source/literature leads.
5. Convert output into the right CompassBear artifact:
   - Claim Passport row;
   - User PI Preference Lens update;
   - mentor-lens candidate rule;
   - source-note candidate;
   - action list.

## Default output

| Topic | Decision / insight | Evidence in chat | Risk | Next action |
|---|---|---|---|---|

Then:

1. Claim Passport candidates
2. User PI Preference updates
3. Mentor-lens candidates
4. Source-note leads
5. Action list
6. Unresolved questions

## Guardrails

- Do not treat chat opinion as literature evidence.
- Do not promote a mentor-lens rule unless it has source notes.
- Do not store private chat content in public examples.
- Do not infer private intent beyond the chat text.
- Do not overwrite user preferences silently; propose updates first.

## Reference routing

- User preference: `../../references/user-preference-lens.md`
- Mentor lens evolution: `../../references/mentor-lens-evolution.md`
- Claim Passport: `../../references/claim-passport.md`
- First-principles iteration: `../../references/first-principles-iteration.md`
