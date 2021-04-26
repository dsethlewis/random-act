#!/usr/bin/env python3.9
import webbrowser
import rand_task
import myactivities
import pickling
import pomodoro

from datetime import datetime
from textwrap import dedent
from statistics import mode
from os import system
from activity import ActivityTreeNode
from timerange import TimeRange
from alias import all_aliases
from termcolor import colored
from messages import niceJob, invalid

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
            print(invalid)
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
        print(invalid)
        return completeTask(tree, choice)
    return tree

# print a summary of the session
def summarize(elapsed, history, pomo=None):
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
        if pomo : summary += "Pomodoros: {}\n".format(pomo.count())
        print(dedent(summary))
    else:
        print("\nNo activities completed.\n")

def dualSummaries(elapsed, session_history, history, old_jar, pomo=None):
    print(colored("Session Summary", "blue", attrs=["bold"]), end='')
    summarize(elapsed, session_history, pomo)
    if old_jar:
        print(colored("Overall Summary", "magenta", attrs=["bold"]), end='')
        elapsed += old_jar[2]
        summarize(elapsed, history)

# follow commands from user to proceed through multiple activities
def activityLoop():

    # initialize session
    
    pickle_file = 'record'

    try:
        old_jar = pickling.continueSession(pickle_file)
    except FileNotFoundError:
        old_jar = None

    tree = updateTasks(old_jar[0]) if old_jar else ActivityTreeNode(myactivities.my_activities)
    gtd = tree.activity.options[0]

    running = True # true while session is active

    t0 = datetime.now() # start time
    t1 = None
    period1 = TimeRange.pick(myactivities.times)

    pomo = pomodoro.PomodoroTimer()

    # check if program started running before noon
    early_start = False
    if t0.hour < 12:
        early_start = True

    # list of completed activities
    history = old_jar[1] if old_jar else []
    session_history = []

    # session loop
    while running:

        # if time of day has changed (e.g., daytime --> evening),
        # update top-level activity priorities
        t2 = datetime.now()
        period2 = TimeRange.pick(myactivities.times)
        gtd_priority = period2.priorities[0]
        if period2 != period1:
            for i, option in enumerate(tree.activity.options):
                option.setPriority(period2.priorities[i])
            tree = ActivityTreeNode(tree.activity)
        period1 = period2
        t1 = t2

        # change priority for getting things done based on
        # status of pomodoro timer
        if pomo.ring():
            if pomo.isOnBreak():
                print("You're on a break.")
                new_prio = gtd_priority
            else:
                print("You're in a pomodoro.")
                new_prio = gtd_priority * 2
            gtd.setPriority(new_prio)
            tree = ActivityTreeNode(tree.activity)

        if (early_start and t2.hour >= 12) or \
            (not session_history and 12 <= t2.hour < 14): # user started before noon and it's now after noon
            print(colored("\nIf you haven't already, consider eating lunch.", "green"))
            early_start = False

        # ask user for command
        response = input("\nSuggest an activity?\n").lower()

        # respond to user command
        if response in all_aliases["quit"]: # user wants to quit
            running = False
        
        elif response in all_aliases["next"]: # user wants to continue with next activity
            choice = suggestActivity(tree)
            if choice:
                print(niceJob())
                if choice.activity.url : webbrowser.open(choice.activity.url, autoraise=False)
                choice.incrementCount()
                if not choice.isActive() : choice.parent.updateProbs()
                if isinstance(choice.activity, rand_task.Task):
                    tree = completeTask(tree, choice)
                history_entry = (choice, choice.prob)
                history.append(history_entry)
                session_history.append(history_entry)

        elif response in all_aliases["stats"]:
            dualSummaries(datetime.now()-t0, session_history, history, old_jar, pomo)

        else: # user did not select a valid command
            print(invalid)

    elapsed = (datetime.now() - t0) # timedelta for how much time passed while program was running
    dualSummaries(elapsed, session_history, history, old_jar, pomo)
    if old_jar : elapsed += old_jar[2]
    jar = (tree, history, elapsed)
    pickling.saveAndQuit(pickle_file, jar)

# start a session
activityLoop()