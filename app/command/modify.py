import command.helpers as hp
from db.helpers.activities import increment_priorities

def modify(session, tip, id, title, *args):

    quoted = "\"" + title + "\""

    choice = int(input(
        "\nHow do you want to modify " + quoted + "?\n"
        "1. Change the description\n"
        "2. Move it to another place in the list\n"
        "3. Archive it\n"
        "4. Change its priority\n"
    ))
    
    if choice == 1:
        new_title = input("New title: ")
        print(quoted + " will be changed to \"" + new_title + "\"")
        return {"title": new_title}

    elif choice == 2:

        node = hp.browser(tip)

        order_index, confirm_order = hp.ordering(node)

        print(
            quoted
            + " will be moved under \"" + node.title + "\""
            + confirm_order
            )
        return {"parent_id": node.id, "order_index": order_index}

    elif choice == 3:
        print("\"" + title + "\" will be archived\n")
        return {"status": 0}

    elif choice == 4:
        change = input("Increase or decrease priority of " + quoted + "? I/d ").lower()
        if change == "i":
            increment = 1, "increased"
        elif change == "d":
            increment = -1, "decreased"
        else:
            print("Not a valid selection. Exiting.")
        print("The priority of " + quoted + " will be " + increment[1])
        
        increment_priorities(session, id, increment[0])
        return {}
        
