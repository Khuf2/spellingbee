import datetime

'''
    Uses the current date to generate a cURL command
    to retrieve the Today's Hints data from the New
    York Times website. This resulting command should be 
    executed each day before running play.py. Retrieved
    HTML is stored in a file named nytimes.html.
'''
current_date = str(datetime.datetime.now()).split(" ")[0]
year, month, day = current_date.split("-")

url = "https://www.nytimes.com/"+ year + "/" + month + "/" + day + "/crosswords/spelling-bee-forum.html"

print("\ncurl -o nytimes.html " + url + "\n")