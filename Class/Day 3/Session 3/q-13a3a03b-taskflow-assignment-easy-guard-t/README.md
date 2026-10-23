# TaskFlow Assignment (Easy) — Guard the task status field

TaskFlow only accepts a few valid statuses. You'll write your own exception type for a bad status, raise it when needed, and then a "safe" wrapper that catches it instead of crashing.

## Worked example

```python
validate_status('done')          # -> 'done'   (valid, returned as-is)
safe_validate_status('bogus')    # -> 'error: invalid status: bogus'
```

`validate_status` returns the status when it's allowed and *raises* when it isn't. `safe_validate_status` runs it inside try/except, so instead of raising it returns a friendly error string.

## What to build

- `TaskFlowError(Exception)` — a custom exception class. Making it subclass `Exception` is all it needs (`class TaskFlowError(Exception): pass`).
- `InvalidStatusError(TaskFlowError)` — a more specific error that inherits from `TaskFlowError`.
- `validate_status(status)` — return `status` when it's one of `todo`, `in_progress`, `done`, `blocked`; otherwise `raise InvalidStatusError(f"invalid status: {status}")`.
- `safe_validate_status(status)` — call `validate_status` inside a `try`/`except`. On success return the status; on failure return the string `f"error: {message}"`, where `message` is the caught exception's text (get it with `str(e)`).

An *exception class* is just a class that inherits from `Exception`; you `raise` it to signal a problem and `except` it to handle one. Building your own lets you catch exactly the errors you care about.

## Concepts you'll use

Custom exception classes, inheritance, `raise`, `try`/`except`, f-strings, `str(exception)`.

<!--LL-CONTRACT-->
### How to solve this
Write your Python **directly in the code editor** on the right, then click **Run Tests**. There is a single editor — you do **not** create or name any file; just define the function(s) below.

**Define:**
- `class TaskFlowError(Exception)`
- `class InvalidStatusError(TaskFlowError)`
- `validate_status(status)`
- `safe_validate_status(status)`

**What the grader runs** (each value is scored **separately**, so a partly-correct answer still earns marks):
- `validate_status('done')`  →  `done`
- `safe_validate_status('bogus')`  →  `error: invalid status: bogus`
- `issubclass(InvalidStatusError, Exception)`  →  `True`

Return the exact value shown (a list stays a list; round numbers only if the task says so). **`return` the value — do not `print` it.**

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
