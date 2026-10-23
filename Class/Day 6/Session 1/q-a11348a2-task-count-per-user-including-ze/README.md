# Task Count Per User, Including Zero (LEFT JOIN + COALESCE)

A workload dashboard needs to list **every** user next to how many tasks they hold — including the idle ones with nothing assigned. An INNER JOIN would silently hide those idle users, so this is a job for a **LEFT JOIN**: it keeps every user row and fills in blanks where there's no matching task.

Each **user** is a dict with `id` and `name`. Each **task** is a dict with `id`, `title` and `assignee_id`.

### Worked example
```python
task_count_per_user(sample_users(), sample_tasks())
# -> [('Ana', 2), ('Ben', 2), ('Cara', 1), ('Dan', 0)]
```
Each user appears once with their task count, sorted by name. Dan shows `0` because he has no tasks — the LEFT JOIN keeps him, and counting a task *column* (not `COUNT(*)`) gives 0 for the empty side instead of 1.

### What to build
- Write `task_count_per_user(users, tasks)`.
- Load both lists into `sqlite3` and **LEFT JOIN** users to tasks on `assignee_id = users.id` so every user appears even with zero tasks.
- Count with `COUNT(tasks.id)` (never `COUNT(*)`), wrapped in `COALESCE(..., 0)`, so a no-match user reads as **0**.
- `GROUP BY` the user, order by user name, and return a list of `(user_name, task_count)` tuples. A task pointing at an id that isn't in `users` counts toward nobody.

### Concepts you'll use
`sqlite3` in-memory database, `LEFT JOIN`, `GROUP BY`, `COUNT(col)`, `COALESCE`, `ORDER BY`.

### How to solve this
**Define:** the helper fixtures `sample_users()`, `sample_tasks()`, `no_tasks()`, `alt_tasks()` (already provided in the starter) and the function `task_count_per_user(users, tasks)`.

**What the grader runs:**
- `task_count_per_user(sample_users(), sample_tasks())`  ->  `[('Ana', 2), ('Ben', 2), ('Cara', 1), ('Dan', 0)]`
- `task_count_per_user(sample_users(), no_tasks())`  ->  `[('Ana', 0), ('Ben', 0), ('Cara', 0), ('Dan', 0)]`
- `task_count_per_user([{'id':1,'name':'Zoe'}], [{'id':9,'title':'X','assignee_id':1},{'id':10,'title':'Y','assignee_id':1}])`  ->  `[('Zoe', 2)]`

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
def sample_users()
def sample_tasks()
def no_tasks()
def alt_tasks()
def task_count_per_user(users, tasks)
```

> **Runtime:** your code is graded on **Python 3.11**, the same version as the Python in your editor. Modern syntax is fine — `match` statements and `int | None` unions in annotations both work.
>
> **`return` your answer — never `print` it.** A printed value is not a returned value, and the
> grader only reads what you return.

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
