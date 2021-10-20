from collections import namedtuple

def modify(id, title, parent_id):

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
        # TBA - reference to version of add_helper() in command.add
        node = namedtuple('Node', 'id')(1)
        print(quoted + " will be moved")
        return {"parent_id": node.id}

    elif choice == 3:
        print("\"" + title + "\" will be archived\n")
        return {"status": 0}
