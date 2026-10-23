# TaskFlow Assignment (Easy) — Roll TaskFlow tasks up into a JSON status report

TaskFlow wants a quick tally of how many tasks sit in each status, saved as text so it can be stored or sent over the wire. You'll count the statuses and hand back a JSON string.

## Worked example

```python
status_counts_json([{'status': 'todo'}, {'status': 'todo'}, {'status': 'done'}])
# -> '{"done": 1, "todo": 2}'
```

Two tasks are `todo` and one is `done`, so the counts are `{'todo': 2, 'done': 1}`. `json.dumps(..., sort_keys=True)` turns that dict into a string with keys in sorted order (`done` before `todo`), so the result is always the same.

## What to build

- `status_counts_json(tasks)` where `tasks` is a list of task dicts (or `None`).
- Count how many tasks have each `status` value. A task with a missing or empty `status` counts under `'unknown'`.
- Return the count dict as a JSON string via `json.dumps(counts, sort_keys=True)` — `sort_keys=True` keeps the key order deterministic.
- If `tasks` is `None`, return the string `"{}"` (an empty JSON object).

Use only the `json` module. The returned value must be a plain string (not a dict).

## Concepts you'll use

The `json` module (`json.dumps`), counting with a dict, `dict.get()` for defaults, checking for `None`.

<!--LL-CONTRACT-->
### How to solve this
Write your Python **directly in the code editor** on the right, then click **Run Tests**. There is a single editor — you do **not** create or name any file; just define the function(s) below.

**Define:**
- `status_counts_json(tasks)`

**What the grader runs** (each value is scored **separately**, so a partly-correct answer still earns marks):
- `status_counts_json([{'status': 'todo'}, {'status': 'todo'}, {'status': 'done'}])`  →  `{"done": 1, "todo": 2}`
- `status_counts_json([])`  →  `{}`
- `status_counts_json([{'status': 'done'}, {'status': 'done'}])`  →  `{"done": 2}`

Return the exact value shown (a list stays a list; round numbers only if the task says so). **`return` the value — do not `print` it.**

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
