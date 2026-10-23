# Cosine Similarity of Two Ticket Embeddings

In a vector database, each TaskFlow ticket is stored as an embedding — a list of floats. To find similar tickets you compare those vectors, and the standard measure is **cosine similarity**: the dot product of two vectors divided by the product of their magnitudes (lengths). You'll write that measure.

Cosine similarity captures how much two vectors point in the *same direction*. It ranges from `-1` (opposite) through `0` (unrelated / at right angles) to `1` (identical direction), and — unlike a raw dot product — it ignores how long the vectors are.

### Worked example
```python
cosine_similarity([1.0, 1.0], [1.0, 0.0])  ->  0.707107
cosine_similarity([1.0, 0.0], [0.0, 1.0])  ->  0.0
```
`[1, 1]` and `[1, 0]` sit 45° apart, and the cosine of 45° is about `0.707107`. `[1, 0]` and `[0, 1]` are at right angles, so they score `0.0`.

### What to build
- Write `cosine_similarity(a, b)`, where `a` and `b` are lists of floats of the same length.
- Use `numpy` for the dot product and the magnitudes (`np.dot`, `np.linalg.norm`).
- If **either** vector has zero magnitude, return `0.0` (never `nan` — you'd otherwise divide by zero).
- Round the result to **6 decimal places** and return a Python `float`.

### Concepts you'll use
`numpy` arrays, `np.dot`, `np.linalg.norm`, guarding division by zero, `round(...)`, casting to `float`.

### How to solve this
- **Define:** `cosine_similarity(a, b)`.
- Convert both inputs with `np.asarray(x, dtype=float)`.
- Compute `denom = norm(a) * norm(b)`; if it is `0.0`, return `0.0`.
- Otherwise return `round(float(dot(a, b) / denom), 6)`.

**What the grader runs**
- `cosine_similarity([1.0,0.0,0.0],[1.0,0.0,0.0])`  →  `1.0`
- `cosine_similarity([1.0,1.0],[1.0,0.0])`  →  `0.707107`
- `cosine_similarity([0.0,0.0],[1.0,1.0])`  →  `0.0`

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
def cosine_similarity(a, b)
```

> **Runtime:** your code is graded on **Python 3.11**, the same version as the Python in your editor. Modern syntax is fine — `match` statements and `int | None` unions in annotations both work.
>
> **`return` your answer — never `print` it.** A printed value is not a returned value, and the
> grader only reads what you return.

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
