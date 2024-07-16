    #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 19:37:51 2019

@author: jiuyang.wei
"""
import argparse
from utils import *
import requests
import os, time
from spider_save_mysql import save_suit
from bs4 import BeautifulSoup
from config import *
import redis
import urllib3

# 禁用未验证HTTPS请求的警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
script_dir = os.path.dirname(os.path.abspath(__file__))

if not os.path.exists(path):
    os.mkdir(path)
if not os.path.exists(previewpath):
    os.mkdir(previewpath)

headers = {}

    
red = redis.Redis(host='localhost', port=6379, db=10)
def get_attribute_web(website = "xgmn", spider_pagenum = 3):
    headers, html_short, urllist, proxy = None, None, None, None
    match website:
        case "xiutaku":
            proxy = True
            html_short = r"https://xiutaku.com"
            urllist = ['https://xiutaku.com']

            for page in range(2,spider_pagenum+1):
                offset = page * 20 - 20
                url = html_short + f"/?start={offset}" 
                urllist.append(url)
        case "xgmn":
            headers = { "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
                        }  
            html_short=r"https://www.xgmn5.top"
            urllist = [f'https://www.xgmn5.top/new.html']
            proxy = False
        case "4khd":
            html_short = r'https://www.4khd.com'
            urllist = [r'https://www.4khd.com']
            page_link = urllist[0]
            print(page_link)
            for page in range(2, spider_pagenum + 4):
                page_link= html_short +"?query-3-page=%s" % page
                urllist.append(page_link)
            headers = {}
            proxy = True

        case "cosplaytele":
            html_short = r'https://cosplaytele.com'
            site = r'https://cosplaytele.com'
            urllist = [site]
            for page in range(1,spider_pagenum):
                if not page == 1:
                    page_link = f"{site}/page/{page}"
                    urllist.append(page_link)
            headers = {}
            proxy = True
    return headers, html_short, urllist, proxy


def spider_web(website = "xgmn"):
    headers = { "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'}  

    headers, html_short, urllist, proxy = get_attribute_web(website)

    print(headers,  html_short, urllist, proxy)
    for url in urllist:
        print(url)
        # r_page = requests.get(url, verify=False)  # 向目标url地址发送get请求，返回一个response对象
        print(proxy)
        if proxy:
            r_page = getHtml(url, html_short)
            # proxy_url = f"{origin}?url={url}"
            # print(f'{proxy_url} : proxy_url')
            # r_page = requests.get(proxy_url, verify=False)
        else:
            r_page = requests.get(url, headers= headers, verify=False)  # 向目标url地址发送get请求，返回一个response对象
            print(r_page.text)
        # print('ss')
        decoded_content = r_page.content.decode('utf-8')
        text_page =BeautifulSoup(decoded_content, 'html.parser')
        pretty_html = text_page.prettify()

        file_path = os.path.abspath(__file__).split('.')[0]
        os.makedirs(f"{file_path}_{website}", exist_ok = True)
        with open(f"{file_path}_{website}/pretty_file.html", "w", encoding="utf-8") as file:
            file.write(pretty_html)  # Save the pretty HTML to another file

        
        r_page.encoding='utf-8'
        text_page=BeautifulSoup(r_page.text, 'html.parser')
        # print(r_page.content)


        match website:
            case 'xiutaku':
                info_suit = text_page.find_all('div', class_='items-row') 
            case 'xgmn':
                info_suit = text_page.find_all('li', class_='i_list') 
            case "4khd":
                info_suit = [
                    (a_tag.get('href'), a_tag.get_text(strip=True))
                    for div in text_page.find_all('div', class_='is-nowrap')  # 查找所有 class 包含 is-nowrap 的 div
                    if (a_tag := div.find('a'))  # 在每个 div 中查找第一个 a 标签，并确保它存在
                ]
            case "cosplaytele":
                info_suit = text_page.find_all('div', class_='image-cover') 


        for info in info_suit:
            match website:

                case 'xiutaku':
                    girl = info.find('a', class_='is-girl').span.text.strip('#') 
                    pre_img_url = info.find('img')['src'] 
                    title = info.find('h2').a.text.strip() 
                    link_tag = info.find('a', class_='item-link')
                    link = html_short +  link_tag['href']
                case 'xgmn':
                    link=info.a['href']
                    title=info.a['title']
                    try:
                        pre_img_url = html_short + info.a.img['src']
                    except:
                        pre_img_url = None
                case "4khd":
                    link, title = info
                    if link == '/faq':
                        continue
                    pre_img_url = None
                case "cosplaytele":

                    time.sleep(10)
                    link=info.a['href']
                    title=info.a['aria-label']
                    title = title.replace('/', '_')
                    pre_img_url = info.a.img['src']
                    print(f"pre_img_url: {pre_img_url}")
            print(f'link: {link}')
            print(f'title: {title}')
            random_sleep_time = random.uniform(0, 1)

            # 暂停执行随机时间
            time.sleep(random_sleep_time)
            if pre_img_url:
                if proxy:
                    # proxy_url = f"{origin}?url={pre_img_url}"
                    # print(f'{proxy_url} : proxy_url')
                    # pre_img = requests.get(proxy_url, verify=False)
                    pre_img = getHtml(pre_img_url, html_short)
                else:
                    pre_img = requests.get(pre_img_url, verify=False)
                # pre_img = requests.get(pre_img_url, verify=False)
                preimg = f'{previewpath}/{title}.webp'
                f = open(preimg, 'wb')    
                f.write(pre_img.content)
                f.close()
            if not red.get(title):
                match website:
                    case 'xgmn':
                        proxy = False
                    case "4khd":
                        proxy = True
                    case "cosplaytele":
                        proxy = True
                    case "xiutaku":
                        proxy = True
                save_suit(headers, title, link, html_short, website, proxy= proxy, force = True) 
            else:
                print('already saved')  




if __name__ == '__main__':
    # website ='https://www.4khd.com/content/02/nekokoyoshi-blast-girl-meow-xiaoji-wind-chime-princess.html'
    # spider_web('cosplaytele')
    
    parser = argparse.ArgumentParser(description="Run the spider web function with a specified spider name.")
    
    parser.add_argument('spider_name', type=str, help='The name of the spider to run')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 调用 spider_web 函数并传递参数
    spider_web(args.spider_name)

