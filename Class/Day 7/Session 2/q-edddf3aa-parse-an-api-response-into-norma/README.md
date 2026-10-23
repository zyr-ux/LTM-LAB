# Parse an API response into normalised TaskFlow tasks

You've just called a TaskFlow partner API and it handed back a JSON body already parsed into a Python `dict` (imagine `resp.json()` ran for you). Real-world API data is messy — wrong casing, stray spaces, out-of-range numbers — so before your app trusts it, you'll write `extract_tasks(response)` to check the envelope and **clean up** each task row.

### Worked example
```python
extract_tasks({'status':'ok','data':[{'id':7,'title':' Hi ','status':'DONE','priority':0}]})
# -> [{'id': 7, 'title': 'Hi', 'status': 'done', 'priority': 1}]
```
The envelope's `status` is `'ok'`, so processing continues. The one row is normalised: the title is trimmed (`' Hi '` → `'Hi'`), the status is lower-cased (`'DONE'` → `'done'`), and the priority `0` is clamped up into the allowed 1..5 range, becoming `1`.

### What to build
Write `extract_tasks(response)` that applies these rules in order:
- If `response` isn't a dict, or `response['status'] != 'ok'`, return `[]`.
- The task rows live in `response['data']` (which may be missing or empty).
- Skip any row whose `id` is `None`/missing. Otherwise cast `id` to `int`.
- `title`: take `row['title']` (default `''`), then strip surrounding whitespace.
- `status`: lower-case and strip it; if it isn't one of `todo`/`in_progress`/`review`/`done`, use `todo`.
- `priority`: cast to `int` (default `3`); if it can't be cast, use `3`; then clamp into the range 1..5.
- Return the list of `{id,title,status,priority}` dicts sorted ascending by `id`.

### Concepts you'll use
Type checks with `isinstance`, `dict.get` with defaults, `str.strip` / `str.lower`, `try/except` around `int(...)`, clamping with `min`/`max`, `sorted(..., key=...)`.

### How to solve this
**Define:** `extract_tasks(response)` and the helper `api_fixture()` (given in the starter) that returns the sample response used by some tests.

**What the grader runs:**
- `extract_tasks(api_fixture())` -> the 3 cleaned tasks sorted by id (priority 9 clamps to 5, `'2'` casts to 2)
- `extract_tasks({'status': 'error', 'data': [{'id': 1, 'title': 'x'}]})` -> `[]`
- `extract_tasks({'status': 'ok', 'data': [{'id': 8, 'title': 'High', 'status': 'todo', 'priority': 12}]})` -> priority clamped to 5

<!--LL-ATTEMPT-->
---

## How to attempt this

1. Open the assignment from your course page. Write your answer **in the code editor on the
   right** — there is no file to create and nothing to name.
2. Click **Run Tests** to grade it. The visible tests run first so you can see where you stand.
3. Read any failure carefully: it shows the **input**, what was **expected**, and what your code
   **actually returned**. That three-way comparison is usually enough to find the bug.
4. Re-run as often as you like. Each value is scored separately, so a partly-correct answer still
   earns marks — submit something rather than nothing.
5. When you are satisfied, **Submit**.

### The exact shape to define

```python
def extract_tasks(response)
def api_fixture()
```

> **Runtime:** your code is graded on **Python 3.11**, the same version as the Python in your editor. Modern syntax is fine — `match` statements and `int | None` unions in annotations both work.
>
> **`return` your answer — never `print` it.** A printed value is not a returned value, and the
> grader only reads what you return.

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
