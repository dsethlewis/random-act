from db.database import Session
from db.helpers.activities import get_activity_by_id, descendants_ids

with Session() as s:
    l=descendants_ids(get_activity_by_id(s, 364))

print(l)