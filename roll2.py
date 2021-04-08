#!/usr/bin/python3
import random
from activity import act
import rand_task

# construct a nested tree of activities to choose from
tree = act("Do something", [
    act("Get things done", [
        rand_task.task_tree.changeRank(2), # Do a task from TickTick
        act("Process stuff", [
            act("Personal email", url = "https://mail.google.com/mail/u/0/#inbox"),
            act("UNC email", url = "https://mail.business.unc.edu/owa/#path=/mail"),
            "Desktop inbox",
            act("Alternate channels", [
                act("YNAB", url = "https://app.youneedabudget.com"),
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
            act("Put something away", rank = 3),
            "Clean a small area of surface",
            "Wash a dish",
            "Clean a small area of floor",
            act("Other", [
                "Empty a bin (or bring bins out/in)",
                "Spray vinegar mixture in shower",
                "Move laundry along",
                "Restock toilet paper, paper towels, tissues, or soap",
                "Move dishwasher along"
            ])
        ]),
    ], rank = 3),

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
                act("Shower", rank=2),
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
                act("Clindamycin", rank=2),
                "Refill body wash tube"
            ]),
            act("Teeth", [
                "Floss",
                "Dental pick",
                "Fluoride rinse",
                act("Brush teeth", rank=2)
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
            act("Drink water", rank=2)
        ], rank = 2),
        act("Read", [
            act("A Byte of Python", url = "https://python.swaroopch.com/oop.html"),
            "Crossroads of Twilight",
            "OneNote Reading List"
        ])
    ], rank = 2),

    act("Connect with others", [
        act("Send a text", [
            "Family",
            "Friend"
        ]),
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
        ])
    ], rank = 1)
])

# t2 = open("roll-table.txt")
# def build(file):
#     reading = open(file).read()
#     listed = reading.split('\n')
#     t = act("Do")
# print(build("roll-table.txt"))
# 

# recurse through tree, choosing paths at random, until reaching a dead end
# tree.choose()