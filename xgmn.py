    #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 19:37:51 2019

@author: jiuyang.wei
"""

import sys,datetime
import ssl
import requests
import os
from save import save_suit
from bs4 import BeautifulSoup
from headers import get_ua
from config import *
import redis
import urllib3
urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context
#基础配置
script_dir = os.path.dirname(os.path.abspath(__file__))

if not os.path.exists(path):
    os.mkdir(path)

if not os.path.exists(previewpath):
    os.mkdir(previewpath)

session=requests.session()

html_short=r"https://www.xg07.xyz"

headers = { "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "referer":html_short,
            "cookie": "UM_distinctid=174639a924226-0629a84b4d047c-15306251-13c680-174639a9243582; CNZZDATA1263487746=579143261-1599398858-https%253A%252F%252Fwww.google.com%252F%7C1607414870; __51cke__=; __tins__19410367=%7B%22sid%22%3A%201607416062237%2C%20%22vd%22%3A%202%2C%20%22expires%22%3A%201607417866359%7D; __51laig__=2",
            } 

url = f'https://www.12356786.xyz/new.html'
url = f'https://www.12356787.xyz/Xiuren/'
short_url = f'https://www.12356786.xyz'
urllist = [f'https://www.xgyw09.xyz/new.html']


red = redis.Redis(host='localhost', port=6379, db=10)
red9 = redis.Redis(host='localhost', port=6379, db=9)

red11 = redis.Redis(host='localhost', port=6379, db=11)


# urllist = ['https://www.12356787.xyz/Xiuren/page_%s.html'%one for one in range(2,100)]

# print(datetime.datetime.now().date())
# print(urllist)
# exit()
for url in urllist:
    r_page = requests.get(url, headers=headers,verify = False)  # 向目标url地址发送get请求，返回一个response对象
    r_page.encoding='utf-8'
    text_page=BeautifulSoup(r_page.text, 'html.parser')

    info_suit = text_page.find_all('li', class_='related_box') 
    for info in info_suit:
        link=info.a['href']
        title=info.a['title']
        print(link, title)
        pre_img_url = short_url + info.a.img['src']
        pre_img = requests.get(pre_img_url) 
        preimg = f'{previewpath}/{title}.webp'
        f = open(preimg, 'wb')    
        f.write(pre_img.content)
        f.close() 
        # exit()
        # continue
        #保存这一期写真
        pathdirs = os.path.join(path, title)

        if  False or not os.path.exists(pathdirs) :
            print('ssss')
            red.set(title, 50)
            nowdate = datetime.datetime.now().date().strftime("%Y%m%d")

            red9.sadd(nowdate, title)
            red11.set(title, 'xgmn')
            save_suit(headers, title, link, html_short) 
            