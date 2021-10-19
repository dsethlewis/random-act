import helpers
from command.display import display
from command.pick import pick
from command.add import add

running = True

while running:

    command = input("What would you like to do? ").lower()

    if command == "d":
        display(helpers.tip())

    elif command == "p":
        print("")
        next = pick(helpers.tip())
        print("")

    elif command == "a":
        add_title, add_parent = add(helpers.tip())
        if add_title or add_parent:
            helpers.addition(add_title, add_parent.id)

    elif command == "q":
        running = False