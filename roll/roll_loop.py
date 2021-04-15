#!/usr/bin/env python3.9
from datetime import datetime
from textwrap import dedent
import webbrowser
from statistics import mode
import rand_task
from os import system
from activity2 import ActivityTreeNode
from roll2 import my_activities

system("")

tree = ActivityTreeNode(my_activities)

# simple function that creates a list of initial substrings for a word
# e.g., aliases("word") -> ["w", "wo", "wor", "word"]
aliases = lambda word : [word[0:x] for x in range(1, len(word)+1)]

def suggestActivity(choice=None):
    if not choice : choice = tree.choose()
    if choice.activity.rep or choice not in history or (isinstance(choice.activity, rand_task.Task) and choice.isDue()):
        choice.displ()
        response2 = input("\nDo or pass? ").lower()
        if response2 in do_aliases:
            return choice
        elif response2 in pass_aliases:
            return suggestActivity()
        elif response2 in quit_aliases:
            return
        else:
            print("\nPlease make a valid selection.\n")
            return suggestActivity(choice)
    return suggestActivity()

def completeActivity(choice):
    response2 = input("\nWould you like to mark this task completed? (Y/n) ")
    if response2 in yes_aliases:
        choice.activity.complete()
        tree.findNode("Do a task")
        print("Task list updated.")
    elif response2 not in no_aliases:
        print("Please enter a valid command.")
        completeActivity(choice)

# create list of options for next activity command
next_options = ["next", "continue", "go", "activity"]
next_aliases = [""]
for word in next_options:
    next_aliases += aliases(word)

# create list of options for quit command
quit_options = ["quit", "exit", "leave"]
quit_aliases = []
for word in quit_options:
    quit_aliases += aliases(word)

# create list of options for update command
# update_aliases = aliases("update")

do_aliases = aliases("do") + [""]
pass_aliases = aliases("pass")
yes_aliases = aliases("yes")
no_aliases = aliases("no")

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
        response = input("\nSuggest an activity?\n").lower()

        # respond to user command

        if response in quit_aliases: # user wants to quit
            running = False
        
        elif early_start and datetime.now().hour >= 12: # user started before noon and it's now after noon
            print("\n\033[32mIf you haven't already, consider eating lunch.\033[0m\n")
            early_start = False
        
        elif response in next_aliases: # user wants to continue with next activity
            choice = suggestActivity()
            if choice:
                if choice.activity.url : webbrowser.open(choice.activity.url, autoraise=False)
                history.append(choice)
                if isinstance(choice.activity, rand_task.Task):
                    completeActivity(choice)
        
        # elif response in update_aliases: # user wants to refresh TickTick tasks
        #     del tree.children[0].children[-1]
        #     tree.children[0].children.append(
        #         rand_task.build_task_tree(rand_task.my_client.sync()).changeRank(2)
        #         )
        #     print("\nTask list has been updated.")
        
        else: # user did not select a valid command
            print("\033[31mPlease enter a valid command.\033[0m")

    elapsed = (datetime.now() - t0) # timedelta for how much time passed while program was running

    # print a summary of the session
    print("\n\033[1;34mSummary\033[0m", end='')
    if history:
        modal = mode(history)
        rarest = min(history) 
        summary = '''
        Time elapsed: {}
        Activities: {}
        Mode: {} ({} times)
        Rarest: {}
        '''.format(
            str(elapsed).split('.')[:-1][0],
            len(history),
            modal.activity.title, history.count(modal),
            rarest.pctProb()
            )
        print(dedent(summary))
    else:
        print("\nNo activities completed.\n")

# start a session
activityLoop()

