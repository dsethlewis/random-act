from sqlalchemy import select, update

from db.models import DBActivity

# activity helpers

def tip(session):
    return session.execute(
        select(DBActivity)
        .filter(DBActivity.parent_id == None, DBActivity.status)
    ).all()[0][0]

def get_activity_by_id(session, activity_id):
    return session.execute(
        select(DBActivity).filter(DBActivity.id == activity_id)
    ).one()[0]

def get_active(session):
    return session.execute(
        select(DBActivity).
        filter(DBActivity.status)
    )

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

def lineage_ids(activity, ancestors=[]):
    if not activity.parent_id:
        return ancestors
    return lineage_ids(activity.parent, ancestors + [activity.id])

def update_activities(session, ids, **kwargs):
    if not kwargs : return
    if isinstance(ids, int) : ids = [ids]
    session.execute(
        update(DBActivity).
        filter(DBActivity.id.in_(ids), DBActivity.status).
        values(**kwargs).
        execution_options(synchronize_session="fetch")
    )
    session.commit()

def increment_priorities(session, ids, increment):
    update_activities(session, ids, priority = DBActivity.priority + increment)

def isancestor(session, ancestor_id, activity_id):
    activity = get_activity_by_id(session, activity_id)
    return ancestor_id in lineage_ids(activity)

def descendants_ids(activity, descendants=[]):
    descendants.append(activity.id)
    if not activity.children : return descendants
    for c in activity.children : descendants_ids(c, descendants)
    return descendants