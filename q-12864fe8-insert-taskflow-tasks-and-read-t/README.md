# Insert TaskFlow tasks and read them back by status

TaskFlow is moving off in-memory lists onto a real database. You'll write its first data-layer helper: load a batch of task rows into a fresh SQLite table using **parameterised** inserts (the safe kind, with `?` placeholders), then read back the titles for one status.

`rows` is a list of dicts, each with keys `title`, `status`, `priority`.

### Worked example
```python
insert_and_fetch([
  {'title': 'Write spec', 'status': 'todo', 'priority': 5},
  {'title': 'Ship v1', 'status': 'done', 'priority': 3},
  {'title': 'Review PR', 'status': 'todo', 'priority': 2},
], 'todo')  ->  ['Write spec', 'Review PR']
```
All three rows go into the table, then you ask for just the `'todo'` ones. `'Write spec'` and `'Review PR'` come back in the order they were inserted; `'Ship v1'` is `'done'`, so it's skipped.

### What to build
- Write `insert_and_fetch(rows, status)`.
- Create an in-memory SQLite database with a `task` table: `id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, status TEXT, priority INTEGER`.
- Insert every row with a placeholder query (`VALUES (?, ?, ?)`) — never paste values straight into the SQL string.
- Return a **list of titles** whose `status` equals the `status` argument, ordered by insertion (ascending `id`).
- An empty `rows` list, or a status no row uses, returns `[]`.

### Concepts you'll use
`sqlite3` in-memory database, `CREATE TABLE`, parameterised `INSERT` with `?` placeholders (and `executemany`), `SELECT ... WHERE ... ORDER BY id`.

### How to solve this
**Define:** `insert_and_fetch(rows, status)` and a zero-arg helper `sample_tasks()` that returns the fixture list used by the grader (copy it exactly from below).

```python
def sample_tasks():
    return [
        {'title': 'Write spec', 'status': 'todo', 'priority': 5},
        {'title': 'Build API', 'status': 'in_progress', 'priority': 4},
        {'title': 'Review PR', 'status': 'todo', 'priority': 2},
        {'title': 'Ship v1', 'status': 'done', 'priority': 3},
    ]
```

Steps: `sqlite3.connect(':memory:')`, `CREATE TABLE`, `executemany` the inserts with a params list, `commit`, then `SELECT title ... WHERE status = ? ORDER BY id` and return the titles.

**What the grader runs**
- `insert_and_fetch(sample_tasks(), 'todo')`  →  `['Write spec', 'Review PR']`
- `insert_and_fetch(sample_tasks(), 'in_progress')`  →  `['Build API']`
- `insert_and_fetch(sample_tasks(), 'review')`  →  `[]`

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
def sample_tasks()
def insert_and_fetch(rows, status)
```

> **Runtime:** your code is graded on **Python 3.11**, the same version as the Python in your editor. Modern syntax is fine — `match` statements and `int | None` unions in annotations both work.
>
> **`return` your answer — never `print` it.** A printed value is not a returned value, and the
> grader only reads what you return.

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
