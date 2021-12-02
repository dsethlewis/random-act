from db.database import Session
from command.pick import ancestor_with_siblings
from db.helpers.activities import get_activity_by_id

with Session() as sesh:
    node = get_activity_by_id(sesh, 20)
    ancestor = ancestor_with_siblings(node)
    print(node.title)
    print(ancestor.title)