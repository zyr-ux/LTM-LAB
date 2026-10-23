# TaskFlow Assignment (Medium) — Parse a TaskFlow CSV export into typed task records

Someone exported TaskFlow tasks to a CSV file. You'll read that text and turn each row into a clean Python dict with the right types (numbers as ints, the done flag as a real boolean).

## Worked example

```python
parse_tasks_csv('id,title,points,done\n1,Fix login,3,true')
# -> [{'id': 1, 'title': 'Fix login', 'points': 3, 'done': True}]
```

The first line is the header. The one data row becomes a dict: `id` parsed to the int `1`, `title` stripped to `'Fix login'`, `points` to `3`, and `done` to `True` because the cell is `"true"`.

## What to build

- `parse_tasks_csv(csv_text)` where `csv_text` is a CSV string with header `id,title,points,done`.
- Parse it with the `csv` module: wrap the text in `io.StringIO(csv_text)` and feed that to `csv.DictReader`, which yields one dict per row keyed by the header names.
- Return a list of dicts, one per data row, with:
  - `id`: the `id` column as an `int`.
  - `title`: the `title` column with surrounding whitespace stripped.
  - `points`: the `points` column as an `int`, or `0` when blank/empty.
  - `done`: `True` only when the `done` column equals `"true"` case-insensitively (after stripping); otherwise `False`.
- If `csv_text` is empty or only whitespace, return `[]`.
- A header row with no data rows returns `[]`.
- Skip any data row whose `id` cell is blank.

Use only the `csv` and `io` modules. Return plain dicts.

## Concepts you'll use

`csv.DictReader`, `io.StringIO`, `str.strip()`, `int()`, `str.lower()`, building a list of dicts.

<!--LL-CONTRACT-->
### How to solve this
Write your Python **directly in the code editor** on the right, then click **Run Tests**. There is a single editor — you do **not** create or name any file; just define the function(s) below.

**Define:**
- `parse_tasks_csv(csv_text)`

**What the grader runs** (each value is scored **separately**, so a partly-correct answer still earns marks):
- `len(parse_tasks_csv('id,title,points,done\n1,Fix login,3,true'))`  →  `1`
- `parse_tasks_csv('id,title,points,done\n1,Fix login,3,true')[0]['id']`  →  `1`
- `parse_tasks_csv('id,title,points,done\n1,Fix login,3,true')[0]['title']`  →  `Fix login`

Return the exact value shown (a list stays a list; round numbers only if the task says so). **`return` the value — do not `print` it.**

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
