from sqlalchemy import (Column, Integer, String, Boolean, DateTime, ForeignKey,
    Float)
from sqlalchemy.orm import declarative_base, relationship, backref

Base = declarative_base()

class DBActivity(Base):
    __tablename__ = 'activity'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('activity.id'))
    children = relationship("DBActivity", backref=backref('parent', remote_side=[id]))
    title = Column(String(140), nullable=False)
    status = Column(Boolean)
    priority = Column(Integer)
    ordered = Column(Boolean)
    order_index = Column(Integer)

class PastActivity(Base):
    __tablename__ = 'past_activity'

    id = Column(Integer, primary_key=True)
    activity_id = Column(Integer, ForeignKey('activity.id'))
    session_id = Column(Integer, ForeignKey('activity_session.id'))
    accepted = Column(Boolean)
    timestamp = Column(DateTime)
    skipped = Column(Boolean)

class ActivitySession(Base):
    __tablename__ = 'activity_session'

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)