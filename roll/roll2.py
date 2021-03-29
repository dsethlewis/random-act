#!/usr/bin/python3
import random
from activity import act
import rand_task

# construct a nested tree of activities to choose from
tree = act("Do something", [
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
    act("Clean", [
        act("Put something away", rank=2),
        "Clean a small area of surface",
        "Wash a dish",
        "Clean a small area of floor",
        "Empty a bin (or bring bins out/in"
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
    act("Send a text", [
        "Family",
        "Friend"
    ]),
    act("Read", [
        "A Byte of Python",
        "Crossroads of Twilight",
        "Chrome Reading List"
    ]),
    rand_task.task_tree.changeRank(2),
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
        act("Drink water", rank=2)
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