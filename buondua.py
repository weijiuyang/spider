    #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 19:37:51 2019

@author: jiuyang.wei
"""

import sys,datetime
import ssl
import requests,time
import os
from buondua_save import save_suit
from bs4 import BeautifulSoup
from headers import get_ua
from config import *
import redis
#基础配置
script_dir = os.path.dirname(os.path.abspath(__file__))

if not os.path.exists(path):
    os.mkdir(path)

if not os.path.exists(previewpath):
    os.mkdir(previewpath)

html_short=r"https://buondua.com"

red = redis.Redis(host='localhost', port=6379, db=10)
red9 = redis.Redis(host='localhost', port=6379, db=9)

red11 = redis.Redis(host='localhost', port=6379, db=11)
red12 = redis.Redis(host='localhost', port=6379, db=12) #column
red13 = redis.Redis(host='localhost', port=6379, db=13) #mnname
red14 = redis.Redis(host='localhost', port=6379, db=14) #keywords
red15 = redis.Redis(host='localhost', port=6379, db=15) #description
red16 = redis.Redis(host='localhost', port=6379, db=16)

if(len(sys.argv)==2):
    page_num_argv=int(sys.argv[1])
else:
    page_num_argv=5
headers = {}
site = r'https://buondua.com'

page_link=site
print(page_link)
for page in range(1,page_num_argv):
    if not page == 1:
        page_link = site+"/?start=%s" % (page-1) * 20
    #得到当前页更新的所有写真
    print(page_link)

    proxy_url = f"{origin}?url={page_link}"
    response = requests.get(proxy_url)
    remote_content = response.content  # 这是从远程服务器获取的原始字节数据
    # 解码字节数据
    decoded_content = response.content.decode('utf-8')
    text_page =BeautifulSoup(decoded_content, 'html.parser')


    pretty_html = text_page.prettify()

    file_path = os.path.abspath(__file__).split('.')[0]
    print(file_path)
    # exit()
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    with open(f"{file_path}/pretty_file.html", "w", encoding="utf-8") as file:
        file.write(pretty_html)  # Save the pretty HTML to another file
    info_suit = text_page.find_all('div', class_='item-thumb') 
    print(len(info_suit))
    for info in info_suit:
        link=info.a['href']
        title=info.a.img['alt']
        print(link, title)
        # pre_img_url = info.a.img['src']
        # proxy_pre_img_url = f"{origin}?url={pre_img_url}"
        # pre_img = requests.get(proxy_pre_img_url) 
        # preimg = f'{previewpath}/{title}.webp'
        # f = open(preimg, 'wb')    
        # f.write(pre_img.content)
        # f.close() 
        # exit()
        # continue
        #保存这一期写真
        pathdirs = os.path.join(path, title)

        if  not os.path.exists(pathdirs) :
            print('ssss')
            time.sleep(10)
            red.set(title, 50)
            nowdate = datetime.datetime.now().date().strftime("%Y%m%d")

            red9.sadd(nowdate, title)
            red11.set(title, 'buondua')
            
            save_suit(headers, title, link, html_short) 
        # exit()