import grequests
from bs4 import BeautifulSoup
import pandas as pd
import glob


def get_urls():
    urls = []
    for x in range(0, 200, 50):
        urls.append(f'https://myanimelist.net/topanime.php?type=bypopularity&limit={x}')
    return urls


def get_data(urls):
    reqs = [grequests.get(link) for link in urls]
    resp = grequests.map(reqs)
    return resp


def parse_data(resp):
    popular_anime_list = []
    for r in resp:
        soup = BeautifulSoup(r.text, 'lxml')
        items = soup.find_all('tr', {'class': 'ranking-list'})
        for item in items:
            details = item.find('div', {'class': 'information di-ib mt4'}).text.strip().split('\n')
            popular_anime = {
                'title': item.find('div', {'class': 'di-ib clearfix'}).find('h3', {
                    'class': 'hoverinfo_trigger fl-l fs14 fw-b anime_ranking_h3'}).text.strip(),
                'eps': details[0],
                'date': details[1],
                'members': details[2],
                'rating': item.find('div', {'class': 'js-top-ranking-score-col di-ib al'}).text.strip()
            }
            popular_anime_list.append(popular_anime)
            print('Added', popular_anime)
    return popular_anime_list


urls = get_urls()
resp = get_data(urls)
df = pd.DataFrame(parse_data(resp))
print(df.head())
df.to_csv('popular-anime.csv', index=False)
