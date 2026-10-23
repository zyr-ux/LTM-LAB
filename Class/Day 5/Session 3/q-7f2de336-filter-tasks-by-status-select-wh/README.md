# Filter Tasks by Status (SELECT + WHERE)

## Filter Tasks by Status (SQLite)

TaskFlow's board needs a "show me all the todo tasks" query. You'll load a list of task dicts into a tiny **in-memory SQLite database** and run a real SQL `SELECT` to pull back the matching rows. SQLite is a full SQL database that can live entirely in memory — perfect for querying data you already have in Python.

### Worked example
```python
filter_by_status([
    {"id": 3, "title": "Write tests", "status": "todo", "priority": 4,
     "project_id": 10, "assignee_id": 100, "estimate_hours": 6.0},
    {"id": 5, "title": "Update docs", "status": "todo", "priority": 2,
     "project_id": 11, "assignee_id": 101, "estimate_hours": 2.0},
    {"id": 1, "title": "Design schema", "status": "done", "priority": 3,
     "project_id": 10, "assignee_id": 100, "estimate_hours": 4.0},
], "todo")
# -> [{'id': 3, 'title': 'Write tests', 'priority': 4},
#     {'id': 5, 'title': 'Update docs', 'priority': 2}]
```
The two `'todo'` rows come back (the `'done'` one is filtered out), ordered by `id`, each trimmed to just `id`, `title`, and `priority`.

### What to build
Write `filter_by_status(tasks, status)`:
- Connect with `sqlite3.connect(":memory:")`, create a `tasks` table, and insert the given rows with `executemany`. Each task dict has: `id, title, status, priority, project_id, assignee_id, estimate_hours`.
- Query with `WHERE status = ?` (a **parameterised** query — the `?` is filled in safely by SQLite; never build SQL by string concatenation) and `ORDER BY id ASC`.
- Return a list of dicts `{'id', 'title', 'priority'}`. No matches -> return `[]`.

### Concepts you'll use
`sqlite3` in-memory DB, `CREATE TABLE`, `executemany`, parameterised `SELECT ... WHERE ... ORDER BY`, building result dicts.

### How to solve this
- **Define:** `filter_by_status(tasks, status)` and the helper `tasks_fixture()` (and, for hidden tests, `tasks_fixture2()`, `empty_tasks()`, `one_task()`) exactly as given in the starter — the grader calls these helpers inside its test expressions.
- **What the grader runs:**
  - `filter_by_status(tasks_fixture(), 'todo')` -> `[{'id': 3, 'title': 'Write tests', 'priority': 4}, {'id': 5, 'title': 'Update docs', 'priority': 2}]`
  - `filter_by_status(tasks_fixture(), 'review')` -> `[]`
  - `filter_by_status(one_task(), 'todo')` -> `[{'id': 42, 'title': 'Kickoff', 'priority': 3}]`

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
