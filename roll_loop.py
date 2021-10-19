#!/usr/bin/env python3.9
import webbrowser
# import rollticktick
import pomodoro
import os
# import rolltodoist

from datetime import datetime as dt
from textwrap import dedent
from statistics import mode
from activity import *
# from timerange import TimeRange
from alias import all_aliases
from termcolor import colored
from messages import niceJob, invalid
from treebuilder import tree#, times, task_tree
# from treebuilder import todoist_client
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import PastActivity

db_path = r"sqlite:///C:\Users\dseth\Documents\rollpy\mydata\roll.db"
engine = create_engine(db_path)

# outdir = os.path.join(os.getcwd(), 'mydata', 'output')

def suggestActivity(tree, choice=None):
    if not choice : choice = tree.choose()
    if choice.isActive():
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

# def updateTasks(tree):
#     # TickTick
#     new = rollticktick.TickTickTaskTree(task_tree.client).tree
#     # # Todoist
#     # new = rolltodoist.buildTree(todoist_client)
#     old = tree.findNode("Do a task")
#     if old:
#         old.replaceWith(new)
#     else:
#         tree.findNode("Get things done").addChild(new)
#     return tree

# def completeTask(tree, choice, todoist_client = None):
#     prompt = "\nWould you like to mark this task completed? (Y/n) "
#     response2 = input(prompt).lower()
#     if response2 in all_aliases["yes"]:
#         if isinstance(choice, rollticktick.TickTickTask):
#             task_tree.complete(choice.activity.task_dict)
#         elif isinstance(choice, rolltodoist.TodoistTask):
#             todoist_client = choice.activity.complete(todoist_client)
#             assert choice.activity.todo_dict["id"] in \
#                 [t["id"] for t in \
#                     todoist_client.state["tasks"] if t["checked"]]
#         updateTasks(tree)
#         print("Task marked complete and list updated.")
#     elif response2 in all_aliases["no"]:
#         print("Task not marked complete")
#     elif response2 not in all_aliases["quit"]:
#         print(invalid)
#         return completeTask(tree, choice)
#     return tree

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
            Mode: {} ({} time{})
            Rarest: {}
            '''.format(
            str(elapsed).split('.')[:-1][0],
            len(history),
            modal.activity.title,
            modal.count,
            "s" if modal.count > 1 else "",
            rarest.pctProb(rarest_prob)
            )
        if pomo:
            summary += '''Pomodoros: {}
            {}'''.format(
                pomo.count(),
                "On a break" if pomo.isOnBreak() else "In a Pomodoro"
                )
        print(dedent(summary))
    else:
        print("\nNo activities completed.\n")

def dualSummaries(elapsed, session_history, pomo=None):
    print(colored("Session Summary", "blue", attrs=["bold"]), end='')
    summarize(elapsed, session_history, pomo)

def linkOut(url):
    prompt = "\nWould you like to open this activity in a browser? (Y/n) "
    response2 = input(prompt).lower()
    if response2 in all_aliases["yes"]:
        webbrowser.open(url, autoraise=False)
    elif response2 in all_aliases["no"]:
        print("Webpage not opened.")
    else:
        print(invalid)
        linkOut(url)

# follow commands from user to proceed through multiple activities
def activityLoop(tree):

    # initialize session
    
    running = True # true while session is active

    t0 = dt.now() # start time
    period1 = None

    pomo = pomodoro.PomodoroTimer()

    # check if program started running before noon
    early_start = False
    if t0.hour < 12:
        early_start = True

    # list of completed activities
    session_history = []

    # session loop
    while running:

        # if time of day has changed (e.g., daytime --> evening),
        # update top-level activity priorities
        t2 = dt.now()
        # period2 = TimeRange.pick(times)
        # gtd_priority = period2.priorities[0]
        # if period2 != period1:
        #     for i, child in enumerate(tree.children):
        #         child.activity.setPriority(period2.priorities[i])
        #     tree.updateProbs()
        # period1 = period2
        t1 = t2

         # it's now after noon
        if ((early_start and t2.hour >= 12)
            or (not session_history and 12 <= t2.hour < 14)):
            print(colored("\nIf you haven't already, consider eating lunch.",
                          "green"))
            early_start = False

        # ask user for command
        response = input("\nSuggest an activity?\n").lower()

        # change priority for getting things done based on
        # status of pomodoro timer
        if pomo.ring():
            if pomo.isOnBreak():
                print("You're on a break.")
                # new_prio = gtd_priority
            else:
                print("You're in a pomodoro.")
                # new_prio = gtd_priority * 3
            # gtd.activity.setPriority(new_prio)
            # tree.updateProbs()

        # respond to user command

        # user wants to quit
        if response in all_aliases["quit"]:
            running = False

        elif response == "tree" : tree.displTree()

        # elif response == "update" : updateTasks(tree)

        elif response in all_aliases["stats"]:
            dualSummaries(dt.now()-t0, session_history, pomo)
        
        # user wants to continue with next activity
        elif response in all_aliases["next"]: 
            choice = suggestActivity(tree)
            if choice:
                print(niceJob())
                if choice.activity.url : linkOut(choice.activity.url)
                choice.incrementCount()
                if not choice.isActive() : choice.parent.updateProbs()
                # if isinstance(choice.activity, rollticktick.TickTickTask):
                #     tree = completeTask(tree, choice)
                # # if isinstance(choice.activity, rolltodoist.TodoistTask):
                # #     tree = completeTask(tree, choice, todoist_client)
                # #     if choice.activity.title == "Add a next action":
                # #         todoist_client.sync()
                # updateTasks(tree)
                history_entry = (choice, choice.prob)
                # history.append(history_entry)
                session_history.append(history_entry)

                # # export to persistent CSV
                # with open(os.path.join(outdir, 'history.csv'),
                #           'a', newline='') as history_file:
                #     history_writer = csv.writer(history_file)
                #     history_writer.writerow([
                #         t1.timestamp(),
                #         choice.activity.title,
                #         choice.ancestryStr(),
                #         choice.prob,
                #         not pomo.isOnBreak()
                #         ])

                with Session(engine) as session:
                    session.add(PastActivity(activity_id=choice.activity.id,
                                             timestamp = dt.now()))
                    session.commit()

        else: # user did not select a valid command
            print(invalid)

    # timedelta for how much time passed while program was running
    elapsed = (dt.now() - t0)

    dualSummaries(elapsed, session_history, pomo)

# start a session
activityLoop(tree)