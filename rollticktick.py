#!/usr/bin/env python3.9

# import statements
from ticktick.oauth2 import OAuth2
from ticktick.api import TickTickClient
from getpass import getpass
from random import choice
import datetime

from activity import *

# create a client (type: dict) object for the user.
# if no username and password are passed as arguments, requests them from user.
def loginTickTick(client_id, client_secret, redirect_uri,
                  username = "", password = ""):
    if username == "":
        username = input("Enter your TickTick username: ")
    if password == "":
        password = getpass()
    auth_client = OAuth2(client_id=client_id,
                         client_secret=client_secret,
                         redirect_uri=redirect_uri)
    return TickTickClient(username, password, auth_client)

class TickTickTask(Activity, Task):

    def __init__(self, client, task_dict):
        
        super().__init__(
            title = task_dict["title"],
            options = [],
            priority = task_dict["priority"] + 1,
            url = None,
            limit = -1
            )

        self.task_dict = task_dict
        self.tickid = task_dict["id"]

        if "childIds" in task_dict : self.addSubtasks(client)

        self.due = None
        if "dueDate" in task_dict:
            self.due = self.dueDate(task_dict["dueDate"])

    @staticmethod
    def dueDate(dd):
        return datetime.date(int(dd[0:4]), int(dd[5:7]), int(dd[8:10]))

    # populate list of subtasks
    def addSubtasks(self, client):
        for sub_t in client.state["tasks"]:
            if sub_t["id"] in self.task_dict["childIds"]:
                self.options.append(TickTickTask(client, sub_t))

class TickTickTaskTree():

    def __init__(self, client):
        self.client = client
        self.tree = self.build_task_tree()

    # call TickTick (or other) API to mark task completed
    def complete(self, task_dict):
        self.task_dict = self.client.task.complete(task_dict)
        assert "completedTime" in self.task_dict

    def taskMaker(self, project):
        if self.client.task.get_from_project(project["id"]):
            return [TickTickTask(self.client, task_dict) for
                    task_dict in
                    self.client.task.get_from_project(project["id"])]
        return ["Add next action to project"]

    # create an activity tree of tasks from TickTick:
    # projects > tasks > subtasks > more subtasks
    def build_task_tree(self):
        act = Activity
        projects = [project for project
                    in self.client.state["projects"]
                    if not project["closed"]]
        project_folders = self.client.state["project_folders"]
        # add pseudo-folder for any projects not in folders
        if not all(["groupId" in project for project in projects]):
            project_folders += [{"id": 0, "name": "Other Projects"}]
        # initialize activity tree for tasks
        return act("Do a task",
                   # turn project folder into Activity
                   [act(folder["name"],
                        # turn project into Activity
                        [act(project["name"], self.taskMaker(project))
                         for project in projects
                         # if project is in the current folder
                         if project["groupId"] == folder["id"]])
                    for folder in project_folders])