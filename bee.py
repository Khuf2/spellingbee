from requester import Soup

class Bee():
    def __init__(self):
        # Need to tag the necessary letter somehow
        # Uppercase?
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

    def readHints(self):
        # Initialize matrix, prefixes, letters, coreLetter
        soup = Soup()
        self.letters = soup.getLetters()
        self.coreLetter = soup.getCoreLetter()
        self.matrix = soup.getMatrix()
        self.prefixes = soup.getPrefixes()
        self.summary = soup.getSummary()
        self.initFound()
    
    def initFound(self):
        for letter in self.letters.keys():
            self.found[letter] = []
    
    def getFound(self):
        for word in self.found.items():
            print(word)
    
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

    def getPrefixes(self):
        print("Prefixes:")
        for item in self.prefixes.items():
            if item[1]:
                print(item)
    
    def getLetters(self):
        return self.letters

    def getInfo(self):
        self.getMatrix()
        print()
        self.getPrefixes()
    
    def getCoreLetter(self):
        return self.coreLetter

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
    
    def setPrefixes(self, prefixes):
        for row in prefixes:
            for pref in row:
                self.prefixes[pref[:2]] = int(pref[pref.find("-")+1:])

    def setMatrix(self, matrix):
        i = 0
        while i < len(matrix):
            j = 0
            while j < len(matrix[i]):
                if matrix[i][j].isdigit():
                    matrix[i][j] = int(matrix[i][j])
                elif matrix[i][j] == '-':
                    matrix[i][j] = 0
                j += 1
            i += 1
        self.matrix = matrix
    
    def printCommands(self):
        for tip in self.commands:
            print(tip)


    