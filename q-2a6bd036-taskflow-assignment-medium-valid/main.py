# TaskFlow — Error Signaling (Medium)
# A validation layer that RAISES, wrapped by a caller that CATCHES into an error dict.
#
# validate_task(payload) raises ValidationError(message, field=...) on the FIRST bad field:
#   * title: required, non-empty string (after strip)      -> field 'title'
#   * status: optional, default 'todo', in {todo,in_progress,done} -> field 'status'
#   * priority: optional, default 'medium', in {low,medium,high}   -> field 'priority'
#   * estimate_hours: optional; if present must be a real number >= 0 (bool is NOT a number)
#                                                          -> field 'estimate_hours'
#   * non-dict payload -> ValidationError('payload must be an object', field=None)
#   On success returns {'title': <stripped>, 'status': ..., 'priority': ...}
#
# submit_task(payload) calls validate_task and returns:
#   success -> {'ok': True, 'task': <validated dict>}
#   failure -> {'ok': False, 'error': {'status':422,'code':'validation_error','message':...,'field':...}}

class TaskFlowError(Exception):
    status = 500
    code = 'internal_error'

class ValidationError(TaskFlowError):
    status = 422
    code = 'validation_error'
    def __init__(self, message, field=None):
        super().__init__(message)
        self.field = field

def validate_task(payload):
    # 1. payload must be a dict
    if not isinstance(payload, dict):
        raise ValidationError('payload must be an object', field=None)

    # 2. title: required, non-empty after stripping whitespace
    title = payload.get('title', '')
    if not isinstance(title, str) or title.strip() == '':
        raise ValidationError('title is required', field='title')
    title = title.strip()

    # 3. status: optional, defaults to 'todo', must be a valid value
    status = payload.get('status', 'todo')
    valid_statuses = {'todo', 'in_progress', 'done'}
    if status not in valid_statuses:
        raise ValidationError(f'status must be one of {valid_statuses}', field='status')

    # 4. priority: optional, defaults to 'medium', must be a valid value
    priority = payload.get('priority', 'medium')
    valid_priorities = {'low', 'medium', 'high'}
    if priority not in valid_priorities:
        raise ValidationError(f'priority must be one of {valid_priorities}', field='priority')

    # 5. estimate_hours: optional, but if present must be a real number >= 0 (bool is NOT allowed)
    if 'estimate_hours' in payload:
        hours = payload['estimate_hours']
        # bools are a subclass of int in Python, so we must reject them explicitly
        if isinstance(hours, bool) or not isinstance(hours, (int, float)) or hours < 0:
            raise ValidationError('estimate_hours must be a non-negative number', field='estimate_hours')

    # All checks passed — return the cleaned/normalised task dict
    return {'title': title, 'status': status, 'priority': priority}

def submit_task(payload):
    try:
        validated = validate_task(payload)
        return {'ok': True, 'task': validated}
    except ValidationError as exc:
        return {
            'ok': False,
            'error': {
                'status': 422,
                'code': 'validation_error',
                'message': str(exc),
                'field': exc.field,
            },
        }