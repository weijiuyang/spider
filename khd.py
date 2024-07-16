    #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 19:37:51 2019

@author: jiuyang.wei
"""

import sys, datetime
import ssl
import requests
import os, redis
from utils import *
from khd_save import save_suit
from bs4 import BeautifulSoup
from headers import get_ua
from config import *
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



red9 = redis.Redis(host='localhost', port=6379, db=9)
red = redis.Redis(host='localhost', port=6379, db=10)
red8 = redis.Redis(host='localhost', port=6379, db=8)

red11 = redis.Redis(host='localhost', port=6379, db=11)

red12 = redis.Redis(host='localhost', port=6379, db=12)
red13 = redis.Redis(host='localhost', port=6379, db=13)
red16 = redis.Redis(host='localhost', port=6379, db=16)


site = r'https://hhhy.quest'
site = r'https://www.4khd.com/page/1'
# site = r'https://hhhy.quest/search/pure+Media/'
page_link=site
print(page_link)


# exit()
for page in range(1,page_num_argv):
    if not page == 1:
        page_link=site+"?query-3-page=%s" % page
    #得到当前页更新的所有写真
    print('---------', page_link)

    # proxy_url = f"{origin}?url={page_link}"
    # print(proxy_url)
    # response = requests.get(proxy_url)

    # response = requests.get(page_link, headers=headers, verify=False)
    response = getHtml(page_link)
    print(response.status_code)
    # print(response.text)
    remote_content = response.content  # 这是从远程服务器获取的原始字节数据

    # 解码字节数据
    decoded_content = remote_content.decode('utf-8')
    text=BeautifulSoup(decoded_content, 'html.parser')
    pretty_html = text.prettify()

    file_path = os.path.abspath(__file__).split('.')[0]
    print(file_path)
    # exit()
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    with open(f"{file_path}/pretty_file.html", "w", encoding="utf-8") as file:
        file.write(pretty_html)  # Save the pretty HTML to another file

    info_suit = text.find_all('div', class_='is-nowrap') 
    info_suit = [suit['src'] for suit in text.find_all('img is-nowrap') if img.get('src')]
    info_suit = [
        (a_tag.get('href'), a_tag.get_text(strip=True))
        for div in text.find_all('div', class_='is-nowrap')  # 查找所有 class 包含 is-nowrap 的 div
        if (a_tag := div.find('a'))  # 在每个 div 中查找第一个 a 标签，并确保它存在
    ]

    # print(info_suit)
    # print(len(info_suit))
    # exit()
    for info in info_suit:
        print(info)
        link, title = info
        print(title)
        dirs=path + "/%s" % title
        if link == '/faq':
            continue

        print(link,title)
        print('00000000')
        if not os.path.exists(dirs):
            os.makedirs(dirs)     
            red.set(title, 50)
            red11.set(title, '4khd')
            nowdate = datetime.datetime.now().date().strftime("%Y%m%d")
            red9.sadd(nowdate, title)
            red8.set(title, link)
            match = re.search(r'\[([^\[\]]*)\]$', title)
            part_one, part_two = None, None
            if match:
                content_inside_brackets = match.group(1)
                print("提取的最后一个方括号内的内容：", content_inside_brackets)

                # 去除末尾的方括号内容
                cleaned_text = re.sub(r'\[([^\[\]]*)\]$', '', title).strip()
                print("清理后的内容：", cleaned_text)

                # 分割剩余的字符串，这里假设使用 " – " 进行分割
                parts = cleaned_text.rsplit("–", 1)  # 使用 rsplit 来确保只从最后一个破折号分割
                if len(parts) == 2:
                    part_one, part_two = parts
                    print("第一部分：", part_one)
                    print("第二部分：", part_two)
                else:
                    print('第一个切割失败，进行第二次切分')
                    print(len(parts))
                    parts = cleaned_text.rsplit("-", 1)  # 使用 rsplit 来确保只从最后一个破折号分割
                    if len(parts) == 2:
                        part_one, part_two = parts
                        print("第一部分：", part_one)
                        print("第二部分：", part_two)
                    else:
                        print('第二个切割失败，进行第三次切分')
                        parts = cleaned_text.rsplit(" ", 1)  # 使用 rsplit 来确保只从最后一个破折号分割
                        if len(parts) == 2:
                            part_one, part_two = parts
                            print("第一部分：", part_one)
                            print("第二部分：", part_two)
                        else:
                            print("分割后不符合预期的两部分")
            else:
                print("没有找到匹配的方括号内容")

            # exit()
            save_suit(headers, title, link) 
            print(link,title)
            print(part_one, part_two)
            print('111111111')
            red12.set(title, part_one)
            red13.set(title, part_two)
            red16.sadd(part_two, title)


                
                
                
                
                
                                
