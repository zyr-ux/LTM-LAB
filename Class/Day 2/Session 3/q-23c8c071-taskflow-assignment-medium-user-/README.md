# TaskFlow Assignment (Medium) — User with an encapsulated task book

## Build a User with a private task book

A TaskFlow `User` owns a set of tasks. You'll keep that data **private** inside `self._tasks` (a dict of `task_id -> status`) and expose tidy methods to work with it.

### Worked example

```python
u = User('u1', 'Alice')
u.assign('T1').open_count()      # 1  (one task, not done)
u.assign('T2')
u.workload()                     # {'total': 2, 'open': 2, 'done': 0}
```

`assign` adds a task as `'todo'` and returns `self`, so calls chain. `open_count()` counts tasks that aren't done, and `workload()` reports the totals.

### What to build

Define a class `User`, keeping the task book PRIVATE in `self._tasks` (a dict of `task_id -> status`):
- `assign(task_id)` adds the task as `'todo'` (idempotent) and returns `self`.
- `complete(task_id)` marks an owned task `'done'` (ignore unknown ids) and returns `self`.
- `task_status(task_id)` returns the status or `'unassigned'`.
- `open_count()` returns how many owned tasks are not done.
- `workload()` returns `{'total':..,'open':..,'done':..}`.
- `__repr__` returns `User(id='<id>', name='<name>', tasks=<count>)`.

**Concepts you'll use:** classes, `self`, private attributes (`_tasks`), dicts, methods, method chaining.

<!--LL-CONTRACT-->
### How to solve this
Write your Python **directly in the code editor** on the right, then click **Run Tests**. There is a single editor — you do **not** create or name any file; just define the function(s) below.

**Define:**
- `class User`

**What the grader runs** (each value is scored **separately**, so a partly-correct answer still earns marks):
- `User('u1', 'Alice').assign('T1').open_count()`  →  `1`
- `User('u1', 'Alice').assign('T1').assign('T2').workload()['total']`  →  `2`
- `User('u1', 'Alice').assign('T1').assign('T2').workload()['open']`  →  `2`

Return the exact value shown (a list stays a list; round numbers only if the task says so). **`return` the value — do not `print` it.**

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
