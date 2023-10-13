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
from save_hhhy import save_suit
from bs4 import BeautifulSoup
from headers import get_ua
from spidersetting import *
from remove import *
import urllib3
urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context
#基础配置

headers = get_ua()

# print(headers)
# headers = { "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
#             "Referer": "https://www.mn5.cc/"}  
 
session=requests.session()

#读取置顶页（默认5页）       
if(len(sys.argv)==2):
    page_num_argv=int(sys.argv[1])
else:
    page_num_argv=5

site = r'https://hhhy.quest'
site = r'https://hhhy.quest/search/pure+Media/'
page_link=site
print(page_link)


remove('d')

# exit()
for page in range(1,page_num_argv):
    if not page == 1:
        page_link=site+"/?query-3-page=%s" % page
    #得到当前页更新的所有写真
    r_page = requests.get(page_link, headers=headers,verify = False)  # 向目标url地址发送get请求，返回一个response对象
    r_page.encoding='utf-8'
    # text_page=BeautifulSoup(r_page.text, 'lxml')
    # print(r_page.text)
    # exit()
    text_page=BeautifulSoup(r_page.text, 'html.parser')
    # print(text_page)
    info_suit = text_page.find_all('div', class_='is-nowrap') 


    # print(info_suit)
    # print(len(info_suit))
    # exit()
    for info in info_suit:
        try:
            link=info.a['href']
            title=info.a.text
            dirs=path + "/%s" % title
            backdirs=backpath + "/%s" % title
            # exit()
            if link == '/faq':
                continue

            # print(link,title)
            # print(dirs, backdirs)

            if not os.path.exists(backdirs) and not os.path.exists(dirs):

                save_suit(headers, title, link) 
            print(link,title)
        except:
            continue
        # second_info = info.find_all('div', class_='wp-block-group')
        # print(second_info)
            
            
            
            
            
                            
