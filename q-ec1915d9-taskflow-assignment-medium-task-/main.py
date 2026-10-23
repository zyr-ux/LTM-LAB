"""TaskFlow S9 - Medium. Complete the hierarchy and the reporting function."""

class TaskFlowError(Exception):
    pass

class ValidationError(TaskFlowError):
    pass

# TODO: MissingFieldError and InvalidValueError, both subclasses of ValidationError

class MissingFieldError(ValidationError):
    pass

class InvalidValueError(ValidationError):
    pass


VALID_STATUSES = {"todo", "in_progress", "done", "blocked"}
REQUIRED_FIELDS = ("title", "status", "priority")

def validate_task(task):
    # TODO: raise MissingFieldError("missing field: <name>") for any absent required field.
    # TODO: raise InvalidValueError for: empty/whitespace title, bad status,
    #       priority not an int in 1..5 (reject booleans too). Return True if ok.

    for field in REQUIRED_FIELDS:
        if field not in task:
            raise MissingFieldError(f'missing field: {field}')
        
    if task['title'].strip() == '':
        raise InvalidValueError('empty title')

    if task['status'] not in VALID_STATUSES:
        raise InvalidValueError(f"invalid status: {task['status']}")

    priority=task['priority']

    if priority<1 or priority>5 or type(priority) is not int:
        raise InvalidValueError('priority must be an int in 1..5')

    return True
    pass

def validate_task_report(task):
    # TODO: call validate_task inside try/except/else/finally and build a report dict:
    #   ok      -> {"valid": True,  "error_type": None,               "message": "ok"}
    #   missing -> {"valid": False, "error_type": "MissingFieldError","message": <str(exc)>}
    #   invalid -> {"valid": False, "error_type": "InvalidValueError","message": <str(exc)>}
    # In finally, add result["checked"] = True. Return the report.

    result = {}
    try:
        validate_task(task)
        result = {'valid':True,'error_type':None,'message':'ok'}
    except MissingFieldError as MFE:
        result = {'valid':False,'error_type':'MissingFieldError','message':str(MFE)}
    except InvalidValueError as IVE:
        result={'valid':False, 'error_type':'InvalidValueError','message':str(IVE)}
    finally:
        result['checked']=True
    
    return result
    pass