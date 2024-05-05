#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 18:53:50 2020

@author: vajorstack
"""

import os
import sys
import requests
# from headers import get_ua
import re
import math
import time,json
from key import keys
from bs4 import BeautifulSoup
from pyexiv2 import Image
from config import *
import time
import redis



# records = red.hgetall(code)
# exit()


# attempts, delay这两个参数是必填的
def stop_f(attempts, delay):

    print('发生异常了，正在进行重试！')

# @retry(stop_func=stop_f,stop_max_attempt_number=5)
def save_suit(headers, title, link, html_short):
    s = requests.session()
    red12 = redis.Redis(host='localhost', port=6379, db=12) #column
    red13 = redis.Redis(host='localhost', port=6379, db=13) #mnname
    red14 = redis.Redis(host='localhost', port=6379, db=14) #keywords
    red15 = redis.Redis(host='localhost', port=6379, db=15) #description

    s.keep_alive = False

    print("save_suit")
    img_short = html_short
    #找到一共多少张图片
    reg="[0-9]+P"
    pages_group=re.search(reg,title)
    if pages_group ==  None:
        return 
    pages_all=int(pages_group.group()[:-1])
    pages=math.ceil(pages_all/3)+2
    page_all_count=1   
    #查找是否重复，不重复的话创立文件夹
    title = title.replace(".","_")
    dirs = os.path.join(path, title)
    print(dirs)

    if False or not os.path.exists(dirs):
        print(dirs)
        # exit()
        begin=time.time()    
        if os.path.exists(dirs):  
            os.makedirs(dirs)      
        for pagee in range(0,pages):    
            #获得每一篇链接
            if pagee == 0:
                suit_link=html_short+link
            else:
                suit_link=html_short+link[0:-5]+"_%s"%pagee+".html"
            try:
                r = requests.get(suit_link, headers=headers,verify = False)  # 向目标url地址发送get请求，返回一个response对象
                r.encoding='utf-8'   
            except Exception as e:
                time.sleep(2)
                # 当重试完成后还未成功，则返回超时
                raise TimeoutError
            text=BeautifulSoup(r.text, 'html.parser')
            if pagee == 0:
                keywords,description,column,mnname=keys(text)
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

            #保存每一篇对三张图片
            all_image= text.find_all('img')                        
            one_page_imgs=min(len(all_image),4)
            for item in range(1,one_page_imgs):
                #获得当前进度
                sys.stdout.write('\r%s%%'%(round(100*page_all_count/pages_all,2)))
                sys.stdout.flush()
                one_image=img_short+all_image[item]['src']
                if len(all_image[item]['src'])<30:
                    continue
                try:
                    image=requests.get(url=one_image,headers=headers,verify = False)
                    imgs_name=dirs+'/%s_%s'%(title,str(page_all_count))+".webp"
                    f = open(imgs_name, 'wb')    
                    f.write(image.content)
                    f.close() 
                    #写入图片关键字和其他信息
                    img_fix=Image(imgs_name)
                    img_fix.clear_exif()
                    _dict = {'Xmp.dc.subject': list(keywords), 
                                'Xmp.dc.title': column+' '+mnname,
                                'Xmp.dc.description': description, 
                                'Xmp.dc.creator': [mnname], 
                                'Xmp.photoshop.DateCreated':str(int(time.strftime('%Y',time.localtime()))-100)+time.strftime('-%m-%dT%H:%M:%S',time.localtime())
                    }  
                    img_fix.modify_xmp(_dict)
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
