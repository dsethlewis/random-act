from db import helpers
from command.display import display
from command.pick import pick
from command.add import add
from command.rate import like, dislike

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
        elif command == "p":
            print("")
            with helpers.new_session() as session:
                next = pick(helpers.tip(session))

                # collect feedback
                choice = (
                    input("\nDo you want to do this activity? (Y/n) ").
                    lower()
                    )
                if choice == "y":
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

        elif command in ["help", "h"]:
            print('\nd(isplay), p(ick), a(dd), q(uit), h(elp)\n')

        # quit session
        elif command == "q":
            running = False

loop()