import pandas as pd


def high_priority_titles(records):
    # `records` is a list of task dicts. Do NOT read any file.
    # 1. Build df = pd.DataFrame(records)
    # 2. Keep rows where priority == 'high' with a boolean mask
    # 3. Return the 'title' values as a plain list of strings ([] when none).
    df = pd.DataFrame(records)
    if df.empty:
        return []
    return df[df['priority'] == 'high']['title'].tolist();