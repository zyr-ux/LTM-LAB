# TaskFlow Assignment (Medium) — Task validation with an exception hierarchy

Before TaskFlow saves a task, it validates the fields. You'll build a small family of exception types and two functions: one that raises on bad data, and one that wraps it in try/except/else/finally to return a tidy report instead of crashing.

## Worked example

```python
report = validate_task_report({'title': 'Demo', 'status': 'done', 'priority': 1})
# -> {'valid': True, 'error_type': None, 'message': 'ok', 'checked': True}
```

The task is valid, so `validate_task` returns `True`, the `else` branch sets `valid=True`/`error_type=None`/`message='ok'`, and the `finally` branch always adds `checked=True`.

## What to build

- The exception hierarchy `TaskFlowError` → `ValidationError` → `{MissingFieldError, InvalidValueError}`. Each is a class inheriting from the one named before it (e.g. `class ValidationError(TaskFlowError): pass`), so catching `ValidationError` also catches both leaf types.
- `validate_task(task)` — check required fields `title`, `status`, `priority`:
  - `raise MissingFieldError("missing field: <name>")` for an absent field.
  - `raise InvalidValueError(...)` for an empty/whitespace title, a status outside `todo/in_progress/done/blocked`, or a priority that is not an int in `1..5` (note: booleans like `True` are NOT valid priorities — guard with `type(priority) is int`).
  - Return `True` when everything is valid.
- `validate_task_report(task)` — wrap `validate_task` in `try`/`except`/`else`/`finally` and return `{valid, error_type, message}`:
  - `except` a `ValidationError`: set `valid=False`, `error_type` to the exception's class name (e.g. `type(e).__name__`), `message` to `str(e)`.
  - `else` (no error): `valid=True`, `error_type=None`, `message='ok'`.
  - `finally`: always add `checked=True` to the report.

Ordering the classes into a hierarchy means one `except ValidationError` handles every validation problem. The `else` block runs only when no exception was raised; `finally` runs no matter what.

## Concepts you'll use

Exception hierarchies, inheritance, `raise`, `try`/`except`/`else`/`finally`, `type(e).__name__`, boolean-vs-int gotcha.

<!--LL-CONTRACT-->
### How to solve this
Write your Python **directly in the code editor** on the right, then click **Run Tests**. There is a single editor — you do **not** create or name any file; just define the function(s) below.

**Define:**
- `class TaskFlowError(Exception)`
- `class ValidationError(TaskFlowError)`
- `class MissingFieldError(ValidationError)`
- `class InvalidValueError(ValidationError)`
- `validate_task(task)`
- `validate_task_report(task)`

**What the grader runs** (each value is scored **separately**, so a partly-correct answer still earns marks):
- `validate_task_report({'title':'Demo','status':'done','priority':1})['valid']`  →  `True`
- `validate_task_report({'title':'Demo','status':'done','priority':1})['error_type']`  →  `None`
- `validate_task_report({'title':'Demo','status':'done','priority':1})['message']`  →  `ok`

Return the exact value shown (a list stays a list; round numbers only if the task says so). **`return` the value — do not `print` it.**

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
