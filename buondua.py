    #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 19:37:51 2019

@author: jiuyang.wei
"""

import sys
import ssl
import requests
import os
from save import save_suit
from bs4 import BeautifulSoup
from headers import get_ua
import urllib3
# urllib3.disable_warnings()
# ssl._create_default_https_context = ssl._create_unverified_context
#基础配置
path=r"/Users/vajorstack/Pictures/image"   
backpath=r"/Users/vajorstack/Pictures/backup"  
# headers = get_ua()
headers = { "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            # "cookie":"_ga=GA1.1.286972078.1696642358; _ga_KQG2TM0VBD=GS1.1.1696679095.2.1.1696680582.0.0.0",
            "host": "buondua.com"} 
# headers = { "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
#             "cookie": "UM_distinctid=174639a924226-0629a84b4d047c-15306251-13c680-174639a9243582; CNZZDATA1263487746=579143261-1599398858-https%253A%252F%252Fwww.google.com%252F%7C1607414870; __51cke__=; __tins__19410367=%7B%22sid%22%3A%201607416062237%2C%20%22vd%22%3A%202%2C%20%22expires%22%3A%201607417866359%7D; __51laig__=2",
#             } 
headers= {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh-Hans;q=0.9",
    "Connection": "keep-alive",
    "Host": "buondua.com", 
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
   "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
    }

# headers = get_ua()
#读取置顶页（默认5页）       
if(len(sys.argv)==2):
    page_num_argv=int(sys.argv[1])
else:
    page_num_argv=5

site = r'https://buondua.com'

page_link=site
print(page_link)
# break_flag=0
#获得前几页写真
for page in range(1,page_num_argv):
    if not page == 1:
        page_link = site+"/?start=%s" % (page-1) * 20
    #得到当前页更新的所有写真
    print(page_link)
    r_page = requests.get(page_link, verify = False,headers=headers, timeout = 5 )  # 向目标url地址发送get请求，返回一个response对象
    r_page.encoding='utf-8'
    text_page=BeautifulSoup(r_page.text, 'lxml')
    print(r_page.text)
    exit()
    text_page=BeautifulSoup(r_page.text, 'html.parser')

    info_suit = text_page.find_all('a', class_='item-link popunder') 

    for info in info_suit:
        link=info.a['href']
        title=info.a['title']
        print(link,title)
        exit()
        #保存这一期写真
        backdirs=backpath+"/%s"%title
        if not os.path.exists(backdirs):
            save_suit(headers, title, link, html_short) 
            
            
            
            
            
                            
