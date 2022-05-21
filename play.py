from bee import Bee
from store import SaveHandler

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

while(True):
    c = input("\nEnter :: ")
    if bee.readCmdLine(c) == -1:
        break
    print("\n" + line)

'''
    All post-quit saving operations go here
'''
save.writeFound(bee.getFound())
