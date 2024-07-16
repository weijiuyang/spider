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

# 禁用未验证HTTPS请求的警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


script_dir = os.path.dirname(os.path.abspath(__file__))

if not os.path.exists(path):
    os.mkdir(path)

if not os.path.exists(previewpath):
    os.mkdir(previewpath)

session=requests.session()

html_short=r"https://www.xgmn5.top"


url = f'https://www.12356786.xyz/new.html'
url = f'https://www.12356787.xyz/Xiuren/'
short_url = f'https://www.12356786.xyz'
short_url = f'https://www.xgyw09.xyz'
short_url = f'https://www.xgmn5.top'

urllist = [f'https://www.xgmn5.top/new.html']

# urllist = [f'https://www.xgmn5.top/plus/search/index.asp?keyword=鱼子酱']

    

red = redis.Redis(host='localhost', port=6379, db=10)
red9 = redis.Redis(host='localhost', port=6379, db=9)
red8 = redis.Redis(host='localhost', port=6379, db=8)

red11 = redis.Redis(host='localhost', port=6379, db=11)
red16 = redis.Redis(host='localhost', port=6379, db=16)


headers = { "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'}  

headers = { "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
            "Host": "www.xgmn5.top",
            "Accept-Encoding": "gzip, deflate, br"}
#urllist = ['https://www.321782.xyz/Xiuren/page_%s.html'%one for one in range(2,100)]

# print(datetime.datetime.now().date())
# print(urllist)
# exit()
print(url)
for url in urllist:
    print(url)
    # exit()
    r_page = requests.get(url,verify=False)  # 向目标url地址发送get请求，返回一个response对象
    
    remote_content = r_page.content  # 这是从远程服务器获取的原始字节数据
    # 解码字节数据
    decoded_content = r_page.content.decode('utf-8')
    text_page =BeautifulSoup(decoded_content, 'html.parser')


    pretty_html = text_page.prettify()

    file_path = os.path.abspath(__file__).split('.')[0]
    print(file_path)
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    with open(f"{file_path}/pretty_file.html", "w", encoding="utf-8") as file:
        file.write(pretty_html)  # Save the pretty HTML to another file

    # exit()
    r_page.encoding='utf-8'
    text_page=BeautifulSoup(r_page.text, 'html.parser')
    # print(r_page.content)
    info_suit = text_page.find_all('li', class_='i_list') 
    for info in info_suit:
        link=info.a['href']
        title=info.a['title']
        title = title.replace("/"," ")

        print(link, title)
        pre_img_url = short_url + info.a.img['src']
        pre_img = requests.get(pre_img_url, verify=False)
        preimg = f'{previewpath}/{title}.webp'
        f = open(preimg, 'wb')    
        f.write(pre_img.content)
        f.close() 
        # exit()
        # continue
        #保存这一期写真
        pathdirs = os.path.join(path, title)

        if not os.path.exists(pathdirs) :
            print(f'whyyyy\n{pathdirs}')
            red.set(title, 50)
            nowdate = datetime.datetime.now().date().strftime("%Y%m%d")
            red8.set(title, link)

            red9.sadd(nowdate, title)
            red11.set(title, 'xgmn')
            save_suit(headers, title, link, html_short) 
            
