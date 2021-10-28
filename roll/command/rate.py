from db.database import Session
from db.helpers.activities import refresh_activity, increment_priorities

# Rate an activity in the activity list

def rate(activity, like):
    text, x = (("more", 1), ("less", -1))[1 - like]
    rating = input(
        "Do you want to get \"{}\" {} often? (Y/n) ".
        format(activity.title, text)
    ).lower()
    if rating == "y":
        with Session() as session:
            increment_priorities(
                session,
                lineage_ids(refresh_activity(session, activity)),
                x
            )
        print("Thanks for the feedback!")

def lineage_ids(activity, ancestors=[]):
    if activity.parent_id == 0:
        return ancestors
    return lineage_ids(activity.parent, ancestors + [activity.id])