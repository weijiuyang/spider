#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 19:02:46 2020

@author: vajorstack
"""

import ssl
import os
import requests, redis, datetime
from save import save_suit
from bs4 import BeautifulSoup
from headers import get_ua
from config import *

import urllib3
urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context

# headers = get_ua()
# headers['Referer']="https://www.jpxgmn.com/"
headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763",
            "Referer": "https://www.jpxgmn.com/"}  


#爬取一个人的全部图片配置
name_list=['唐婉儿','徐微微','芝芝','绯月樱','杨晨晨','糯美子','徐cake','恩率babe','yoo优优','王梓童','张思允','鱼子酱']
name_list=['张思允']
name_list=['鱼子酱']

html_search=r'https://www.xgmn5.top/plus/search/index.asp?keyword='
html_search=r'https://www.xgmn5.top/plus/search/'
html_short=r"https://www.xgmn5.top/"

red = redis.Redis(host='localhost', port=6379, db=10)
red9 = redis.Redis(host='localhost', port=6379, db=9)
red8 = redis.Redis(host='localhost', port=6379, db=8)

red11 = redis.Redis(host='localhost', port=6379, db=11)
red16 = redis.Redis(host='localhost', port=6379, db=16)


#获取所有模特对写真
for name in name_list:
    #search=html_search+str(name.encode("gbk"))[2:-1].replace('\\x','%')+r'&searchtype=title'
    search = html_search + '?keyword=' + name
    print(search)
    r_search = requests.get(search, verify=False)  # 向目标url地址发送get请求，返回一个response对象
    r_search.encoding='utf-8'
    #print(r_search.text)
    remote_content = r_search.content  # 这是从远程服务器获取的原始字节数据
    # 解码字节数据
    decoded_content = r_search.content.decode('utf-8')
    text_page =BeautifulSoup(decoded_content, 'html.parser')

    pretty_html = text_page.prettify()

    file_path = os.path.abspath(__file__).split('.')[0]
    print(file_path)
    # exit()
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    with open(f"{file_path}/pretty_file.html", "w", encoding="utf-8") as file:
        file.write(pretty_html)  # Save the pretty HTML to another file


    r_search.encoding='utf-8'
    text_page=BeautifulSoup(r_search.text, 'html.parser')


    # print(bs_text)
    pages_list = text_page.find_all('div', class_='page')[0].find_all('a')
    # pages_list = text_page.find_all('div', class_='pagination').find_all('a')
    print(pages_list)
    # exit()
    for page_link in pages_list:
        #获得模特该页上所有套图的写真
        href = page_link.get('href')
        if href:
            full_link = html_search + href  # 替换为实际的基础URL
            print(full_link)

            r_page = requests.get(full_link, verify = False)  # 向目标url地址发送get请求，返回一个response对象
            r_page.encoding='utf-8'
            text_page = BeautifulSoup(r_page.text, 'html.parser')
            # info_suit = text_page.find_all('div', class_='list')


            sousuo_divs = text_page.find_all('div', class_='sousuo')
            for div in sousuo_divs:
                # 找到 div 下的所有 a 标签
                a_tags = div.find_all('a')
                for a in a_tags:
                    link = a['href']  # 获取 href 属性
                    title = a.get_text(strip=True)  # 获取 a 标签内的所有文本内容
                    title = title.split('  ')[0]
                    # title = title.replace(".","_")
                    title = title.replace("/","_")
                    print(f"link: {link}")
                    print(f"title: {title}")
                    print(link, title)
                    # exit()
                    pathdirs = os.path.join(path, title)

                    if not os.path.exists(pathdirs)  or True:
                        print(f'whyyyy\n{pathdirs}')
                        red.set(title, 50)
                        nowdate = datetime.datetime.now().date().strftime("%Y%m%d")
                        red8.set(title, link)

                        red9.sadd(nowdate, title)
                        red11.set(title, 'xgmn')
                        save_suit(headers, title, link, html_short) 
                        
                    

