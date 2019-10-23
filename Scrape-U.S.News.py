import urllib.request
from bs4 import BeautifulSoup
import re
import pandas as pd

def Read(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0')]
    opener.addheaders = [('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]
    html = opener.open(url).read()

    return html

items, rankings, universities, locations = [], [], [], []

for i in range(125): #There are 125 pages for 1250 universities in the 2020 edition
    url = 'https://www.usnews.com/education/best-global-universities/rankings?page=' + str(i+1)
    html = Read(url).decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    for ranking in soup.findAll('span', attrs={'class': 'rankscore-bronze'}):
        rankings.append(int(re.findall('\d+', ranking.text)[0]))
    for university in soup.findAll('a', attrs={'class': None, 'id': None, 'href': re.compile("^https://www.usnews.com/education/best-global-universities/")}):
        universities.append(university.text)
    for location in soup.findAll('span', attrs={'class': None, 'id': None}):
        if location.text != 'Tie':
            locations.append(location.text)
        
    print("Page {} Completed...".format(i+1))

items.append(rankings)
items.append(universities)
items.append(locations)

item = ['Ranking', 'University', 'Location']
data = pd.DataFrame(index=item, data=items)
data.T.to_csv('USNews_global_ranking.csv', encoding='utf-8')
