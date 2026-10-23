# Raw form input for this task
task_id = 128
raw_title = "deploy api gateway"
hours_str = "6"
rate_str = "72.5"
assignee = "Priya Menon"

# TODO: convert hours_str to int
hours = int(hours_str)

# TODO: convert rate_str to float
rate = float(rate_str)

# TODO: cost = hours * rate
cost = hours*rate

# TODO: raw_title in title-case
title_pretty = raw_title.title()

# TODO: first 3 chars of raw_title, uppercased
code = raw_title[:3].upper()

# TODO: assignee[0] + assignee[6]
initials = assignee[0] + assignee[6]

# TODO: f-string "Task #128: Deploy Api Gateway (PM)"
label = f"Task #{task_id}: {title_pretty} ({initials})"

# TODO: is cost greater than 400?
is_expensive = cost>400