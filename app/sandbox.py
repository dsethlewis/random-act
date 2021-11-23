from db.database import Session
from db.helpers.past_activities import time_of_day_weight

with Session() as sesh:
    w = time_of_day_weight(sesh, 388)

print(w)