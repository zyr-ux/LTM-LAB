def task_status_code(task_id, task_ids):
    # Return 200 if the task exists, else 404
    return 200 if task_id in task_ids else 404
    pass