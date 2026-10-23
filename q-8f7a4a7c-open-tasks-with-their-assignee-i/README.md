# Open Tasks With Their Assignee (INNER JOIN)

TaskFlow needs a quick roster of who's on the hook for each unfinished task. You'll load the users and tasks into a tiny in-memory SQLite database and use an **INNER JOIN** to pair every open task with the name of the person it's assigned to.

Each **user** is a dict with `id` and `name`. Each **task** is a dict with `id`, `title`, `status` (`todo`/`in_progress`/`review`/`done`) and `assignee_id` (which may be `None`).

### Worked example
```python
open_tasks_with_assignee(sample_users(), sample_tasks())
# -> [('Build API', 'Ben'), ('Deploy', 'Cara'), ('Write tests', 'Ana')]
```
Every open (not `done`) task is matched to its assignee's name, and the pairs come back sorted by task title. An INNER JOIN keeps only rows that have a match, so a task with `assignee_id = None` (or an id that matches no user) has no partner and quietly drops out.

### What to build
- Write `open_tasks_with_assignee(users, tasks)`.
- Load both lists into an in-memory `sqlite3` database and **INNER JOIN** tasks to users on `assignee_id = users.id`.
- Keep only tasks whose `status` is not `'done'`; unmatched tasks fall away naturally because of the join.
- Return a list of `(task_title, assignee_name)` tuples, **sorted by task title** ascending.

### Concepts you'll use
`sqlite3` in-memory database, `INNER JOIN ... ON`, `WHERE`, `ORDER BY`, returning a list of tuples.

### How to solve this
**Define:** the helper fixtures `sample_users()`, `sample_tasks()`, `no_tasks()`, `all_done_tasks()`, `alt_tasks()` (already provided in the starter) and the function `open_tasks_with_assignee(users, tasks)`.

**What the grader runs:**
- `open_tasks_with_assignee(sample_users(), sample_tasks())`  ->  `[('Build API', 'Ben'), ('Deploy', 'Cara'), ('Write tests', 'Ana')]`
- `open_tasks_with_assignee(sample_users(), no_tasks())`  ->  `[]`
- `open_tasks_with_assignee(sample_users(), all_done_tasks())`  ->  `[]`

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
def all_done_tasks()
def alt_tasks()
def open_tasks_with_assignee(users, tasks)
```

> **Runtime:** your code is graded on **Python 3.11**, the same version as the Python in your editor. Modern syntax is fine — `match` statements and `int | None` unions in annotations both work.
>
> **`return` your answer — never `print` it.** A printed value is not a returned value, and the
> grader only reads what you return.

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
