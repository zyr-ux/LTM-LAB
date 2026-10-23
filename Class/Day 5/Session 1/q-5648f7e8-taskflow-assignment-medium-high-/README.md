# TaskFlow Assignment (Medium) — High-Priority Triage List

## Pull the high-priority work

The lead wants the titles of every **high-priority** task, to triage those first. You'll filter a table of tasks with **pandas** and pull out the matching titles.

Filtering in pandas uses a **boolean mask**: you write a condition like `df['priority'] == 'high'`, which produces a True/False for each row, and `df[mask]` keeps only the True rows.

### Worked example
```python
high_priority_titles([{'title':'A','priority':'high'},{'title':'B','priority':'low'}])
# ['A']
```
Row `A` is high priority so its title is kept; row `B` is low and dropped.

### What to build
Write `high_priority_titles(records)` where `records` is a **list of task dicts** with `title` and `priority` keys. Data arrives as a literal argument — **no file reads**.

1. `df = pd.DataFrame(records)`.
2. Filter rows where `priority == 'high'` with a boolean mask.
3. Return the matching `title` values as a **plain list of strings** (`.tolist()`), preserving the original order. Return `[]` when nothing matches.

### Concepts you'll use
pandas `DataFrame`, boolean masks, column selection, `.tolist()`.

<!--LL-CONTRACT-->
### How to solve this
Write your Python **directly in the code editor** on the right, then click **Run Tests**. There is a single editor — you do **not** create or name any file; just define the function(s) below.

**Define:**
- `high_priority_titles(records)`

**What the grader runs** (each value is scored **separately**, so a partly-correct answer still earns marks):
- `len(high_priority_titles([{'title':'A','priority':'high'},{'title':'B','priority':'low'},{'title':'C','priority':'high'}]))`  →  `2`
- `high_priority_titles([{'title':'A','priority':'high'},{'title':'B','priority':'low'},{'title':'C','priority':'high'}])[0]`  →  `A`
- `high_priority_titles([{'title':'A','priority':'high'},{'title':'B','priority':'low'},{'title':'C','priority':'high'}])[1]`  →  `C`

Return the exact value shown (a list stays a list; round numbers only if the task says so). **`return` the value — do not `print` it.**

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
