from datetime import datetime, timedelta

from sqlalchemy import select, func, Integer, extract, or_, case, not_

from db.models import PastActivity, DBActivity
import db.helpers.activities as ac

# past_activity helpers

def add_past_activity(session, activity_id, activity_session_id, accepted, skipped):
    session.add(PastActivity(
        activity_id=activity_id,
        timestamp=datetime.now(),
        session_id=activity_session_id,
        accepted=accepted,
        skipped=skipped
    ))
    session.commit()

def acpt_rate_dev(session, activity_id):

    if session.execute(
        select(func.count(PastActivity.id)).
        filter(PastActivity.activity_id == activity_id)
    ).scalar() < 5:
        return 1

    rates_by_activity = (
        select(
            PastActivity.activity_id, 
            func.ln(
                (0.01 + func.avg(PastActivity.accepted.cast(Integer)))
                / (1.01 - func.avg(PastActivity.accepted.cast(Integer)))
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
    lsi = session.execute(
        select(DBActivity.order_index)
        .join(PastActivity)
        .filter(
            DBActivity.parent_id == parent_id,
            DBActivity.status,
            or_(PastActivity.accepted, PastActivity.skipped),
            PastActivity.timestamp > (
                datetime.now().
                replace(hour=5, minute=0, second=0, microsecond=0)
            )
        )
        .order_by(PastActivity.timestamp.desc())
    ).first()
    return lsi[0] if lsi else None

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

def time_of_day_weight(session, activity_id):
    descendants = ac.descendants_ids(
        ac.get_activity_by_id(session, activity_id)
    )

    julian_times = (
        select(
            extract("julian", PastActivity.timestamp).label("julian"),
            PastActivity.accepted
        )
        .filter(PastActivity.activity_id.in_(descendants))
        .subquery()
    )

    radial_times = select(
        (
            (julian_times.c.julian - func.trunc(julian_times.c.julian))
            * 2 * func.pi()
        ).label("rad"),
        julian_times.c.accepted
    ).subquery()

    rev_reject = select(case(
        (radial_times.c.accepted, radial_times.c.rad),
        (not_(radial_times.c.accepted), radial_times.c.rad + func.pi())
    ).label("rad_reversed"))

    agg = select(
            func.sum(func.sin(rev_reject.c.rad_reversed)).label("s"),
            func.sum(func.cos(rev_reject.c.rad_reversed)).label("c"),
            func.count(rev_reject.c.rad_reversed).label("n")
    ).subquery()

    t, radius = session.execute(
        select(
            (func.atan2(agg.c.s, agg.c.c) * 12 / func.pi()),
            func.sqrt(func.pow(agg.c.s, 2) + func.pow(agg.c.c, 2)) / agg.c.n
        )
    ).all()[0]

    t = t % 24
    t_now = datetime.now()
    t_now = (t_now - datetime(t_now.year, t_now.month, t_now.day)) / timedelta(hours=1)
    t_dev = min(abs(t - t_now), abs(t + 12 - t_now))

    return (t_dev / 6) ** radius