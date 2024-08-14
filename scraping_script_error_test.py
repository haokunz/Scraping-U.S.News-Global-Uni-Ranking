import urllib.request
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import requests
#r=requests.get(url='https://www.usnews.com/education/best-global-universities/rankings?page=' + str(i + 1), params= {'param':'1'}, headers={'Connection':'close'})

def Read(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'),
        ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    ]
    html = opener.open(url).read()
    return html

items, rankings, universities, locations = [], [], [], []

for i in range(246):  # There are 246 pages for 2460 universities in the 2024 edition
    url = 'https://www.usnews.com/education/best-global-universities/rankings'
    #r=requests.get(url='https://www.usnews.com/education/best-global-universities/rankings?page=' + str(i + 1), params= {'param':'1'}, headers={'Connection':'close'})
    
    retry_count = 3
    for attempt in range(retry_count):
        try:
            html = Read(url).decode('utf-8')
            break  # Exit the retry loop if the request is successful
        except Exception as e:
            print(f"Error on page {i + 1}: {e}")
            if attempt < retry_count - 1:
                print(f"Retrying... ({attempt + 1}/{retry_count})")
                time.sleep(2)  # Delay between retries
            else:
                print("Failed after multiple attempts.")
                continue  # Skip to the next page after retries
    
    soup = BeautifulSoup(html, 'html.parser')

    for ranking in soup.findAll('span', attrs={'class': 'rankscore-bronze'}):
        rankings.append(int(re.findall(r'\d+', ranking.text)[0]))
    for university in soup.findAll('a', attrs={'class': None, 'id': None, 'href': re.compile("^https://www.usnews.com/education/best-global-universities/rankings")}):
        universities.append(university.text)
    for location in soup.findAll('span', attrs={'class': None, 'id': None}):
        if location.text != 'Tie':
            locations.append(location.text)

    print("Page {} Completed...".format(i + 1))
    time.sleep(1)  # Delay between page requests to avoid rate limiting

items.append(rankings)
items.append(universities)
items.append(locations)

item = ['Ranking', 'University', 'Location']
data = pd.DataFrame(index=item, data=items)
data.T.to_csv('USNews_global_ranking.csv', encoding='utf-8')
