import yaml
import os

from models import DBActivity

# from rollticktick import TickTickTaskTree, loginTickTick
# from rolltodoist import loginTodoist, buildTree

# from timerange import TimeRange

indir = os.path.join(os.getcwd(), 'mydata', 'input')

with open(os.path.join(indir, 'activities.yml'), 'r') as infile:
    activities = yaml.load(infile, Loader=yaml.FullLoader)

print(activities["ttl"])

from sqlalchemy import select, update, func
from sqlalchemy.orm import Session, aliased
from models import DBActivity
from database import engine

'''
Four possibilities:
1. Task is already in the database with the same parent
2. Task is not in database but parent is
3. Task is already in the database with a different parent
4. Neither task nor parent is in database

Pseudo-code for this database procedure

next_id = max(id) + 1

for each item in yaml, starting at the top row and working down:

    if title already in db:
        if parent has changed:
            add it
        else:
            skip it
    else:
        if parent's title is already in db:
            parent_id = parent's id
            add it
        else:
            add it as is
'''

session = Session(engine, future=True)
next_id = session.execute(select(func.max(DBActivity.id))).scalar() + 1

print(next_id)

frame = []

def dct_to_tbl(node, pttl, pid):

    global next_id
    myid = next_id
    next_id += 1

    frame.append({'id': myid, 'title': node['ttl'], 'parent_ttl': pttl, 'parent_id': pid})

    if "opts" in node:
        for opt in node["opts"]:
            dct_to_tbl(opt, node['ttl'], myid)

dct_to_tbl(activities, "None", 0)

# def without_state(obj):
#     vs = vars(obj)
#     return {k: vs[k] for k in vs if k != "_sa_instance_state"}
# print([without_state(x) for x in frame])

# overlap = (session.execute(select(DBActivity).where(DBActivity.title.in_([row['title'] for row in frame]))).all())
aliasedActivity = aliased(DBActivity)
all_rows = session.execute(select(DBActivity)).all()

additions = []
activate = []

for new_row in frame:
    match = None
    parent_match = None
    for old_row, in all_rows:
        if new_row["title"] == old_row.title:
            match = old_row
        elif new_row["parent_ttl"] == old_row.title:
            parent_match = old_row
    if not match or not parent_match or match not in parent_match.children:
        if parent_match:
            new_row["parent_id"] = parent_match.id
        additions.append(new_row)
    elif not match.status:
        activate.append(new_row["title"])

for row in additions:
    session.add(DBActivity(id=row["id"], title=row["title"], parent_id=row["parent_id"], status=True))
session.commit()

session.execute(update(DBActivity).where(DBActivity.title in activate).values(status=True))

# import activity

# tree = activity.ActivityTreeNode(activities).updateProbs()

# # TickTick integration
# with open(os.path.join(indir, 'credentials.hjson')) as infile:
#     credentials = hjson.load(infile)
# task_tree = TickTickTaskTree(loginTickTick(**credentials["TickTick"]))
# tree.findNode("Get things done").addChild(task_tree.tree.setPriority(3))
# tree.updateProbs()

# # # Todoist integration
# # with open(os.path.join(indir, 'credentials.hjson')) as infile:
# #     credentials = hjson.load(infile)
# # todoist_client = loginTodoist(credentials["Todoist"]["token"])
# # todoist_client.sync()
# # task_tree = buildTree(todoist_client).setPriority(3)
# # assert task_tree, "Task tree is missing."
# # tree.findNode("Get things done").addChild(task_tree)
# # tree.updateProbs()

# with open(os.path.join(indir, 'timeranges.json')) as infile:
#     times = [TimeRange(**time) for time in hjson.load(infile).values()]