# Top-K Nearest Tickets by Cosine Similarity

This is the search step of a vector database. You have a matrix of TaskFlow ticket embeddings — one row per ticket — plus a query vector, and you want the `k` tickets closest to the query. You'll score every row by **cosine similarity** and return the best matches, best first.

Each returned element is a two-item list `[row_index, score]`, where `score` is the cosine similarity rounded to 6 decimals.

### Worked example
```python
matrix = [[1,0,0,0], [0,1,0,0], [0.9,0.1,0,0], [0,0,1,0], [0.5,0,0.5,0]]
top_k(matrix, [1,0,0,0], 2)  ->  [[0, 1.0], [2, 0.993884]]
```
Row 0 is identical to the query, so it scores `1.0`. Row 2 (`[0.9, 0.1, 0, 0]`) points almost the same way, scoring `0.993884`. With `k=2` those two win; the rest are cut.

### What to build
- Write `top_k(matrix, query, k)`.
- Score every row against the query with cosine similarity (use `numpy`). If a row (or the query) has zero magnitude, its score is `0.0` (never `nan`).
- Sort by score **descending**; break ties by **smaller row index** so the output is deterministic.
- Return the first `k` results as a list of `[index, score]` pairs — `index` is an `int`, `score` is a rounded `float`.

### Concepts you'll use
`numpy` for cosine similarity, guarding zero norms, building a list of `(index, score)`, `sorted(..., key=...)` with a two-part key (`-score`, then `index`), list slicing.

### How to solve this
- **Define:** `top_k(matrix, query, k)` **and** the zero-arg helper `ticket_matrix()` returning the fixed 5x4 matrix from the example.
- For each row, compute cosine similarity (guard zero norms), collect `(index, round(score, 6))`.
- `scored.sort(key=lambda t: (-t[1], t[0]))`, then return the first `k` as `[index, score]` lists.

**What the grader runs**
- `top_k(ticket_matrix(),[1.0,0.0,0.0,0.0],2)`  →  `[[0, 1.0], [2, 0.993884]]`
- `top_k(ticket_matrix(),[0.5,0.0,0.5,0.0],3)`  →  `[[4, 1.0], [0, 0.707107], [3, 0.707107]]`
- `top_k([[1.0,0.0],[0.0,1.0]],[0.0,0.0],2)`  →  `[[0, 0.0], [1, 0.0]]`

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
def ticket_matrix()
def top_k(matrix, query, k)
```

> **Runtime:** your code is graded on **Python 3.11**, the same version as the Python in your editor. Modern syntax is fine — `match` statements and `int | None` unions in annotations both work.
>
> **`return` your answer — never `print` it.** A printed value is not a returned value, and the
> grader only reads what you return.

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
