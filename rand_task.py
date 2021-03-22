from ticktick import api
from getpass import getpass
from random import choice
from activity import act

def login(username = "", password = ""):
    if username == "":
        username = input("Enter your TickTick username: ")
    if password == "":
        password = getpass()
    return api.TickTickClient(username, password)

my_client = login("dsethlewis@gmail.com", "zq3vzIGUmN5y")
    
def build_task_tree(client):

    state = client.state
    projects = state["projects"]
    tasks = state["tasks"]

    active_projects = [x for x in projects if not x["closed"]]

    def task_children(t):
        if "childIds" in t:
            return [act(t2["title"], task_children(t2)) for t2 in tasks if t2["id"] in t["childIds"]]
        else:
            return []

    tree = act("Do a task", [
        act(p["name"], [
            act(t["title"], task_children(t)) for t in client.task.get_from_project(p["id"]) if not "parentId" in t
        ]) for p in active_projects
    ])

    return tree

task_tree = build_task_tree(my_client)