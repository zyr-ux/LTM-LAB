def stream_open_tasks(tasks):
    """Yield the 'title' of every task whose status is not 'done'.
    Must be a GENERATOR (use yield) -- do not build and return a list.
    """
    # TODO: loop over tasks and yield the title of each open task
    for task in tasks:
        if task.get('status') != 'done':
            yield task.get('title')
    pass