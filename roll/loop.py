from db.helpers import activities, past_activities, sessions
from db.database import Session
from command.display import display
from command.pick import pick
from command.add import add
from command.rate import like, dislike
from command.modify import modify

def loop():

    with Session() as session:
        activity_session_id = sessions.start_activity_session(session)
    running = True

    next = None
    last_title = None
    z = 1.28

    while running:

        command = input("What would you like to do? ").lower()

        # display list
        if command == "d":
            with Session() as session:
                display(activities.tip(session))

        # pick next activity
        elif command in ["p", ""]:
            print("")
            with Session() as session:
                next = pick(activities.tip(session), last_title)
                next_tpl = next.id, next.title, next.parent_id
            next_id = next_tpl[0]
            last_title = next_tpl[1]

            # collect feedback
            accepted = (
                input("\nDo you want to do this activity? (Y/n) ").
                lower()
            ) in ["y", ""]
            with Session() as session:
                past_activities.add_past_activity(
                    session, next_id,
                    activity_session_id, accepted
                )

            # tweak priority
            with Session() as session:
                stddvs = past_activities.acpt_rate_dev(session, next_id)
            if accepted and stddvs >= z:
                if like(next):
                    with Session() as session:
                        for a in activities.get_ancestry(session, next):
                            a.priority += 1
                        session.commit()
                    print("OK, thanks for the feedback!")
            elif not accepted and stddvs <= z:
                if dislike(next):
                    with Session() as session:
                        for a in activities.get_ancestry(session, next):
                            a.priority -= 1
                        session.commit()
                    print("OK, thanks for the feedback!")
            print("")

        # add a new activity
        elif command == "a":
            with Session() as session:
                add_title, add_parent = add(activities.tip(session))
                if add_title or add_parent:
                    activities.addition(session, add_title, add_parent.id)

        # make changes to the most recent activity
        elif command == "m":
            if not next:
                print("Pick an activity first.\n")
            else:
                with Session() as session:
                    activities.update_activity(
                        session, 
                        next_tpl[0], 
                        **modify(activities.tip(session), *next_tpl)
                    )

        elif command in ["help", "h"]:
            print('\nd(isplay), p(ick), a(dd), m(odify), q(uit), h(elp)\n')

        # quit session
        elif command == "q":
            running = False
    
    with Session() as session:
        sessions.end_activity_session(session, activity_session_id)

loop()