from activity import act
from roll2 import tree
from datetime import datetime
import math

aliases = lambda word : [word[0:x] for x in range(1, len(word)+1)]

next_options = ["next", "continue", "go", "do", "activity"]
next_aliases = [""]
for word in next_options:
    next_aliases += aliases(word)

quit_options = ["quit", "exit", "leave"]
quit_aliases = []
for word in quit_options:
    quit_aliases += aliases(word)

def activityLoop():

    running = True
    n = 0

    t = datetime.now()

    early_start = False
    if t.hour < 12:
        early_start = True

    while running:

        if early_start and datetime.now().hour >= 12:
            print("\n\033[32mIf you haven't already, consider eating lunch.\033[0m\n")
            early_start = False

        response = input("\nDo an activity or quit?\n").lower()

        print(" ")

        if response in quit_aliases:
            running = False
        elif response in next_aliases:
            tree.choose()
            n += 1
        else:
            print("\033[31mPlease enter a valid command.\033[0m")

    elapsed = (datetime.now() - t)

    summary = '''\033[1;34mSummary\033[0m
    Activities: {}
    Time elapsed: {}
    '''.format(n, str(elapsed).split('.')[:-1][0])

    print(summary)

activityLoop()

