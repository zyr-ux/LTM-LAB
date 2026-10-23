class User:
    """A TaskFlow user who owns an ENCAPSULATED set of assigned tasks.

    Keep the task book private (self._tasks) and expose only the methods
    below. Assigning is idempotent; completing an unknown task is a no-op.
    """

    def __init__(self, user_id, name):
        self.id = user_id
        self.name = name
        self._tasks = {}          # task_id -> status

    def assign(self, task_id):
        # add task_id as "todo" if not already present; return self
        if task_id not in self._tasks:
            self._tasks[task_id]='todo'
        return self

    def complete(self, task_id):
        # mark an assigned task "done" (ignore unknown ids); return self
        if task_id in self._tasks:
            self._tasks[task_id]='done'
        return self

    def task_status(self, task_id):
        # return the task's status, or "unassigned" if not owned
        if task_id not in self._tasks:
            return 'unassigned'
        else:
            return self._tasks[task_id]

    def open_count(self):
        # number of owned tasks whose status is not "done"
        c=0
        for status in self._tasks.values():
            if status != 'done':
                c+=1
        
        return c

    def workload(self):
        # {"total": n, "open": not-done, "done": done}
        return {'total':len(self._tasks),'open':self.open_count(),'done':len(self._tasks)-self.open_count()}

    def __repr__(self):
        # User(id='...', name='...', tasks=<count>)
        return f"User(id='{self.id}', name='{self.name}', tasks={len(self._tasks)})"