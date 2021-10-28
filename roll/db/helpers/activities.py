from sqlalchemy import select, update

from db.models import DBActivity

# activity helpers

def tip(session):
    return session.execute(
        select(DBActivity).
        where(DBActivity.parent_id == 0 and DBActivity.status)
    ).all()[0][0]

def refresh_activity(session, activity):
    return session.execute(
        select(DBActivity).
        filter(DBActivity.id == activity.id)
    ).all()[0][0]

def addition(session, title, parent_id, ordered=False, order_index=None):
    session.add(DBActivity(
        title=title,
        parent_id=parent_id,
        status=True,
        priority=0,
        ordered=ordered,
        order_index=order_index
    ))
    session.commit()

def update_activities(session, ids, **kwargs):
    if isinstance(ids, int) : ids = [ids]
    session.execute(
        update(DBActivity).
        filter(DBActivity.id in ids, DBActivity.status).
        values(**kwargs).
        execution_options(synchronize_session="fetch")
    )
    session.commit()

def increment_priorities(session, ids, increment):
    update_activities(session, ids, priority = DBActivity.priority + increment)