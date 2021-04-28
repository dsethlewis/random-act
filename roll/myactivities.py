#!/usr/bin/env python3.9

import rand_task

from activity import Activity, ActivityTreeNode
from timerange import TimeRange

act = Activity

# TickTick credentials
ttuser = "dsethlewis@gmail.com"
ttpw = "zq3vzIGUmN5y"

task_tree = rand_task.TaskTree(rand_task.login(ttuser, ttpw))

times = [
    TimeRange(4, 9, "morning", (1, 5, 1)),
    TimeRange(9, 17, "daytime", (5, 4, 1)),
    TimeRange(17, 22, "evening", (1, 5, 3)),
    TimeRange(22, 4, "nighttime", (1, 5, 1))
    ]
priorities = TimeRange.pick(times).priorities

# construct a nested tree of activities to choose from
my_activities = act("Do something", [
    act("Get things done", [
        act("Process stuff", [
            act("Personal email", url = "https://mail.google.com/mail/u/0/#inbox"),
            act("UNC email", url = "https://heelmail.unc.edu"),
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
                    act("Move mail from tray to desktop inbox", limit=1),
                    act("Move mail from mailbox to mail tray", limit=1)
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
                "Pour boiling water down shower drain",
                "Move laundry along",
                act("Restock", [
                    "Toilet paper",
                    "Paper towels",
                    "Tissues",
                    "Soap",
                    act("Conditioner", limit=1),
                    act("Body wash", limit=1)
                ]),
                "Move dishwasher along",
                act("Change sheets", limit=1),
                act("Change towels", limit=1)
            ])
        ]),
        act("Study", [
            act("Programming", [
                act(
                    "Work through next step in Flask tutorial",
                    url = "https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vi-profile-page-and-avatars"
                    ),
                act("Read A Byte of Python", url = "https://python.swaroopch.com/io.html"),
                act(
                    "Work through next step in interactive SQL tutorial",
                    url = "https://sqlbolt.com"
                    )
            ]),
            act("Thesis", [
                "Read a page of an article"
            ])
        ]),
        task_tree.tree.setPriority(3) # Do a task from TickTick
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
                act("Shower", priority=2, limit=2),
                "Brush hair",
                act("Add product to hair", limit=1),
                act("Shave", limit=1),
                "Trim body hair",
                "Cut nails"
            ]),
            act("Skin", [
                "Vaseline lips",
                act("Wash face", limit=2),
                act("Benzoyl peroxide", limit=2),
                "Moisturize",
                act("Face toner", limit=1),
                "Triamcinolone acetonide",
                act("Fluticasone", limit=2),
                act("Acne dot"),
                act("Clindamycin", priority=2, limit=2)
            ]),
            act("Teeth", [
                act("Floss", limit=2),
                act("Dental pick", limit=1),
                act("Fluoride rinse", limit=1),
                act("Brush teeth", priority=2, limit=3)
            ]),
            act("Other", [
                "Eye drops",
                act("Deoderant", limit=2),
                act("Vaseline nose", limit=3),
                act("Q-Tip ear", limit=2),
                act("Wipe glasses", limit=2),
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
                    act("Empty trash or recycling in her office", limit=2),
                    "Declutter something in her office",
                    "Fold some of her laundry",
                    "Clean her side of the bathroom vanity",
                    "Clean her nightstand",
                    "Offer to solve a problem",
                    act("Offer to pick up prescriptions", limit=1),
                    "Offer to make a phone call she's avoiding",
                    "Clean her computer monitor, desk, whiteboard, or window",
                    act("Make the bed", limit=1)
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
            ], limit=1),
            act("Serve", [
                "Bake something for a neighbor or friend",
                "Look up one-off volunteer opportunities",
                "Walk around the block picking up litter"
            ], limit=1),
            act("Love", [
                "Write a thank you note",
                "Send a gift to a friend or family member",
                "Organize a meal for friends or family"
            ])
        ])
    ], priority=priorities[2])
])