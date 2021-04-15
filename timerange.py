from datetime import datetime, time

class TimeRange():
    def __init__(self, start: int, end: int, name: str=None, priorities=None):
        self.start = time(start)
        self.end = time(23, 59, 59) if end in (24, 0) else time(end)
        self.name = name
        self.priorities = priorities

    def isNow(self):
        t = datetime.now().time()
        before = t >= self.start
        after = t < self.end
        if self.end < self.start : return before or after
        return before and after

    def pick(times):
        return [x.priorities for x in times if x.isNow()][0]