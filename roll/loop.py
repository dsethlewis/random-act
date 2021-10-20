from db import helpers
from command.display import display
from command.pick import pick
from command.add import add
from command.rate import like, dislike
from command.modify import modify

def loop():

    running = True
    next = None

    while running:

        command = input("What would you like to do? ").lower()

        # display list
        if command == "d":
            with helpers.new_session() as session:
                display(helpers.tip(session))

        # pick next activity
        elif command in ["p", ""]:
            print("")
            with helpers.new_session() as session:
                next = pick(helpers.tip(session))
                next_tpl = next.id, next.title, next.parent_id

                # collect feedback
                choice = (
                    input("\nDo you want to do this activity? (Y/n) ").
                    lower()
                    )
                if choice in ["y", ""]:
                    if like(next):
                        for a in helpers.get_ancestry(session, next):
                            a.priority += 1
                        print("OK, thanks for the feedback!")
                elif choice == "n":
                    if dislike(next):
                        for a in helpers.get_ancestry(session, next):
                            a.priority -= 1
                        print("OK, thanks for the feedback!")
                print("")
                session.commit()

        # add a new activity
        elif command == "a":
            with helpers.new_session() as session:
                add_title, add_parent = add(helpers.tip(session))
                if add_title or add_parent:
                    helpers.addition(session, add_title, add_parent.id)

        # make changes to the most recent activity
        elif command == "m":
            if not next:
                print("Pick an activity first.\n")
            else:
                with helpers.new_session() as session:
                    helpers.update_activity(
                        session, 
                        next_tpl[0], 
                        **modify(*next_tpl)
                        )

        elif command in ["help", "h"]:
            print('\nd(isplay), p(ick), a(dd), m(odify), q(uit), h(elp)\n')

        # quit session
        elif command == "q":
            running = False

loop()