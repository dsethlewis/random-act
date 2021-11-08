from datetime import datetime
from math import pi

from sqlalchemy import select, func, Integer

from db.models import PastActivity, DBActivity
import db.helpers.activities as ac

# past_activity helpers

def add_past_activity(session, activity_id, activity_session_id, accepted):
    session.add(PastActivity(
        activity_id=activity_id,
        timestamp=datetime.now(),
        session_id=activity_session_id,
        accepted=accepted
    ))
    session.commit()

def acpt_rate_dev(session, activity_id):

    if session.execute(
        select(func.count(PastActivity.id)).
        filter(PastActivity.activity_id == activity_id)
    ).scalar() < 5:
        return 0

    rates_by_activity = (
        select(
            PastActivity.activity_id, 
            func.ln(
                func.avg(PastActivity.accepted)
                / (1 - func.avg(PastActivity.accepted))
            ).label("rate")
        ).
        filter(PastActivity.accepted != None).
        group_by(PastActivity.activity_id).
        subquery()
    )

    mean = session.execute(
        select(func.avg(rates_by_activity.c.rate))
    ).scalar()

    sd = session.execute(
        select(
            func.sqrt(func.avg(func.pow(rates_by_activity.c.rate - mean, 2)))
        )    
    ).scalar()

    rate = session.execute(
        select(rates_by_activity.c.rate).
        filter(rates_by_activity.c.activity_id == activity_id)
    ).scalar()

    return (rate - mean) / sd if rate else 0

def last_seq_index(session, parent_id):
    session.execute(
        select(DBActivity.order_index).
        join(PastActivity).
        filter(
            DBActivity.parent_id == parent_id
            and DBActivity.status
            and PastActivity.accepted
            and PastActivity.timestamp > (
                datetime.now().
                replace(hour=5, minute=0, second=0, microsecond=0)
                )
        ).
        order_by(PastActivity.timestamp.desc())
    ).first()

def activity_n(session, activity_id):
    return session.execute(
        select(func.count(PastActivity.id)).
        filter(PastActivity.activity_id == activity_id)
    ).scalar()

def curr_period():
    datetime.now().hour // 4

def period_acpt_rt(session, activity_id):
    per = curr_period()
    descendants = ac.descendants_ids(
        ac.get_activity_by_id(session, activity_id)
    )
    rt = session.execute(
        select(func.avg(PastActivity.accepted.cast(Integer))).
        filter(
            func.mod(func.time(PastActivity.timestamp) + 2, 24) / 6 == per,
            PastActivity.activity_id in descendants
        )
    ).scalar()
    return rt if rt else 1