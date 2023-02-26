from requester import Soup

class Bee():
    '''
        Creates variables such as letters, matrix, prefixes,
        coreLetter, summary, found, and commands.
        These variables are given values after the initial
        call to readHints() at the top of play.py.
    '''
    def __init__(self):
        self.letters = {}
        self.matrix = []
        self.prefixes = {}
        self.coreLetter = ""
        self.summary = ""
        self.answers = []

        self.found = {}
        self.commands = [
            ("-q", "Quit"),
            ("-h", "Help"),
            ("-i", "Show all hint info"),
            ("-m", "Show matrix"),
            ("-p", "Show prefixes"),
            ("-l", "Show letters"),
            ("-f", "Show found words"),
            "Type any other word to guess"
        ]

    '''
        Initializes the relevant variables using calls from
        requester.py's Soup class. This reads through the
        retrieved text and parses the variables to be sent
        to the bee.py client.
    '''
    def readHints(self):
        soup = Soup()
        self.letters = soup.getLetters()
        self.coreLetter = soup.getCoreLetter()
        self.matrix = soup.getMatrix()
        self.prefixes = soup.getPrefixes()
        self.summary = soup.getSummary()
        self.answers = soup.getAnswers()
        self.initFound()
    
    '''
        Initializes the found dictionary with an empty list
        corresponding to each letter.
    '''
    def initFound(self):
        for letter in self.letters.keys():
            self.found[letter] = []
    
    '''
        Prints the found dictionary item-by-item
    '''
    def printFound(self):
        for word in self.found.items():
            print(word)
    
    def getFound(self):
        return self.found

    def getAnswers(self):
        return self.answers
    
    '''
        Prints the matrix with nice formatting by
        building an output string, s.
    '''
    def getMatrix(self):
        print("Matrix:")
        for row in self.matrix:
            s = "| "
            for e in row:
                if e == 0:
                    s += "  -  "
                else:
                    s += "  " + str(e) + " "
                    if len(str(e)) < 2:
                        s += " "
            s += " |"
            print(s)

    '''
        Prints items from the prefix dictionary as
        long as the count of words remaining with
        the given prefix is non-zero.
    '''
    def getPrefixes(self):
        print("Prefixes:")
        for item in self.prefixes.items():
            if item[1]:
                print(item)

    def getSummary(self):
        print(" ".join(self.summary))
    
    '''
        Returns the dictionary of letters, which is
        primarily used by play.py to print a list of
        the keys (letters).
    '''
    def getLetters(self):
        print(list(self.letters.keys()))

    '''
        Makes calls to getMatrix() and getPrefixes()
        to print the full set of relevant data on user
        request.
    '''
    def getInfo(self):
        self.getMatrix()
        print()
        self.getPrefixes()
    
    '''
        Returns the core letter
    '''
    def getCoreLetter(self):
        return self.coreLetter

    '''
        Function that takes a user's guess and adds it to
        the list of found words if valid. It also updates
        the matrix and prefixes according to the letters
        used and the length of the word. According to the
        Spelling Bee rules, guesses must:
            - Be at least 4 letters long
            - Contain an instance of the core letter
            - Contain only letters from the given 7 letters
        Refer to readCmdLine() for more information on what
        different return values correspond to.
    '''
    def guess(self, guess):
        guess = guess.upper()
        if len(guess) < 4:
            return -1
        if guess.find(self.getCoreLetter()) == -1:
            return -2
        for letter in guess:
            if letter not in self.letters:
                return -3

        # We don't verify that the word is a real word
        try:
            if guess not in self.found.get(guess[0]):
                if guess in self.answers:
                    self.prefixes[guess[0:2]] -= 1
                    self.found[guess[0]].append(guess)
                    
                    self.matrix[self.letters[guess[0]]][len(guess)-3] -= 1
                    self.matrix[self.letters[guess[0]]][-1] -= 1
                    self.matrix[-1][len(guess)-3] -= 1
                    self.matrix[-1][-1] -= 1

                    return 1 
                else:
                    return -4
        except:
            return -5
            
        else:
            return 0
    
    '''
        Prints options for user-inputted commands from
        the self.commands list, such as -m, -p, or -q.
    '''
    def printCommands(self):
        for tip in self.commands:
            print(tip)
    
    '''
        Handles recurring user inputs, either submitting a guess and
        printing a subsequent response, or opening another function
        to display game information. 
    '''
    def readCmdLine(self, input):
        commands = [x.strip() for x in input.split(" ")]
        for comm in commands:
            if comm == "-h":
                self.printCommands()
            elif comm == "-q":
                return -1
            elif comm == "-i":
                self.getInfo()
            elif comm == "-m":
                self.getMatrix()
            elif comm == "-p":
                self.getPrefixes()
            elif comm == "-l":
                self.getLetters()
            elif comm == "-f":
                self.printFound()
            else:
                code = self.guess(comm)
                if code == 1:
                    val, pangram = self.wordValue(comm.upper())
                    print("Added " + comm.upper() + " to found words for " + str(val) + " points.")
                    if pangram:
                        print(comm.upper() + " was a PANGRAM!")
                elif code == 0:
                    print(comm.upper() + " has already been found.")
                elif code == -1:
                    print("Word must be at least 4 letters long.")
                elif code == -2:
                    print("Word must contain " + self.getCoreLetter() + ".")
                elif code == -3:
                    print("Word can only contain letters given in the puzzle.")
                elif code == -4:
                    print(comm.upper() + " was not accepted as an answer.")
                elif code == -5:
                    print("Guess unsuccessful, perhaps there is no word with that prefix?")

    '''
    Get spelling bee word value of a guess, taking in a bool value of pangram.
    '''
    def wordValue(self, word):
        val, pangram = None, self.isPangram(word)
        if len(word) == 4:
            val = 1
        elif len(word) < 7:
            val = len(word)
        else:
            val = len(word) + int(self.isPangram(word))*7
        return(val, pangram)

    '''
    Check to see if all letters are present in the guess.
    '''
    def isPangram(self, word):
        flag_array = [0 for x in range(7)]
        for char in word:
            flag_array[self.letters.get(char)-1] = 1
        if 0 in flag_array:
            return False
        return True
        


    