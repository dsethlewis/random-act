#!/usr/bin/env python3.9
import webbrowser
import rand_task
import myactivities
import pickling

from datetime import datetime
from textwrap import dedent
from statistics import mode
from os import system
from activity import ActivityTreeNode
from timerange import TimeRange
from alias import all_aliases

system("")

def suggestActivity(tree, choice=None):
    if not choice : choice = tree.choose()
    if choice.isActive() \
        and (not isinstance(choice.activity, rand_task.Task) or choice.activity.isDue()):
        choice.displ()
        response2 = input("\nDo or pass? ").lower()
        if response2 in all_aliases["do"]:
            return choice
        elif response2 in all_aliases["pass"]:
            return suggestActivity(tree)
        elif response2 in all_aliases["quit"]:
            return
        else:
            print("\nPlease make a valid selection.\n")
            return suggestActivity(tree, choice)
    return suggestActivity(tree)

def updateTasks(tree):
    n = tree.findNode("Do a task")
    o = n.parent.activity.options
    new = rand_task.TaskTree(myactivities.task_tree.client).tree
    o[o.index(n.activity)] = new
    n.replaceWith(ActivityTreeNode(new))
    return tree

def completeTask(tree, choice):
    response2 = input("\nWould you like to mark this task completed? (Y/n) ").lower()
    if response2 in all_aliases["yes"]:
        myactivities.task_tree.complete(choice.activity)
        updateTasks(tree)
        print("Task marked complete and list updated.")
    elif response2 in all_aliases["no"]:
        print("Task not marked complete")
    elif response2 not in all_aliases["quit"]:
        print("Please enter a valid command.")
        return completeTask(tree, choice)
    return tree

# follow commands from user to proceed through multiple activities
def activityLoop():

    # initialize session
    
    pickle_file = 'record'

    try:
        old_jar = pickling.continueSession(pickle_file)
    except FileNotFoundError:
        old_jar = None

    tree = updateTasks(old_jar[0]) if old_jar else ActivityTreeNode(myactivities.my_activities)

    running = True # true while session is active

    t0 = datetime.now() # start time
    t1 = None
    period1 = TimeRange.pick(myactivities.times)

    # check if program started running before noon
    early_start = False
    if t0.hour < 12:
        early_start = True

    # list of completed activities
    history = old_jar[1] if old_jar else []

    # session loop
    while running:

        t2 = datetime.now()
        period2 = TimeRange.pick(myactivities.times)
        if period2 != period1:
            for i, option in enumerate(myactivities.my_activities.options):
                option.setPriority(period2.priorities[i])
            tree = ActivityTreeNode(myactivities.my_activities)
        period1 = period2
        t1 = t2

        if (early_start and t2.hour >= 12) or \
            (not history and 12 <= t2.hour < 14): # user started before noon and it's now after noon
            print("\n\033[32mIf you haven't already, consider eating lunch.\033[0m")
            early_start = False

        # ask user for command
        response = input("\nSuggest an activity?\n").lower()

        # respond to user command
        if response in all_aliases["quit"]: # user wants to quit
            running = False
        
        elif response in all_aliases["next"]: # user wants to continue with next activity

            choice = suggestActivity(tree)

            if choice:

                if choice.activity.url : webbrowser.open(choice.activity.url, autoraise=False)

                history.append((choice, choice.prob))
                choice.incrementCount()
                if not choice.isActive() : choice.parent.updateProbs()

                if isinstance(choice.activity, rand_task.Task):
                    tree = completeTask(tree, choice)


        else: # user did not select a valid command
            print("\033[31mPlease enter a valid command.\033[0m")

    elapsed = (datetime.now() - t0) # timedelta for how much time passed while program was running
    if old_jar : elapsed += old_jar[2]

    # print a summary of the session
    print("\n\033[1;34mSummary\033[0m", end='')
    if history:
        modal = mode([x[0] for x in history])
        rarest_prob = min([x[1] for x in history])
        for x in history:
            if x[1] == rarest_prob:
                rarest = x[0]
        summary = '''
        Time elapsed: {}
        Activities: {}
        Mode: {} ({} times)
        Rarest: {}
        '''.format(
            str(elapsed).split('.')[:-1][0],
            len(history),
            modal.activity.title, modal.count,
            rarest.pctProb(rarest_prob)
            )
        print(dedent(summary))
    else:
        print("\nNo activities completed.\n")

    jar = (tree, history, elapsed)
    pickling.saveAndQuit(pickle_file, jar)

# start a session
activityLoop()

