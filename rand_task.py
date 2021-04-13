# import functions
from ticktick import api
from getpass import getpass
from random import choice
import activity
import datetime

# create a client (type: dict) object for the user.
# if no username and password are passed as arguments, requests them from user.
def login(username = "", password = ""):
    if username == "":
        username = input("Enter your TickTick username: ")
    if password == "":
        password = getpass()
    return api.TickTickClient(username, password)

class Task(activity.Activity):

    def __init__(self, client, task_dict):
        
        super().__init__(
            title = task_dict["title"],
            children = [],
            parent = None,
            rank = task_dict["priority"] + 1,
            url = None,
            rep = True
            )

        self.client = client
        self.task_dict = task_dict
        self.id = task_dict["id"]

        if "childIds" in task_dict : self.addSubtasks()

        dueDate = lambda dd : datetime.date(int(dd[0:4]), int(dd[5:7]), int(dd[8:10]))
        self.due = dueDate(task_dict["dueDate"]) if "dueDate" in task_dict else None

    # check if task is due yet
    def isDue(self):
        if not self.due : return True
        return datetime.datetime.now().date() >= self.due

    # populate list of subtasks
    def addSubtasks(self):
        for sub_t in self.client.state["tasks"]:
            if sub_t["id"] in self.task_dict["childIds"] : self.children.append(Task(self.client, sub_t))

    # call TickTick (or other) API to mark task completed
    def complete(self):
        self.client.task.complete(self.id)

        # find task component of overall tree
        def topTaskNode(node):
            for c in node.children:
                if c.title == "Do a task" : return c
                topTaskNode(c)

        task_tree = topTaskNode(self.ancestry[0])
        supernode = task_tree.parent
        supernode.children[supernode.children.index(task_tree)] = build_task_tree(self.client)


# create an activity tree of tasks from TickTick: projects > tasks > subtasks > more subtasks
def build_task_tree(client):

    act = activity.act

    # client state is the core database of tasks
    state = client.state

    def taskMaker(client, project):
        if client.task.get_from_project(project["id"]):
            return [Task(client, task_dict) for task_dict in client.task.get_from_project(project["id"])]
        return "Add next action to project"

    # initialize activity tree for tasks
    return act("Do a task", [
        # turn project folder into Activity
        act(folder["name"], [
            # turn project into Activity
            act(project["name"], taskMaker(client, project)) \
                # loop through projects 
                for project in state["projects"] \
                # that are active and in the current folder
                if not project["closed"] and project["groupId"] == folder["id"]
        # loop through folders
        ]) for folder in state["project_folders"]] \
            # add pseudo-folder for any projects not in folders
            + [{"id": None, "name": "Other Projects"}]
    )

# client = login("dsethlewis@gmail.com", "zq3vzIGUmN5y")
# tree = build_task_tree(client)