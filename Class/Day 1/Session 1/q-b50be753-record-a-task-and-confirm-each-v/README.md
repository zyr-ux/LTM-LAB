# Record a task and confirm each value's type

## Record a task's types as text

Sometimes you don't just want a value — you want to know what **kind** of value it is. Python's built-in `type()` reports that, and `type(x).__name__` gives the type's name as a plain string.

### A quick example

```python
x = 7
print(type(x).__name__)   # prints: int
```

`type(7)` is the int type, and `.__name__` turns it into the readable string `"int"`. You'll store four task values (an int, a float, a str, and a bool) and, next to each, a `*_type` variable holding its type name — all with plain assignments, no functions of your own.

**Concepts you'll use:** variables, the four basic types, `type()`, `.__name__`.

### What to define

- `task_id` — the integer `7` (`int`)
- `estimate_hours` — the float `8.0` (`float`)
- `status` — the string `"open"` (`str`)
- `is_blocked` — the boolean `False` (`bool`)
- `id_type` — set it to `type(task_id).__name__` (will be `"int"`)
- `estimate_type` — set it to `type(estimate_hours).__name__` (will be `"float"`)
- `status_type` — set it to `type(status).__name__` (will be `"str"`)
- `blocked_type` — set it to `type(is_blocked).__name__` (will be `"bool"`)

Print the values so the script produces output.

**What the grader checks**

- `task_id` → `7`
- `id_type` → `int`
- `estimate_type` → `float`

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
