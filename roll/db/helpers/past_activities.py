from datetime import datetime

from sqlalchemy import select, func

from db.models import PastActivity

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