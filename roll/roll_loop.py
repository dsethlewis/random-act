#!/usr/bin/python3
from roll2 import tree
from datetime import datetime
from textwrap import dedent
#from selenium import webdriver
from webbrowser import open
from statistics import mode

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

#drv = webdriver.Chrome()

# follow commands from user to proceed through multiple activities
def activityLoop():

    # initialize session

    running = True # true while session is active

    t0 = datetime.now() # start time

    # check if program started running before noon
    early_start = False
    if t0.hour < 12:
        early_start = True

    # list of completed activities
    history = []

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
            choice = tree.choose()
            if choice.rep or choice not in history:
                choice.displ()
                if choice.url : open(choice.url)
                history.append(choice)
        
        elif response in update_aliases: # user wants to refresh TickTick tasks
            tree.children[0].children[0] = rand_task.task_tree.changeRank(2)
            print("\nTask list has been updated.")
        
        else: # user did not select a valid command
            print("\033[31mPlease enter a valid command.\033[0m")

    elapsed = (datetime.now() - t0) # timedelta for how much time passed while program was running

    modal = mode(history)
    rarest = min(history)

    # print a summary of the session
    summary = '''
    \033[1;34mSummary\033[0m
    Time elapsed: {}
    Activities: {}
    Mode: {} ({} times)
    Rarest: {} ({}%)'''.format(
        str(elapsed).split('.')[:-1][0],
        len(history),
        modal.title, history.count(modal),
        rarest.title, rarest.getPct()
        )
    print(dedent(summary))

# start a session
activityLoop()

