import pickle

def continueSession(filename):
    response = input("\nWould you like to continue from last session? (Y/n) ").lower()
    if response in all_aliases["yes"]:
        infile = open(filename, 'rb')
        old_jar = pickle.load(infile)
        infile.close()
        print("Session continued.")
        return old_jar
    elif response not in all_aliases["no"]:
        print("Please enter a valid command.")
        return continueSession(filename)

def saveAndQuit(filename, jar):
    quit_response = input("Would you like to save? (Y/n) ").lower()
    if quit_response in all_aliases["yes"]:
        outfile = open(filename, 'wb')
        pickle.dump(jar, outfile)
        outfile.close()
        print("Session saved.")
    elif quit_response not in all_aliases["no"]:
        print("Please enter a valid command.")
        saveAndQuit(filename, jar)