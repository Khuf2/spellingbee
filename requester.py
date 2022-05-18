from bs4 import BeautifulSoup

'''
    From __init__'s self.paragraphs, need children 1, 2, 3, 5 (0-indexed)
    1: Letters
    2: Words, Points, Pangrams, Bingos
    3: Matrix
    5: 2-letter list
'''
class Soup():
    '''
        Initialize the soup object and extract the relevant
        blocks of information. Initialize coreLetter to None
    '''
    def __init__(self):
        nyt = open('nytimes.html', "r")
        soup = BeautifulSoup(nyt, 'html.parser')

        relevant_block = soup.find_all('div', {'class': 'css-53u6y8'})[1]
        self.paragraphs = relevant_block.findChildren('p', {'class': 'evys1bk0'}, recursive=False)
        self.coreLetter = None

    '''
        Retrieves core letter, calls self.getLetters if
        core letter is not yet set. Should not happen
        with current bee.py implementation.
    '''
    def getCoreLetter(self):
        if self.coreLetter is None:
            self.getLetters()
        return self.coreLetter

    '''
        Returns alphabetically sorted dictionary of candidate
        letters for the Spelling Bee. Values of dictionary
        correspond to the resulting row index of the letter
        in the full matrix. This is used by guess() and other
        bee.py functions to update the matrix accordingly.
    '''
    def getLetters(self):
        s = self.paragraphs[1].text
        letters = (s.split(" "))
        self.coreLetter = letters[0]
        # Put letters in alphabetical order
        letters.sort()
        l = {}
        for row_index, char in enumerate(letters, 1):
            l[char] = row_index
        
        return l

    '''
        Returns a list of relevant summary values, such as:
            - Number of points in today's puzzle
            - Number of words in today's puzzle
            - Number of pangrams in today's puzzle
            - Bingo (T/F)
    '''
    def getSummary(self):
        s = self.paragraphs[2].text
        summary = s.split(",")
        i = 1
        while i < len(summary):
            summary[i] = summary[i].strip(" ")
            i += 1
        return summary

    '''
        Returns a dictionary mapping 2-letter prefixes to
        the number of words in the puzzle that begin with
        that prefix. 
    '''
    def getPrefixes(self):
        s = self.paragraphs[5].text + " "
        prefixes = {}
        temp = ""
        digit = False
        i = 0
        while i < len(s):
            # Below conditional called when reading of an integer ends
            # Add the given prefix from temp and continue
            if digit and not s[i].isdigit():
                digit = False
                temp = temp.strip(" ")
                prefixes[temp[:2]] = int(temp[temp.find("-")+1:])
                temp = ""
            temp += s[i]
            if s[i].isdigit():
                digit = True
            i += 1
        return prefixes

    '''
        Returns a 2D-list representing the given hints matrix,
        which provides counts on words of a given length and
        counts on words starting with a given letter. Most of
        this function is just parsing the text from HTML. 
    '''
    def getMatrix(self):
        matrix = []
        s = "* " + self.paragraphs[3].text

        i = 0
        temp = ""
        while i < len(s):
            if s[i] == ":":
                # This conditional ignores the first colon
                if len(temp) > 3:
                    # Separates values in a given row
                    line = temp[:-1].split("  ")
                    # Removes colon if present
                    line[0] = line[0][0]
                    # Designate core letter with an asterisk
                    if line[0] == self.coreLetter:
                        line[0] += "*"
                    
                    # Convert all numerical values into ints
                    # Strip any whitespace off of values
                    # Add to building matrix
                    x = 0
                    while x < len(line):
                        line[x] = line[x].strip(" ")
                        if line[x].isnumeric():
                            line[x] = int(line[x])
                        x += 1
                    matrix.append(line)
                    temp = temp[-1:]
            temp += s[i]
            i += 1

        # Same process as within the while loop
        # One last iteration to catch hanging temp value
        temp = temp.split("  ")
        temp[0] = temp[0][0]

        x = 0
        while x < len(temp):
            temp[x] = temp[x].strip(" ")
            if temp[x].isnumeric():
                temp[x] = int(temp[x])
            x += 1

        matrix.append(temp)
        return matrix
