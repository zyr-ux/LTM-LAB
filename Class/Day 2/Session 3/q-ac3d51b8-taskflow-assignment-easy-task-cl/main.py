class Task:
    """A single TaskFlow task with a lifecycle.

    Attributes:
        id     : the task identifier (any value)
        title  : task title; empty/None must become "Untitled"
        status : one of "todo" / "in_progress" / "done";
                 any other value must default to "todo"
    """
    ALLOWED = {"todo", "in_progress", "done"}

    def __init__(self, task_id, title="Untitled", status="todo"):
        # TODO: set self.id, self.title (default "Untitled"),
        #       self.status (default "todo" if not allowed)
        self.id = task_id
        self.title = title
        self.status = status

        if (status=='') or (status not in Task.ALLOWED):
            self.status='todo'

        if title=='':
            self.title='Untitled'

    def mark_done(self):
        # TODO: set status to "done" and return self (so calls can chain)
        self.status='done'
        return self
        

    def reopen(self):
        # TODO: set status to "todo" and return self
        self.status = 'todo'
        return self

    def is_done(self):
        # TODO: return True only when status == "done"
        if(self.status == 'done'):
            return True
        else:
            return False

    def __repr__(self):
        # TODO: return  Task(id=..., title='...', status='...')
        return f"Task(id={self.id}, title='{self.title}', status='{self.status}')"
        #return "Task(id={},title='{}',status='{}')".format(self.id,self.title,self.status)
