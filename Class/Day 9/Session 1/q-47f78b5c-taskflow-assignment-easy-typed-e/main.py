# TaskFlow — Error Signaling (Easy)
# Build a small exception hierarchy and one mapper function.
#
# Requirements:
#   * Base class TaskFlowError(Exception) with class attrs status=500, code='internal_error'.
#   * Subclasses (each sets its own status + code):
#       ValidationError      -> 422, 'validation_error'
#       NotFoundError        -> 404, 'not_found'
#       PermissionDeniedError-> 403, 'permission_denied'
#       ConflictError        -> 409, 'conflict'
#   * error_response(exc) -> {'status': <int>, 'code': <str>, 'message': str(exc)}

class TaskFlowError(Exception):
    status = 500
    code = 'internal_error'

class ValidationError(TaskFlowError):
    status = 422
    code = 'validation_error'

class NotFoundError(TaskFlowError):
    status = 404
    code = 'not_found'

class PermissionDeniedError(TaskFlowError):
    status = 403
    code = 'permission_denied'

class ConflictError(TaskFlowError):
    status = 409
    code = 'conflict'

def error_response(exc):
    # Read status, code, and message off the exception and return as a plain dict
    return {
        'status': exc.status,
        'code': exc.code,
        'message': str(exc),
    }