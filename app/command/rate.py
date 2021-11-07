from db.database import Session
import db.helpers.activities as ac

# Rate an activity in the activity list

def rate(activity, like):
    text, x = (("more", 1), ("less", -1))[1 - like]
    rating = input(
        "Do you want to get \"{}\" {} often? (Y/n) ".
        format(activity.title, text)
    ).lower()
    if rating == "y":
        with Session() as session:
            ac.increment_priorities(
                session,
                ac.lineage_ids(ac.refresh_activity(session, activity)),
                x
            )
        print("Thanks for the feedback!")