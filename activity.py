import collections.abc as abc

from random import choice

class Activity:

    def __init__(
        self, title: str, options: abc.Sequence=[],
        priority: int=1, limit: int=-1, url: str=None
        ):
        self.title = title
        self.options = options
        self.priority = priority
        self.limit = limit
        self.url = url

    # set a new priority and return self
    def setPriority(self, priority):
        self.priority = priority
        return self

    # set new options
    def setOptions(self, options):
        self.options = options
        return self

    def __key(self):
        return (self.title, self.priority, self.limit, self.url)

    def __hash__(self):
        return hash(self.__key())

    # ActivityTreeNode object equivalence
    def __eq__(self, other):
        if isinstance(other, Activity):
            return self.__key() == other.__key()
        return NotImplemented

class ActivityTreeNode:

    def __init__(self, activity, parent=None):
        self.activity = activity if isinstance(activity, Activity) \
            else activity.activity if isinstance(activity, ActivityTreeNode) \
            else Activity(activity)
        self.parent = parent

        # calculate further variables
        self.count = 0
        self.ancestry = parent.ancestry + [parent] if parent else []
        self.prob = (self.activity.priority * parent.prob) \
            / sum([x.priority if isinstance(x, Activity) else 1 for x in parent.activity.options]) \
            if parent else 1
        self.children = [ActivityTreeNode(option, self) for option in self.activity.options]

    def setProb(self, prob):
        self.prob = prob

    def displLimit(self):
        return "{}/{}".format(self.count, self.activity.limit) \
            if self.activity.limit != -1 else ""

    # get Activity's probability as a percentage
    def pctProb(self, prob=None):
        if not prob : prob = self.prob
        return "{} ({}%) {}".format(self.activity.title, round(prob * 100, 2), self.displLimit())

    # print full tree from this node down
    def displTree(self, spc=""):
        print("{}{}".format(spc, self.pctProb()))
        for child in self.children : child.displTree(spc+" ")

    # print task and all parents
    def displ(self):
        [print(t.activity.title) for t in self.ancestry[1:]]
        print(self.pctProb())

    # recurse through activity tree to select next activity
    def choose(self):

        # list indices with rank number of duplicates
        weighted = [] 
        [weighted.extend([x] * self.children[x].activity.priority) for x in range(len(self.children))]

        c = self.children[choice(weighted)]
        if c.children:
            return c.choose()
        else:
            return c

    def findNode(self, query):
        if self.activity.title == query : return self
        if self.children:
            for child in self.children:
                target = child.findNode(query)
                if target : return target
        
    def replaceWith(self, other):
        self.parent.children[self.parent.children.index(self)] = ActivityTreeNode(other, self.parent)

    def incrementCount(self):
        self.count += 1

    def isActive(self):
        return self.activity.limit == -1 or self.count < self.activity.limit

    def priorityValue(self):
        return 0 if not self.isActive() else self.activity.priority

    # calculate probability of current node being selected
    def calcProb(self):
        return (self.priorityValue() * self.parent.prob) \
            / sum([x.priorityValue() for x in self.parent.children]) \
            if self.parent else 1

    # update all probabilities in tree
    def updateProbs(self):
        self.setProb(self.calcProb())
        for child in self.children : child.updateProbs()

    def __key(self):
        return (self.activity, self.parent)

    def __hash__(self):
        return hash(self.__key())

    # ActivityTreeNode object equivalence
    def __eq__(self, other):
        if isinstance(other, ActivityTreeNode):
            return self.__key() == other.__key()
        return NotImplemented