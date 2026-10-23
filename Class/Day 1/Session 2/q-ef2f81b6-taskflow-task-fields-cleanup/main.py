# Fixed facts for this task
task_id = 7
title = "  Refactor Login  "
hourly_rate = 65.0
hours_logged = 12
estimated_hours = 10

# TODO: strip surrounding whitespace from title
title_clean = title.strip();

# TODO: cost = hours_logged * hourly_rate
cost = hours_logged * hourly_rate

# TODO: is hours_logged greater than estimated_hours?
over_estimate = hours_logged > estimated_hours

# TODO: f-string "Task #7: Refactor Login"
label = f"Task #{task_id}: {title}"

# TODO: title_clean in uppercase
title_upper = title_clean.upper()

# TODO: number of characters in title_clean
name_len = len(title_clean)