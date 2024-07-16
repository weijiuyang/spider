import requests
from bs4 import BeautifulSoup
import os
import sys
import re
import math
import time,json
from key import keys
from pyexiv2 import Image
from config import *
import time
import redis

def save_suit(headers, title, link, html_short):
    # link = f'https://cosplaytele.com/2b-34/'
    # link = f'https://cosplaytele.com/after-work-5/'
    # link = f'https://cosplaytele.com/huajia-zombie-night/'
    red12 = redis.Redis(host='localhost', port=6379, db=12) #column
    red13 = redis.Redis(host='localhost', port=6379, db=13) #mnname
    red14 = redis.Redis(host='localhost', port=6379, db=14) #keywords
    red15 = redis.Redis(host='localhost', port=6379, db=15) #description
    red16 = redis.Redis(host='localhost', port=6379, db=16) #description


    print("save_suit")
    img_short = html_short
    #找到一共多少张图片
    reg="[0-9]+ photos"
    # title = f'りんごみつき(ringo_mitsuki) cosplay 2B – Nier:Automata “149 photos and 1 videos”'


    title = title.replace(".","_")
    dirs = os.path.join(path, title)
    print(dirs)

    if True or not os.path.exists(dirs):
        print(dirs)
        # exit()
        begin=time.time()    
    
        try:
            proxy_url = f"{origin}?url={link}"
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
        worktitle = title.split('"')[0]
        worktitle = worktitle.split('“')[0]
        if 'cosplay' in worktitle:
            girl = worktitle.split('cosplay')[0]
            girl = girl.strip()

            red13.set(title, girl)
            worktitle = worktitle.split('cosplay')[1]
            print(worktitle.split('–'))
            cosplay = worktitle.split('–')[0]
            red14.set(title, cosplay)
            ablumn = '–'.join(worktitle.split('–')[1:])
            red12.set(title, ablumn)
        else:
            girl = worktitle.split('–')[0]
            girl = girl.strip()
            red13.set(title, girl)
            ablumn = '–'.join(worktitle.split('–')[1:])
            red12.set(title, ablumn)
        red16.sadd(girl, title)
        
        print('专辑', red12.get(title).decode("utf-8") if red15.get(title) else None)
        print('主演', red13.get(title).decode("utf-8") if red15.get(title) else None )
        print('关键字',red14.get(title).decode("utf-8") if red15.get(title) else None)
        print('描述', red15.get(title).decode("utf-8") if red15.get(title) else None)
        # exit()


        if not os.path.exists(dirs):  
            os.makedirs(dirs)  
        all_image = [img['src'] for img in text_page.select('figure.gallery-item img') if img.get('src')]
        page_all_count = 1
        for one_image in all_image:
            #获得当前进度
            sys.stdout.write('\r%s%%'%(round(100*page_all_count/len(all_image),2)))
            sys.stdout.flush()
            try:
                proxy_url = f"{origin}?url={one_image}"
                print(proxy_url)
                image = requests.get(proxy_url)
                # image = requests.get(one_image)
                suffix = proxy_url.split('.')[-1]
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


# save_suit({},'ss','sss','sss')
# exit()
