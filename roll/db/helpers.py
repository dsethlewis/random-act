from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select, update, func

from db.database import engine
from db.models import DBActivity, ActivitySession, PastActivity

# General DBMS helpers

def new_session():
    return Session(engine, future=True)

# activity helpers

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

def get_parent(session, activity):
    return session.execute(
        select(DBActivity).
        where(DBActivity.id == activity.parent_id and DBActivity.status)
    ).all()[0][0]

def get_ancestry(session, activity, descendants=[]):
    if activity.parent_id == 0:
        return descendants
    descendants.append(activity)
    return get_ancestry(session, get_parent(session, activity), descendants)

def update_activity(session, id, **kwargs):
    session.execute(
        update(DBActivity).
        where(DBActivity.id == id and DBActivity.status).
        values(**kwargs)
    )
    session.commit()

# activity_session helpers

def start_activity_session(session):
    new_activity_session = ActivitySession(start_time=datetime.now())
    session.add(new_activity_session)
    session.flush()
    id = new_activity_session.id
    session.commit()
    return id

def end_activity_session(session, activity_session_id):
    session.execute(
        update(ActivitySession).
        where(ActivitySession.id == activity_session_id).
        values(end_time=datetime.now())
    )
    session.commit()

# past_activity helpers

def add_past_activity(session, activity, activity_session_id, accepted):
    session.add(PastActivity(
        activity_id=activity.id,
        timestamp=datetime.now(),
        session_id=activity_session_id,
        accepted=accepted
    ))
    session.commit()

def acpt_rate_dev(session, activity):

    mean = session.execute(
        select(func.avg(PastActivity.accepted))
    ).scalar()

    rates_by_activity = (
        select(
            PastActivity.activity_id, 
            func.avg(PastActivity.accepted).label("rate")
        ).
        filter(PastActivity.accepted != None).
        group_by(PastActivity.activity_id).
        subquery()
    )

    sd = session.execute(
        select(func.sqrt(func.avg(func.pow(rates_by_activity.c.rate - mean, 2))))    
    ).scalar()

    rate = session.execute(
        select(rates_by_activity.c.rate).
        filter(rates_by_activity.c.activity_id == activity.id)
    ).scalar()

    return (rate - mean) / sd if rate else 0

