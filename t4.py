import requests, os
from bs4 import BeautifulSoup
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Accept-Encoding': 'gzip, deflate, br'
}
xhs_url = 'https://www.xiaohongshu.com/user/profile/6538a3cd000000000301ec58'

response = requests.get(xhs_url, headers=headers)



content = response.text
# decoded_content = content.decode('utf-8')
text_page =BeautifulSoup(content, 'html.parser')
pretty_html = text_page.prettify()

file_path = os.path.abspath(__file__).split('.')[0]
os.makedirs(f"{file_path}", exist_ok = True)
with open(f"{file_path}/pretty_file.html", "w", encoding="utf-8") as file:
    file.write(pretty_html)  # Save the pretty HTML to another file
