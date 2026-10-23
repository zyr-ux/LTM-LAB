# Linear commit history (newest first)

In Git, every commit points back at its **parent**, and following those parent pointers from a starting commit (the `HEAD`) back to the very first commit gives you the project's history. Here you'll model a **linear** history — each commit has at most one parent — and reproduce what `git log` shows: the commit messages, newest first.

`commits` is a list of dicts shaped like `{"id": str, "parent": str|None, "message": str}` (the root commit has `parent=None`). You also get a `head_id` to start from.

### Worked example
```python
commits = [
  {'id':'a1','parent':None,'message':'init TaskFlow repo'},
  {'id':'b2','parent':'a1','message':'add Task model'},
  {'id':'c3','parent':'b2','message':'add status field'},
]
history_messages(commits, 'c3')
# -> ['add status field', 'add Task model', 'init TaskFlow repo']
```
Starting at `c3`, you follow `parent` links: `c3 → b2 → a1`, collecting each message as you go. `a1`'s parent is `None`, so the walk stops there.

### What to build
- Write `history_messages(commits, head_id)`.
- Start at `head_id` and follow `parent` links, collecting each commit's `message`, until `parent` is `None` (or the id can't be found).
- Return the messages in the order visited (newest first).
- If `head_id` isn't present in `commits`, return `[]`. Don't assume the list is sorted — look commits up by id.

### Concepts you'll use
Building a lookup `dict` (`{id: commit}`) for O(1) access, a `while` loop following pointers, appending to a list.

### How to solve this
- **Define:** `commits_fixture()` (returns the sample list of 4 commits below) and `history_messages(commits, head_id)`.
- Build a dict `{id: commit}` for O(1) lookup, then loop following `parent`.
- The grader calls your `commits_fixture()` inside its test inputs, so define it exactly.

**What the grader runs**
- `history_messages(commits_fixture(), 'd4')`  →  `['add priority field', 'add status field', 'add Task model', 'init TaskFlow repo']`
- `history_messages(commits_fixture(), 'a1')`  →  `['init TaskFlow repo']`
- `history_messages(commits_fixture(), 'zz')`  →  `[]`

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
def commits_fixture()
def history_messages(commits, head_id)
```

> **Runtime:** your code is graded on **Python 3.11**, the same version as the Python in your editor. Modern syntax is fine — `match` statements and `int | None` unions in annotations both work.
>
> **`return` your answer — never `print` it.** A printed value is not a returned value, and the
> grader only reads what you return.

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
