# import functions
from ticktick import api
from getpass import getpass
from random import choice
from activity import act
import datetime

# create a client (type: dict) object for the user.
# if no username and password are passed as arguments, requests them from user.
def login(username = "", password = ""):
    if username == "":
        username = input("Enter your TickTick username: ")
    if password == "":
        password = getpass()
    return api.TickTickClient(username, password)

# client object for me
my_client = login("dsethlewis@gmail.com", "zq3vzIGUmN5y")

# create an activity tree of tasks from TickTick: projects > tasks > subtasks > more subtasks
def build_task_tree(client):

    # client state is the core database of tasks
    state = client.state
    projects = state["projects"]
    tasks = state["tasks"]

    # drop archived projects
    active_projects = [x for x in projects if not x["closed"]]

    # change TickTick date string into datetime.date object
    def isDue(t):
        if "dueDate" not in t : return True
        dd = t["dueDate"]
        return datetime.datetime.now().date() >= datetime.date(int(dd[0:4]), int(dd[5:7]), int(dd[8:10]))

    # transform TickTick task into Activity
    def taskToActivity(t):
        return act(
            title = t["title"],
            children = task_children(t),
            rank = t["priority"] + 1
            )

    # recurse through subtasks and transform into activity tree
    def task_children(t):
        tc = []
        if "childIds" in t:
            for sub_t in tasks:
                if sub_t["id"] in t["childIds"] and isDue(sub_t):
                    tc.append(taskToActivity(sub_t))
        return tc

    # map through projects and high-level tasks
    tree = act("Do a task", [
        act(p["name"], [
            # subtasks have key "parentId", so this pulls only top-level tasks
            taskToActivity(t) for t in client.task.get_from_project(p["id"]) if not "parentId" in t and isDue(t)
        # if project list is empty, add activity for adding to project list
        ]) if client.task.get_from_project(p["id"]) else act(p["name"], "Add next action to project") for p in active_projects
    ])

    return tree

# construct an activity tree for my TickTick account
task_tree = build_task_tree(my_client)