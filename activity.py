import random

# define an activity object
class Activity:

    def __init__(self, title, children = [], parent = None, rank = 1):
        self.title = title # text of activity
        self.children = [] # sub-categories of activity
        self.rank = rank # how many times an activity should appear in tree
        self.parent = parent
        self.prob = (rank / parent.n_children) * parent.prob if parent else 1
        self.n_children = 1
        if children:
            self.n_children = sum([x.rank if type(x) == Activity else 1 for x in children])
            self.addChild(children)

    def addChild(self, a):
        '''Constructs a hierarchical activity tree.'''
        if type(a) == str:
            self.children.append(Activity(a, parent = self))
        elif type(a) == Activity:
            self.children.append(Activity(a.title, a.children, self, a.rank))
        elif type(a) == list:
            [self.addChild(x) for x in a]

    # return true if children attribute is not empty
    def hasChild(self):
        return bool(self.children)
    
    # recurse through activity tree to select next activity
    def choose(self):
        weighted = []
        [weighted.extend([x] * self.children[x].rank) for x in range(len(self.children))]
        c = self.children[random.choice(weighted)]
        print("{} ({})".format(c.title, round(c.prob, 3)))
        if c.hasChild():
            c.choose()
    
    # set a new rank and return self
    def changeRank(self, new_rank):
        self.rank = new_rank
        return self

    # how object will appear when printed
    def __repr__(self):
        return "<Activity title:%s>" % (self.title)

# create an alias for the object
act = Activity