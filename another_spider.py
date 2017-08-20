#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: cirq
# Created Time: 2017-08-19 22:38:38

from bs4 import BeautifulSoup
from PIL import Image
import requests
import sqlite3
import re
import io
import os

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

host = 'http://www.hpoi.net/'
se = requests.session()
tre = re.compile(r'^相册:(.*?) by (.*?) \| Hpoi手办维基$')
sre = re.compile(r'fn_comment.init\((\d+)\);')
image_dir = 'images/'

insert_album = 'INSERT INTO album(url,title,author,date,pics,clicks,source,intro) VALUES(?,?,?,?,?,?,?,?);'
insert_image = 'INSERT INTO image(name,url,album_id) VALUES(?,?,?);'
find_albumid = 'SELECT id FROM album WHERE url=?;'

def fetch(link):
    db = sqlite3.connect('hpoi.db')
    cur = db.cursor()
    try:
        if not os.path.exists(os.path.join(os.getcwd(), image_dir)):
            os.mkdir(image_dir)

        url = host + link
        response = se.get(url)
        bs = BeautifulSoup(response.text, 'lxml')

        title = str(bs.title.string.encode('utf-8'))
        m = tre.match(title)
        title, author = m.group(1), m.group(2)

        table = bs.find('table', class_='table')
        trs = table.find_all('tr')
        date = trs[0].find_all()[1].string.strip()
        pics = int(trs[1].find_all()[1].string.strip())
        clicks = int(trs[2].find_all()[1].string.strip())
        s = trs[3].find_all()[1]
        try:
            source = s.string.strip()
        except AttributeError:
            source = next(s.strings).strip()[:-2]

        bq = bs.find('blockquote')
        intro = bq.strings.strip() if bq else ''

        image_list = []
        for image_div in bs.find_all('div', class_='av-masonry-image-container'):
            img_url = image_div.find('img')['src']
            img_name = img_url.split('/')[-1]
            image_list.append( (img_url, img_name) )
        times = pics / 18
        if times > 0:
            script = bs.find_all('script')[-1].string
            tupian = sre.findall(script)[0]
            furl = host + 'album/gallery/' + tupian
            params = {
                "offset": 0,
                "action": 'gal',
                "items": 18
            }
            for i in range(1, times+1):
                params['offset'] = 18 * i
                response = se.get(furl, params=params)
                subbs = BeautifulSoup(response.text, 'lxml')
                for image_div in subbs.find_all('div', class_='av-masonry-image-container'):
                    img_url = image_div.find('img')['src']
                    img_name = img_url.split('/')[-1]
                    image_list.append( (img_url, img_name) )

        t = (unicode(url), unicode(title), unicode(author), unicode(date), pics, clicks, unicode(source), unicode(intro))
        cur.execute(insert_album, t)
        t = (t[0],)
        cur.execute(find_albumid, t)
        aid = cur.fetchone()[0]
        for iurl, name in image_list:
            resp = se.get(iurl).content
            img = Image.open(io.BytesIO(resp))
            img.save(os.path.join(image_dir, name))
            t = (unicode(name), unicode(iurl), aid)
            cur.execute(insert_image, t)
        db.commit()
    finally:
        cur.close()
        db.close()

if __name__ == '__main__':
    l = 'album/466'
    fetch(l)
