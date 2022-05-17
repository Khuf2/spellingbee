from bs4 import BeautifulSoup

class Soup():
    # need child 1, 2, 3, 5 (0-indexed)
    '''
        1: Letters
        2: Words, Points, Pangrams, Bingos
        3: Matrix
        5: 2-letter list
    '''
    def __init__(self):
        nyt = open('nytimes.html', "r")
        soup = BeautifulSoup(nyt, 'html.parser')

        relevant_block = soup.find_all('div', {'class': 'css-53u6y8'})[1]
        self.paragraphs = relevant_block.findChildren('p', {'class': 'evys1bk0'}, recursive=False)
        self.coreLetter = None

    def getCoreLetter(self):
        if self.coreLetter is None:
            self.getLetters()
        return self.coreLetter

    def getLetters(self):
        s = self.paragraphs[1].text
        # Put letters in alphabetical order
        # Add asterisk after core letter
        letters = (s.split(" "))
        self.coreLetter = letters[0]
        letters.sort()
        l = {}
        for row_index, char in enumerate(letters, 1):
            l[char] = row_index
        
        return l

    def getSummary(self):
        s = self.paragraphs[2].text
        summary = s.split(",")
        i = 1
        while i < len(summary):
            summary[i] = summary[i].strip(" ")
            i += 1
        return summary

    def getPrefixes(self):
        s = self.paragraphs[5].text
        # split on digits
        prefixes = {}
        i = 0
        temp = ""
        while i < len(s):
            temp += s[i]
            if s[i].isdigit():
                temp = temp.strip(" ")
                prefixes[temp[:2]] = int(temp[temp.find("-")+1:])
                temp = ""
            i += 1
        return prefixes

    def getMatrix(self):
        matrix = []
        s = "* " + self.paragraphs[3].text
        # ord($sigma$) = 931, $sigma$ = chr(931)
        
        lines = []
        i = 0
        temp = ""
        while i < len(s):
            if s[i] == ":":
                if len(temp) > 3:
                    line = temp[:-1].split("  ")
                    line[0] = line[0][0]
                    if line[0] == self.coreLetter:
                        line[0] += "*"
                    
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
        temp = temp.split("  ")
        temp[0] = temp[0][0]

        x = 0
        while x < len(temp):
            line[x] = temp[x].strip(" ")
            if temp[x].isnumeric():
                temp[x] = int(temp[x])
            x += 1

        matrix.append(temp)
        return matrix

'''
req = Soup()

print(req.getLetters())
print(req.getSummary())
for pref in req.getPrefixes().items():
    print(pref)
print(req.getMatrix())
'''
