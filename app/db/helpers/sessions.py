from datetime import datetime

from sqlalchemy import update

from db.models import ActivitySession

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