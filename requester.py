from bs4 import BeautifulSoup
import requests

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

        # Parsing of Hints using bs4 and cURLed HTML file
        '''
            Changed so that it will read the text of different
            HTML blocks and find the spelling bee grid div.
            This was a problem on infrequent cases.
        ''' 
        relevant_block = soup.find('section', {'class': 'meteredContent'})
        self.paragraphs = relevant_block.findChildren('p', {'class': 'content'}, recursive=True)
        self.matrix = relevant_block.findChildren('table', recursive=True)
        
        '''
            Trash paragraph 1.
            Paragraph 2 = letters
            Paragraph 3 = Words, Points, Pangrams, Bingos
            Trash paragraph 4.
            Paragraph 5 = Table/Matrix

        '''
        
        # Parsing of Spelling Bee answers using bs4 and requests
        sb = requests.get('https://www.nytimes.com/puzzles/spelling-bee')
        answers = BeautifulSoup(sb.content, 'html.parser')
        relevant_block = answers.find('div', {'class': 'pz-game-screen'})
        self.search_text = str(relevant_block.findChildren('script', recursive=False)[0])
        
        self.coreLetter = None
        self.letters = {}

    '''
        Retrieves core letter, calls self.getLetters if
        core letter is not yet set. Should not happen
        with current bee.py implementation.
    '''
    def getCoreLetter(self):
        if self.coreLetter is None:
            self.getLetters()
        return self.coreLetter

    def getAnswers(self):
        start = self.search_text.find('"answers"')
        end = self.search_text.find('"id"')
        self.search_text = self.search_text[start:end]
        start = self.search_text.find('[')
        end = self.search_text.find(']')
        self.search_text = self.search_text[start+1:end]

        answers = self.search_text.split(",")
        i = 0
        while i < len(answers):
            answers[i] = answers[i][1:-1].upper()
            i += 1
        return answers

    '''
        Returns alphabetically sorted dictionary of candidate
        letters for the Spelling Bee. Values of dictionary
        correspond to the resulting row index of the letter
        in the full matrix. This is used by guess() and other
        bee.py functions to update the matrix accordingly.
    '''
    def getLetters(self):
        s = self.paragraphs[1].text.upper()
        s = s.replace("\n", "").split()
        letters = []
        for e in s:
            letters.append(e)
        self.coreLetter = letters[0]
        # Put letters in alphabetical order
        letters.sort()
        l = {}
        for row_index, char in enumerate(letters, 1):
            l[char] = row_index
        
        self.letters = l
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
        prefixList = self.paragraphs[4].text.replace("\n", "").split()
        prefixes = {}
        for prefix in prefixList:
            p = prefix.split("-")
            prefixes[p[0].upper()] = int(p[1])

        return prefixes

    '''
        Returns a 2D-list representing the given hints matrix,
        which provides counts on words of a given length and
        counts on words starting with a given letter. Most of
        this function is just parsing the text from HTML. 
    '''
    def getMatrix(self):
        matrix = []

        rows = self.matrix[0].findChildren("tr", {'class': 'row'}, recursive=True)
        for row in rows:
            cells = row.findChildren("td", {'class': 'cell'}, recursive=False)
            matrixRow = []
            for cell in cells:
                if cell.text.replace(":", "").isdigit():
                    matrixRow.append(int(cell.text.replace(":", "")))
                else:
                    matrixRow.append(cell.text.upper())
            matrix.append(matrixRow)

        return matrix
