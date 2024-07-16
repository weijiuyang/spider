#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 18:53:50 2020

@author: vajorstack
"""

import os
import sys
from utils import *
import requests
# from headers import get_ua
import re
import math, datetime
import time,json
from key import keys, key_girl, ai_key
from bs4 import BeautifulSoup
from pyexiv2 import Image
from config import *
import time
import redis




red8 = redis.Redis(host='localhost', port=6379, db=8)
red9 = redis.Redis(host='localhost', port=6379, db=9)
red = redis.Redis(host='localhost', port=6379, db=10)
red10 = redis.Redis(host='localhost', port=6379, db=10) #column
red11 = redis.Redis(host='localhost', port=6379, db=11) #column

red12 = redis.Redis(host='localhost', port=6379, db=12) #column
red13 = redis.Redis(host='localhost', port=6379, db=13) #mnname
red14 = redis.Redis(host='localhost', port=6379, db=14) #keywords
red15 = redis.Redis(host='localhost', port=6379, db=15) #description
red16 = redis.Redis(host='localhost', port=6379, db=16)
red17 = redis.Redis(host='localhost', port=6379, db=17)
red18 = redis.Redis(host='localhost', port=6379, db=18)
red19 = redis.Redis(host='localhost', port=6379, db=19)
red20 = redis.Redis(host='localhost', port=6379, db=20)


# records = red.hgetall(code)
# exit()


# attempts, delay这两个参数是必填的
def stop_f(attempts, delay):

    print('发生异常了，正在进行重试！')

def redis_save(title, link, public, public_no, public_name, girlname, keywords, description, website):
    dirs = os.path.join(path, title)
    os.makedirs(dirs, exist_ok = True)
    red.set(title, 50)
    nowdate = datetime.datetime.now().date().strftime("%Y%m%d")
    red8.set(title, link)
    red9.sadd(nowdate, title)
    red11.set(title, website)
    red12.set(title, public)
    red13.set(title, girlname)
    red19.set(title, public_no)
    red20.set(title, public_name)
    if keywords:
        red14.set(title, ','.join(keywords))
        for keyword in keywords:
            red17.sadd(keyword, title)
    if description:
        red15.set(title, description)
    red16.sadd(girlname, title)


def get_src_list(link, text, img_short, website = 'xgmn'):
    match website:
        case "xiutaku":
            div_contents = text.find_all('div', class_='article-fulltext')
            src_list = []
            try:
                for div_content in div_contents:
                    all_images = div_content.find_all('img')
                    for img in all_images:
                        print(img['src'])
                        src_list.append(img['src'])
            except Exception as e:
                print(f"An error occurred: {e}")
        case "xgmn":
            div_contents = text.find_all('div', class_='content')
            src_list = []
            try:
                for div_content in div_contents:
                    all_images = div_content.find_all('img')
                    for img in all_images:
                        # one_image = img_short + src
                        src_list.append( img_short + img['src'])
            except Exception as e:
                print(f"An error occurred: {e}")
        case "4khd":
            src_list = [img['src'] for img in text.find_all('img') if img.get('src')]
            src_list = src_list[:20]
            one, two = link.split('.html')
            three = one.split('/')[-1]
            print(three)
            print('999999')
            newsrc_list = [src for src in src_list if three in src]
            if not len(newsrc_list) == 0 :
                src_list = newsrc_list
        case "cosplaytele":
            src_list = [img['src'] for img in text.select('figure.gallery-item img') if img.get('src')]
    return src_list


def find_pages(title, link, html_short, website = 'xgmn', headers={}):
    match website:
        case "xiutaku":
            # proxy_url = f"{origin}?url={link}"
            # r = requests.get(proxy_url, headers = headers, verify = False) 
            r = getHtml(link, html_short)

            decoded_content = r.content.decode('utf-8')
            soup = BeautifulSoup(decoded_content, 'html.parser')
            page_link_box = soup.find('div', class_='pagination-list')
            save_links = []
            if page_link_box:
                page_links = page_link_box.find_all('a')
                for link in page_links:
                    href = link.get('href')
                    if href:
                        print(href)
                        save_links.append(html_short + href)
            return save_links, True
        case "xgmn":
            reg="[0-9]+P"
            pages_group = re.search(reg,title)
            if pages_group == None:
                print("no suit return")
                return 
            pages_all=int(pages_group.group()[:-1])
            pages = math.ceil((pages_all +1) /3)
            print(f'html_short : {html_short}')
            print(f'link : {link}')
            base_link = link.split('.')[0]
            save_links = [f'{html_short}{link}' if pagee == 0 else f'{html_short}{base_link}_{pagee}.html' for pagee in range(pages)]
            return save_links, False
        case "4khd":
            # proxy_url = f"{origin}?url={link}"
            # print(proxy_url)
            # r = requests.get(proxy_url, headers = headers, verify = False) 
            r = getHtml(link, html_short)

            decoded_content = r.content.decode('utf-8')
            soup = BeautifulSoup(decoded_content, 'html.parser')
            page_link_box = soup.find('div', class_='page-link-box')
            save_links = []
            save_links.append(link)
            if page_link_box:
                page_links = page_link_box.find_all('a', class_='page-numbers')
                for link in page_links:
                    href = link.get('href')
                    if href:
                        print(href)
                        save_links.append(href)
            return save_links, True
        case "cosplaytele":
            return [link], True

def getkeys(title, text, website = 'xgmn'):
    keywords, description, column, girl = None, None, None, None
    match website:
        case "xiutaku":
            description = text.find('div', class_='article-info').text
            girlname = text.find('a', class_='is-girl').text
            public = text.find('a', class_='is-medium').text
            pattern = re.compile(r'\d+')
            match = pattern.search(title)
            public_name = title
            if match:
                public_no = match.group(0)
        case "xgmn":
            keywords, description, column, girl = keys(title, text)
        case "4khd":
            origin_title = title
            public, public_no, public_name, girlname, keywords  = ai_key(title)
            if title[0] == '[':
                title = title.split(']')[1]
            title = title.split('[')[0]
            title = title.split('()')[0]
            print(title)
            parts = title.rsplit("-", 1)  # 使用 rsplit 来确保只从最后一个破折号分割
            if len(parts) == 2:
                part_one, part_two = parts
                print("第一部分：", part_one)
                print("第二部分：", part_two)

            else:
                print('第二个切割失败，进行第三次切分')
                parts = title.rsplit(" ", 1)  # 使用 rsplit 来确保只从最后一个破折号分割
                if len(parts) == 2:
                    part_one, part_two = parts
                    print("第一部分：", part_one)
                    print("第二部分：", part_two)
                else:
                    print('第三个切割失败，进行第四次切分')
                    parts = title.rsplit("《", 1)  # 使用 rsplit 来确保只从最后一个破折号分割
                    if len(parts) == 2:
                        part_one, part_two = parts
                        part_two = part_two.replace('》', ' ')
                        print("第一部分：", part_one)
                        print("第二部分：", part_two)
                    else:
                        print("分割后不符合预期的两部分")
            print(part_one, part_two)
            part_one = part_one.strip()
            part_two = part_two.strip()
            if origin_title[0] == '[':
                column = part_one
                girl = part_two
            else:
                if ' ' in part_one:
                    girl = part_one.split(' ')[1]
                else:
                    girl = part_one
                column = part_two
            print("girl：", girl)

            print("column", column)
            if not public:
                public = column
            if not girlname :
                girlname = girl
            
        case "cosplaytele":
            public, public_no, public_name, girlname, keywords  = ai_key(title)

            worktitle = title.split('"')[0]
            worktitle = worktitle.split('“')[0]
            if 'cosplay' in worktitle:
                girl = worktitle.split('cosplay')[0].strip()
                print(f'{girl}: girl')

                worktitle = worktitle.split('cosplay')[1]
                print(worktitle.split('-'))
                cosplay = worktitle.split('-')[0]
                print(f'{cosplay}: cosplay')

                column = '-'.join(worktitle.split('-')[1:])
            else:
                girl = worktitle.split('-')[0]
                girl = girl.strip()
                column = '-'.join(worktitle.split('-')[1:])
            if not public:
                public = column
            if not girlname :
                girlname = girl
    return public, public_no, public_name, girlname, keywords, description 

# @retry(stop_func=stop_f,stop_max_attempt_number=5)
def save_suit(headers, title, link, html_short, website, proxy = False, force = False):
    dirs = os.path.join(path, title)
    print(dirs)
    print("save_suit")
    print( title, link, html_short, website, proxy, force)
    # exit()
    img_short = html_short
    #找到一共多少张图片
    print(title, link, html_short, website)
    print("find_pages")

    save_links, proxy = find_pages(title, link, html_short, website, headers)
    print(save_links)
    # exit()
    begin=time.time()   
    page_all_count = 1    
    print(save_links)
    image = None

    for suit_link in save_links:    
        try:
            print(suit_link)
            if proxy:
                # proxy_url = f"{origin}?url={suit_link}"
                # # print(proxy_url)
                # r = requests.get(proxy_url, headers = headers, verify = False) 
                r = getHtml(suit_link, html_short)

            else:
                r = requests.get(suit_link, headers = headers,verify = False)  # 向目标url地址发送get请求，返回一个response对象
            r.encoding='utf-8'   
            remote_content = r.content  # 这是从远程服务器获取的原始字节数据
            # 解码字节数据
            decoded_content = r.content.decode('utf-8')
            text_page =BeautifulSoup(decoded_content, 'html.parser')
            pretty_html = text_page.prettify()
            file_path = os.path.abspath(__file__).split('.')[0]
            print(file_path)
            os.makedirs(f"{file_path}_{website}", exist_ok = True)
            with open(f"{file_path}_{website}/pretty_file.html", "w", encoding="utf-8") as file:
                file.write(pretty_html)  # Save the pretty HTML to another file
        
        except Exception as e:
            time.sleep(2)
            print(e)
            # pass-6]\
        text = BeautifulSoup(r.text, 'html.parser')

        if not red10.get(title) :
            try:
                public, public_no, public_name, girlname, keywords, description = getkeys(title, text, website)
            except:
                public, public_no, public_name, girlname, keywords, description = None, None, None, None, None, None
            print('get_key')
            print(public, public_no, public_name, girlname, keywords, description)
            # exit()
            redis_save(title, link, public, public_no, public_name, girlname, keywords, description, website)
        
        if not force:
            continue
        print("task: get_src_list")

        src_list = get_src_list(link, text, html_short, website)
        print(src_list)
        random_sleep_time = random.uniform(0, 1)

        # 暂停执行随机时间
        time.sleep(random_sleep_time)
        for src in src_list:
            try:
                if proxy:
                    # proxy_url = f"{origin}?url={src}"
                    # image = requests.get(proxy_url, headers = headers, verify = False) 
                    print(proxy)
                    image = getHtml(src, html_short)

                else:
                    image = requests.get(src, headers = headers, verify = False) 
                imgs_name=f'{dirs}/{page_all_count}.webp'
                f = open(imgs_name, 'wb')    
                f.write(image.content)
                f.close() 
                #写入图片关键字和其他信息
                img_fix=Image(imgs_name)
                img_fix.clear_exif()
                try:
                    _dict = {'Xmp.dc.subject': list(keywords), 
                                'Xmp.dc.title': column+' '+mnname,
                                'Xmp.dc.description': description, 
                                'Xmp.dc.creator': [mnname], 
                                'Xmp.photoshop.DateCreated':str(int(time.strftime('%Y',time.localtime()))-100)+time.strftime('-%m-%dT%H:%M:%S',time.localtime())
                    }  
                    img_fix.modify_xmp(_dict)
                except:
                    pass
                page_all_count+=1
            except Exception as e:
                print('15')
                time.sleep(2)
                print(e)
            # 当重试完成后还未成功，则返回超时
                raise TimeoutError
    print('100 %')
    pre_img = f'{previewpath}/{title}.webp'
    if not os.path.exists(pre_img) and image:
        f = open(pre_img, 'wb')    
        f.write(image.content)
        f.close() 
    #记录保存套图 用时
    end=time.time()
    last=end-begin
    print(round(last,2))
    print(dirs)


def get_attribute_web_for_one(link):
    if  "xgmn" in link:
        headers = { "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'}  
        
        html_short=r"https://www.xgmn5.top"
        proxy = False
        r = requests.get(link, verify=False, headers = headers)
        r.encoding='utf-8'   
        remote_content = r.content  # 这是从远程服务器获取的原始字节数据
        # 解码字节数据
        decoded_content = r.content.decode('utf-8')
        text_page =BeautifulSoup(remote_content, 'html.parser')
        title = text_page.title.text
        website = 'xgmn'
    if  "4khd" in link:
        if link.split('/')[-2][-4:] == 'html':
            link = ('/').join(link.split('/')[:-1])
        html_short = r'https://www.4khd.com'
        headers = {}
        proxy = True
        proxy_url = f"{origin}?url={link}"
        # print(proxy_url)
        # r = requests.get(proxy_url, headers = headers,verify = False)  # 向目标url地址发送get请求，返回一个response对象
        
        r = getHtml(link, html_short)
        r.encoding='utf-8'   
        remote_content = r.content  # 这是从远程服务器获取的原始字节数据
        # 解码字节数据
        # decoded_content = r.content.decode('utf-8')
        text_page =BeautifulSoup(remote_content, 'html.parser')
        pretty_html = text_page.prettify()
        file_path = os.path.abspath(__file__).split('.')[0]
        print(file_path)
        os.makedirs(f"{file_path}_{website}", exist_ok = True)
        with open(f"{file_path}_{website}/pretty_file.html", "w", encoding="utf-8") as file:
            file.write(pretty_html) 
        h3_tag = text.find('h3')

        # 提取并打印 <h1> 标签的文本内容
        if h3_tag:
            h3_text = h3_tag.get_text(strip=True)
            title = h3_text
            print(f"H1 Text: {h1_text}")
        else:
            print("No matching <h1> tag found")
        website = '4khd'

      
    if "cosplaytele" in link:
        html_short = r'https://cosplaytele.com'
        headers = {}
        proxy = True
        proxy_url = f"{origin}?url={link}"
        # print(proxy_url)
        # # r_page = requests.get(proxy_url, verify=False)
        # r = requests.get(proxy_url, headers = headers,verify = False)  # 向目标url地址发送get请求，返回一个response对象
        
        r = getHtml(link, html_short)
        r.encoding='utf-8'   
        remote_content = r.content  # 这是从远程服务器获取的原始字节数据
        # 解码字节数据
        decoded_content = r.content.decode('utf-8')
        text =BeautifulSoup(decoded_content, 'html.parser')
        h1_tag = text.find('h1', class_='entry-title')

        # 提取并打印 <h1> 标签的文本内容
        if h1_tag:
            h1_text = h1_tag.get_text(strip=True)
            title = h1_text
            print(f"H1 Text: {h1_text}")
        else:
            print("No matching <h1> tag found")
        
        website = 'cosplaytele'
    return headers, html_short, title, link, website, proxy

def save_for_one(link):
    headers, html_short, title, link, website, proxy = get_attribute_web_for_one(link)
    print(link)
    # exit()
    save_suit(headers, title, link, html_short, website, proxy, force = True)


if __name__ == "__main__":
    website = r'https://www.4khd.com/content/02/nekokoyoshi-blast-girl-meow-xiaoji-wind-chime-princess.html'
    website = r'https://www.4khd.com/content/27/caviar-fish-in-app-purchase-series-37-degrees-2.html'
    website = r'https://www.4khd.com/content/26/emergency-planning-xiao-en-vip-gymnastics-suit-r18.html'
    save_for_one(input('请输入网址'))
    # get_attribute_web_for_one()

