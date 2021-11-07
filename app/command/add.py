import command.helpers as hp

# Add a new activity to the list
def add(tip):

    title = input("What activity would you like to add? ")
    output = {"title": title}

    print("\nOK. Where in the list would you like to add it?")
    node = hp.browser(tip)
    output["parent_id"] = node.id

    ordered = input("Would you like the activities under it to be ordered? (Y/n) ").lower() == "y"
    assert isinstance(ordered, bool)
    output["ordered"] = ordered

    order_index, confirm_ordered = hp.ordering(node)
    output["order_index"] = order_index

    confirm = input(
        'You want to add \"' + title
        + "\" under \"" + node.title + "\""
        + confirm_ordered
        + ". Is that correct? (Y/n) "
    ).lower()
    print("")
    if confirm == "y" : return output