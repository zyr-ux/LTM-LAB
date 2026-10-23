def tasks_fixture():
    return [
        {"id": 1, "title": "Design schema", "status": "done", "priority": 3, "estimate_hours": 4.0},
        {"id": 2, "title": "Build API", "status": "in_progress", "priority": 5, "estimate_hours": 8.0},
        {"id": 3, "title": "Write unit tests", "status": "todo", "priority": 2, "estimate_hours": 3.0},
        {"id": 4, "title": "Deploy to staging", "status": "todo", "priority": 4, "estimate_hours": 2.0},
        {"id": 5, "title": "Review PR", "status": "review", "priority": 1, "estimate_hours": 1.5},
    ]


def filter_tasks(tasks, status):
    # Return the tasks whose status matches; "all" means every task.
    if status == 'all':
        return list(tasks)
    
    return [task for task in tasks if task['status'] == status]
    pass