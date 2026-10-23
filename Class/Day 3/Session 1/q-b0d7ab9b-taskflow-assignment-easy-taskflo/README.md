# TaskFlow Assignment (Easy) — TaskFlow task types: BugTask & FeatureTask

Every card on the TaskFlow board needs a short label. Different kinds of tasks (a plain task, a bug, a feature) show slightly different labels — so you'll build one base `Task` class and let two subclasses reuse it.

## Worked example

```python
Task('Onboarding docs', 'low').label()   # -> "[TASK] Onboarding docs (low)"
```

The base label is just the tag `[TASK]`, then the title, then the priority in parentheses. A `BugTask` and a `FeatureTask` follow the same idea but add their own extra field.

## What to build

- `Task(title, priority='medium')` — stores `title`, `priority`, and a `status` fixed to `'todo'`. Its `label()` returns `"[TASK] <title> (<priority>)"` (where `<title>` means: drop the task's title in here, `<priority>` means its priority).
- `BugTask(title, priority='medium', severity='minor')` — a subclass of `Task`. Call `super().__init__(...)` so the parent stores `title`/`priority` for you, then keep `severity`. Its `label()` returns `"[BUG] <title> (<priority>/<severity>)"`.
- `FeatureTask(title, priority='medium', story_points=1)` — a subclass of `Task`. Same `super()` idea, plus `story_points`. Its `label()` returns `"[FEATURE] <title> (<priority>) sp=<story_points>"`.

`super()` gives you the parent class, so `super().__init__(...)` runs `Task`'s setup instead of copy-pasting it. Each subclass writes its own `label()` — that's overriding: the child's method replaces the parent's.

## Concepts you'll use

Classes, inheritance, `super().__init__()`, method overriding, f-strings.

<!--LL-CONTRACT-->
### How to solve this
Write your Python **directly in the code editor** on the right, then click **Run Tests**. There is a single editor — you do **not** create or name any file; just define the function(s) below.

**Define:**
- `class Task`
- `class BugTask(Task)`
- `class FeatureTask(Task)`

**What the grader runs** (each value is scored **separately**, so a partly-correct answer still earns marks):
- `BugTask('Login fails','high','critical').label()`  →  `[BUG] Login fails (high/critical)`
- `Task('Onboarding docs','low').label()`  →  `[TASK] Onboarding docs (low)`
- `isinstance(BugTask('x'), Task)`  →  `True`

Return the exact value shown (a list stays a list; round numbers only if the task says so). **`return` the value — do not `print` it.**

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
