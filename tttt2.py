import requests


def getHtml(url):
    # ....
    retry_count = 5
    proxy = 'http://127.0.0.1:1080'
    proxies = {
        'http://': 'socks5://127.0.0.1:1080',
        'https://': 'socks5://127.0.0.1:1080'
    }
    print(proxy)
    while retry_count > 0:
        try:
            html = requests.get(url, proxies=proxies)
            # 使用代理访问
            print(html.text)
            return html
        except Exception:
            retry_count -= 1
    return None


if __name__ == '__main__':
    # url = "http://www.baidu.com"
    # url = 'https://www.google.com'
    url = 'https://www.xiutaku.com'

    html_content = getHtml(url)
    if html_content:
        print("Successfully retrieved HTML content.")
    else:
        print("Failed to retrieve HTML content.")
