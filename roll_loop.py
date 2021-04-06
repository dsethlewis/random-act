#!/usr/bin/python3
from activity import act
import roll2
from datetime import datetime
import math
from textwrap import dedent
from importlib import reload

# simple function that creates a list of initial substrings for a word
# e.g., aliases("word") -> ["w", "wo", "wor", "word"]
aliases = lambda word : [word[0:x] for x in range(1, len(word)+1)]

# create list of options for next activity command
next_options = ["next", "continue", "go", "do", "activity"]
next_aliases = [""]
for word in next_options:
    next_aliases += aliases(word)

# create list of options for quit command
quit_options = ["quit", "exit", "leave"]
quit_aliases = []
for word in quit_options:
    quit_aliases += aliases(word)

# create list of options for update command
update_aliases = aliases("update")

# follow commands from user to proceed through multiple activities
def activityLoop():

    # initialize session

    running = True # true while session is active

    n = 0 # number of activities initiated

    t0 = datetime.now() # start time

    # check if program started running before noon
    early_start = False
    if t0.hour < 12:
        early_start = True

    # session loop
    while running:

        # ask user for command
        response = input("\nDo an activity, update, or quit?\n").lower()

        # respond to user command
        if response in quit_aliases: # user wants to quit
            running = False
        elif early_start and datetime.now().hour >= 12: # user started before noon and it's now after noon
            print("\n\033[32mIf you haven't already, consider eating lunch.\033[0m\n")
            early_start = False
        elif response in next_aliases: # user wants to continue with next activity
            roll2.tree.choose()
            n += 1
        elif response in update_aliases:
            reload(roll2)
            print("\nActivity list has been updated.")
        else: # user did not select a valid command
            print("\033[31mPlease enter a valid command.\033[0m")

    elapsed = (datetime.now() - t0) # timedelta for how much time passed while program was running

    # print a summary of the session
    summary = '''
    \033[1;34mSummary\033[0m
    Activities: {}
    Time elapsed: {}'''.format(n, str(elapsed).split('.')[:-1][0])
    print(dedent(summary))

# start a session
activityLoop()

