import random

def roll():
    t1 = [
        "Workout",
        "Clean",
        "Personal care",
        "Send a text",
        "Read",
        "Do a task",
        "Process stuff",
        "Relax",
        "Replenish",
        "Do something nice for Emily"
    ]

    r1 = random.randint(0, len(t1) - 1)

    print(t1[r1])

    t2 = [
        # Workout
        [
            "Aerobic Fitness",
            "Muscular Fitness",
            "Flexibility",
            "Stability"
        ],
        # Clean
        [
            "Put something away",
            "Clean a small area of surface",
            "Wash a dish",
            "Clean a small area of floor"
        ],
        # Personal care
        [
            "Hair and nails",
            "Skin",
            "Teeth",
            "Other"
        ],
        # Send a text
        ["Family", "Friend"],
        # Read a page
        ["A Byte of Python", "Crossroads of Twilight"],
        # Do a task
        [],
        # Process stuff
        [
            "Personal email",
            "UNC email",
            "Desktop inbox",
            "Alternate channels"
        ],
        # Relax
        [
            "Be mindful",
            "Play",
            "Enjoy",
            "Rest"
        ],
        # Replenish
        ["Eat a piece of fruit", "Eat a vegetable"] + ["Drink water"] * 2,
        # Do something nice for Emily
        [
            "Quick massage",
            "Hug and kiss",
            "Mad props",
            "Snack or drink"
        ]
    ]

    a2 = t2[r1]
    if a2:
        r2 = random.randint(0, len(a2) - 1)
        print(a2[r2])
    
    t3 = [
        [
            [
                "Jump rope",
                "Boxing",
                "DDR",
                "Stairs",
                "Burpees",
                "Mountain climbers"
            ],
            [
                "Squats",
                "Floor press",
                "Rows",
                "Overhead press",
                "Deadlift",
                "Accessory"
            ],
            [
                "Happy baby",
                "Child pose",
                "Roll neck out",
                "Swing arms around",
                "High knees",
                "Butt kicks"
            ],
            [
                "Tree pose",
                "Balance a book on your head",
                "Tightrope walk",
                "Flamingo stand-and-reach",
                "Single-leg bodyweight squat",
                "Single-leg Romanian deadlift"
            ]
        ],
        [],
        [
            [
                "Shower",
                "Brush hair and add product",
                "Shave",
                "Trim body hair",
                "Cut nails"
            ],
            [
                "Vaseline lips",
                "Wash face",
                "Benzoyl peroxide",
                "Moisturize",
                "Face toner",
                "Triamcinolone acetonide",
                "Fluticasone",
                "Acne dot"
            ],
            [
                "Floss",
                "Dental pick",
                "Fluoride rinse",
                "Brush teeth"
            ],
            [
                "Eye drops",
                "Deoderant",
                "Vaseline nose",
                "Q-Tip ear",
                "Wipe glasses",
                "Pick a random Birch Box thing"
            ]
        ],
        [],
        [],
        [],
        [
            [], [], [],
            [
                "YNAB",
                "Texts",
                "Discord",
                "WhatsApp",
                "OneNote",
                "FB Messenger",
                "TickTick inbox",
                "Mailbox"
            ]
        ],
        [
            [
                "Meditate",
                "Pause, breathe, and listen",
                "Walking meditation"
            ],
            [
                "Puzzle",
                "Color",
                "Play a video game"
            ],
            [
                "Listen to a song",
                "Read a poem",
                "Mindfully eat chocolate"
            ],
            [
                "Shake it out",
                "Do nothing",
                "Go out for fresh air"
            ]
        ],
        [],
        [],
        []
    ]
    a3 = t3[r1]
    if a3 and a3[r2]:
        r3 = random.randint(0, len(a3[r2]) - 1)
        print(a3[r2][r3])

roll()