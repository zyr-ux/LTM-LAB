# TaskFlow Assignment (Medium) — Sprint Estimate Summary

## Estimate Summary Stats (NumPy)

TaskFlow wants a quick statistical summary of a batch of task estimates — total, average, spread, and range. You'll compute them with **NumPy** aggregations.

NumPy gives you each statistic with one call on the array: `.sum()`, `.mean()`, `.std()`, `.min()`, `.max()`.

### Worked example
```python
estimate_summary([5, 2, 2, 13, 13])
# {'total': 35, 'mean': 7.0, 'std': 5.02, 'min': 2.0, 'max': 13.0}
```
Sum is `35`; mean is `35/5 = 7.0`; `std` is the population standard deviation (≈`5.02`); min and max are `2.0` and `13.0`. Everything but `total` is a float rounded to 2 decimals.

### What to build
Write `estimate_summary(estimates)`:
- `estimates` is a list of task estimate hours. `None` entries are tasks **not yet estimated** — **filter them out** before computing.
- Return a dict `{'total','mean','std','min','max'}`: `total` as a plain `int`; `mean`, `std` (population), `min`, `max` as floats **rounded to 2 dp**.
- An **empty** list (or all-`None`) must return the zeroed dict `{'total':0,'mean':0.0,'std':0.0,'min':0.0,'max':0.0}` — never NaN.
- If `estimates` is **not a list**, or a non-`None` entry is not a number, return `None`.

Use only NumPy array creation, dtype, indexing/slicing and the aggregations sum/mean/std/min/max. Return **plain Python** types (int / float / dict) — never a NumPy scalar, NumPy array, or NaN/inf. ("Population" std divides by N, which is NumPy's default `.std()`; wrap each result in `round(float(x), 2)`.)

### Concepts you'll use
NumPy aggregations (sum/mean/std/min/max), filtering out `None`, `round()`, converting NumPy scalars to plain floats/ints.

<!--LL-CONTRACT-->
### How to solve this
Write your Python **directly in the code editor** on the right, then click **Run Tests**. There is a single editor — you do **not** create or name any file; just define the function(s) below.

**Define:**
- `estimate_summary(estimates)`

**What the grader runs** (each value is scored **separately**, so a partly-correct answer still earns marks):
- `estimate_summary([5, 2, 2, 13, 13])`  →  `{"total": 35, "mean": 7.0, "std": 5.02, "min": 2.0, "max": 13.0}`
- `estimate_summary([])`  →  `{"total": 0, "mean": 0.0, "std": 0.0, "min": 0.0, "max": 0.0}`
- `estimate_summary([4, None, 6])`  →  `{"total": 10, "mean": 5.0, "std": 1.0, "min": 4.0, "max": 6.0}`

Return the exact value shown (a list stays a list; round numbers only if the task says so). **`return` the value — do not `print` it.**

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
