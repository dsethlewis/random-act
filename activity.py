from random import choice

# define an activity object
class Activity:

    def __init__(self, title, children = [], parent = None, rank = 1, url = None, rep = True):
        self.title = title # text of activity
        self.children = [] # sub-categories of activity
        self.rank = rank # how many times an activity should appear in tree
        self.parent = parent
        self.ancestry = parent.ancestry + [parent] if parent else []
        self.prob = (rank / parent.n_children) * parent.prob if parent else 1
        self.n_children = 1
        if children:
            self.n_children = sum([x.rank if type(x) == Activity else 1 for x in children])
            self.addChild(children)
        self.url = url
        self.rep = rep

    def addChild(self, a):
        '''Constructs a hierarchical activity tree.'''
        if type(a) == str:
            self.children.append(Activity(a, parent = self))
        elif type(a) == Activity:
            self.children.append(Activity(a.title, a.children, self, a.rank, a.url))
        elif type(a) == list:
            [self.addChild(x) for x in a]
    
    # recurse through activity tree to select next activity
    def choose(self):

        # list indices with rank number of duplicates
        weighted = [] 
        [weighted.extend([x] * self.children[x].rank) for x in range(len(self.children))]

        c = self.children[choice(weighted)]
        if c.children:
            return c.choose()
        else:
            return c

    # set a new rank and return self
    def changeRank(self, new_rank):
        self.rank = new_rank
        return self
    
    # get Activity's probability as a percentage
    def getPct(self):
        return round(self.prob * 100, 2)

    # print task and all parents
    def displ(self):
        # if self.parent:
        #     self.parent.displ()
        #     if self.children:
        #         print(self.title)
        #     else:
        #         print("{} ({}%)".format(self.title, self.getPct()))
        [print(t.title) for t in self.ancestry]
        print("{} ({}%)".format(self.title, self.getPct()))

    def displTree(self, spc=""):
        print("{}{} ({}%)".format(spc, self.title, self.getPct()))
        for a in self.children : a.displTree(spc+" ")

    # how Activity object will be compared with other Activity objects
    def __lt__(self, other):
        return self.prob < other.prob

    # how object will appear when printed
    def __repr__(self):
        return "<Activity title:%s>" % (self.title)

# create an alias for the object
act = Activity