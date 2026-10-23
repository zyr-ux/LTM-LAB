class Task:
    """Base task in the TaskFlow board.
    Store title and priority; every new task starts with status 'todo'.
    """
    def __init__(self, title, priority='medium'):
        # TODO: set self.title, self.priority, self.status
        self.title=title
        self.priority=priority
        self.status='todo'

    def label(self):
        # TODO: return f"[TASK] <title> (<priority>)"
        return f"[TASK] {self.title} ({self.priority})"
        pass


class BugTask(Task):
    """A bug. Adds a `severity` (default 'minor'). Reuse Task via super()."""
    def __init__(self, title, priority='medium', severity='minor'):
        # TODO: call super().__init__(...) then set self.severity
        super().__init__(title,priority)
        self.severity=severity

    def label(self):
        # TODO: return f"[BUG] <title> (<priority>/<severity>)"
        return f"[BUG] {self.title} ({self.priority}/{self.severity})"


class FeatureTask(Task):
    """A feature. Adds `story_points` (default 1). Reuse Task via super()."""
    def __init__(self, title, priority='medium', story_points=1):
        # TODO
        super().__init__(title,priority)
        self.story_points=story_points

    def label(self):
        # TODO: return f"[FEATURE] <title> (<priority>) sp=<story_points>"
        return f"[FEATURE] {self.title} ({self.priority}) sp={self.story_points}"