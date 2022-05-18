from bee import Bee

bee = Bee()
bee.readHints()
line = "***********************"

print("Spelling Bee Dynamic Hints Program")

while(True):
    c = input("\nEnter :: ")
    if c == "-h":
        bee.printCommands()
    elif c == "-q":
        break
    elif c == "-i":
        bee.getInfo()
    elif c == "-m":
        bee.getMatrix()
    elif c == "-p":
        bee.getPrefixes()
    elif c == "-l":
        print(list(bee.getLetters().keys()))
    elif c == "-f":
        bee.getFound()
    elif c == "-u":
        bee.undo()
    else:
        code = bee.guess(c)
        if code == 1:
            print("Added " + c.upper() + " to found words.")
        elif code == 0:
            print(c.upper() + " has already been found.")
        elif code == -1:
            print("Word must be at least 4 letters long.")
        elif code == -2:
            print("Word must contain " + bee.getCoreLetter() + ".")
        elif code == -3:
            print("Word can only contain letters given in the puzzle.")
    print(line)
