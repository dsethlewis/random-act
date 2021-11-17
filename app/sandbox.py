from db.database import Session
from db.helpers.past_activities import time_of_day_weight

with Session() as sesh:
    m = time_of_day_weight(sesh, 369)

print(m)
