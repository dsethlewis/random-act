import command.helpers as hp

def modify(tip, id, title, parent_id):

    quoted = "\"" + title + "\""

    choice = int(input(
        "\nHow do you want to modify " + quoted + "?\n"
        "1. Change the description\n"
        "2. Move it to another place in the list\n"
        "3. Archive it\n"
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
