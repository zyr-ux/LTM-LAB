# TaskFlow: Task Label & Cost

## Turn task facts into a label and a cost

A task already has its facts filled in. Your job is to combine them into two new values: a readable board label and the billable cost so far. These fixed facts are already assigned for you:

- `task_id = 42`
- `title = "Ship v2"`
- `hourly_rate = 80.0`
- `hours_logged = 3.5`

### A quick example

```python
a = 3
b = 4.0
product = a * b              # 12.0
line = f"Task #{a}: hello"   # "Task #3: hello"
```

An **f-string** (the `f"..."` form) drops a variable's value into text wherever you put `{...}`, and `*` multiplies numbers. You'll build `label` and `cost` the same way — with only variables, arithmetic, and an f-string.

**Concepts you'll use:** variables, arithmetic (`*`), f-strings.

### What to define
- `label` — a string built with an f-string in the form `Task #<id>: <title>`, i.e. `"Task #42: Ship v2"`.
- `cost` — the billable cost so far as a float: `hours_logged * hourly_rate`.

### What the grader checks
- `label` → `"Task #42: Ship v2"`
- `cost` → `280.0`

Do NOT use functions, dictionaries, lists, loops, or conditionals — just top-level statements.

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
