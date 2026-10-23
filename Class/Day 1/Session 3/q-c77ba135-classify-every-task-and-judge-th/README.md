# Classify Every Task and Judge the Board

## Classify every status and judge the board

Same encoded board — but now you'll classify **every** character in one pass (each one is exactly one of todo / in_progress / review / done), then decide the board's overall state.

The board is fixed:

```python
statuses = "tttdirdt"
```

### A quick example

```python
a_count = 0
other = 0
for ch in "abc":
    if ch == "a":
        a_count += 1
    else:
        other += 1
```

Use one `for` loop with `if/elif/elif/else` so exactly one counter goes up per character. Then use plain conditionals on the counts to choose the board state.

**Concepts you'll use:** strings, `for` loops, `if/elif/else`, counters, `len()`.

### What to define
- `todo_count` — count of `"t"`.
- `in_progress_count` — count of `"i"`.
- `review_count` — count of `"r"`.
- `done_count` — count of `"d"` (the `else` branch).
- `board_state` — a string chosen with conditionals against `total = len(statuses)` and `active_count = todo_count + in_progress_count + review_count`:
  - `"complete"` if `done_count == total`
  - else `"not started"` if `done_count == 0`
  - else `"mostly done"` if `done_count >= active_count`
  - else `"in progress"`

### What the grader checks
- `todo_count`  →  `4`
- `done_count`  →  `2`
- `board_state`  →  `in progress`

No functions, lists, or dicts.

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
