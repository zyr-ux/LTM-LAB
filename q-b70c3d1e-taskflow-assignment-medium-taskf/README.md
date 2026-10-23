# TaskFlow Assignment (Medium) — TaskFlow: Tidy the Messy Task Rows

# TaskFlow -- Tidy the Messy Task Rows

A batch of task rows was exported from a legacy tool (`messy_tasks.csv`) and
it's full of noise: padded titles, inconsistent status casing, estimate hours
stored as strings (some garbage), and duplicate rows for the same task id.
You'll turn these raw rows into clean, typed records with **pandas** (plus a
few string methods).

### Worked example
```python
clean_tasks([{'id':2,'title':'Write specs','status':'Todo','estimate_hours':'3'},
             {'id':1,'title':'  Fix bug ','status':'DONE','estimate_hours':'2.5'}])[0]
# {'id': 1, 'title': 'Fix bug', 'status': 'done', 'estimate_hours': 2.5}
```
Rows are sorted by `id`, so id `1` comes first. Its title is stripped of
spaces, its status lowercased, and the estimate string `'2.5'` becomes the
float `2.5`.

### What to build
Implement `clean_tasks(records)`. Each row dict has keys
`id, title, status, estimate_hours`. Produce a list of tidy dicts **sorted
ascending by id**, where:

1. `title` is stripped of surrounding whitespace (str methods like `.strip()`).
2. `status` is trimmed and lowercased (`.strip().lower()`).
3. `estimate_hours` is coerced to `float`; non-numeric or missing values
   become `0.0`; round to 2 decimals (use `pd.to_numeric(..., errors='coerce')`).
4. Duplicate `id`s collapse to a single row, **keeping the first occurrence**
   (`drop_duplicates`).

Return native python types (`int` id, `str`, `float`). An empty input returns
`[]`.

The batch of rows is passed directly to your function as a Python list literal
(the argument `records`) -- there are no file reads; `messy_tasks.csv` is only
the backstory for where this noisy data came from.

**Concepts:** str methods, dtype coercion (`pd.to_numeric`), dedup
(`drop_duplicates`).

<!--LL-CONTRACT-->
### How to solve this
Write your Python **directly in the code editor** on the right, then click **Run Tests**. There is a single editor — you do **not** create or name any file; just define the function(s) below.

**Define:**
- `clean_tasks(records)`

**What the grader runs** (each value is scored **separately**, so a partly-correct answer still earns marks):
- `len(clean_tasks([{'id':2,'title':'Write specs','status':'Todo','estimate_hours':'3'},{'id':1,'title':'  Fix bug ','status':'DONE','estimate_hours':'2.5'}]))`  →  `2`
- `clean_tasks([{'id':2,'title':'Write specs','status':'Todo','estimate_hours':'3'},{'id':1,'title':'  Fix bug ','status':'DONE','estimate_hours':'2.5'}])[0]['id']`  →  `1`
- `clean_tasks([{'id':2,'title':'Write specs','status':'Todo','estimate_hours':'3'},{'id':1,'title':'  Fix bug ','status':'DONE','estimate_hours':'2.5'}])[0]['title']`  →  `Fix bug`

Return the exact value shown (a list stays a list; round numbers only if the task says so). **`return` the value — do not `print` it.**

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
