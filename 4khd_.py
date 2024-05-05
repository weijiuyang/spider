import sys
import ssl
import requests
import os
from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

import time, os, shutil
from pyexiv2 import Image
import requests



import urllib3
urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context
#基础配置
path=r"~/images"   

 
html_short=r"https://www.4khd.com/"
headers = { "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "referer":html_short,
            "cookie": "UM_distinctid=174639a924226-0629a84b4d047c-15306251-13c680-174639a9243582; CNZZDATA1263487746=579143261-1599398858-https%253A%252F%252Fwww.google.com%252F%7C1607414870; __51cke__=; __tins__19410367=%7B%22sid%22%3A%201607416062237%2C%20%22vd%22%3A%202%2C%20%22expires%22%3A%201607417866359%7D; __51laig__=2",
            } 

chrome_options = Options()
# chrome_options.add_argument("--headless")  # 添加无头参数
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-infobars")    
chrome_options.add_argument("--no-sandbox")  # 在非root权限下运行时需要
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")

path = '/home/weijiuyang/images'
# driver = webdriver.Chrome(options=chrome_options)
# service = Service(ChromeDriverManager().install())

chrome_options = Options()
# chrome_options.add_argument("--headless")  # 添加无头参数
chrome_options.add_argument("--no-sandbox")  # 在非root权限下运行时需要
chrome_options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems



path = '/home/weijiuyang/images'
driver = webdriver.Chrome(options=chrome_options)
#读取置顶页（默认5页）       
if(len(sys.argv)==2):
    page_num_argv=int(sys.argv[1])
else:
    page_num_argv=10


page_link = html_short
print(page_link)
# break_flag=0

websites = []
#获得前几页写真
for page in range(1,page_num_argv):
    if not page == 1:
        page_link = html_short + f"?query-3-page={page}&cst.html" 
    #得到当前页更新的所有写真
    r_page = requests.get(page_link, headers=headers,verify = False)  # 向目标url地址发送get请求，返回一个response对象
    r_page.encoding='utf-8'
    # text_page=BeautifulSoup(r_page.text, 'lxml')
    # print(r_page.text)
    # exit()
    soup=BeautifulSoup(r_page.text, 'html.parser')
    links = soup.find_all('a')
    
    for link in links:
        href = link.get('href')
        if href:
            print(href)
            if href not in websites and 'https://www.4khd.com' in href and not 'https://www.4khd.com' == href:
                websites.append(href)
                
    print(websites)
    print(len(websites))
    
    for web in websites:
        r_page = requests.get(web, headers=headers,verify = False)  # 向目标url地址发送get请求，返回一个response对象
        r_page.encoding='utf-8'
        print(r_page)
        print(web)
        driver.get(web)
        # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(2)  # 等待页面加载
        time.sleep(randint(2, 5))
        html_source = driver.page_source
        print(html_source)
        # r_page = requests.get(web, headers=headers,verify = False)  # 向目标url地址发送get请求，返回一个response对象
        # r_page.encoding='utf-8'
        
        # print(web)
        # print(r_page.text)
        # exit()
        # soup=BeautifulSoup(r_page.text, 'html.parser')
        
        exit()
    # info_suit = text_page.find_all('li', class_='related_box') 

    # for info in info_suit:
    #     link=info.a['href']
    #     title=info.a['title']
    #     #保存这一期写真
    #     backdirs=backpath+"/%s"%title
    #     if not os.path.exists(backdirs):
    #         save_suit(headers, title, link, html_short) 
    
    
    
    
    
    
    
    
    