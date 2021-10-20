from sqlalchemy import create_engine
# from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

db_path = r"sqlite:///C:\Users\dseth\Documents\rollpy\mydata\roll.db"

engine = create_engine(db_path)
if not database_exists(engine.url):
    create_database(engine.url)