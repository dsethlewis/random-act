from sqlalchemy.orm import Session
from db.database import engine
from db.models import DBActivity
from sqlalchemy import select, insert, update

def new_session():
    return Session(engine, future=True)

def tip(session):
    return session.execute(
        select(DBActivity).
        where(DBActivity.parent_id == 0 and DBActivity.status)
    ).all()[0][0]

def addition(session, title, parent_id):
    session.add(DBActivity(
        title=title,
        parent_id=parent_id,
        status=True,
        priority=1
        ))
    session.commit()