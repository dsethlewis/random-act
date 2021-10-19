
# Add a new activity to the list
def add(tip):

    title = input("What activity would you like to add? ")
    print("\nOK. Where in the list would you like to add it?")
    node = add_helper(tip)

    confirm = input('You want to add \"' + title + "\" under \"" + node.title + '". Is that correct? Y/n ').lower()
    if confirm == "y":
        return title, node


def add_helper(node):
    children = [n for n in node.children if n.status]
    if not children:
        return node
    print(node.title)
    print("1. Here")
    for i, c in enumerate(children):
        print("{}. {}".format(i + 2, c.title))
    selection = int(input("Make a selection. "))
    if selection == 1:
        return node
    else:
        return add_helper(children[selection - 2])