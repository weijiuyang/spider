import httpx
import random

# 代理配置
proxies = {
    'http://': 'socks5://127.0.0.1:1080',
    'https://': 'socks5://127.0.0.1:1080'
}

# 随机 User-Agent 列表
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
]

headers = {
    'User-Agent': random.choice(user_agents),
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'https://www.google.com/'
}

# 目标 URL
url = 'https://www.xiutaku.com'

# 发起请求
try:
    response = httpx.get(url, proxies=proxies, headers=headers, verify=False)

    # 检查响应状态码
    if response.status_code == 200:
        print(f"Successfully fetched {url}")
        # 打印部分响应内容
        print(response.text[:500])  # 只打印前500个字符
    else:
        print(f"Failed to fetch {url}, status code: {response.status_code}")
except httpx.HTTPStatusError as e:
    print(f"HTTP error occurred: {e}")
except httpx.RequestError as e:
    print(f"An error occurred: {e}")
except httpx.TimeoutException as e:
    print(f"Timeout occurred: {e}")
