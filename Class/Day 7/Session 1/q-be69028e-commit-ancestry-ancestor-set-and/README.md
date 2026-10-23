# Commit ancestry: ancestor set and is-ancestor test

Real Git history is a **DAG** (directed acyclic graph): a merge commit has more than one parent, so each commit now carries a `parents` **list** (empty for the root). Two questions come up constantly in Git internals — *what are all the ancestors of a commit?* and *is commit A an ancestor of commit B?* (that second one is exactly how Git decides whether a branch can fast-forward). You'll answer both.

`commits` is a list of `{"id": str, "parents": [str, ...]}`.

### Worked example
```python
# a <- b, a <- c, (b,c) <- m, m <- d   (m is a merge commit)
ancestors(dag_fixture(), 'm')   # -> ['a', 'b', 'c']
is_ancestor(dag_fixture(), 'a', 'd')  # -> True
is_ancestor(dag_fixture(), 'b', 'c')  # -> False
```
From `m` you can walk back to `b`, `c`, and `a` — that's its ancestor set, returned sorted (and not including `m` itself). `a` is an ancestor of `d`, so the second call is `True`. `b` and `c` are siblings (neither reaches the other), so the third is `False`.

### What to build
- `ancestors(commits, commit_id)` — return every id reachable by following `parents` transitively from `commit_id`, **excluding** `commit_id` itself, as a **sorted list**. If `commit_id` is unknown, return `[]`.
- `is_ancestor(commits, a, b)` — return `True` if `a` appears in `b`'s ancestor set, else `False`. A commit is **not** its own ancestor, so `is_ancestor(commits, x, x)` is `False`.
- Handle diamonds: if a shared ancestor is reachable by several paths, count it once. Return a **sorted list** (not a Python set) for deterministic output; an iterative walk with a visited-set avoids any recursion-depth worries.

### Concepts you'll use
Building a `{id: commit}` lookup, graph traversal with a stack/queue and a `visited` set, `sorted(...)`, composing one function on top of another.

### How to solve this
- **Define:** `dag_fixture()` (the 5-commit merge DAG below), `ancestors(commits, commit_id)`, and `is_ancestor(commits, a, b)`.
- Build `{id: commit}`, push the start's parents onto a stack, pop-and-visit until empty, then `sorted(seen)`.
- Implement `is_ancestor` on top of `ancestors` (and short-circuit `a == b` to `False`).

**What the grader runs**
- `ancestors(dag_fixture(), 'd')`  →  `['a', 'b', 'c', 'm']`
- `is_ancestor(dag_fixture(), 'a', 'd')`  →  `True`
- `is_ancestor(dag_fixture(), 'b', 'c')`  →  `False`

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
def dag_fixture()
def ancestors(commits, commit_id)
def is_ancestor(commits, a, b)
```

> **Runtime:** your code is graded on **Python 3.11**, the same version as the Python in your editor. Modern syntax is fine — `match` statements and `int | None` unions in annotations both work.
>
> **`return` your answer — never `print` it.** A printed value is not a returned value, and the
> grader only reads what you return.

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
