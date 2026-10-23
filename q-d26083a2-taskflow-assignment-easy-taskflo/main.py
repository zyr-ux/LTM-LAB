def create_task(store, task_id, title):
    # TODO: if task_id already in store -> return ({'error': 'exists'}, 409)
    # TODO: build task = {'id': ..., 'title': ..., 'status': 'todo'}
    # TODO: save it in store and return (task, 201)
    pass
    if task_id in store:
        return({'error':'exists'},409)
    
    task = {
        'id':task_id,
        'title':title,
        'status':'todo'
    }

    store[task_id] = task
    return(task,201)

def get_task(store, task_id):
    # TODO: return (task, 200) when present, else (None, 404)
    pass
    if task_id in store:
        return (store[task_id],200)

    return (None, 404)