# TaskFlow Assignment (Easy) — Task class basics

## Build a Task class

This is your first TaskFlow **class** — a blueprint for creating task objects that carry their own data (`id`, `title`, `status`) and know how to update themselves.

### Worked example

```python
t = Task(1, 'Write docs')
t.status                 # 'todo'  (the default)
t.mark_done().status     # 'done'  (mark_done returns self, so you can chain)
repr(t)                  # "Task(id=1, title='Write docs', status='done')"
```

Creating `Task(1, 'Write docs')` runs `__init__` and stores the values. Because `mark_done()` returns `self`, you can immediately read `.status` on the same object.

### What to build

Define a class `Task`:
- `__init__(self, task_id, title, status='todo')` stores `id`, `title`, `status`. An empty/None title becomes `'Untitled'`; a status outside `{'todo','in_progress','done'}` defaults to `'todo'`.
- `mark_done()` sets status to `'done'` and returns `self`.
- `reopen()` sets it to `'todo'` and returns `self`.
- `is_done()` returns a bool.
- `__repr__` returns `Task(id=<id>, title='<title>', status='<status>')`.

Returning `self` from the mutators is what lets calls chain, like `Task(1,'X').mark_done().status`.

**Concepts you'll use:** classes, `__init__`, `self`, methods, default arguments, `__repr__`, method chaining.

<!--LL-CONTRACT-->
### How to solve this
Write your Python **directly in the code editor** on the right, then click **Run Tests**. There is a single editor — you do **not** create or name any file; just define the function(s) below.

**Define:**
- `class Task`

**What the grader runs** (each value is scored **separately**, so a partly-correct answer still earns marks):
- `Task(1, 'Write docs').status`  →  `todo`
- `Task(1, 'Write docs').mark_done().status`  →  `done`
- `repr(Task(1, 'Write docs'))`  →  `Task(id=1, title='Write docs', status='todo')`

Return the exact value shown (a list stays a list; round numbers only if the task says so). **`return` the value — do not `print` it.**

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
