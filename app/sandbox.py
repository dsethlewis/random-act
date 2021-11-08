from db.database import Session
from db.helpers.activities import get_activity_by_id
from db.helpers.past_activities import last_seq_index

x = None
s = Session()
c = get_activity_by_id(s, 387).children
c.sort(key=lambda child: child.order_index)
print(c[0])