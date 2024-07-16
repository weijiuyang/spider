import requests
import random


import requests
import random
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
# def get_proxy():
#     return requests.get("http://127.0.0.1:5010/get/").json()

# def delete_proxy(proxy):
#     requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

# # your spider code

# def getHtml(url):
#     # ....
#     retry_count = 5
#     proxy = get_proxy().get("proxy")
#     print(proxy)
#     while retry_count > 0:
#         try:
#             html = requests.get(url, proxies={"http": "http://{}".format(proxy)})
#             # 使用代理访问
#             print(html.text)
#             return html
#         except Exception:
#             retry_count -= 1
#     # 删除代理池中代理
#     # delete_proxy(proxy)
#     return None


# 代理配置
proxies = {
    'http': 'socks5h://127.0.0.1:1080',
    'https': 'socks5h://127.0.0.1:1080'
}

# # 目标 URL
url = 'https://xiutaku.com'
# url = 'https://www.v2ph.com/'
# url = 'https://www.boundua.com/'
# url = 'https://www.baidu.com/'
# url = 'https://www.xiaohongshu.com/'
# url = 'https://www.4khd.com'

# url = 'https://www.cosplaytele.com'
# url = 'https://www.github.com'

url = 'https://i.xiutaku.com/photo/uploadfile/202407/5/1313854630.jpg'

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
]

headers = {
    'User-Agent': random.choice(user_agents),
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    # 'Referer': 'https://www.google.com/',
    'Referer': 'https://xiutaku.com/'

}
def get_html_with_retry(url, headers, proxies, referer=None, retries=5, backoff_factor=1):
    session = requests.Session()
    retry_strategy = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    if referer:
        headers['Referer'] = referer 

    try:
        response = session.get(url, proxies=proxies, headers=headers, verify=False, timeout=10)
        response.raise_for_status()  # Raises an HTTPError if the response code was unsuccessful
        logging.info(f"Successfully fetched {url}")
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None

def getHtml(url, referer=None):
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://xiutaku.com/'
    }

    return get_html_with_retry(url, headers, proxies, referer)

if __name__ == '__main__':
    getHtml(url)