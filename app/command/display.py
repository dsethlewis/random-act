# This function prints a representation of the activity list to the terminal
def display(tip):
    print(tip.title)
    for c in tip.children:
        display_helper(c)

# Recurse through tree, displaying each activity on a new line
def display_helper(node, spc="- "):
    print(spc + node.title)
    for c in node.children:
        if c.status:
            display_helper(c, "-" + spc)