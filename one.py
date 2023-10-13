#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 19:02:46 2020

@author: vajorstack
"""

import ssl
import os
import requests
from save import save_suit
from bs4 import BeautifulSoup
from headers import get_ua
import urllib3
urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context

#基础配置
path=r"/home/vajor/images"   
backpath=r"/home/vajor/backup"  
# headers = get_ua()
# headers['Referer']="https://www.jpxgmn.com/"
headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763",
            "Referer": "https://www.jpxgmn.com/"}  


#爬取一个人的全部图片配置
name_list=['唐婉儿','徐微微','芝芝','绯月樱','杨晨晨','糯美子','徐cake','恩率babe','yoo优优','王梓童']
name_list=['张思允']
html_search=r'https://www.xgmn09.com/plus/search/index.asp?keyword='
html_search=r'https://www.xgmn09.com/plus/search/'
html_short=r"https://www.xgmn09.com/"

#获取所有模特对写真
for name in name_list:
    #search=html_search+str(name.encode("gbk"))[2:-1].replace('\\x','%')+r'&searchtype=title'
    search = html_search + '?keyword=' + name
    print(search)
    r_search = requests.get(search, headers=headers)  # 向目标url地址发送get请求，返回一个response对象
    r_search.encoding='utf-8'
    #print(r_search.text)
    bs_text=BeautifulSoup(r_search.text, 'lxml')
    #获得该模特一共有几页
    # print(bs_text)
    #pages = bs_text.find_all('div', class_='page')[0].find_all('a')
    pages_list = bs_text.find_all('div', class_='pagination')[1].find_all('a')
    
    for page_link in pages_list:
        #获得模特该页上所有套图的写真
        page_link = html_search + str(page_link['href'])
        print(page_link)

        r_page = requests.get(page_link,headers=headers)  # 向目标url地址发送get请求，返回一个response对象
        r_page.encoding='utf-8'
        text_page=BeautifulSoup(r_page.text, 'lxml')
        info_suit = text_page.find_all('div', class_='list')
        for info in info_suit:
            link=info.a['href']
            title=info.a.text
            #保存这一期写真
            print(title)
            print(link)
            backdirs=backpath+"/%s"%title
            if not os.path.exists(backdirs):
                save_suit(headers,title,link,html_short) 
            # else:
                # break
        # else:
        #     continue
        # break


            

