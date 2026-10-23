# Filter tasks by status (the selectbox handler)

In a Streamlit dashboard, a `st.selectbox("Status", ...)` widget lets the user pick a status, and the app then shows only the matching tasks. The UI glue belongs to Streamlit, but the *data-shaping* underneath is a plain, testable Python function — and that's what you'll write here (no Streamlit needed).

### Worked example
```python
filter_tasks([{"id":1,"status":"todo"}, {"id":2,"status":"done"}], "done")
# -> [{"id":2,"status":"done"}]
```
Only the task whose `status` is `"done"` survives, and it keeps its place in the list.

### What to build
- Write `filter_tasks(tasks, status)`. `tasks` is a list of task dicts (each has at least `id`, `title`, `status`, `priority`, `estimate_hours`).
- Return a **new list** of the tasks whose `status` equals the given `status`, keeping the input order.
- The special value `status == "all"` means *no filter* — return all tasks (a shallow copy of the list, not the same object).
- A status that matches nothing (or empty input) returns `[]`. Never mutate the input tasks.

### Concepts you'll use
List comprehensions, comparing dict values, returning a copy with `list(...)`, keeping functions pure (no mutation).

### How to solve this
- **Define:** `filter_tasks(tasks, status)`, plus a zero-arg helper `tasks_fixture()` that returns the sample task list used by the grader (copy it from below).
- Handle `status == "all"` first (return `list(tasks)`), otherwise return a list comprehension keeping tasks where `t["status"] == status`.

**What the grader runs:**
- `filter_tasks(tasks_fixture(), "todo")` → the two todo tasks (ids 3 and 4)
- `filter_tasks(tasks_fixture(), "archived")` → `[]`
- `len(filter_tasks(tasks_fixture(), "all"))` → `5`

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
def filter_tasks(tasks, status)
```

> **Runtime:** your code is graded on **Python 3.11**, the same version as the Python in your editor. Modern syntax is fine — `match` statements and `int | None` unions in annotations both work.
>
> **`return` your answer — never `print` it.** A printed value is not a returned value, and the
> grader only reads what you return.

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
