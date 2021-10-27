def active_children(parent):
    return [c for c in parent.children if c.status]

def selector(parent):
    print("\n" + parent.title)
    print("1. Here")
    children = [parent] + active_children(parent)
    for i, c in enumerate(children[1:]):
        print("{}. {}".format(i + 2, c.title))
    return children[int(input("Make a selection. ")) - 1]

def browser(parent):
    if not active_children(parent):
        return parent
    selection = selector(parent)
    if selection.id == parent.id:
        return parent
    else:
        return browser(selection)

def ordering(parent):
    order_index = None
    confirm_ordered = ""
    if parent.ordered:
        if active_children(parent):
            print("\nAfter which item would you like to place it?")
            neighbor = selector(parent)
            confirm_ordered = " and next to \"" + neighbor.title + "\""
            order_index = neighbor.order_index + 1
        else:
            order_index = 0
    return order_index, confirm_ordered