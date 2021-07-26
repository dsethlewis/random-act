from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

db_path = r"sqlite:///C:\Users\dseth\Documents\rollpy\mydata\roll.db"

engine = create_engine(db_path)
if not database_exists(engine.url):
    create_database(engine.url)

from models import Base, DBActivity

with Session(engine) as session:
    Base.metadata.create_all(engine)
    session.commit()

from treebuilder import tree

frame = []

def detree(node):
    for c in node.getChildren():
        frame.append(DBActivity(id=c.activity.id,
                                title=c.activity.title,
                                parent_id=c.parent.activity.id))
        detree(c)

detree(tree)

with Session(engine) as session:
    for a in frame:
        session.add(a)
    session.commit()