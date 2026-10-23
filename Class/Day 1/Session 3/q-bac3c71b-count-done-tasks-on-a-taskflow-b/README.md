# Count Done Tasks on a TaskFlow Board

## Count the done tasks on the board

A TaskFlow board is packed into a single status string — each character is one task's status: `t`=todo, `i`=in_progress, `r`=review, `d`=done. You'll loop over it to count the done tasks and build a headline.

The board is fixed:

```python
statuses = "tttdirdt"
```

### A quick example

```python
letters = "aba"
count = 0
for ch in letters:
    if ch == "a":
        count += 1
# count is now 2
```

Looping over a string hands you one character at a time; an `if` lets you count only the ones you care about. Use the same idea to count the `"d"` characters, then compute the totals with **one `for` loop** and an `if`.

**Concepts you'll use:** strings, `for` loops, `if`, `len()`, arithmetic, `int()`, f-strings.

### What to define
- `total_tasks` — the number of tasks on the board (the length of the string).
- `done_count` — how many characters equal `"d"`, counted with a `for` loop and an `if`.
- `completion_pct` — `done_count / total_tasks * 100` converted to a whole number with `int()`.
- `label` — an f-string reading `"<done_count> of <total_tasks> tasks done"`.

### What the grader checks
- `total_tasks`  →  `8`
- `done_count`  →  `2`
- `label`  →  `2 of 8 tasks done`

Use only loops, conditionals, arithmetic, type conversion, and f-strings. No functions, lists, or dicts.

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
