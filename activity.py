from random import choice

# define an activity object
class Activity:

    def __init__(self, title, children = [], parent = None, rank = 1, url = None, rep = True):

        self.title = title # text of activity
        self.children = children # sub-categories of activity expressed as string or Activity or list thereof
        self.rank = rank # how many times an activity should appear in tree
        self.url = url # related webpage
        self.rep = rep # whether this activity can be done repeatedly during a given session

        if children : self.addChild(children) # finish initializing inputted children

    def traceAncestry(self):
        return self.parent.ancestry + [self.parent] if self.parent else []

    def calcProb(self):
        return (self.rank / self.parent.n_children) * self.parent.prob if self.parent else 1

    def nChildren(self, children):
        return sum([a.rank if isinstance(a, Activity) else 1 for a in children])

    def addChild(self, a):
        '''Constructs a hierarchical activity tree.'''
        if type(a) == str:
            self.children.append(Activity(a, parent = self))
        elif isinstance(a, Activity):
            # self.children.append(Activity(a.title, a.children, self, a.rank, a.url))
            self.children.append(a.reinit(self))
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

    # Activity object equivalence
    def __eq__(self, other):
        return vars(self) == vars(other)

    # how Activity object will be compared with other Activity objects
    def __lt__(self, other):
        return self.prob < other.prob

    # how object will appear when printed
    def __repr__(self):
        return "<Activity title:%s>" % (self.title)

# create an alias for the object
act = Activity

sample_activity = Activity("Do something", ["This", "That"])

class activityTreeNode():
    
    def __init__(self, activity, parent = None, children = []):
        self.activity = activity
        self.parent = parent
        self.children = [activityTreeNode(child, self,) for child in children]


        self.ancestry = self.traceAncestry() # lineage of node
        self.prob = self.calcProb() # overall probability of being selected
        self.n_children = self.nChildren(children) if children else 1 # weighted (by rank) number of sub-activities

    