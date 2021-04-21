import rand_task

from activity import Activity, ActivityTreeNode
from timerange import TimeRange

act = Activity

# TickTick credentials
ttuser = "dsethlewis@gmail.com"
ttpw = "zq3vzIGUmN5y"

times = [
    TimeRange(4, 9, "morning", (1, 5, 1)),
    TimeRange(9, 17, "daytime", (5, 2, 1)),
    TimeRange(17, 22, "evening", (1, 3, 5)),
    TimeRange(22, 4, "nighttime", (1, 5, 1))
    ]
priorities = list(TimeRange.pick(times))

# construct a nested tree of activities to choose from
my_activities = act("Do something", [
    act("Get things done", [
        act("Process stuff", [
            act("Personal email", url = "https://mail.google.com/mail/u/0/#inbox"),
            act("UNC email", url = "https://mail.business.unc.edu/owa/#path=/mail"),
            "Desktop inbox",
            act("Alternate channels", [
                act(
                    "YNAB",
                    url = "https://app.youneedabudget.com/411791cc-fb41-4e42-aae5-e9596f27dbf7/accounts"
                    ),
                "Texts",
                "Discord",
                "WhatsApp",
                "OneNote",
                "FB Messenger",
                "TickTick inbox",
                act("Mail", [
                    "Move mail from tray to desktop inbox",
                    "Move mail from mailbox to mail tray"
                ]),
            ]),
        ]),
        act("Clean", [
            act("Put something away", priority=3),
            "Clean a small area of surface",
            "Wash a dish",
            "Clean a small area of floor",
            act("Other", [
                "Empty a bin (or bring bins out/in)",
                "Spray vinegar mixture in shower",
                "Move laundry along",
                "Restock toilet paper, paper towels, tissues, or soap",
                "Move dishwasher along",
                "Change sheets",
                "Change towels"
            ])
        ]),
        act("Study", [
            act("Python", [
                act(
                    "Work through next step in Flask tutorial",
                    url = "https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vi-profile-page-and-avatars"
                    ),
                act("Read A Byte of Python", url = "https://python.swaroopch.com/io.html"),
                act(
                    "Work through next step in SQLAlchemy tutorial",
                    url = "https://www.tutorialspoint.com/sqlalchemy/index.htm"
                    )
            ]),
            act("Thesis", [
                "Read a page of an article"
            ])
        ]),
        rand_task.build_task_tree(rand_task.login(ttuser, ttpw)).setPriority(3) # Do a task from TickTick
    ], priority=priorities[0]),

    act("Take care of yourself", [
        act("Workout", [
            act("Aerobic Fitness", [
                "Jump rope",
                "Boxing",
                "DDR",
                "Stairs",
                "Burpees",
                "Mountain climbers",
                "Go for a short run"
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
                        "Superman",
                        "TRX knee tucks",
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
                "Butt kicks",
                act("Gokhale Method", [
                    "Stretchsitting",
                    "Stacksitting",
                    "Stretchlying",
                    "Tallstanding",
                    "Hip-hinging",
                    "Inner corset",
                    "Glidewalking"
                ])
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
        act("Personal care", [
            act("Hair and nails", [
                act("Shower", priority=2),
                "Brush hair",
                "Add product to hair",
                "Shave",
                "Trim body hair",
                "Cut nails",
                "Refill conditioner tube"
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
                act("Clindamycin", priority=2),
                "Refill body wash tube"
            ]),
            act("Teeth", [
                "Floss",
                "Dental pick",
                "Fluoride rinse",
                act("Brush teeth", priority=2)
            ]),
            act("Other", [
                "Eye drops",
                "Deoderant",
                "Vaseline nose",
                "Q-Tip ear",
                "Wipe glasses",
                "Pick a random Birch Box thing"
            ]),
        ], priority=2),
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
                    act("Spelling Bee", url = "https://www.nytimes.com/puzzles/spelling-bee"),
                    "Jigsaw puzzle",
                    act("Edabit", url = "https://edabit.com/challenges"),
                    "DOX",
                    act("Answer a question on Quora", url = "https://quora.com")
                ]),
                "Color",
                "Play a video game"
            ]),
            act("Enjoy", [
                "Listen to a song",
                act("Read a poem", url = "https://www.reddit.com/r/Poetry/top/?t=all"),
                "Eat something yummy",
                act("Watch a funny video", url = "https://www.youtube.com/")
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
            act("Drink water", priority=2)
        ], priority=2),
        act("Read", [
            "Crossroads of Twilight",
            "OneNote Reading List"
        ])
    ], priority=priorities[1]),

    act("Connect with others", [
        act("Send a text", [
            "Family",
            "Friend"
        ]),
        act("Do a good turn", [
            act("Do something nice for Emily", [
                act("Touch", [
                    "Massage",
                    "Hug",
                    "Kiss",
                    "Hold hand"
                ]),
                act("Words of affirmation", [
                    "Mad props",
                    "Sweet nothing"
                ]),
                "Quality time",
                act("Acts of service", [
                    "Empty trash or recycling in her office",
                    "Declutter something in her office",
                    "Fold some of her laundry",
                    "Clean her side of the bathroom vanity",
                    "Clean her nightstand",
                    "Offer to solve a problem",
                    "Offer to pick up prescriptions",
                    "Offer to make a phone call she's avoiding",
                    "Clean her computer monitor, desk, whiteboard, or window",
                    "Make the bed"
                ]),
                act("Gifts", [
                    "Snack",
                    "Drink"
                ])
            ], priority=5),
            act("Give", [
                "Bring a book to a nearby little free library",
                "Donate stuff to Goodwill/etc.",
                "Make a small donation to a charity",
                "Bring food to a local food bank/drop-off location"
            ]),
            act("Serve", [
                "Bake something for a neighbor or friend",
                "Look up one-off volunteer opportunities",
                "Walk around the block picking up litter"
            ]),
            act("Love", [
                "Write a thank you note",
                "Send a gift to a friend or family member",
                "Organize a meal for friends or family"
            ])
        ])
    ], priority=priorities[2])
])