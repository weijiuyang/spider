import requests

# 代理配置
proxies = {
    'http': 'socks5h://127.0.0.1:1080',
    'https': 'socks5h://127.0.0.1:1080'
}

# # 目标 URL
# url = 'https://www.xiutaku.com'
# url = 'https://www.v2ph.com/'
# url = 'https://www.baidu.com/'
# url = 'https://www.xiaohongshu.com/'
# url = 'https://www.4khd.com'

# url = 'https://www.google.com'
# url = 'https://www.github.com'





def getHtml(url) :

    # 发起请求
    response = requests.get(url, proxies=proxies, verify=False)

    # 检查响应状态码
    if response.status_code == 200:
        print(f"Successfully fetched {url} homepage")
        # 打印部分响应内容
        print(response.text)  # 只打印前500个字符
    else:
        print(f"Failed to fetch {url} homepage, status code: {response.status_code}")
