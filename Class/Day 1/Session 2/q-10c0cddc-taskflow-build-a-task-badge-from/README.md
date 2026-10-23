# TaskFlow: Build a Task Badge from Raw Input

## Convert and reshape raw form data

Raw task data comes in from a form as **text**, so numbers arrive as strings and must be converted before you can do math. You'll convert, calculate, and reformat. These fixed facts are already assigned:

- `task_id = 128`
- `raw_title = "deploy api gateway"`
- `hours_str = "6"`  (a string!)
- `rate_str = "72.5"`  (a string!)
- `assignee = "Priya Menon"`

### A quick example

```python
n = int("6")                 # 6      (text -> whole number)
r = float("72.5")            # 72.5   (text -> decimal)
nice = "deploy api".title()  # "Deploy Api"
first3 = "deploy"[:3]        # "dep"  (slice: first 3 characters)
letter = "Priya"[0]          # "P"    (indexing: one character)
```

`int(...)` and `float(...)` convert text to numbers, `.title()` capitalises each word, `[:3]` slices a piece of a string, and `[0]` reads one character by position. You'll combine these with arithmetic, a comparison, and an f-string.

**Concepts you'll use:** type conversion (`int`, `float`), arithmetic, comparison, f-strings, string methods (`.title()`, `.upper()`), slicing and indexing.

### What to define
- `hours` — `hours_str` converted to an int (`int(...)`) → `6`.
- `rate` — `rate_str` converted to a float (`float(...)`) → `72.5`.
- `cost` — `hours * rate` (a float).
- `title_pretty` — `raw_title` in title-case (`.title()`) → `"Deploy Api Gateway"`.
- `code` — the first 3 characters of `raw_title`, uppercased (slice `[:3]` then `.upper()`) → `"DEP"`.
- `initials` — the assignee's initials by indexing: `assignee[0] + assignee[6]` → `"PM"`.
- `label` — f-string `Task #<id>: <title_pretty> (<initials>)`.
- `is_expensive` — a bool: is `cost` greater than `400`?

### What the grader checks
- `cost` → `435.0`
- `title_pretty` → `"Deploy Api Gateway"`
- `initials` → `"PM"`

No functions, dictionaries, lists, loops, or conditionals.

---
Edit **main.py** in this folder. **Run Test** (in the platform) grades it.
