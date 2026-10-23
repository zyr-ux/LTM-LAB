# Board Estimate, First Done, and a Progress Bar

## Build a full board report

Same encoded board, now the full picture: you'll combine a counting loop, a `while` accumulator, and a `for` loop that stops early with `break` to produce one report line.

The board is fixed:

```python
statuses = "tttdirdt"
```

### A quick example

```python
i = 0
total = 0
while i < len(statuses):
    total += 1        # do something each pass
    i += 1            # move your own index forward
```

A `while` loop runs as long as its condition is true, and you advance your own index each pass. A `for` with `break` lets you stop at the first match (like the first `"d"`). You'll use both, plus a string you grow one character at a time.

**Concepts you'll use:** `while` loops, indexing, `for` + `break`, string building, arithmetic, f-strings.

### What to define
- `total_tasks` — `len(statuses)`.
- `total_hours` — using a **`while`** loop with your own index over `range`-style positions: add `1` for each done (`"d"`) task (wrap-up) and `3` for every other task, into an integer accumulator.
- `first_done_index` — start at `-1`; scan positions with a `for` over `range(total_tasks)` and, at the first `"d"`, store the index and `break`.
- `progress_bar` — a string accumulator: append `"#"` for each done task and `"."` otherwise.
- `headline` — f-string `"First done at index <first_done_index>, <total_hours}h total"` → exactly `"First done at index 3, 20h total"`.

### What the grader checks
- `total_hours`  →  `20`
- `first_done_index`  →  `3`
- `progress_bar`  →  `...#..#.`

Use only loops, conditionals, arithmetic, string ops, and f-strings. No functions, lists, or dicts.

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
