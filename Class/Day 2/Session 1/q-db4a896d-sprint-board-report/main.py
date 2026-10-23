# TaskFlow sprint board — each task is a tuple: (id, title, status, assignee, hours)
tasks = [
    (1, "Design login page", "done", "Ava", 4.0),
    (2, "Write API tests", "todo", "Ben", 3.0),
    (3, "Fix payment bug", "in_progress", "Ava", 5.5),
    (4, "Deploy release", "todo", "Cara", 2.0),
    (5, "Review PR", "done", "Ben", 1.5),
]

# Start with empty containers, then fill them in ONE for loop over tasks:
task_titles = []       # TODO: append each title (t[1])
status_counts = {}     # TODO: count each status (t[2]) with if/else
unique_assignees = set()  # TODO: add each assignee (t[3])
total_hours = 0.0      # TODO: add each hours value (t[4])

# After the loop:
# TODO: sorted_titles  = task_titles sorted alphabetically (use sorted)
# TODO: assignee_count = number of distinct assignees (len of the set)
# TODO: has_ava        = is "Ava" one of the assignees? (membership with in)


for row in tasks:
    task_titles.append(row[1])

todo_count=0
done_count=0
in_progress_count=0

for i in tasks:
    if tasks[2] == 'done':
        done_count+=1
    elif tasks[2] == 'todo':
        todo_count+=1
    else:
        in_progress_count+=1

status_counts = {'done':done_count,
                'todo':todo_count,
                'in_progress':in_progress_count}

