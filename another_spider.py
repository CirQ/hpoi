#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: cirq
# Created Time: 2017-08-19 22:38:38

from bs4 import BeautifulSoup
import requests
import re

host = 'http://www.hpoi.net/'
s = requests.session()
tre = re.compile(r'^相册:(.*?) by (.*?) \| Hpoi手办维基$')

def fetch(link):
    url = host + link
    response =  s.get(url)
    bs = BeautifulSoup(response.text, 'lxml')

    # title = str(bs.title.string.encode('utf-8'))
    # m = tre.match(title)
    # title, author = m.group(1), m.group(2)

    table = bs.find('table', class_='table')
    trs = table.find_all('tr')
    # date = trs[0].find_all('td')[1].string.strip()
    pics = trs[1].find_all('td')[1].string.strip()
    # clicks = trs[2].find_all('td')[1].string.strip()
    # source = trs[3].find_all('td')[1].string.strip()

    # bq = bs.find('blockquote')
    # intro = bq.string.strip() if bq else ''

    # fetch images

    times = int(pics) / 18
    if times > 1:

        # fetch more images

        pass


    # save all data


if __name__ == '__main__':
    l = 'album/466'
    fetch(l)
