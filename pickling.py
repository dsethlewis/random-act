from pickle import load, dump
from alias import all_aliases
from messages import invalid

def continueSession(filename):
    response = input("\nWould you like to continue "
                     "from last session? (Y/n) ").lower()
    if response in all_aliases["yes"]:
        infile = open(filename, 'rb')
        old_jar = load(infile)
        infile.close()
        print("Session continued.")
        return old_jar
    elif response not in all_aliases["no"]:
        print(invalid)
        return continueSession(filename)

def saveAndQuit(filename, jar):
    quit_response = input("Would you like to save? (Y/n) ").lower()
    if quit_response in all_aliases["yes"]:
        outfile = open(filename, 'wb')
        dump(jar, outfile)
        outfile.close()
        print("Session saved.")
    elif quit_response not in all_aliases["no"]:
        print(invalid)
        saveAndQuit(filename, jar)