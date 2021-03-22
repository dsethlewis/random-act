import random

class Activity:

    def __init__(self, title, children = [], rank = 1):
        self.title = title
        self.children = []
        self.rank = rank
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

    def hasChild(self):
        return len(self.children) != 0
    
    def choose(self):
        c = random.choice(self.children)
        print(c.title)
        if c.hasChild():
            c.choose()

    def __repr__(self):
        return "<Activity title:%s children:%s rank:%s>" % (self.title, self.children, self.rank)

act = Activity