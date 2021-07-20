from treebuilder import tree

import pandas as pd

frame1 = []
frame2 = []

def detree(node):
    for c in node.getChildren():
        frame1.append((c.activity.id, c.parent.activity.id))
        frame2.append((c.activity.id, c.activity.title))
        detree(c)

detree(tree)

frame1 = pd.DataFrame(frame1, columns=["id", "parent_id"])
frame2 = pd.DataFrame(frame2, columns=["id", "title"])

print(frame1)
print(frame2)