import database, models, helpers

with helpers.new_session() as session:
    models.Base.metadata.create_all(database.engine)
    session.commit()