import requests
from bs4 import BeautifulSoup
from utils import *
import urllib3
import gzip
from io import BytesIO
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_proxy():
    # 1999: The listening port set in settings, not the Redis service port
    return requests.get(f"http://127.0.0.1:5010/get?type=https").json()

def delete_proxy(proxy):
    requests.get(f"http://127.0.0.1:5010/delete/?proxy={proxy}")

# Main code
def get_html():
    retry_count = 5
    proxy = get_proxy().get("proxy")
    print(f"Using proxy: {proxy}")
    # proxy = '8.219.97.248:80'
    print(f"Using proxy: {proxy}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Accept-Encoding': 'gzip, deflate, br'
    }

    while retry_count > 0:
        try:
            xhs_url = 'https://www.xiaohongshu.com/user/profile/6538a3cd000000000301ec58'
            xhs_url ='https://www.4khd.com'
            xhs_url = 'https://xiutaku.com'

            proxies = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}",
            }
            proxies = {
                "https": f"http://{proxy}",
            }
            # response = requests.get(xhs_url, proxies={"http": "http://{}".format(proxy)}, timeout=10, headers=headers,verify=False)
            response = requests.get(xhs_url, proxies=proxies, timeout=5, verify=False)
            response.encoding = 'utf-8'
        
            content = response.text
            print(content)


            print(f"Final Encoding Used: {response.encoding}")
            print(response.text)
            break
        except Exception as e:
            print(f"Failed to retrieve content: {e}")
            retry_count -= 1

    # Delete proxy from the proxy pool
    delete_proxy(proxy)
    return None

get_html()
