from bs4 import BeautifulSoup
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
    "page": ''
}
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0'
}

for p in range(1, 11):
    params['page'] = str(p)
    response = s.get(url, params=params, headers=headers)
    bs = BeautifulSoup(response.text, 'lxml')

    for figure in bs.find_all('figure', class_='album-box-figure'):
        link = host + figure.find('a')['href']
        fetch(link)
