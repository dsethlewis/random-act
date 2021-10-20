from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from db import models, helpers

db_path = r"sqlite:///C:\Users\dseth\Documents\rollpy\mydata\roll.db"
engine = create_engine(db_path)

if not database_exists(engine.url):
    create_database(engine.url)
    with helpers.new_session() as session:
        models.Base.metadata.create_all(engine)
        session.commit()