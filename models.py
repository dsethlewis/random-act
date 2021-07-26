from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class DBActivity(Base):
    __tablename__ = 'activity'

    id = Column(Integer, primary_key=True)
    title = Column(String(140), nullable=False)
    parent_id = Column(Integer, ForeignKey('activity.id'))
    children = relationship("DBActivity")

class PastActivity(Base):
    __tablename__ = 'past_activity'

    id = Column(Integer, primary_key=True)
    activity_id = Column(Integer, ForeignKey('activity.id'))
    timestamp = Column(DateTime)