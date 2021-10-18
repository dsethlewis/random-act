from sqlalchemy.orm import Session
from database import engine
from models import DBActivity
from sqlalchemy import select

# This function prints a representation of the activity list to the terminal
def display():
    session = Session(engine, future=True)
    tip = session.execute(select(DBActivity).where(DBActivity.parent_id == 0 and DBActivity.status)).all()[0][0]
    print(tip.title)
    for c in tip.children:
        display_helper(c)

# Recurse through tree, displaying each activity on a new line
def display_helper(node, spc="- "):
    print(spc + node.title)
    for c in node.children:
        if c.status:
            display_helper(c, "-" + spc)

display()