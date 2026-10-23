def summarize_tasks(tasks, include_rate=True):
    by_status = {}
    for t in tasks:
        # TODO: count tasks per status; use 'unknown' when 'status' is missing
        status=t.get('status','unknown')
        by_status[status]=by_status.get(status,0)+1
    total = len(tasks)
    result = {'total': total, 'by_status': by_status}
    if include_rate:
        # TODO: add 'rate' = percent of 'done' tasks (1 decimal). 0.0 when empty.
        if(tasks==[]):
            result = {'total': 0, 'by_status': {},'rate':0.0}
        else:
            rate = round(by_status.get('done', 0) / total * 100, 1)
            result = {'total':total,'by_status':by_status,'rate':rate}
            return result
        
    return result

