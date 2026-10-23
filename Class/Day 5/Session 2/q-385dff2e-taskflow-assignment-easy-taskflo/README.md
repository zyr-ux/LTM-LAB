# TaskFlow Assignment (Easy) — TaskFlow: Fill Missing Task Status

# TaskFlow -- Fill Missing Task Status

The TaskFlow importer just loaded a batch of task rows from an old spreadsheet,
and many rows have a blank or missing `status`. Product wants every task to
carry a status so the board never shows an empty column — any missing status
should default to `"todo"`. You'll fix this with **pandas** missing-data
handling.

In pandas, "missing" is represented as `NaN`. `fillna("todo")` replaces every
missing value with `"todo"` in one step; the trick is to first turn
blanks/whitespace into NaN so they count as missing too.

### Worked example
```python
fill_missing_status([{'id':1,'status':'done'},{'id':2,'status':''}])
# -> ['done', 'todo']
```
Row 1 already has `'done'`, kept as-is. Row 2's status is a blank string,
treated as missing and filled with `'todo'`.

### What to build
Implement `fill_missing_status(records)`:

- `records` is a `list[dict]`, one dict per task row.
- A status is **missing** when it is `None`, `NaN`, an **absent** `"status"`
  key, or a **blank / whitespace-only** string.
- Return the list of statuses (row order preserved) with missing ones filled
  as `"todo"`. Present values are returned unchanged (do not lowercase them).

**Concept:** pandas missing-data handling (`fillna`, treating blanks as NA).

<!--LL-CONTRACT-->
### How to solve this
Write your Python **directly in the code editor** on the right, then click **Run Tests**. There is a single editor — you do **not** create or name any file; just define the function(s) below.

**Define:**
- `fill_missing_status(records)`

**What the grader runs** (each value is scored **separately**, so a partly-correct answer still earns marks):
- `len(fill_missing_status([{'id':1,'status':'done'},{'id':2,'status':'todo'}]))`  →  `2`
- `fill_missing_status([{'id':1,'status':'done'},{'id':2,'status':'todo'}])[0]`  →  `done`
- `fill_missing_status([{'id':1,'status':'done'},{'id':2,'status':'todo'}])[1]`  →  `todo`

Return the exact value shown (a list stays a list; round numbers only if the task says so). **`return` the value — do not `print` it.**

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
