STATUSES = ["todo", "in_progress", "review", "done"]


def tasks_fixture():
    return [
        {"id": 1, "title": "Design schema", "status": "done", "priority": 3, "estimate_hours": 4.0},
        {"id": 2, "title": "Build API", "status": "in_progress", "priority": 5, "estimate_hours": 8.0},
        {"id": 3, "title": "Write unit tests", "status": "todo", "priority": 2, "estimate_hours": 3.0},
        {"id": 4, "title": "Deploy to staging", "status": "todo", "priority": 4, "estimate_hours": 2.0},
        {"id": 5, "title": "Review PR", "status": "done", "priority": 1, "estimate_hours": 1.5},
    ]


def build_status_summary(tasks):
    # Return total, by_status (all 4 keys), done, completion_rate,
    # total_estimate_hours, done_estimate_hours.

    by_status = {status: 0 for status in STATUSES}

    total_estimate_hours = 0.0
    done_estimate_hours = 0.0

    for task in tasks:
        status = task.get('status')
        
        if status in by_status:
            by_status[status]+=1
        
        hours = float(task.get('estimate_hours',0.0))
        total_estimate_hours +=hours

        if status == 'done':
            done_estimate_hours += hours

    total = len(tasks)
    done = by_status['done']

    completion_rate = round(done/total,4) if total else 0.0

    return {
        'total':total,
        'by_status':by_status,
        'done':done,
        'completion_rate':completion_rate,
        'total_estimate_hours':round(total_estimate_hours,4),
        'done_estimate_hours':round(done_estimate_hours,4)
    }
    pass