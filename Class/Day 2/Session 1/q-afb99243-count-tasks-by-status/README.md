# Count tasks by status

## Count how often each status appears

You're given every task's status (with repeats). You'll tally them into a **dictionary** that maps each status to its count. Here's the data:

```python
statuses = ["todo", "done", "in_progress", "done", "todo", "done"]
```

### A quick example

```python
counts = {}
for word in ["a", "b", "a"]:
    if word in counts:
        counts[word] += 1
    else:
        counts[word] = 1
# counts is now {"a": 2, "b": 1}
```

Start with an empty dict, then loop and either bump an existing count or start a new one at `1`. Do the same over `statuses` — with a `for` loop and an `if/else`, no comprehension and no function.

**Concepts you'll use:** dicts, `for` loops, `if/else`, membership (`in`), `len()`.

### What to define
- `status_counts` — a **dict** mapping each status string to its count, e.g. `{"todo": 2, "done": 3, "in_progress": 1}`. Build it with an empty dict + a `for` loop + `if/else`.
- `done_count` — the number of `"done"` tasks, read from `status_counts`.
- `total` — the total number of tasks (use `len` on `statuses`).
- `has_todo` — a **bool**: is `"todo"` one of the keys in `status_counts`? (use `in`).

### What the grader checks
- `status_counts` → `{'todo': 2, 'done': 3, 'in_progress': 1}`
- `done_count` → `3`
- `total` → `6`

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
