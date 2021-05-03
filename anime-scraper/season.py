import requests
from bs4 import BeautifulSoup
import pandas as pd

seasonal_anime_list = []

def extract():
    year = input('Input airing year :')
    season = input('Input airing season :')
    url = 'https://myanimelist.net/anime/season/{}/{}'.format(year, season)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup.find_all('div', {'class': 'seasonal-anime js-seasonal-anime'})

def transform(items):
    for item in items:
        title = item.find('h2', {'class': 'h2_anime_title'}).text
        synopsis = item.find('span', {'class': 'preline'}).text.strip()
        eps = item.find('div', {'class': 'eps'}).text.strip()
        studio = item.find('span', {'class': 'producer'}).text.strip()
        air = item.find('div', {'class': 'info'}).text.strip().replace('\n', '')
        rating = item.find('span', {'title': 'Score'}).text.strip()
        members = item.find('span', {'class': 'member fl-r'}).text.strip()
        seasonal_anime = {
            'title': title,
            'synopsis': synopsis,
            'eps': eps,
            'studio': studio,
            'air': air,
            'rating': rating,
            'members': members
        }
        seasonal_anime_list.append(seasonal_anime)
    return

def load():
    df = pd.DataFrame(seasonal_anime_list)
    df.to_csv('seasonal-anime.csv', index=False)

items = extract()
transform(items)
load()
print('Saved to CSV')
