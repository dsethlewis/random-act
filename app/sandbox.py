from db.database import Session
from db.helpers.activities import get_activity_by_id
from command.pick import pick
from db.helpers.past_activities import last_seq_index

with Session() as sesh:
    print(last_seq_index(sesh, 387))
    # pick(sesh, get_activity_by_id(sesh, 387), "")