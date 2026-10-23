# Record a TaskFlow task AND the name of each value's type.

# TODO: task_id -> the integer 7

# TODO: estimate_hours -> the float 8.0

# TODO: status -> the string "open"

# TODO: is_blocked -> the boolean False

# Now capture each value's type NAME as a string using type(...).__name__
# TODO: id_type = type(task_id).__name__

# TODO: estimate_type = type(estimate_hours).__name__

# TODO: status_type = type(status).__name__

# TODO: blocked_type = type(is_blocked).__name__

# Print a few of them:
# print(task_id)
# print(id_type)
# print(estimate_type)

task_id = 7
estimate_hours = 8.0
status = "open"
is_blocked=False

id_type = type(task_id).__name__
estimate_type = type(estimate_hours).__name__
status_type = type(status).__name__
blocked_type = type(is_blocked).__name__