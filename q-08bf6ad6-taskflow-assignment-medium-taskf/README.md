# TaskFlow Assignment (Medium) — TaskFlow effort weighting across task types

A TaskFlow task tracks how much work is left and how "heavy" it is. You'll grow the `Task` family so each kind computes its own weight, and add a small helper that builds the right task for you.

## Worked example

```python
FeatureTask('Dark mode', 10, 3).weight()   # -> 16.0
```

A feature's weight is its base weight (`float(estimate_hours)` = `10.0`) plus `story_points * 2` (= `6`), giving `16.0`. A bug instead multiplies the base weight by a severity factor.

## What to build

- `Task(title, estimate_hours, logged_hours=0)`:
  - `remaining_hours` — a `@property` (call it as `task.remaining_hours`, no parentheses) returning `estimate_hours - logged_hours`, but never below `0`.
  - `is_complete` — a `@property` returning `True` when `logged_hours >= estimate_hours`.
  - `weight()` — returns `float(estimate_hours)`.
- `BugTask(title, estimate_hours, severity='minor', logged_hours=0)` — subclass of `Task`. Give it a class attribute `SEVERITY_MULT={'minor':1.0,'major':1.5,'critical':2.0,'blocker':3.0}`. Its `weight()` is the base weight times the matching multiplier, rounded to 2.
- `FeatureTask(title, estimate_hours, story_points, logged_hours=0)` — subclass of `Task`. Its `weight()` is the base weight plus `story_points*2`, rounded to 2. Get the base weight by calling `super().weight()` (the parent's version) rather than recomputing it.
- `build_task(kind, title, estimate_hours, extra, logged_hours=0)` — a factory: return the right object for `kind` `'bug'`, `'feature'`, or `'task'` (pass `extra` as severity/story_points where needed). Return the string `'error: negative estimate'` when `estimate_hours < 0`, and `'error: unknown kind'` for any other kind.

A `@property` lets a method be read like a plain attribute. A *factory* is just a function that decides which class to build and returns an instance.

## Concepts you'll use

`@property`, inheritance, `super().weight()`, class attributes, a factory function, `round()`.

<!--LL-CONTRACT-->
### How to solve this
Write your Python **directly in the code editor** on the right, then click **Run Tests**. There is a single editor — you do **not** create or name any file; just define the function(s) below.

**Define:**
- `class Task`
- `class BugTask(Task)`
- `class FeatureTask(Task)`
- `build_task(kind, title, estimate_hours, extra, logged_hours=0)`

**What the grader runs** (each value is scored **separately**, so a partly-correct answer still earns marks):
- `FeatureTask('Dark mode',10,3).weight()`  →  `16.0`
- `BugTask('Crash',8,'critical').weight()`  →  `16.0`
- `Task('X',8,3).remaining_hours`  →  `5`

Return the exact value shown (a list stays a list; round numbers only if the task says so). **`return` the value — do not `print` it.**

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
