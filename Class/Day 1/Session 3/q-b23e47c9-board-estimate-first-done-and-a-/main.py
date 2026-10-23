statuses = "tttdirdt"
total_tasks = len(statuses)

# TODO: total_hours via a WHILE loop (index i from 0):
#   +1 for each 'd', +3 for every other task

# TODO: first_done_index — start at -1, for idx in range(total_tasks),
#   at first 'd' store idx and break

# TODO: progress_bar — string accumulator: '#' for done, '.' otherwise

# TODO: headline — f-string "First done at index <first_done_index>, <total_hours>h total"


i = 0
total_hours = 0

while i < len(statuses):
    if(statuses[i]=='d'):
        total_hours+=1
    else:
        total_hours+=3
    i+=1

first_done_index = -1

for idx in range(total_tasks):
    if(statuses[idx]=='d'):
        first_done_index=idx
        break

progress_bar = ""

for task in statuses:
    if(task=='d'):
        progress_bar+='#'
    else:
        progress_bar+='.'

headline=f"First done at index {first_done_index}, {total_hours}h total"

print(total_hours)
print(first_done_index)
print(progress_bar)