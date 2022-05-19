import datetime

class SaveHandler():
    '''
        Opens the file and determines the current date for the file
        header. 
    '''
    def __init__(self):
        current_date = datetime.datetime.now()
        month, day, year = current_date.strftime("%B"), current_date.day, current_date.year
        self.header = month + " " + str(day) + ", " + str(year)
        self.save = open(r"save.txt", "a+")

    '''
        If file header is not the current date, wipes the file
        Otherwise, do nothing so we can read in previously found
        words. 
    '''
    def update(self):
        self.save.seek(0)
        x = self.save.readline().rstrip()
        if x != self.header:
            # clear the file
            self.save.truncate(0)

    '''
        Reads in all previously found words (if any) and returns them
        to the client, play.py, in the form of a list. This list is then
        iterated through the guess() function to recover prior game state.
    '''
    def readFound(self):
        self.save.seek(0)
        self.save.readline().rstrip()
        preFound = [x.strip("\n").strip() for x in self.save.readlines()]
        return preFound

    '''
        This will be called by play.py, sending the current found dictionary
        to store.py to update the file with.
    '''
    def writeFound(self, found):
        # Wipe file, rewrite header, write words
        self.save.truncate(0)
        self.save.write(self.header + "\n")
        for words in found.values():
            for word in words:
                self.save.write(word + "\n")
        self.save.close()
