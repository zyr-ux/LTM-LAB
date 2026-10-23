# Sprint task list

## Store the sprint's tasks in a list

A **list** holds many values in order, which makes it perfect for the sprint's task titles. You'll build the list, then pull a few facts out of it. The sprint has exactly four tasks, in this order:

1. `"Design login page"`
2. `"Write API tests"`
3. `"Fix payment bug"`
4. `"Deploy release"`

### A quick example

```python
colors = ["red", "green", "blue"]
colors[0]            # "red"   (first item, index 0)
colors[-1]           # "blue"  (last item)
len(colors)          # 3
"green" in colors    # True
```

Indexing reads one item by position, `len` counts them, and `in` checks membership. You'll use those same four tools below — no functions needed.

**Concepts you'll use:** lists, indexing (`[0]`, `[-1]`), `len()`, membership (`in`), booleans.

### What to define
- `task_titles` — a **list** of the four titles above, in the given order.
- `first_task` — the first title in the list (use indexing).
- `last_task` — the last title in the list (use indexing, e.g. `[-1]`).
- `task_count` — how many titles are in the list (use `len`).
- `has_deploy` — a **bool**: is `"Deploy release"` in the list? (use `in`).

### What the grader checks
- `first_task` → `Design login page`
- `task_count` → `4`
- `has_deploy` → `True`

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
