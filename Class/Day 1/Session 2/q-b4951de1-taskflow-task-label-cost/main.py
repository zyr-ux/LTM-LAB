# Fixed facts for this task
task_id = 42
title = "Ship v2"
hourly_rate = 80.0
hours_logged = 3.5

# TODO: build an f-string label like "Task #42: Ship v2"
label = f"Task #{task_id}: {title}"

# TODO: compute the billable cost (hours_logged * hourly_rate)
cost = hours_logged*hourly_rate