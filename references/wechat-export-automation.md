# WeChat Export Automation Boundary

Use this reference when the user wants a more automated way to collect long
WeChat conversations for CompassBear distillation.

## Reality

WeChat Desktop does not provide a stable public API for exporting arbitrary chat
ranges as structured text. Full automation through the UI is possible but
fragile because message selection, scrolling and context menus depend on screen
layout, WeChat version, DPI and chat content.

## Recommended automation ladder

| Level | What is automated | Risk | Recommended? |
|---|---|---|---|
| A. Clipboard capture | user copies chunks; script saves each chunk | low | yes |
| B. Folder distillation | user exports notes/text files; script merges/dedupes | low | yes |
| C. Assisted UI macro | script opens WeChat/searches contact; user selects range | medium | possible after calibration |
| D. Full UI selection/export | script clicks/scrolls/selects/exports | high | only after explicit screen calibration |
| E. Direct WeChat DB read/write | reads/decrypts/modifies WeChat data | high | not part of CompassBear |

## Safe default

Use:

```bash
python scripts/cb.py wechat-capture --watch
```

Then, in WeChat:

1. Open the target chat.
2. Select up to 100 messages.
3. Merge forward / collect / convert to note as usual.
4. Copy the note text.
5. The watcher saves each copied chunk automatically.
6. Stop the watcher with Ctrl+C.
7. Distill:

```bash
python scripts/cb.py wechat --input outputs/wechat-capture --project "<project>" --topic "<topic>"
```

## Assisted UI macro policy

If building a UI macro later, it must:

- ask for the contact name and date/range;
- open/search WeChat but pause before destructive or send-like actions;
- never send messages;
- never delete, move, or modify chat records;
- never write the WeChat database;
- allow the user to review before export;
- save outputs only to the CompassBear project.

## Calibrated UI macro

For long chats where clipboard capture is still too manual, use the guarded macro
runner:

```bash
python scripts/cb.py wechat-ui init
python scripts/cb.py wechat-ui pos
python scripts/cb.py wechat-ui run --loops 10 --i-understand-ui-automation-risk
```

Workflow:

1. Run `wechat-ui init` to create `templates/wechat-ui-macro.example.json`.
2. Use `wechat-ui pos` to capture mouse coordinates for your WeChat window.
3. Edit the macro actions: drag/click/hotkey/scroll/capture_clipboard.
4. Test with `--loops 1`.
5. Only then increase loops.
6. Distill captured chunks with `cb.py wechat`.

The macro runner can replay:

- click / right_click / double_click;
- drag;
- scroll;
- key / hotkey;
- wait / prompt;
- capture_clipboard.

It cannot understand WeChat semantics. It just repeats configured UI actions.
Bad coordinates can click the wrong place, so use a small test first.

## Guardrails

- Do not bypass WeChat security or decrypt private databases.
- Do not scrape chats without the user's explicit instruction.
- Do not store private chat content in public examples.
- Treat chat records as private source material, not literature evidence.
- Run UI macros first with `--loops 1`; scale only after verifying output.
