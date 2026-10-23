# Build the dashboard status summary (KPI metrics)

The KPI tiles at the top of a Streamlit dashboard (`st.metric(...)`) and the bar chart beside them both need the same aggregated numbers. Rather than compute them twice in the UI, you'll gather everything once in a single pure function, and the dashboard just reads the result.

### Worked example
```python
build_status_summary([{"id":1,"status":"done","estimate_hours":5.0},
                      {"id":2,"status":"todo","estimate_hours":3.0}])
# -> {"total": 2, "by_status": {"todo": 1, "in_progress": 0, "review": 0, "done": 1},
#     "done": 1, "completion_rate": 0.5, "total_estimate_hours": 8.0, "done_estimate_hours": 5.0}
```
Two tasks in, so `total` is 2. `by_status` always lists all four statuses (the ones with no tasks show `0`). One task is `done`, so `done` is 1 and `completion_rate` is `1/2 = 0.5`. Hours add up to `8.0` overall and `5.0` for the done task.

### What to build
Write `build_status_summary(tasks)` returning a dict with exactly these keys:
- `"total"` — number of tasks (int).
- `"by_status"` — a dict with **all four** canonical statuses as keys, in this order: `todo`, `in_progress`, `review`, `done`, each mapping to the count of tasks with that status. A status must appear with `0` even if no task has it; statuses outside this set are ignored (not counted).
- `"done"` — count of `done` tasks (int).
- `"completion_rate"` — `done / total` rounded to 4 decimals; `0.0` when there are no tasks (guard against dividing by zero).
- `"total_estimate_hours"` — sum of every task's `estimate_hours` (missing → 0), rounded to 4 decimals.
- `"done_estimate_hours"` — sum of `estimate_hours` over `done` tasks only, rounded to 4 decimals.

Integral sums print as `X.0` (e.g. `8.0`).

### Concepts you'll use
Initialising a dict from a fixed key list, a single loop accumulating counts and sums, `dict.get` with a default, `round(x, 4)`, guarding division by zero.

### How to solve this
- **Define:** `build_status_summary(tasks)`, plus a zero-arg helper `tasks_fixture()` (copy it from below).
- Initialise `by_status` from the canonical list, loop once accumulating counts and hour sums, then assemble the dict. Use `round(x, 4)`.

**What the grader runs:**
- `build_status_summary(tasks_fixture())["by_status"]` → `{'todo': 2, 'in_progress': 1, 'review': 0, 'done': 2}`
- `build_status_summary(tasks_fixture())["completion_rate"]` → `0.4`
- `build_status_summary([])["completion_rate"]` → `0.0`

<!--LL-ATTEMPT-->
---

## How to attempt this

1. Open the assignment from your course page. Write your answer **in the code editor on the
   right** — there is no file to create and nothing to name.
2. Click **Run Tests** to grade it. The visible tests run first so you can see where you stand.
3. Read any failure carefully: it shows the **input**, what was **expected**, and what your code
   **actually returned**. That three-way comparison is usually enough to find the bug.
4. Re-run as often as you like. Each value is scored separately, so a partly-correct answer still
   earns marks — submit something rather than nothing.
5. When you are satisfied, **Submit**.

### The exact shape to define

```python
def tasks_fixture()
def build_status_summary(tasks)
```

> **Runtime:** your code is graded on **Python 3.11**, the same version as the Python in your editor. Modern syntax is fine — `match` statements and `int | None` unions in annotations both work.
>
> **`return` your answer — never `print` it.** A printed value is not a returned value, and the
> grader only reads what you return.

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
