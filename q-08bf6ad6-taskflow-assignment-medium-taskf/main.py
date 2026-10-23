class Task:
    def __init__(self, title, estimate_hours, logged_hours=0):
        self.title = title
        self.estimate_hours = estimate_hours
        self.logged_hours = logged_hours

    @property
    def remaining_hours(self):
        # TODO: never below 0
        diff = self.estimate_hours - self.logged_hours
        if diff > 0:
            return diff
        return 0
        pass

    @property
    def is_complete(self):
        # TODO
        return True if self.logged_hours>=self.estimate_hours else False
        pass

    def weight(self):
        # base weight is just the estimate (as float)
        return float(self.estimate_hours)


class BugTask(Task):
    SEVERITY_MULT = {'minor': 1.0, 'major': 1.5, 'critical': 2.0, 'blocker': 3.0}
    # TODO: __init__ adds `severity`; weight() = base weight * severity multiplier, rounded to 2
    def __init__(self,title,estimate_hours,severity,logged_hours=0):
        super().__init__(title,estimate_hours,logged_hours)
        self.severity=severity
    
    def weight(self):
        return super().weight() * BugTask.SEVERITY_MULT[self.severity]


class FeatureTask(Task):
    # TODO: __init__ adds `story_points`; weight() = base weight + story_points*2, rounded to 2
    def __init__(self,title,estimate_hours,story_points,logged_hours=0):
        super().__init__(title,estimate_hours,logged_hours)
        self.story_points=story_points
    
    def weight(self):
        return round(super().weight() + self.story_points*2,2)
    pass


def build_task(kind, title, estimate_hours, extra, logged_hours=0):
    """Factory. Return 'error: negative estimate' if estimate_hours < 0,
    'error: unknown kind' for an unknown kind, else the built task object."""
    # TODO
    if estimate_hours < 0:
        return 'error: negative estimate'
    
    if kind == 'bug':
        return BugTask(title,estimate_hours,extra,logged_hours)
    elif kind == 'feature':
        return FeatureTask(title,estimate_hours,extra,logged_hours)
    elif kind == 'task':
        return Task(title,estimate_hours,logged_hours)
    else:
        return 'error: unknown kind'
    pass