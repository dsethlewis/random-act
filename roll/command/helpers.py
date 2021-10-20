def browser(node):
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
        return browser(children[selection - 2])