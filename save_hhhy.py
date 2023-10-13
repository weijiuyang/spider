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
from key import keys
from bs4 import BeautifulSoup
from pyexiv2 import Image
import time
from spidersetting import *


def save_suit(headers, title, link):
    # print(headers)

    #找到一共多少张图片
    reg="[0-9]+photos"
    pages_group=re.search(reg,title)
    if pages_group ==  None:
        return 
    pages_all=int(pages_group.group()[:-6])
    pages=math.ceil(pages_all/20)
    page_all_count=1   
    print(pages)
    # exit()
    #查找是否重复，不重复的话创立文件夹
    dirs = path+"/%s"%title
    backdirs = backpath+"/%s"%title

    print(dirs)
    # if not os.path.exists(backdirs):
    #     os.makedirs(backdirs)      
    if not os.path.exists(dirs):
        os.makedirs(dirs)     

    begin=time.time()
    for pagee in range(0,pages):    
        #获得每一篇链接
        if pagee == 0:
            suit_link=link
        else:
            suit_link=link + "/%s" % pagee
        print(suit_link)
        r = requests.get(suit_link, headers=headers,verify = False)  # 向目标url地址发送get请求，返回一个response对象
        r.encoding='utf-8'   
        # print(r.text)
        # exit(0)
        #获取每一篇关键字
        text=BeautifulSoup(r.text, 'html.parser')
        # print(text)
        # print(text.head)
        # exit(0)
        # if pagee ==0:
        #     keywords,description,column,mnname=keys(text)
        #     print(keywords,description,column,mnname)
        #保存每一篇对三张图片
        all_image = text.find_all('figure')    
        # print(all_image)
        # print(len(all_image))
        # exit()                    
        # one_page_imgs = min(len(all_image),4)
        for item in range(0, len(all_image)):
            #获得当前进度
            sys.stdout.write('\r%s%%'%(round(100*page_all_count/pages_all,2)))
            sys.stdout.flush()
            one_image=all_image[item].a['href']
            # if len(all_image[item]['src'])<30:
            #     continue
            # print(one_image)
            image=requests.get(url=one_image,headers=headers,verify = False)
            imgs_name=dirs+'//%s_%s_%s'%(title,str(page_all_count),pagee+1)+".jpg"
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
    print('100 %')
    
    #记录保存套图 用时
    end=time.time()
    last=end-begin
    print(round(last,2))

    
    
    
    
    
    
    
    
