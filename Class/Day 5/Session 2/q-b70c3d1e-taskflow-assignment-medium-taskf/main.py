import pandas as pd

def clean_tasks(records):
    """records: list[dict] messy task rows with keys:
    id, title, status, estimate_hours.
    Return a list of tidy dicts sorted ascending by id, where:
      - title  : stripped of surrounding whitespace
      - status : trimmed and lowercased
      - estimate_hours : float; non-numeric/missing -> 0.0; rounded to 2 dp
      - duplicate ids collapsed keeping the FIRST occurrence
    """
    if not records:
        return []
    df = pd.DataFrame(records)
    # TODO: clean title (str methods)
    # TODO: normalize status (str methods)
    # TODO: coerce estimate_hours (dtype coercion) and fill missing with 0.0
    # TODO: drop_duplicates on id keeping first, sort by id
    out = []
    # TODO: build list of dicts with native python types
    df['status'] = df['status'].str.strip().str.lower()

    df['estimate_hours']=(pd.to_numeric(df['estimate_hours'], errors='coerce').fillna(0.0).round(2))

    df = df.drop_duplicates(subset = 'id', keep = 'first')

    df = df.sort_values('id')

    for _,row in df.iterrows():
      out.append({
        'id':int(row['id']),
        'title': str(row['title']),
        'status': str(row['status']),
        'estimate_hours': float(row['estimate_hours'])
      })
    return out