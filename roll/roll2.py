import random

class Activity:

    def __init__(self, title, children = [], rank = 1):
        self.title = title
        self.children = []
        self.rank = rank
        if children:
            self.addChild(children)


    def addChild(self, a):
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

tree = act("Do something")
t1 = [
        act("Workout", [
            "Aerobic Fitness",
            "Muscular Fitness",
            "Flexibility",
            "Stability"
        ]),
        act("Clean", [
            "Put something away",
            "Clean a small area of surface",
            "Wash a dish",
            "Clean a small area of floor"
        ]),
        act("Personal care", [
            "Hair and nails",
            "Skin",
            "Teeth",
            "Other"
        ]),
        act("Send a text", [
            "Family",
            "Friend"
        ]),
        act("Read", [
            "A Byte of Python",
            "Crossroads of Twilight"
        ]),
        "Do a task",
        act("Process stuff", [
            "Personal email",
            "UNC email",
            "Desktop inbox",
            "Alternate channels"
        ]),
        act("Relax", [
            "Be mindful",
            "Play",
            "Enjoy",
            "Rest"
        ]),
        act("Replenish", [
            "Eat a piece of fruit",
            "Eat a vegetable",
            act("Drink water", rank = 2)
            ]),
        act("Do something nice for Emily", [
            "Quick massage",
            "Hug and kiss",
            "Mad props",
            "Snack or drink"
        ])
    ]

tree.addChild(t1)

t2 = open("roll-table.txt")

def build(file):
    reading = open(file).read()
    listed = reading.split('\n')
    t = act("Do")
    

print(build("roll-table.txt"))

tree.choose()