import collections.abc as abc

from random import choice

class Activity():

    def __init__(self, title: str, options: abc.Sequence=[], priority: int=1, rep: bool=True, url: str=None):
        self.title = title
        self.options = options
        self.priority = priority
        self.rep = rep
        self.url = url

        # [Activity(options)] if isinstance(options, str) else [Activity(option) for option in options]

    # set a new priority and return self
    def setPriority(self, priority):
        self.priority = priority
        return self

    def __eq__(self, other):
        return vars(self) == vars(other)

class ActivityTreeNode():

    def __init__(self, activity, parent=None):
        self.activity = activity if isinstance(activity, Activity) \
            else activity.activity if isinstance(activity, ActivityTreeNode) \
            else Activity(activity)
        self.parent = parent

        # calculate further variables
        self.ancestry = parent.ancestry + [parent] if parent else []
        self.prob = (self.activity.priority / sum(
            [x.priority if isinstance(x, Activity) else 1 for x in parent.activity.options]
            )) * parent.prob if parent else 1
        self.children = [ActivityTreeNode(option, self) for option in self.activity.options]

    # get Activity's probability as a percentage
    def pctProb(self):
        return "{} ({}%)".format(self.activity.title, round(self.prob * 100, 2))

    # print full tree from this node down
    def displTree(self, spc=""):
        print("{}{}".format(spc, self.pctProb()))
        for child in self.children : child.displTree(spc+" ")

    # print task and all parents
    def displ(self):
        [print(t.activity.title) for t in self.ancestry]
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
    
    # how ActivityTreeNode object will be compared with other ActivityTreeNode objects
    def __lt__(self, other):
        return self.prob < other.prob

    # ActivityTreeNode object equivalence
    def __eq__(self, other):
        return vars(self) == vars(other)