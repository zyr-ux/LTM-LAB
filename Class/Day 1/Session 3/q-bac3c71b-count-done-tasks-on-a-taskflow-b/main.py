# TaskFlow board status string: t=todo, i=in_progress, r=review, d=done
statuses = "tttdirdt"

# TODO: total_tasks = number of tasks (length of the string)

# TODO: done_count = how many characters are "d" (use a for loop + if)

# TODO: completion_pct = int(done_count / total_tasks * 100)

# TODO: label = f-string "<done_count> of <total_tasks> tasks done"


total_tasks = len(statuses)

done_count = 0

for task in statuses:
    if task == "d":
        done_count+=1

completion_pct = int(done_count/total_tasks * 100)

label = f"{done_count} of {total_tasks} tasks done"