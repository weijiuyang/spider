#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 18:53:50 2020

@author: vajorstack
"""

import os
import sys
import requests
import re
import math
import time,json
from key import keys
from bs4 import BeautifulSoup
from pyexiv2 import Image
from config import *
import time
import redis


def save_suit(headers, title, link, html_short):
    red12 = redis.Redis(host='localhost', port=6379, db=12) #column
    red13 = redis.Redis(host='localhost', port=6379, db=13) #mnname
    red14 = redis.Redis(host='localhost', port=6379, db=14) #keywords
    red15 = redis.Redis(host='localhost', port=6379, db=15) #description
    red16 = redis.Redis(host='localhost', port=6379, db=16)

    print("save_suit")
    img_short = html_short
    #找到一共多少张图片
    reg="[0-9]+ photos"
    pages_group=re.search(reg,title)
    if pages_group ==  None:
        return
    print(pages_group.group())
    pages_all=int(pages_group.group().split()[0])
    pages=math.ceil(pages_all/20)
    page_all_count=1 
    # exit()

    pages=math.ceil(pages_all/3)+2
    page_all_count=1   
    #查找是否重复，不重复的话创立文件夹
    title = title.replace(".","_")
    dirs = os.path.join(path, title)
    print(dirs)

    if True or not os.path.exists(dirs):
        print(dirs)
        # exit()
        begin=time.time()    
        if not os.path.exists(dirs):  
            os.makedirs(dirs)      
        for pagee in range(0,pages):    
            #获得每一篇链接
            if pagee == 0:
                suit_link=html_short+link
            else:
                suit_link=html_short+link+"?page=%s"%pagee+".html"
            try:
                time.sleep(2)

                proxy_url = f"{origin}?url={suit_link}"
                response = requests.get(proxy_url)
                print(proxy_url)
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
            except Exception as e:
                time.sleep(2)
                # 当重试完成后还未成功，则返回超时
                raise TimeoutError
            # exit()
            if pagee == 0 and  False:
                keywords,description,column,mnname=keys(text_page)
                print(keywords,description,column,mnname)
                print('tttt')
                print(' '.join(keywords))
                print(description)
                red12.set(title, column)
                red13.set(title, mnname)
                red14.set(title, ' '.join(keywords))
                red15.set(title, description)
                print('pppp')
                print(red12.get(title))
                print(red13.get(title))
                print(red14.get(title))
                print(red15.get(title))

            all_image= text_page.find_all('img')   
            
            
            all_image = [img['src'] for img in text_page.select('div.article-fulltext img') if img.get('src')]

            # img_sources = [img for img in text_page.find_all('img') if img.get('src')]
            # 打印所有找到的 src 属性值
            for one_image in all_image:
                #获得当前进度
                sys.stdout.write('\r%s%%'%(round(100*page_all_count/pages_all,2)))
                sys.stdout.flush()
                try:
                    # image=requests.get(url=one_image,headers=headers,verify = False)
                    one_image = one_image.split('?')[0]
                    suffix = one_image.split('.')[-1]
                    time.sleep(2)

                    referer = 'https://buondua.com/'
                    proxy_url = f"{origin}?url={one_image}&referer={referer}"
                    print(proxy_url)
                    image = requests.get(proxy_url)
                    # image = requests.get(one_image)
                    imgs_name=f'{dirs}/{page_all_count}.{suffix}'
                    f = open(imgs_name, 'wb')  
                    print(imgs_name)  
                    f.write(image.content)
                    f.close() 
                    #写入图片关键字和其他信息
                    # img_fix=Image(imgs_name)
                    # img_fix.clear_exif()
                    # _dict = {'Xmp.dc.subject': list(keywords), 
                    #             'Xmp.dc.title': column+' '+mnname,
                    #             'Xmp.dc.description': description, 
                    #             'Xmp.dc.creator': [mnname], 
                    #             'Xmp.photoshop.DateCreated':str(int(time.strftime('%Y',time.localtime()))-100)+time.strftime('-%m-%dT%H:%M:%S',time.localtime())
                    # }  
                    # img_fix.modify_xmp(_dict)
                    page_all_count+=1
                except Exception as e:
                    print('15')
                    time.sleep(2)
                    print(e)
                # 当重试完成后还未成功，则返回超时
                    raise TimeoutError
        print('100 %')
        preimg = f'{previewpath}/{title}.webp'
        f = open(preimg, 'wb')    
        f.write(image.content)
        f.close() 
        #记录保存套图 用时
        end=time.time()
        last=end-begin
        print(round(last,2))
