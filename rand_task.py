#!/usr/bin/env python3.9

# import statements
from ticktick import api
from getpass import getpass
from random import choice
import datetime

from activity import Activity as act

# create a client (type: dict) object for the user.
# if no username and password are passed as arguments, requests them from user.
def login(username = "", password = ""):
    if username == "":
        username = input("Enter your TickTick username: ")
    if password == "":
        password = getpass()
    return api.TickTickClient(username, password)

class Task(act):

    def __init__(self, client, task_dict):
        
        super().__init__(
            title = task_dict["title"],
            options = [],
            priority = task_dict["priority"] + 1,
            url = None,
            limit = -1
            )

        self.task_dict = task_dict
        self.id = task_dict["id"]

        if "childIds" in task_dict : self.addSubtasks(client)

        self.due = self.dueDate(task_dict["dueDate"]) if "dueDate" in task_dict else None

    @staticmethod
    def dueDate(dd):
        return datetime.date(int(dd[0:4]), int(dd[5:7]), int(dd[8:10]))

    # check if task is due yet
    def isDue(self):
        if not self.due : return True
        return datetime.datetime.now().date() >= self.due

    # populate list of subtasks
    def addSubtasks(self, client):
        for sub_t in client.state["tasks"]:
            if sub_t["id"] in self.task_dict["childIds"]:
                self.options.append(Task(client, sub_t))

class TaskTree():

    def __init__(self, client):
        self.client = client
        self.tree = self.build_task_tree()

    # call TickTick (or other) API to mark task completed
    def complete(self, t):
        self.client.task.complete(t.id)

    def taskMaker(self, project):
        if self.client.task.get_from_project(project["id"]):
            return [Task(self.client, task_dict) for task_dict in self.client.task.get_from_project(project["id"])]
        return ["Add next action to project"]

    # create an activity tree of tasks from TickTick: projects > tasks > subtasks > more subtasks
    def build_task_tree(self):
        # initialize activity tree for tasks
        return act("Do a task", [
            # turn project folder into Activity
            act(folder["name"], [
                # turn project into Activity
                act(project["name"], self.taskMaker(project)) \
                    # loop through projects 
                    for project in self.client.state["projects"] \
                    # that are active and in the current folder
                    if not project["closed"] and project["groupId"] == folder["id"]
            # loop through folders
            ]) for folder in self.client.state["project_folders"] \
                # add pseudo-folder for any projects not in folders
                + [{"id": None, "name": "Other Projects"}]
        ])