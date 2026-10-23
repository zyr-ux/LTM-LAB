# TaskFlow — the status of each task in the sprint (with repeats):
statuses = ["todo", "done", "in_progress", "done", "todo", "done"]

# TODO: build status_counts, a dict mapping each status -> how many times it appears.
#       Use an empty dict, then a for loop over statuses with an if/else.
#       (NO comprehension, NO functions.)
status_counts = {}

# TODO: done_count = number of "done" tasks (read it from status_counts)
# TODO: total      = total number of tasks (len of statuses)
# TODO: has_todo    = is "todo" one of the keys in status_counts? (membership with in)

todo_count=0
done_count=0
in_progress_count=0

for task in statuses:
    if(task=='todo'):
        todo_count+=1
    elif(task=='done'):
        done_count+=1
    else:
        in_progress_count+=1
    status_counts={"todo":todo_count,
                    "done":done_count,
                    "in_progress_count":in_progress_count}

total = len(statuses)
has_todo = "todo" in status_counts
status_counts={'todo':todo_count,'done':done_count,'in_progress':in_progress_count}