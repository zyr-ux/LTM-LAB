# TaskFlow Assignment (Medium) — Paginate the Event Stream

## Paginate & First-Match over an Event Stream

TaskFlow streams task events, sometimes far too many to hold in memory at once. You'll build two small lazy helpers: one that chops a stream into fixed-size pages, and one that finds the first event with a given status.

"Lazy" means you pull items one at a time instead of loading everything up front. A **generator** (a function using `yield`) is how Python does this.

### Worked example
```python
list(paginate([1,2,3,4,5], 2))            # [[1, 2], [3, 4], [5]]
find_first([{'id':1,'status':'todo'}], 'todo')  # 1
```
`paginate` walks the five numbers and emits pages of size 2 — the last page holds the single leftover `5`. `find_first` scans events and returns the `id` of the first one whose status matches (`'todo'` → id `1`).

### What to build

**1. `paginate(items, size)`** — a **generator** that yields successive lists ("pages") of up to `size` items from any iterable `items`. The final page may be shorter. If `size <= 0`, yield nothing. Keep it lazy: call `iter(items)` once, then repeatedly grab a slice with `itertools.islice(it, size)` and yield it as a `list` until the slice comes back empty.

**2. `find_first(events, status)`** — return the `id` of the **first** event whose `status` equals the given value, or `None` if none match. Use `next(<generator expression>, None)` — the second argument is the default returned when nothing is found. Events may be missing a `status` key; treat those as non-matching (use `e.get('status')`).

### Concepts you'll use
Generators, `yield`, `iter` + `itertools.islice`, generator expressions, `next(..., default)`.

<!--LL-CONTRACT-->
### How to solve this
Write your Python **directly in the code editor** on the right, then click **Run Tests**. There is a single editor — you do **not** create or name any file; just define the function(s) below.

**Define:**
- `paginate(items, size)`
- `find_first(events, status)`

**What the grader runs** (each value is scored **separately**, so a partly-correct answer still earns marks):
- `len(list(paginate([1,2,3,4,5], 2)))`  →  `3`
- `list(paginate([1,2,3,4,5], 2))[0]`  →  `[1, 2]`
- `list(paginate([1,2,3,4,5], 2))[1]`  →  `[3, 4]`

Return the exact value shown (a list stays a list; round numbers only if the task says so). **`return` the value — do not `print` it.**

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
