from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def main():
    # 设置 WebDrive

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # 启用无头模式
    options.add_argument("--no-sandbox")  # 禁用沙盒模式
    options.add_argument("--disable-dev-shm-usage")  # 减少资源消耗

    # service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=options)


    try:
        # 打开 Google 主页
        driver.get("https://www.google.com")

        # 在搜索框中输入 "Hello World" 并按 Enter 键
        search_box = driver.find_element("name", "q")
        search_box.send_keys("Hello World")
        search_box.send_keys(Keys.RETURN)

        # 等待页面加载完成（实际开发中应使用显式等待代替 time.sleep）
        driver.implicitly_wait(5)

        # 打印出搜索结果页面的标题
        print(driver.title)

    finally:
        # 关闭浏览器
        driver.quit()

if __name__ == "__main__":
    main()
