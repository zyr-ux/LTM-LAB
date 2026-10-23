# TaskFlow Assignment (Easy) — Stream Open Tasks Lazily

## Stream Open Tasks

A TaskFlow board only wants to show work that still needs doing. You'll write a function that walks a stream of tasks and hands back the title of each one that isn't finished yet — one at a time, as they're asked for.

A **generator** is a function that uses `yield` instead of `return`. Each `yield` pauses the function and gives one value back to the caller; the next value is only computed when it's needed. That's what "lazily" means — nothing is built up front, so it even works on an endless stream.

### Worked example
```python
list(stream_open_tasks([{'title':'A','status':'todo'},{'title':'B','status':'done'}]))
# ['A']
```
Task `A` is `'todo'` (not done), so its title is yielded. Task `B` is `'done'`, so it's skipped. Wrapping the generator in `list(...)` collects everything it yields.

### What to build
Write a generator function `stream_open_tasks(tasks)` where `tasks` is an iterable of dicts, each with a `title` and usually a `status` (`'todo'`, `'in_progress'`, `'review'`, `'blocked'`, or `'done'`).
- For every task whose status is **not** `'done'`, `yield` its `title`.
- A task with **no** `status` key counts as open — yield it too (don't crash on the missing key; `dict.get('status')` helps).
- Keep the original order.
- Use `yield` — it must be a generator, not a function that builds and returns a list.

### Concepts you'll use
Generators, `yield`, iterating dicts, `dict.get` for a possibly-missing key.

<!--LL-CONTRACT-->
### How to solve this
Write your Python **directly in the code editor** on the right, then click **Run Tests**. There is a single editor — you do **not** create or name any file; just define the function(s) below.

**Define:**
- `stream_open_tasks(tasks)`

**What the grader runs** (each value is scored **separately**, so a partly-correct answer still earns marks):
- `len(list(stream_open_tasks([{'title':'A','status':'todo'},{'title':'B','status':'done'}])))`  →  `1`
- `list(stream_open_tasks([{'title':'A','status':'todo'},{'title':'B','status':'done'}]))[0]`  →  `A`
- `list(stream_open_tasks([]))`  →  `[]`

Return the exact value shown (a list stays a list; round numbers only if the task says so). **`return` the value — do not `print` it.**

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
