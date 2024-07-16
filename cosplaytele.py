import requests
import json
from bs4 import BeautifulSoup
import os
import time
from config import *
import redis
import sys,datetime
from cosplaytele_save import save_suit

site = r'https://cosplaytele.com'

# site = r'https://cosplaytele.com/category/blacqkl'

page_link=site
html_short = site
print(page_link)

if(len(sys.argv)==2):
    page_num_argv=int(sys.argv[1])
else:
    page_num_argv=5

red = redis.Redis(host='localhost', port=6379, db=10)
red9 = redis.Redis(host='localhost', port=6379, db=9)
red16 = redis.Redis(host='localhost', port=6379, db=16)

red11 = redis.Redis(host='localhost', port=6379, db=11)
headers = {}

for page in range(1,page_num_argv):
    if not page == 1:
        page_link = f"{site}/page/{page}"
    #得到当前页更新的所有写真
    print(page_link)
    proxy_url = f"{origin}?url={page_link}"
    response = requests.get(proxy_url)
    remote_content = response.content  # 这是从远程服务器获取的原始字节数据
    # 解码字节数据
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

    info_suit = text_page.find_all('div', class_='image-cover') 
    for info in info_suit:
        time.sleep(10)
        link=info.a['href']
        title=info.a['aria-label']
        title = title.replace('/', '_')
        print(f"link:   {link}")
        print(f"title:   {title}")
        pre_img_url = info.a.img['src']
        print(f"pre_img_url:     {pre_img_url}")

        # proxy_pre_img_url = f"{origin}?url={pre_img_url}"
        # pre_img = requests.get(proxy_pre_img_url) 
        # preimg = f'{previewpath}/{title}.webp'
        # f = open(preimg, 'wb')    
        # f.write(pre_img.content)
        # f.close() 
        # exit()
        # continue
        #保存这一期写真
        pathdirs = os.path.join(path, title)

        if  True or not os.path.exists(pathdirs) :
            print('ssss')
            red.set(title, 50)
            nowdate = datetime.datetime.now().date().strftime("%Y%m%d")

            red9.sadd(nowdate, title)
            red11.set(title, 'cosplaytele')
            save_suit(headers, title, link, html_short) 
        # exit()


