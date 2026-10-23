import json


def status_counts_json(tasks):
    if tasks is None:
        return "{}"
    counts = {}
    # TODO: tally each task's status into counts (missing/empty status -> 'unknown')
    # TODO: return the tally as a sorted-key JSON string
    for task in tasks:
        status = task.get('status','unknown')
        if status == '':
            status = 'unknown'
        counts[status]=counts.get(status,0)+1

    return json.dumps(counts,sort_keys=True)
    pass