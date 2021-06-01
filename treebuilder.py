import hjson
import activity
import os

from rollticktick import TickTickTaskTree, loginTickTick
from rolltodoist import loginTodoist, buildTree

from timerange import TimeRange

indir = os.path.join(os.getcwd(), 'mydata', 'input')

with open(os.path.join(indir, 'myactivities.hjson')) as infile:
    activities = hjson.load(infile)
tree = activity.ActivityTreeNode(activities)

## TickTick integration
# with open(os.path.join(indir, 'credentials.hjson')) as infile:
#     credentials = hjson.load(infile)
# task_tree = TaskTree(login(
#     credentials["TickTick"]["username"],
#     credentials["TickTick"]["password"]
# ))
# tree.findNode("Get things done").addChild(task_tree.tree.setPriority(3))
# tree.updateProbs()

# Todoist integration
with open(os.path.join(indir, 'credentials.hjson')) as infile:
    credentials = hjson.load(infile)
todoist_client = loginTodoist(credentials["Todoist"]["token"])
task_tree = buildTree(todoist_client)

tree.findNode("Get things done").addChild(task_tree.setPriority(3))
tree.updateProbs()

with open(os.path.join(indir, 'timeranges.json')) as infile:
    times = [TimeRange(**time) for time in hjson.load(infile).values()]