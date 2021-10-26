from sqlalchemy import select, update

from db.models import DBActivity

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