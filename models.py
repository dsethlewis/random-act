from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey

metadata = MetaData()

activity_table = Table(
    "activities",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(140), nullable=False),
    Column('parent_id', ForeignKey('activities.id'), nullable=False)
)

history_table = Table(
    "history",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('activity_id', ForeignKey('activities.id'), nullable=False)
)