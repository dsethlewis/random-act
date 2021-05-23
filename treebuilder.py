import hjson
import activity
import os

from rand_task import TaskTree, login
from timerange import TimeRange

indir = os.path.join(os.getcwd(), 'mydata', 'input')

with open(os.path.join(indir, 'myactivities.hjson')) as infile:
    activities = hjson.load(infile)
tree = activity.ActivityTreeNode(activities)

# TickTick credentials
with open(os.path.join(indir, 'credentials.json')) as infile:
    credentials = hjson.load(infile)
task_tree = TaskTree(login(
    credentials["TickTick"]["username"],
    credentials["TickTick"]["password"]
))
tree.findNode("Get things done").addChild(task_tree.tree.setPriority(3))
tree.updateProbs()

with open(os.path.join(indir, 'timeranges.json')) as infile:
    times = [TimeRange(**time) for time in hjson.load(infile).values()]