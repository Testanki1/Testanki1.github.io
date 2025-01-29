import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from googletrans import Translator
from bs4 import BeautifulSoup

# 目标页面和存放路径
URL = "https://en.tankiwiki.com/Tanki_Online_Wiki"
OUTPUT_DIR = "wiki"
OUTPUT_FILE = "Tanki_Online_Wiki.md"

# 初始化翻译器
translator = Translator()

# 初始化 Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 无头模式
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-software-rasterizer")

# 启动 Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def fetch_and_translate(url, output_file):
    """使用 Selenium 爬取页面并翻译"""
    print(f"Fetching {url}...")
    driver.get(url)
    time.sleep(5)  # 等待页面加载完毕，避免被防护拦截

    # 获取页面内容
    soup = BeautifulSoup(driver.page_source, "lxml")

    # 提取主要内容区域
    content_div = soup.find("div", {"id": "mw-content-text"})
    if not content_div:
        print(f"No content found for {url}")
        return

    text = content_div.get_text("\n", strip=True)

    # 翻译文本
    print("Translating content...")
    translated_text = translator.translate(text, src="en", dest="zh-cn").text

    # 保存到 markdown 文件
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    file_path = os.path.join(OUTPUT_DIR, output_file)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# Tanki Online Wiki\n\n")
        f.write(translated_text)

    print(f"Saved: {file_path}")

# 运行爬取和翻译
if __name__ == "__main__":
    fetch_and_translate(URL, OUTPUT_FILE)

# 关闭浏览器
driver.quit()
