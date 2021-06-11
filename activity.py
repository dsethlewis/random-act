import datetime
from collections.abc import Sequence
from random import choice

class Activity:
    def __init__(self, title: str, options: Sequence=[],
                 priority: int=1, limit: int=-1, url: str=None):
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

    # Activity object equivalence
    def __eq__(self, other):
        if isinstance(other, Activity):
            return self.__key() == other.__key()
        return NotImplemented

class ActivityTreeNode:

    def __init__(self, activity, parent=None):
        self.activity = activity if isinstance(activity, Activity) \
            else activity.activity if isinstance(activity, ActivityTreeNode) \
            else Activity(**activity) if isinstance(activity, dict) \
            else Activity(activity)
        self.parent = parent

        # calculate further variables
        self.count = 0
        self.ancestry = parent.ancestry + [parent] if parent else []
        self.prob = 0
        self.children_weight = 0
        self.children = [ActivityTreeNode(option, self) for option in self.activity.options]

    def setProb(self, prob):
        self.prob = prob

    def addChild(self, child: Activity):
        self.children.append(ActivityTreeNode(child, self))
        # self.activity.options.append(child)

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
        # print("{}{}".format(spc, type(self.activity)))
        for child in self.children : child.displTree(spc+"-")
        
    # print task and all parents
    def displ(self):
        [print(t.activity.title) for t in self.ancestry[1:]]
        print(self.pctProb())

    def ancestryStr(self):
        return '/'.join([a.activity.title for a in self.ancestry])

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
        # print("{} == {}?".format(query, self.activity.title))
        if self.activity.title == query : return self
        if self.children:
            for child in self.children:
                target = child.findNode(query)
                if target : return target
        
    def replaceWith(self, other):
        # self.parent.activity.options[self.parent.activity.options.index(self.activity)] = other
        self.parent.children[self.parent.children.index(self)] = ActivityTreeNode(other, self.parent)

    def incrementCount(self):
        self.count += 1

    def isActive(self):
        return self.activity.limit == -1 or self.count < self.activity.limit

    def priorityValue(self):
        return self.activity.priority if self.isActive() else 0

    # calculate probability of current node being selected
    def calcProb(self):
        return (self.priorityValue()
                * self.parent.prob
                / self.parent.children_weight) if self.parent else 1

    # update all probabilities in tree
    def updateProbs(self):
        self.children_weight = sum([c.priorityValue() for c in self.children])
        self.setProb(self.calcProb())
        assert self.prob >= 0 and self.prob <= 1, \
            ("["
             + self.activity.title
             + "]'s probability is invalid: "
             + str(self.prob))
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

class Task:
    def __init__(self, due = None):
        self.due = due

    # check if task is due yet
    def isDue(self):
        if not self.due : return True
        return datetime.datetime.now().date() >= self.due