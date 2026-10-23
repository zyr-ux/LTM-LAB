import pandas as pd


def status_counts(records):
    # `records` is a list of task dicts. Do NOT read any file.
    # 1. Build a DataFrame: df = pd.DataFrame(records)
    # 2. Count the 'status' column (value_counts) and return a plain dict
    #    {status: int_count}. Return {} when there are no records.
    df = pd.DataFrame(records)
    if not records:
        return {}
    
    count_dict={}
    counts=df['status'].value_counts()
    for status,count in counts.items():
        count_dict[status] = int(count)

    return count_dict