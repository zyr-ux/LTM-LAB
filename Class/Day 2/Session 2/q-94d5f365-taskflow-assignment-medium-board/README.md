# TaskFlow Assignment (Medium) — Board Status Rollup

## Summarize a batch of tasks

Given a batch of TaskFlow tasks, you'll produce a small summary dict: how many there are, a per-status breakdown, and (optionally) the completion rate.

### Worked example

```python
summarize_tasks([{'status':'todo'}, {'status':'done'}, {'status':'done'}])
# -> {'total': 3, 'by_status': {'todo': 1, 'done': 2}, 'rate': 66.7}
```

Three tasks, so `'total'` is 3. Counting statuses gives `{'todo': 1, 'done': 2}`. Two of the three are done, so the rate is `2 / 3 * 100 = 66.7` (rounded to 1 decimal place).

### What to build

Define `summarize_tasks(tasks, include_rate=True)`, where `tasks` is a list of dicts that each usually have a `'status'` key. Return a dict:
- `'total'`: number of tasks.
- `'by_status'`: a dict mapping each status to its count. Use `'unknown'` when a task has no `'status'` key.
- `'rate'`: percent of tasks with status `'done'`, rounded to 1 decimal place. Include this key ONLY when `include_rate` is True. When the list is empty the rate is `0.0` (never divide by zero).

Keep the function pure: do not mutate the input list or its dicts.

**Concepts you'll use:** functions, default/keyword args, loops, dicts, `round()`, `return`, purity.

<!--LL-CONTRACT-->
### How to solve this
Write your Python **directly in the code editor** on the right, then click **Run Tests**. There is a single editor — you do **not** create or name any file; just define the function(s) below.

**Define:**
- `summarize_tasks(tasks, include_rate=True)`

**What the grader runs** (each value is scored **separately**, so a partly-correct answer still earns marks):
- `summarize_tasks([{'status':'todo'},{'status':'done'},{'status':'done'}])['total']`  →  `3`
- `summarize_tasks([{'status':'todo'},{'status':'done'},{'status':'done'}])['by_status']`  →  `{"todo": 1, "done": 2}`
- `summarize_tasks([{'status':'todo'},{'status':'done'},{'status':'done'}])['rate']`  →  `66.7`

Return the exact value shown (a list stays a list; round numbers only if the task says so). **`return` the value — do not `print` it.**

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
