# CompassBear Public Evals

These lightweight evals check public routing and guardrails.

Run a JSONL parse check:

```bash
python -c "import json, pathlib; [json.loads(line) for line in pathlib.Path('evals/cases.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]; print('OK')"
```

Use the prompts manually to verify that CompassBear demotes unsupported claims, routes figure tasks to figure strategy and treats literature search leads as provisional.
