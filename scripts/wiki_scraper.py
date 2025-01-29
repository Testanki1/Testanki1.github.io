import os
import requests
from bs4 import BeautifulSoup
from googletrans import Translator

# 目标存放路径
OUTPUT_DIR = "wiki"
BASE_URL = "https://en.tankiwiki.com/"

# 伪装成真实用户
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
    "DNT": "1",
    "Connection": "keep-alive"
}

# 初始化翻译器
translator = Translator()

# 确保目标目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_and_translate(url, filename):
    """抓取页面并翻译"""
    print(f"Fetching {url}...")
    response = requests.get(url, headers=HEADERS, timeout=10)
    
    if response.status_code != 200:
        print(f"Failed to fetch {url} - Status Code: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.text, "lxml")

    # 仅提取主要内容区域
    content_div = soup.find("div", {"id": "mw-content-text"})
    if not content_div:
        print(f"No content found for {url}")
        return
    
    text = content_div.get_text("\n", strip=True)

    # 翻译文本
    print(f"Translating {filename}...")
    translated_text = translator.translate(text, src="en", dest="zh-cn").text

    # 保存到 wiki 目录
    file_path = os.path.join(OUTPUT_DIR, f"{filename}.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# {filename}\n\n")
        f.write(translated_text)

    print(f"Saved: {file_path}")

# 爬取首页的所有链接
def scrape_wiki():
    """爬取 Tanki Wiki 并翻译"""
    print(f"Accessing {BASE_URL}...")
    response = requests.get(BASE_URL, headers=HEADERS, timeout=10)
    
    if response.status_code != 200:
        print(f"Failed to access main page - Status Code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "lxml")

    # 获取所有 Wiki 文章链接
    links = soup.select("a[href^='/wiki/']")
    urls = {BASE_URL + link["href"][6:]: link["href"].split("/")[-1] for link in links}

    print(f"Found {len(urls)} pages to scrape...")

    for url, filename in urls.items():
        fetch_and_translate(url, filename)

# 运行爬取
if __name__ == "__main__":
    scrape_wiki()
