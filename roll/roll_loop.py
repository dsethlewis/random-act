#!/usr/bin/env python3.9

from datetime import datetime
from textwrap import dedent
import webbrowser
from statistics import mode
import rand_task
import myactivities

from os import system
from activity import ActivityTreeNode
from timerange import TimeRange
from alias import all_aliases

system("")

tree = ActivityTreeNode(myactivities.my_activities)

def suggestActivity(choice=None):
    if not choice : choice = tree.choose()
    if choice.activity.rep \
        or choice not in history \
        or (isinstance(choice.activity, rand_task.Task) and choice.isDue()):
        choice.displ()
        response2 = input("\nDo or pass? ").lower()
        if response2 in all_aliases["do"]:
            return choice
        elif response2 in all_aliases["pass"]:
            return suggestActivity()
        elif response2 in all_aliases["quit"]:
            return
        else:
            print("\nPlease make a valid selection.\n")
            return suggestActivity(choice)
    return suggestActivity()

def completeActivity(choice):
    response2 = input("\nWould you like to mark this task completed? (Y/n) ").lower()
    if response2 in all_aliases["yes"]:
        choice.activity.complete()
        n = tree.findNode("Do a task")
        o = n.parent.activity.options
        new = rand_task.build_task_tree(choice.activity.client)
        o[o.index(n)] = new
        n.replaceWith(ActivityTreeNode(new))
        print("Task marked complete and list updated.")
    elif response2 in all_aliases["no"]:
        print("Task not marked complete")
    elif response2 in all_aliases["quit"]:
        return
    else:
        print("Please enter a valid command.")
        completeActivity(choice)

#drv = webdriver.Chrome()

# follow commands from user to proceed through multiple activities
def activityLoop():

    # initialize session

    running = True # true while session is active

    t0 = datetime.now() # start time
    t1 = None

    # check if program started running before noon
    early_start = False
    if t0.hour < 12:
        early_start = True

    # list of completed activities
    history = []

    # session loop
    while running:

        t2 = datetime.now()
        hour = t2.hour
        if t1 and t1.hour != hour:
            priorities = TimeRange.pick(myactivities.times)
            for i, option in enumerate(myactivities.my_activities):
                option.setPriority(priorities[i])
            tree = ActivityTreeNode(myactivities.my_activities)
        t1 = t2

        if (early_start and hour >= 12) or \
            (not history and hour < 14): # user started before noon and it's now after noon
            print("\n\033[32mIf you haven't already, consider eating lunch.\033[0m")
            early_start = False

        # ask user for command
        response = input("\nSuggest an activity?\n").lower()

        # respond to user command
        if response in all_aliases["quit"]: # user wants to quit
            running = False
        
        elif response in all_aliases["next"]: # user wants to continue with next activity
            choice = suggestActivity()
            if choice:

                if choice.activity.url : webbrowser.open(choice.activity.url, autoraise=False)

                history.append(choice)
                choice.incrementCount()

                if isinstance(choice.activity, rand_task.Task): completeActivity(choice)

                if not choice.activity.rep : choice.parent.updateProbs()

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
            modal.activity.title, modal.count,
            rarest.pctProb()
            )
        print(dedent(summary))
    else:
        print("\nNo activities completed.\n")

# start a session
activityLoop()

