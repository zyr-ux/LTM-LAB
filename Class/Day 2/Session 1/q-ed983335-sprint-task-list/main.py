# TaskFlow — this sprint has four tasks, in order:
#   "Design login page", "Write API tests", "Write API tests", "Deploy release"

# TODO: build a list called task_titles with the four titles above, in order
task_titles = []

# TODO: first_task  = the first title in the list (indexing)
# TODO: last_task   = the last title in the list (indexing, e.g. [-1])
# TODO: task_count  = how many titles are in the list (len)
# TODO: has_deploy  = is "Deploy release" in the list? (membership with in)
task_titles.append("Design login page")
task_titles.append("Write API tests")
task_titles.append("Fix payment bug")
task_titles.append("Deploy release")

first_task=task_titles[0]
last_task=task_titles[len(task_titles)-1]
task_count=len(task_titles)
if (task_titles.__contains__("Deploy release")):
    has_deploy=True