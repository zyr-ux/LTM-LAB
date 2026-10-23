# Record a task's basic details

## Store a task's basic details

TaskFlow needs to remember a few facts about one task. In Python you "remember" a value by putting it in a **variable** — a name that points to a value. Here you'll create three variables.

### A quick example

```python
project_name = "TaskFlow"
print(project_name)   # prints: TaskFlow
```

The line `project_name = "TaskFlow"` stores the text on the right into the name on the left. After that, writing `project_name` gives you back `"TaskFlow"`. You'll do the same for a task's id, title, and assignee.

**Concepts you'll use:** variables, integers (`int`), strings (`str`), `print()`.

### What to define

- `task_id` — the integer `101`
- `task_title` — the string `"Design login page"`
- `assignee` — the string `"Priya"`

Print each of them (any order) so your script produces output when run.

**What the grader checks**

- `task_id` → `101`
- `task_title` → `Design login page`
- `assignee` → `Priya`

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
