import random

# define an activity object
class Activity:

    def __init__(self, title, children = [], parent = None, n_siblings = 1, rank = 1):
        self.title = title # text of activity
        self.children = [] # sub-categories of activity
        self.rank = rank # how many times an activity should appear in tree
        self.parent = parent
        self.n_siblings = n_siblings
        self.prob = (rank / n_siblings) * parent.prob if parent else 1
        self.n_children = 1
        if children:
            self.n_children = sum([x.rank if type(x) == Activity else 1 for x in children])
            self.addChild(children)

    def addChild(self, a):
        '''Constructs a hierarchical activity tree.'''
        if type(a) == str:
            act_a = Activity(a, parent = self, n_siblings = self.n_children)
            self.children.append(act_a)
        elif type(a) == Activity:
            act_a = Activity(a.title, a.children, self, self.n_children, a.rank)
            [self.children.append(act_a) for x in range(act_a.rank)]
        elif type(a) == list:
            for x in a:
                self.addChild(x)

    # return true if children attribute is not empty
    def hasChild(self):
        return bool(self.children)
    
    # recurse through activity tree to select next activity
    def choose(self):
        c = random.choice(self.children)
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