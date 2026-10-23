# TaskFlow Assignment (Easy) — Backlog Status Counts

## Backlog status snapshot

TaskFlow's product lead wants to see how the backlog breaks down by **status** — how many tasks are todo, done, and so on. You'll build a small count using **pandas**, the go-to library for working with tables of data (a table is called a `DataFrame`).

### Worked example
```python
status_counts([{'status':'todo'},{'status':'done'},{'status':'todo'}])
# {'done': 1, 'todo': 2}
```
Three rows go in; two are `'todo'` and one is `'done'`, so each status maps to its count.

### What to build
Write `status_counts(records)` where `records` is a **list of task dicts** (each has at least a `status` key). The autograder passes the data in directly as a Python literal — **there is no `tasks.csv` and you must not read any file**.

1. Build a DataFrame with `pd.DataFrame(records)` (each dict becomes a row).
2. Count the `status` column — `df['status'].value_counts()` gives status → count.
3. Return a plain `dict` `{status: count}` with **int** counts (convert each count with `int(...)` so no numpy ints leak out). Return `{}` for an empty list.

### Concepts you'll use
pandas `DataFrame`, selecting a column, `value_counts()`, converting to a plain `dict` with `int` values.

<!--LL-CONTRACT-->
### How to solve this
Write your Python **directly in the code editor** on the right, then click **Run Tests**. There is a single editor — you do **not** create or name any file; just define the function(s) below.

**Define:**
- `status_counts(records)`

**What the grader runs** (each value is scored **separately**, so a partly-correct answer still earns marks):
- `status_counts([{'status':'todo'},{'status':'done'},{'status':'todo'}])['done']`  →  `1`
- `status_counts([{'status':'todo'},{'status':'done'},{'status':'todo'}])['todo']`  →  `2`
- `status_counts([{'status':'in_progress'}])`  →  `{"in_progress": 1}`

Return the exact value shown (a list stays a list; round numbers only if the task says so). **`return` the value — do not `print` it.**

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
