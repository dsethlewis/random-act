import time

class PomodoroTimer:

    def __init__(self):
        self.start = time.time()
        self.prev = self.start

    def nowInMinutes(self, t1=None):
        if not t1 : t1 = time.time() - self.start
        return t1 / 60

    def isOnBreak(self, t1=None):
        return self.nowInMinutes(t1) % 30 > 25

    def count(self):
        n = self.nowInMinutes() // 30
        if self.isOnBreak() : n += 1
        return n

    def ring(self):
        prev = self.prev
        self.prev = time.time()
        return self.isOnBreak() != self.isOnBreak(prev)