#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 18:53:50 2020

@author: vajorstack
"""

import os
import sys,redis
import requests
import re
import math
from key import keys
from bs4 import BeautifulSoup
from pyexiv2 import Image
import time
from config import *


def save_suit(headers, title, link):
    print('true link start')

    print(link)
    print('true link end')
    # exit()
    #找到一共多少张图片
    reg="[0-9]+photos"
    # 正则表达式来匹配文本
    pattern = re.compile(r"\[(\d+MB)-(\d+)photos\]")

    # 在文本中搜索匹配项
    match = pattern.search(title)

    if match:
        mb_size = match.group(1)
        photo_count = match.group(2)
        print(f"MB Size: {mb_size}, Photo Count: {photo_count}")
    else:
        print("No match found")
    pages_group=re.search(reg,title)
    if pages_group ==  None:
        return 
    pages_all = int(photo_count)
    page = math.ceil(pages_all/20)
    page_all_count = 1   
    print(pages)
    dirs = path+"/%s"%title

    print(dirs)    
    begin=time.time()
    for pagee in range(0,pages):    
        #获得每一篇链接
        if pagee == 0:
            suit_link=link
        else:
            suit_link=link + "/%s" % pagee
        print(suit_link)

        proxy_url = f"{origin}?url={suit_link}"

        album_name = proxy_url.split('/')[-1].split('.')[0]
        print(album_name)
        response = requests.get(proxy_url)
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


        # 仅选择在特定类下的 <a> 标签
        img_sources = [img['src'] for img in text.find_all('img') if img.get('src')]
        all_image = []
        # # 打印所有找到的 src 属性值
        # for src in img_sources:
        #     if album_name in src:
        #         print(src, album_name)
        #         all_image.append(src)
        all_image = img_sources[:20]
        print(len(all_image))
        print('4444444444')
        # exit()
        for one_image in all_image:
            #获得当前进度
            sys.stdout.write('\r%s%%'%(round(100*page_all_count/pages_all,2)))
            sys.stdout.flush()
            # if len(all_image[item]['src'])<30:
            #     continue
            print('33333333333333')
            print('fffff', one_image)
            # exit()
            proxy_one_url = f"{origin}?url={one_image}"
            print('kkkkkk')
            print(proxy_one_url)
            image = requests.get(proxy_one_url)
            remote_content = response.content
            # image=requests.get(url=one_image,headers=headers,verify = False)
            # imgs_name=dirs+'/%s_%s_%s'%(title,str(page_all_count),pagee+1)+".webp"
            # imgs_name=dirs+'/%s_%s'%(title,str(page_all_count))+".webp"
            imgs_name=f'{dirs}/{page_all_count}.webp'
            
            print(imgs_name)
            f = open(imgs_name, 'wb')    
            # print(one_image)
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
    preimg = f'{previewpath}/{title}.webp'
    f = open(preimg, 'wb')    
    f.write(image.content)
    f.close() 
    print('100 %')
    
    #记录保存套图 用时
    end=time.time()
    last=end-begin
    print(round(last,2))

    
    
    
    
    
    
    
    
