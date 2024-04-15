from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time, os, shutil
from pyexiv2 import Image
import requests
chrome_options = Options()
chrome_options.add_argument("--headless")  # 添加无头参数

chrome_options.add_argument("--no-sandbox")  # 在非root权限下运行时需要

driver = webdriver.Chrome(options=chrome_options)


try:
    driver.get("https://www.google.com")
    print(f"Title: {driver.title}")
    print(f"URL: {driver.current_url}")
except Exception as e:
    print(f"An error occurred while interacting with the browser: {e}")

path = '/home/weijiuyang/images'
# driver = webdriver.Chrome(options=chrome_options)
# 打开一个网页
driver.get('https://xx.knit.bid/sort/new/')

# 打印网页标题
WebDriverWait(driver, 30).until(lambda d: d.title != "Just a moment...")
print(driver.title)

# 关闭浏览器
driver.quit()
