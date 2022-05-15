class Bee():
    def __init__(self):
        # Need to tag the necessary letter somehow
        # Uppercase?
        self.letters = {}
        self.matrix = []
        self.prefixes = {}
        self.coreLetter = ""

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
        with open('hints.txt', 'r') as f:
            l = [[char.strip("\n").strip(" ") for char in line.split(',')] for line in f]
        divider = l.index([''])
        for index, row in enumerate(l[1:divider-1],1):
            if row[0].find('*') != -1:
                row[0] = row[0].strip('*')
                self.coreLetter = row[0]
            self.letters[row[0]] = index
        self.setMatrix(l[:divider])
        self.setPrefixes(l[divider+1:])
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
            print(row)

    def getPrefixes(self):
        print("Prefixes:")
        for item in self.prefixes.items():
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

            print("Added " + guess + " to found words.")

            self.matrix[self.letters[guess[0]]][len(guess)-3] -= 1
            self.prefixes[guess[0:2]] -= 1
        else:
            print(guess + " has already been found.")

    def undo(self):
        if len(self.guessStack) > 0:
            word = self.guessStack.pop()
            self.found[word[0]].remove(word)

            self.matrix[self.letters[word[0]]][len(word)-3] += 1
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


    