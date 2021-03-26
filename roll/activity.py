import random

# define an activity object
class Activity:

    def __init__(self, title, children = [], rank = 1):
        self.title = title # text of activity
        self.children = [] # sub-categories of activity
        self.rank = rank # how many times an activity should appear in tree
        if children:
            self.addChild(children)


    def addChild(self, a):
        '''Constructs a hierarchical activity tree.'''
        if type(a) == str:
            self.children.append(Activity(a))
        elif type(a) == Activity:
            self.children.extend([a] * a.rank)
        elif type(a) == list:
            for x in a:
                self.addChild(x)

    # return true if children attribute is not empty
    def hasChild(self):
        return bool(self.children)
    
    # recurse through activity tree
    def choose(self):
        c = random.choice(self.children)
        print(c.title)
        if c.hasChild():
            c.choose()
    
    # set a new rank
    def changeRank(self, new_rank):
        self.rank = new_rank
        return self

    # how object will appear when printed
    def __repr__(self):
        return "<Activity title:%s children:%s rank:%s>" % (self.title, self.children, self.rank)

# create an alias for the object
act = Activity