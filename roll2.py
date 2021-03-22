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

tree = act("Do something")
t1 = [
        act("Workout", [
            act("Aerobic Fitness", [
                "Jump rope",
                "Boxing",
                "DDR",
                "Stairs",
                "Burpees",
                "Mountain climbers"
            ]),
            act("Muscular Fitness", [
                "Squats",
                "Floor press",
                "Rows",
                "Overhead press",
                "Deadlift",
                act("Accessory", [
                    act("Core", [
                        "Plank",
                        "Side plank",
                        "Superman"
                        "TRX knee tucks"
                        "TRX hip press"
                    ]),
                    act("Upper body", [
                        act("Biceps", [
                        "TRX curls",
                        "Dumbbell curls"
                        ]),
                        act("Triceps", [
                        "TRX tricep extensions",
                        "Diamond push-ups",
                        "Skull crushers"
                        ]),
                        act("Shoulders", [
                            "TRX clock press",
                            "Resistance band pull aparts"])
                    ]),
                ])
            ]),
            act("Flexibility", [
                "Happy baby",
                "Child pose",
                "Roll neck out",
                "Swing arms around",
                "High knees",
                "Butt kicks"
                "Gokhale Method"
            ]),
            act("Stability", [
                "Tree pose",
                "Balance a book on your head",
                "Tightrope walk",
                "Flamingo",
                "Single-leg bodyweight squat",
                "Single-leg Romanian deadlift"
            ])
        ]),
        act("Clean", [
            act("Put something away", rank = 2),
            "Clean a small area of surface",
            "Wash a dish",
            "Clean a small area of floor"
        ]),
        act("Personal care", [
            act("Hair and nails", [
                act("Shower", rank = 2),
                "Brush hair",
                "Add product to hair",
                "Shave",
                "Trim body hair",
                "Cut nails"
            ]),
            act("Skin", [
                "Vaseline lips",
                "Wash face",
                "Benzoyl peroxide",
                "Moisturize",
                "Face toner",
                "Triamcinolone acetonide",
                "Fluticasone",
                "Acne dot",
                act("Clindamycin", rank = 2)
            ]),
            act("Teeth", [
                "Floss",
                "Dental pick",
                "Fluoride rinse",
                act("Brush teeth", rank = 2)
            ]),
            act("Other", [
                "Eye drops",
                "Deoderant",
                "Vaseline nose",
                "Q-Tip ear",
                "Wipe glasses",
                "Pick a random Birch Box thing"
            ]),
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
            act("Alternate channels", [
                "YNAB",
                "Texts",
                "Discord",
                "WhatsApp",
                "OneNote",
                "FB Messenger",
                "TickTick inbox",
                "Mailbox"
            ]),
        ]),
        act("Relax", [
            act("Be mindful", [
                "Meditate",
                "Mindfully eat a piece of chocolate",
                "Mindful movement",
                "Pause, breathe, and listen",
                "Buddha Board"
            ]),
            act("Play", [
                act("Puzzle", [
                    "Spelling Bee",
                    "Jigsaw puzzle",
                    "Edabit",
                    "DOX"
                ]),
                "Color",
                "Play a video game"
            ]),
            act("Enjoy", [
                "Listen to a song",
                "Read a poem",
                "Eat something yummy",
                "Watch a funny video"
            ]),
            act("Rest", [
                "Shake it out",
                "Do nothing",
                "Go out for fresh air"
            ])
        ]),
        act("Replenish", [
            "Eat a piece of fruit",
            "Eat a vegetable",
            act("Drink water", rank = 2)
            ]),
        act("Do something nice for Emily", [
        	act("Touch", [
        		"Massage",
        		"Hug",
        		"Kiss",
        		"Hold hand",
        		"Shoot your shot"
        		]),
        	act("Words of affirmation", [
        		"Mad props",
        		"Sweet nothing"
        		]),
        	"Quality time",
        	"Acts of service",
        	act("Gifts", [
        		"Snack",
        		"Drink"
        		]),
        ])
    ]

tree.addChild(t1)

t2 = open("roll-table.txt")

def build(file):
    reading = open(file).read()
    listed = reading.split('\n')
    t = act("Do")
    

# print(build("roll-table.txt"))

tree.choose()