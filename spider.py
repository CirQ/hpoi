from bs4 import BeautifulSoup
import logging
import requests
from another_spider import fetch

s = requests.session()

host = 'http://hpoi.net/'

url = host + 'album/list'

params = {
    "order": 'update',
    "r18": '-1',
    "pageCuunt": '10',
    "original": '0',
    "itemCategory": '0',
    "category": '60001',
    "page": 0
}

for p in range(1, 2):
    params['page'] = p
    response = s.get(url, params=params)
    bs = BeautifulSoup(response.text, 'lxml')

    for figure in bs.find_all('figure', class_='album-box-figure'):
        link = figure.find('a')['href']
        logging.debug('fetching ' + link)
        fetch(link)
