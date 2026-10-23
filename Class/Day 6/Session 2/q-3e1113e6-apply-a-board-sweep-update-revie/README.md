# Apply a board sweep: UPDATE reviews to done, DELETE low-priority tasks

TaskFlow runs a nightly "board sweep": every task still in `review` is promoted to `done`, and any low-priority task is deleted as noise. You'll write the sweep as parameterised `UPDATE` and `DELETE` statements and report how many rows each one touched — SQLite hands you that count for free via `cursor.rowcount` after a write.

`rows` is a list of dicts with keys `title`, `status`, `priority`.

### Worked example
```python
rows = [
  {'title': 'A', 'status': 'review', 'priority': 5},
  {'title': 'B', 'status': 'review', 'priority': 1},
  {'title': 'C', 'status': 'todo',   'priority': 2},
  {'title': 'D', 'status': 'done',   'priority': 4},
]
apply_changes(rows, 3)  ->  {'updated': 2, 'deleted': 2}
# A and B were in review -> updated=2; then B(1) and C(2) are below 3 -> deleted=2
```
First the UPDATE flips both `review` rows (A and B) to `done`, so `rowcount` is 2. Then the DELETE removes every row with `priority < 3` — that's B (1) and C (2) — so `rowcount` is 2 again. Order matters: update first, delete second.

### What to build
- Write `apply_changes(rows, min_priority)` and load the rows into an in-memory `task` table.
- **First** run a parameterised `UPDATE` setting `status = 'done'` for every row whose `status` is `'review'`. Capture its `rowcount` as `updated`.
- **Then** run a parameterised `DELETE` removing every row whose `priority` is strictly less than `min_priority` (`priority < ?`). Capture its `rowcount` as `deleted`.
- Read both counts from `cursor.rowcount` (don't re-query). Return the dict `{'updated': updated, 'deleted': deleted}`.
- Empty input returns `{'updated': 0, 'deleted': 0}`.

### Concepts you'll use
`sqlite3`, parameterised `UPDATE` / `DELETE` with a `WHERE` clause and `?` placeholders, `cursor.rowcount`, ordering of write operations.

### How to solve this
**Define:** `apply_changes(rows, min_priority)` and a zero-arg helper `sample_board()` returning the fixture below (copy exactly).

```python
def sample_board():
    return [
        {'title': 'A', 'status': 'review', 'priority': 5},
        {'title': 'B', 'status': 'review', 'priority': 1},
        {'title': 'C', 'status': 'todo',   'priority': 2},
        {'title': 'D', 'status': 'done',   'priority': 4},
    ]
```

Create the table, insert the rows, run the UPDATE then the DELETE, read each `rowcount`, and return the dict.

**What the grader runs**
- `apply_changes(sample_board(), 3)`  →  `{'updated': 2, 'deleted': 2}`
- `apply_changes(sample_board(), 1)`  →  `{'updated': 2, 'deleted': 0}`
- `apply_changes([], 3)`  →  `{'updated': 0, 'deleted': 0}`

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
def sample_board()
def apply_changes(rows, min_priority)
```

> **Runtime:** your code is graded on **Python 3.11**, the same version as the Python in your editor. Modern syntax is fine — `match` statements and `int | None` unions in annotations both work.
>
> **`return` your answer — never `print` it.** A printed value is not a returned value, and the
> grader only reads what you return.

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
