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
        for time in times:
            if time.isNow() : return time

    def __key(self):
        return (self.start, self.end, self.name)

    def __hash__(self):
        return hash(self.__key())

    # TimeRange object equivalence
    def __eq__(self, other):
        if isinstance(other, TimeRange):
            return self.__key() == other.__key()
        return NotImplemented