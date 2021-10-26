from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker

from db import models, helpers

db_path = r"sqlite:///C:\Users\dseth\Documents\repos\random-act\mydata\roll.db"
engine = create_engine(db_path)

if not database_exists(engine.url):
    create_database(engine.url)
    with helpers.new_session() as session:
        models.Base.metadata.create_all(engine)
        session.commit()

Session = sessionmaker(engine, future=True)