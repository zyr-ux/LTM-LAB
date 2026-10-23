# Sprint board report

## Build a one-pass sprint report

The full sprint board is a **list of task tuples**, each shaped `(id, title, status, assignee, hours)`. You'll walk it **once** and gather several answers at the same time — using a list, a dict, and a set together.

```python
tasks = [
    (1, "Design login page", "done", "Ava", 4.0),
    (2, "Write API tests", "todo", "Ben", 3.0),
    (3, "Fix payment bug", "in_progress", "Ava", 5.5),
    (4, "Deploy release", "todo", "Cara", 2.0),
    (5, "Review PR", "done", "Ben", 1.5),
]
```

### A quick example

```python
titles = []
seen = set()
for row in tasks:
    tid, title, status, assignee, hours = row   # unpack the tuple
    titles.append(title)
    seen.add(assignee)
# titles keeps order; seen holds the distinct assignees
```

Unpack each tuple into named parts, then feed a list (`.append`), a dict (counting), and a set (`.add`) as you go — all in one loop, with no comprehensions and no functions.

**Concepts you'll use:** lists, dicts, sets, tuple unpacking, `for` loops, `.append()` / `.add()`, `sorted()`, `len()`, membership.

### What to define
- `task_titles` — a **list** of every task title in board order (loop + `.append()`).
- `status_counts` — a **dict** mapping each status to its count (loop + `if/else`).
- `unique_assignees` — a **set** of the distinct assignees (loop + `.add()`).
- `total_hours` — a **float**: the sum of all `hours` (accumulator in the loop).
- `sorted_titles` — `task_titles` sorted alphabetically (use `sorted(...)`).
- `assignee_count` — how many distinct assignees there are (`len` of the set).
- `has_ava` — a **bool**: is `"Ava"` one of the assignees? (membership).

### What the grader checks
- `status_counts` → `{'done': 2, 'todo': 2, 'in_progress': 1}`
- `sorted_titles` → titles in alphabetical order
- `total_hours` → `16.0`

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
