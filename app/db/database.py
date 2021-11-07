from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker

from db import models
from db.helpers.activities import addition

db_path = ("sqlite:///" + str(Path(__file__).parents[2] / "data" / "random.db")).encode("unicode_escape").decode()
engine = create_engine(db_path)

Session = sessionmaker(engine, future=True)

if not database_exists(engine.url):
    print("Database does not exist. Initializing new database.")
    create_database(engine.url)
    with Session() as session:
        models.Base.metadata.create_all(engine)
        session.commit()

    with Session() as session:
        addition(session, "Do something", 0)