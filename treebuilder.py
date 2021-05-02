import json
import activity
import os

from rand_task import TaskTree, login
from timerange import TimeRange

indir = os.path.join(os.getcwd(), 'mydata', 'input')

with open(os.path.join(indir, 'myactivities.json')) as infile:
    activities = json.load(infile)
tree = activity.ActivityTreeNode(activities)

# TickTick credentials
with open(os.path.join(indir, 'credentials.json')) as infile:
    credentials = json.load(infile)
task_tree = TaskTree(login(
    credentials["TickTick"]["username"],
    credentials["TickTick"]["password"]
))
tree.findNode("Get things done").addChild(task_tree.tree.setPriority(3))
tree.updateProbs()

with open(os.path.join(indir, 'timeranges.json')) as infile:
    times = [TimeRange(**time) for time in json.load(infile).values()]