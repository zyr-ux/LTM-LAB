def create_task(store, task_id, title, status='todo'):
    
    if task_id in store:
        return({'error':'exists'},409)
    
    task = {
        'id':task_id,
        'title':title,
        'status':status
    }
    store[task_id] = task
    return (task,201)
    #raise NotImplementedError("Write your solution here")


def get_task(store, task_id):
    # TODO: (task, 200) if present else (None, 404)
    #raise NotImplementedError("Write your solution here")
    if task_id in store:
        return (store[task_id],200)
    return(None,404)


def update_task(store, task_id, fields):
    # TODO: (None, 404) if missing
    # TODO: apply fields but NEVER allow 'id' to change; return (task, 200)
    #raise NotImplementedError("Write your solution here")
    if task_id not in store:
        return (None,404)

    for key,value in fields.items():
        if key != 'id':
            store[task_id][key] = value

    return (store[task_id],200)

def delete_task(store, task_id):
    # TODO: (True, 200) on success else (None, 404)
    #raise NotImplementedError("Write your solution here")
    if task_id not in store:
        return (None,404)

    del store[task_id]
    return (True,200)


def list_tasks(store, status=None):
    # TODO: return (list_of_tasks, 200); when status is given, filter by it
    #raise NotImplementedError("Write your solution here")

    tasks = list(store.values())

    if status is not None:
        tasks = [task for task in tasks if task.get('status') == status]

    return (tasks,200)