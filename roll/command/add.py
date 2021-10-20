from command.helpers import browser

# Add a new activity to the list
def add(tip):

    title = input("What activity would you like to add? ")
    print("\nOK. Where in the list would you like to add it?")
    node = browser(tip)

    confirm = input('You want to add \"' + title + "\" under \"" + node.title + '". Is that correct? Y/n ').lower()
    print("")
    if confirm == "y":
        return title, node