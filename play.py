from bee import Bee
from store import SaveHandler

'''
    Initialize Bee and SaveHandler() objects, along with
    line divider string for console logging.
'''
bee = Bee()
save = SaveHandler()
bee.readHints()
line = "*************************************************"

'''
    Update save.txt to the current date if expired, read in
    any words previously found and stored on save.txt
'''
save.update()
preFound = save.readFound()
for word in preFound:
    bee.guess(word)

'''
    Introductory comments
'''
print("\n*** Spelling Bee Dynamic Hints Program ***")
print("*** Enter -h for list of user commands ***\n")
bee.getSummary()

'''
    The main program loop. Awaits input, parses it,
    then executes relevant command before returning to
    the loop (unless quit command issued).
'''
while(True):
    c = input("\nEnter :: ")
    if bee.readCmdLine(c) == -1:
        break
    print("\n" + line)

'''
    All post-quit saving operations go here
'''
save.writeFound(bee.getFound())
