import datetime

current_date = str(datetime.datetime.now()).split(" ")[0]
year, month, day = current_date.split("-")

url = "https://www.nytimes.com/"+ year + "/" + month + "/" + day + "/crosswords/spelling-bee-forum.html"

print("\ncurl -o nytimes.html " + url + "\n")