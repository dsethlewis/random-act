from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists

db_path = ("sqlite:///" + str(Path(__file__).parents[1] / "mydata" / "roll.db")).encode("unicode_escape").decode()
print(db_path)

engine = create_engine(db_path)

# from sqlalchemy import text

# with engine.connect() as conn:
#      result = conn.execute(text("select * from activity where status=1 limit 10"))
#      print(result.all())

print(engine.url)

print(database_exists(engine.url))