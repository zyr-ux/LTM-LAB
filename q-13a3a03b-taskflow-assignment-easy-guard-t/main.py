"""TaskFlow S9 - Easy. Fill in the TODOs. Do not use input()/print for grading."""

class TaskFlowError(Exception):
    """Base of every TaskFlow domain error."""
    pass

# TODO: define InvalidStatusError as a subclass of TaskFlowError

class InvalidStatusError(TaskFlowError):
    pass


VALID_STATUSES = {"todo", "in_progress", "done", "blocked"}

def validate_status(status):
    # TODO: return status if it is in VALID_STATUSES,
    #       otherwise raise InvalidStatusError(f"invalid status: {status}")
    if status in VALID_STATUSES:
        return status
    else:
        raise InvalidStatusError(f'invalid status: {status}')
    pass

def safe_validate_status(status):
    # TODO: call validate_status inside try/except.
    #       Return the status on success; on InvalidStatusError return
    #       the string f"error: {the exception message}"
    try:
        validate_status(status)
        return status
    except InvalidStatusError as er:
        return f'error: {er}'

    pass