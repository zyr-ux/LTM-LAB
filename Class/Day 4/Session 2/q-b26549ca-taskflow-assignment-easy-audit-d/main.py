import functools

def audit(func):
    """Count how many times a TaskFlow operation runs.
    Use functools.wraps so the wrapped function keeps its name and docstring.
    Store the running total on wrapper.calls (start it at 0)."""
    # TODO: define wrapper, increment wrapper.calls, call func, return result
    # TODO: initialise wrapper.calls = 0 and return wrapper
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)

    wrapper.calls = 0
    return wrapper
    pass

@audit
def complete_task(task):
    """Mark a TaskFlow task as done."""
    # TODO: if 'id' not in task -> return {'error': 'missing id'}
    # TODO: otherwise return {'id': <id>, 'status': 'done'}
    if 'id' not in task:
        return {'error':'missing id'}

    return {'id':task['id'],'status':'done'}
    pass

def count_calls(n):
    """Reset the counter, run complete_task n times, return complete_task.calls."""
    complete_task.calls = 0
    for _ in range(n):
        complete_task({'id':1})

    return complete_task.calls
    # TODO
    pass