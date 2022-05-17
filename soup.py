from bs4 import BeautifulSoup
import requests
import datetime

current_date = str(datetime.datetime.now()).split(" ")[0]
year, month, day = current_date.split("-")
print(year, month, day)

url = "https://www.nytimes.com/"+ year + "/" + month + "/" + day + "/crosswords/spelling-bee-forum.html"
print(url)

nyt_hints = requests.get(url)
print(nyt_hints.content)
soup = BeautifulSoup(nyt_hints.content, 'html.parser')

'''
    Now extract the relevant HTML elements from the Spelling Bee Hints page
        Whole block: <div class="css-53u6y8">
'''

for block_tag in soup.find_all('div', {'class': 'css-53u6y8'}):
    print(block_tag)