# Merge paginated API pages and filter by status

When an API has too many results to send at once, it splits them across **pages** — and those pages can arrive out of order, sometimes repeating a task that appeared on an earlier page. You'll write `merge_pages(pages, status=None)` to stitch the pages back into one clean, de-duplicated, sorted list. Each page looks like `{'page': int, 'next': bool, 'results': [task, ...]}`.

### Worked example
```python
merge_pages([{'page':1,'results':[{'id':2,'status':'done'},{'id':1,'status':'todo'}]}])
# -> [{'id': 1, 'status': 'todo'}, {'id': 2, 'status': 'done'}]
```
The single page's two tasks are pulled out and returned sorted by `id`, so the task with `id` 1 comes before `id` 2.

### What to build
Write `merge_pages(pages, status=None)` that:
- Processes pages in ascending `page` order (don't trust the incoming order).
- Flattens every page's `results` into one list, **de-duplicating by task `id`** — the first time you see an `id` wins.
- If `status` is given (not `None`), keeps only tasks whose `status` equals it.
- Returns the resulting list sorted ascending by `id`. An empty `pages` list yields `[]`.

### Concepts you'll use
`sorted(..., key=...)`, looping over nested lists, tracking seen ids with a `set`, optional filtering, building a result list.

### How to solve this
**Define:** `merge_pages(pages, status=None)` and the helper `pages_fixture()` (given in the starter).

**What the grader runs:**
- `merge_pages(pages_fixture())` -> ids 1..5, each unique, sorted (the duplicate id 4 across pages appears once)
- `merge_pages(pages_fixture(), 'todo')` -> only the todo tasks (ids 1, 3, 5)
- `merge_pages([], 'todo')` -> `[]`

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
def merge_pages(pages, status=None)
def pages_fixture()
```

> **Runtime:** your code is graded on **Python 3.11**, the same version as the Python in your editor. Modern syntax is fine — `match` statements and `int | None` unions in annotations both work.
>
> **`return` your answer — never `print` it.** A printed value is not a returned value, and the
> grader only reads what you return.

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
