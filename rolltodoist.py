import todoist
import datetime

from activity import *

def loginTodoist(token = ""):
    if token == "":
        token = input("Enter your Todoist token: ")
    return todoist.TodoistAPI(token)

class TodoistObject(Activity):

    baseURL = "https://todoist.com/app/project/"

    def __init__(self, todo_dict: dict):
        self.todo_dict = todo_dict

class TodoistProject(TodoistObject):

    def __init__(self, proj_dict):
        super().__init__(proj_dict)
        super(TodoistObject, self).__init__(
            title = proj_dict["name"],
            url = self.createURL(self.todo_dict)
        )

    @staticmethod
    def createURL(todo_dict):
        return TodoistObject.baseURL + str(todo_dict["id"])

    def addOptions(self, projects, sections, tasks):
        options = []
        project_parent_ids = {p["parent_id"] for p in projects}
        section_project_ids = {s["project_id"] for s in sections}
        task_section_ids = {t["section_id"] for t in tasks}
        for p in projects:
            if p["parent_id"] == self.todo_dict["id"]:
                pact = TodoistProject(p)
                options.append(pact)
                if p["id"] in project_parent_ids or p["id"] in section_project_ids:
                    projects, sections, tasks = pact.addOptions(projects, sections, tasks)
        for s in sections:
            if s["project_id"] == self.todo_dict["id"]:
                sact = TodoistSection(s)
                options.append(sact)
                if s["id"] in task_section_ids:
                    tasks = sact.addOptions(tasks)
        if not options : options.append("Add a next action")
        self.setOptions(options)
        return projects, sections, tasks

class TodoistSection(TodoistObject):

    def __init__(self, sect_dict):
        super().__init__(sect_dict)
        super(TodoistObject, self).__init__(
            title = sect_dict["name"]
        )

    def addOptions(self, tasks):
        options = []
        task_parent_ids = {t["parent_id"] for t in tasks}
        for t in tasks:
            if t["section_id"] == self.todo_dict["id"] and not t["parent_id"]:
                tact = TodoistTask(t)
                options.append(tact)
                if t["id"] in task_parent_ids:
                    tasks = tact.addOptions(tasks)
        if not options : options.append("Add a next action")
        self.setOptions(options)
        return tasks

class TodoistTask(TodoistObject, Task):

    def __init__(self, task_dict):
        TodoistObject.__init__(self, task_dict)
        Task.__init__(self, self.dueDate(task_dict))
        super(TodoistObject, self).__init__(
            title = task_dict["content"],
            priority = task_dict["priority"],
            url = self.createURL(task_dict)
            )

    @staticmethod
    def createURL(todo_dict):
        return TodoistObject.baseURL + \
            str(todo_dict["project_id"]) + "/task/" + \
            str(todo_dict["id"])
    
    def addOptions(self, tasks):
        options = []
        task_parent_ids = {t["parent_id"] for t in tasks}
        for t in tasks:
            if t["parent_id"] == self.todo_dict["id"]:
                tact = TodoistTask(t)
                options.append(tact)
                if t["id"] in task_parent_ids:
                    tasks = tact.addOptions(tasks)
        self.setOptions(options)
        return tasks

    def complete(self, client):
        client.close(self.todo_dict["id"])
        client.commit()

    @staticmethod
    def dueDate(todo_dict):
        if todo_dict["due"]:
            dd = todo_dict["due"]["date"]
            return datetime.date(int(dd[0:4]), int(dd[5:7]), int(dd[8:10]))

def buildTree(client):
    state = client.state
    projects = list(state["projects"])
    sections = list(state["sections"])
    tasks = [item for item in state["items"] if not item["checked"]]
    tip = Activity("Do a task").setOptions([TodoistProject(p) \
        for p in projects \
        if "inbox_project" not in p and not p["parent_id"]])
    for p in tip.options:
        projects, sections, tasks = p.addOptions(projects, sections, tasks)
    return tip