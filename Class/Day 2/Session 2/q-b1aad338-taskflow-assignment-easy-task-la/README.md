# TaskFlow Assignment (Easy) — Task Label Formatter

## Build a task's board label

Every task on the TaskFlow board shows a tidy label like `[DONE] Deploy API` — a status tag in brackets, then the title. You'll write one function that builds this label.

### Worked example

```python
format_task_label('Fix login bug')          # -> '[TODO] Fix login bug'
format_task_label('Deploy API', 'done')     # -> '[DONE] Deploy API'
```

The status is uppercased and wrapped in brackets, then the title follows after a space. The first call gives no status, so it falls back to the default `'todo'` — which is why it shows `[TODO]`.

### What to build

Define `format_task_label(title, status='todo')` that returns the string `'[STATUS] Title'`, where:
- STATUS is `status` **uppercased** (e.g. `'done'` becomes `DONE`).
- `status` defaults to `'todo'` when the caller omits it.
- If `title` is empty (`''`) or `None`, use the literal `'untitled'` in its place.

**Concepts you'll use:** functions, parameters, default arguments, `return`, string methods (`.upper()`), f-strings.

<!--LL-CONTRACT-->
### How to solve this
Write your Python **directly in the code editor** on the right, then click **Run Tests**. There is a single editor — you do **not** create or name any file; just define the function(s) below.

**Define:**
- `format_task_label(title, status='todo')`

**What the grader runs** (each value is scored **separately**, so a partly-correct answer still earns marks):
- `format_task_label('Fix login bug')`  →  `[TODO] Fix login bug`
- `format_task_label('Deploy API', 'done')`  →  `[DONE] Deploy API`
- `format_task_label('Write tests', 'in_progress')`  →  `[IN_PROGRESS] Write tests`

Return the exact value shown (a list stays a list; round numbers only if the task says so). **`return` the value — do not `print` it.**

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
