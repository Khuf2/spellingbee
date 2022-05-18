from requester import Soup

class Bee():
    '''
        Creates variables such as letters, matrix, prefixes,
        coreLetter, summary, found, guessStack, and commands.
        These variables are given values after the initial
        call to readHints() at the top of play.py.
    '''
    def __init__(self):
        self.letters = {}
        self.matrix = []
        self.prefixes = {}
        self.coreLetter = ""
        self.summary = ""

        self.found = {}
        self.guessStack = []
        self.commands = [
            ("-q", "Quit"),
            ("-h", "Help"),
            ("-i", "Show all hint info"),
            ("-m", "Show matrix"),
            ("-p", "Show prefixes"),
            ("-l", "Show letters"),
            ("-f", "Show found words"),
            ("-u", "Undo last guess"),
            "Type any other word to guess"
        ]

    '''
        Initializes the relevant variables using calls from
        requester.py's Soup class. This reads through the
        retrieved text and parses the variables to be sent
        to the bee.py client.
    '''
    def readHints(self):
        # Initialize matrix, prefixes, letters, coreLetter
        soup = Soup()
        self.letters = soup.getLetters()
        self.coreLetter = soup.getCoreLetter()
        self.matrix = soup.getMatrix()
        self.prefixes = soup.getPrefixes()
        self.summary = soup.getSummary()
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
    def getFound(self):
        for word in self.found.items():
            print(word)
    
    '''
        Prints the matrix with nice formatting by
        building an output string, s.
    '''
    def getMatrix(self):
        print("Matrix:")
        for row in self.matrix:
            s = "| "
            for e in row:
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
    
    '''
        Returns the dictionary of letters, which is
        primarily used by play.py to print a list of
        the keys (letters).
    '''
    def getLetters(self):
        return self.letters

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
    '''
    def guess(self, guess):
        guess = guess.upper()
        if len(guess) < 4:
            return -1
        if guess.find(self.getCoreLetter()) == -1:
            return -2
        for letter in guess:
            if letter not in self.getLetters().keys():
                return -3

        # We don't verify that the word is a real word
        if guess not in self.found.get(guess[0]):
            self.found[guess[0]].append(guess)
            self.guessStack.append(guess)
            
            self.matrix[self.letters[guess[0]]][len(guess)-3] -= 1
            self.matrix[self.letters[guess[0]]][-1] -= 1
            self.matrix[-1][len(guess)-3] -= 1
            self.prefixes[guess[0:2]] -= 1
            
            return 1
        else:
            return 0
        '''
            When we implement saving guesses to a file, the file
            will call this method for each of the words in it. This
            means that we need to change the print statements to return,
            and do the printing outside in play.py
        '''

    '''
        Uses the guess stack to revert the last executed guess. This is
        useful in case the user misinputs a word that is not accepted
        by the spelling bee, which would alter the matrix and prefixes
        to be inaccurate. This method shouldn't be necessary if word
        validation was included. 
    '''
    def undo(self):
        if len(self.guessStack) > 0:
            word = self.guessStack.pop()
            self.found[word[0]].remove(word)

            self.matrix[self.letters[word[0]]][len(word)-3] += 1
            self.matrix[self.letters[word[0]]][-1] += 1
            self.matrix[-1][len(word)-3] += 1
            self.prefixes[word[0:2]] += 1
        else:
            print("No guesses to undo.")
    
    '''
        Prints options for user-inputted commands from
        the self.commands list, such as -m, -p, or -q.
    '''
    def printCommands(self):
        for tip in self.commands:
            print(tip)


    