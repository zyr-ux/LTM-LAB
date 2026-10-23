# TaskFlow Assignment (Easy) — Audit Decorator for TaskFlow Task Completion

## Count How Often a Task Completes

TaskFlow wants to know how many times its "complete a task" action runs. You'll write a **decorator** that wraps a function and quietly keeps a running count of every call, then use it on the task-completion function.

A **decorator** is a function that takes another function and returns a new one wrapping it — handy for adding behavior (like counting) without editing the original. `functools.wraps` copies the original's name and docstring onto the wrapper so it still looks like itself.

### Worked example
```python
complete_task({'id': 7, 'status': 'todo'})   # {'id': 7, 'status': 'done'}
complete_task.calls                          # e.g. 1  (how many times it has run)
```
Completing a task returns it marked `'done'`; each call also bumps the counter stored on the wrapper.

### What to build
- `audit(func)` — a decorator that counts invocations of the wrapped function on `wrapper.calls` (start it at `0`), and uses `functools.wraps(func)` so the wrapped function keeps its name and docstring.
- `complete_task(task)` — decorated with `@audit`. Given a task dict it returns `{'id': <id>, 'status': 'done'}` (where `<id>` means the task's own id value); if the task has no `'id'` key it returns `{'error': 'missing id'}`.
- `count_calls(n)` — reset the counter to `0`, call `complete_task` `n` times, and return `complete_task.calls`.

### Concepts you'll use
Decorators, `functools.wraps`, storing state on the wrapper function (`wrapper.calls`).

<!--LL-CONTRACT-->
### How to solve this
Write your Python **directly in the code editor** on the right, then click **Run Tests**. There is a single editor — you do **not** create or name any file; just define the function(s) below.

**Define:**
- `audit(func)`
- `complete_task(task)`
- `count_calls(n)`

**What the grader runs** (each value is scored **separately**, so a partly-correct answer still earns marks):
- `complete_task({'id': 7, 'status': 'todo'})['id']`  →  `7`
- `complete_task({'id': 7, 'status': 'todo'})['status']`  →  `done`
- `complete_task.__name__`  →  `complete_task`

Return the exact value shown (a list stays a list; round numbers only if the task says so). **`return` the value — do not `print` it.**

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
