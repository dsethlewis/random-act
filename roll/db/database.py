import os

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker

from db import models
from db.helpers.activities import addition

db_path = os.path.join("sqlite:///mydata", "roll.db")
engine = create_engine(db_path)

Session = sessionmaker(engine, future=True)

if not database_exists(engine.url):
    create_database(engine.url)
    with Session() as session:
        models.Base.metadata.create_all(engine)
        session.commit()

    with Session() as session:
        addition(session, "Do something", 0)