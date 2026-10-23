# TaskFlow: Task Fields Cleanup

## Clean up a task and compute its numbers

A TaskFlow task arrives with a messy title and a few numbers. You'll tidy the title and compute several result values from the facts. These fixed facts are already assigned:

- `task_id = 7`
- `title = "  Refactor Login  "`  (note the surrounding spaces)
- `hourly_rate = 65.0`
- `hours_logged = 12`
- `estimated_hours = 10`

### A quick example

```python
raw = "  hello  "
clean = raw.strip()          # "hello"  (spaces removed from both ends)
shout = clean.upper()        # "HELLO"
n = len(clean)               # 5
over = 12 > 10               # True  (a comparison gives a bool)
```

String methods like `.strip()` and `.upper()` return a new cleaned-up string, `len(...)` counts characters, and comparisons like `>` give `True`/`False`. You'll use these plus an f-string.

**Concepts you'll use:** variables, operators (`*`, `>`), f-strings, string methods (`.strip()`, `.upper()`), `len()`.

### What to define
- `title_clean` — `title` with surrounding whitespace removed (`.strip()`) → `"Refactor Login"`.
- `cost` — `hours_logged * hourly_rate` as a float.
- `over_estimate` — a bool: is `hours_logged` greater than `estimated_hours`?
- `label` — an f-string `Task #<id>: <title_clean>`.
- `title_upper` — `title_clean` in uppercase (`.upper()`).
- `name_len` — the number of characters in `title_clean` (`len(...)`).

### What the grader checks
- `title_clean` → `"Refactor Login"`
- `cost` → `780.0`
- `over_estimate` → `True`

No functions, dictionaries, lists, loops, or conditionals.

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
