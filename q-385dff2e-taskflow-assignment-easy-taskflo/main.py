import pandas as pd

def fill_missing_status(records):
    """records: list[dict] of task rows. Return a list of each row's status
    with MISSING statuses filled as "todo".
    Missing = None, NaN, an absent "status" key, or a blank/whitespace-only string.
    """
    if not records:
        return []
    df = pd.DataFrame(records)
    # TODO: ensure a "status" column exists even if some/all rows lack it
    # TODO: treat blank / whitespace-only strings as missing
    # TODO: fill missing with "todo" and return df["status"].tolist()
    if 'status' not in df.columns:
        df['status'] = 'todo'
    
    df['status'] = df['status'].fillna('todo')
    df.loc[df['status'].fillna('').str.strip() == '', 'status'] = pd.NA
    df['status'] = df['status'].fillna('todo')
    # df = df.replace()
    return df['status'].tolist()