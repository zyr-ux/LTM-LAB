# TaskFlow Assignment (Easy) — Total Estimated Hours (Vectorised)

## Total Estimated Hours (NumPy)

TaskFlow wants the total estimated effort across a list of tasks. You'll add up the hours using **NumPy**, a library for fast number-crunching on arrays.

The idea behind NumPy is **vectorisation**: instead of looping in Python, you put the numbers in an array and let NumPy do the math in one fast operation (like `arr.sum()`).

### Worked example
```python
total_estimated_hours([5, 2, 2, 13, 13])   # 35
```
The five estimates go into a NumPy array and get summed: `5+2+2+13+13 = 35`, returned as a plain Python `int`.

### What to build
Write `total_estimated_hours(estimates)`:
- `estimates` is a list of task estimate hours (numbers). Build a NumPy array and return the **sum** as a plain `int` (whole hours).
- An **empty** list must return `0` (not NaN).
- If any entry is `None` or not a number, return `None` — don't let it turn into NaN.
- If `estimates` is **not a list**, return `None`.

Use only NumPy array creation, dtype, indexing/slicing and the aggregations sum/mean/std/min/max. Return **plain Python** types (int / float / dict) — never a NumPy scalar, NumPy array, or NaN/inf. (NaN = "not a number", the junk you get from bad or missing numeric data; `int(arr.sum())` turns a NumPy number into a plain `int`.)

### Concepts you'll use
NumPy arrays, `.sum()`, converting a NumPy scalar to a Python `int`, input validation.

<!--LL-CONTRACT-->
### How to solve this
Write your Python **directly in the code editor** on the right, then click **Run Tests**. There is a single editor — you do **not** create or name any file; just define the function(s) below.

**Define:**
- `total_estimated_hours(estimates)`

**What the grader runs** (each value is scored **separately**, so a partly-correct answer still earns marks):
- `total_estimated_hours([5, 2, 2, 13, 13])`  →  `35`
- `total_estimated_hours([8])`  →  `8`
- `total_estimated_hours([])`  →  `0`

Return the exact value shown (a list stays a list; round numbers only if the task says so). **`return` the value — do not `print` it.**

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
