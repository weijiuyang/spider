from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, os, shutil
from pyexiv2 import Image
import requests
chrome_options = Options()
chrome_options.add_argument("--headless")  # 添加无头参数
chrome_options.add_argument("--no-sandbox")  # 在非root权限下运行时需要
chrome_options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems



path = '/home/weijiuyang/images'
driver = webdriver.Chrome(options=chrome_options)
# 现在你可以使用driver对象来访问网页，进行自动化操作


# short_url = 'http://xiutaku.com'
# url = 'http://xiutaku.com'
short_url = 'https://www.v2ph.com/actor/8689xa7m.html?hl=zh-Hant'
test_url = 'https://www.v2ph.com/actor/8689xa7m.html?hl=zh-Hant'
url = 'https://www.v2ph.com/actor/8689xa7m.html?hl=zh-Hant'

# frontend=522f3e888be0c71ec97a55491bc15589; _ga=GA1.1.143578938.1712484793; cf_clearance=YZQr36.BnvNQWt7fp1BW5Ey83WeRJI7TtMV8At1Pt5E-1712484795-1.0.1.1-ss2GdojwhYjJ55SnQcCKKlEv4PgZvNUQUEyeSbzA50s.YjCdng6Mo_oq.Y.4PrCFMIXHX7f05QQ2HmHV304KRA; frontend-rmu=Cx31p%2FlO%2FqAr9rwoSCaQCi%2FgBfQFsA%3D%3D; frontend-rmt=R87hnzzcXFENUGjybaQ5BWz7D5rR5yCHGEgdegoiqmI%2B2C1coiBIc1Y0YvkbxLbw; _ga_170M3FX3HZ=GS1.1.1712484793.1.1.1712484964.35.0.0

cookie_string = "frontend=522f3e888be0c71ec97a55491bc15589; _ga=GA1.1.143578938.1712484793; cf_clearance=YZQr36.BnvNQWt7fp1BW5Ey83WeRJI7TtMV8At1Pt5E-1712484795-1.0.1.1-ss2GdojwhYjJ55SnQcCKKlEv4PgZvNUQUEyeSbzA50s.YjCdng6Mo_oq.Y.4PrCFMIXHX7f05QQ2HmHV304KRA; frontend-rmu=Cx31p%2FlO%2FqAr9rwoSCaQCi%2FgBfQFsA%3D%3D; frontend-rmt=R87hnzzcXFENUGjybaQ5BWz7D5rR5yCHGEgdegoiqmI%2B2C1coiBIc1Y0YvkbxLbw; _ga_170M3FX3HZ=GS1.1.1712484793.1.1.1712484964.35.0.0"

# 将cookie字符串转换为Selenium可以使用的格式
cookies = []
for pair in cookie_string.split('; '):
    name, value = pair.split('=', 1)
    cookies.append({
        'name': name,
        'value': value,
        'domain': 'www.v2ph.com'  # 修改为实际的域名
    })

# cookies现在是一个字典列表，可以被Selenium使用
print(cookies)
# exit()



headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate,  zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "max-age=0",
    "Referer": "https://www.v2ph.com/album/z7nnx65a.html?page=13&hl=zh-Hant",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"
}

# Cookies
cookies = {
    'frontend': '522f3e888be0c71ec97a55491bc15589',
    '_ga': 'GA1.1.143578938.1712484793',
    'cf_clearance': 'YZQr36.BnvNQWt7fp1BW5Ey83WeRJI7TtMV8At1Pt5E-1712484795-1.0.1.1-ss2GdojwhYjJ55SnQcCKKlEv4PgZvNUQUEyeSbzA50s.YjCdng6Mo_oq.Y.4PrCFMIXHX7f05QQ2HmHV304KRA',
    'frontend-rmu': 'Cx31p%2FlO%2FqAr9rwoSCaQCi%2FgBfQFsA%3D%3D',
    'frontend-rmt': 'R87hnzzcXFENUGjybaQ5BWz7D5rR5yCHGEgdegoiqmI%2B2C1coiBIc1Y0YvkbxLbw',
    '_ga_170M3FX3HZ': 'GS1.1.1712484793.1.1.1712484939.60.0.0'
}

response = requests.get(url, headers=headers, cookies=cookies)
# response.encoding = response.apparent_encoding
response.encoding = 'utf-8'
# 打印响应内容
print(response.text)
# 打印响应内容
print(response.text)
exit()

page_num_argv = 100 
for page in range(1,page_num_argv):
    if not page == 1:
        offset = page * 20 - 20
        url = short_url + f"?start={offset}.html" 
    print(url)
    for cookie in cookies:
        driver.add_cookie(cookie)
    # driver.add_cookie(cookies)
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # 等待页面加载
    html_source = driver.page_source
    print(html_source)
    # 找到所有的img元素
    exit()
    front_links = driver.find_elements(By.CSS_SELECTOR, 'a.item-link.popunder')

    suit_links = []
    for front_link in front_links:
        href = front_link.get_attribute('href')  # 获取<a>元素的href属性
        img = front_link.find_element(By.TAG_NAME, 'img')  # 在<a>元素内部查找<img>
        src = img.get_attribute('src')  # 获取<img>元素的src属性
        alt = img.get_attribute('alt')
        print(f'href: {href}, src: {src}, alt : {alt}')
        suit_links.append((href, img, src, alt))


    for suit_link in suit_links:   
        href, img, src, alt = suit_link
        dirs = path+"/%s" % alt
        if os.path.exists(dirs):
            continue
        os.makedirs(dirs)   
        driver.get(href)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # 等待页面加载
        html_source = driver.page_source
        # print(html_source)

        
        article_infos = driver.find_elements(By.CSS_SELECTOR, 'div.article-info')

        for article_info in article_infos:
            print(article_info.text)
        create_time = article_infos[0].text    
        
        description = article_infos[1].text    
        
        
        # 定位到包含标签的div元素
        tags_container = driver.find_element(By.CSS_SELECTOR, 'div.article-tags')

        # 在该元素内部查找所有的span元素
        tags = tags_container.find_elements(By.TAG_NAME, 'span')
        
        # 打印每个标签的文本
        keywords = []
        for tag in tags:
            print(tag.text)
            keywords.append(tag.text)
        column = tags[0].text
        girl = tags[1].text    
        
        # 找到所有的img元素
        pagination_links = driver.find_elements(By.CSS_SELECTOR, 'a.pagination-link')


        pages_hrefs = list()
        
        imagescount = 0
        
        
        for link in pagination_links:
            href = link.get_attribute('href') 
            if not href in pages_hrefs:
                pages_hrefs.append(href)
        for href in pages_hrefs:
            print(href)
            driver.get(href) 
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # 等待页面加载
            html_source = driver.page_source
            # print(html_source)
            
            content = driver.find_element(By.CSS_SELECTOR, 'div.article-fulltext')
            # 在找到的content元素内部查找所有的<img>元素
            images = content.find_elements(By.TAG_NAME, 'img')

            for img in images:
                src = img.get_attribute('src')  # 获取每个<img>元素的src属性
                print(src) 
                image_suffix = src.split('.')[-1]
                try:
                    image=requests.get(url=src)
                    imagescount += 1
                    imgs_name = f"{dirs}/{alt}_{imagescount}.{image_suffix}"

                    f = open(imgs_name, 'wb')    
                    # print(one_image)
                    f.write(image.content)
                    f.close() 
                    #写入图片关键字和其他信息
                    img_fix=Image(imgs_name)
                    img_fix.clear_exif()
                    _dict = {'Xmp.dc.subject': list(keywords), 
                                'Xmp.dc.title': column +' ' + girl,
                                'Xmp.dc.description': description, 
                                'Xmp.dc.creator': [girl], 
                                'Xmp.photoshop.DateCreated':str(create_time)
                    }  
                    img_fix.modify_xmp(_dict)
                except Exception as e:
                    print('15')
                    time.sleep(2)
                    print(e)
                    shutil.rmtree(dirs)
                # 当重试完成后还未成功，则返回超时
                    raise TimeoutError


