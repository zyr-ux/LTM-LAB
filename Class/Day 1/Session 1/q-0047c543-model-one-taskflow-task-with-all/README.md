# Model one TaskFlow task with all four basic types

## Model a task with the four basic types

Every task in TaskFlow mixes a few kinds of data: whole numbers, text, decimals, and yes/no flags. Python has a **type** for each one. You'll store one task using all four.

### A quick example

```python
count = 3          # int   — a whole number
name = "Priya"     # str   — text in quotes
rate = 4.5         # float — a number with a decimal point
active = True      # bool  — either True or False
```

Each value on the right has a natural type, and the variable simply holds it. Below you'll create one variable per value, matching the type shown in brackets.

**Concepts you'll use:** variables, `int`, `str`, `float`, `bool`, `print()`.

### What to define

- `task_id` — the integer `42` (`int`)
- `task_title` — the string `"Ship v2 release"` (`str`)
- `hours_logged` — the float `3.5` (`float`)
- `task_done` — the boolean `False` (`bool`)
- `is_priority` — the boolean `True` (`bool`)

Print each variable so the script produces output.

**What the grader checks**

- `task_id` → `42`
- `hours_logged` → `3.5`
- `task_done` → `False`

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
