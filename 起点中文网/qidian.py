import requests
from bs4 import BeautifulSoup
import pandas as pd

# 发送HTTP请求并获取网页内容
def get_html(url):
    response = requests.get(url)
    return response.text

# 解析网页内容，提取小说信息
def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    novel_list = soup.find_all('div', class_='book-mid-info')
    novels = []

    for novel in novel_list:
        name = novel.find('h4').text.strip()
        author = novel.find('p', class_='author').text.strip()
        intro = novel.find('p', class_='intro').text.strip()
        novels.append({'Name': name, 'Author': author, 'Introduction': intro})

    return novels

# 主程序入口
if __name__ == '__main__':
    url = 'https://www.qidian.com/all'
    html = get_html(url)
    novels = parse_html(html)

    # 创建一个DataFrame对象，用于存储小说信息
    df = pd.DataFrame(novels)

    # 导出数据到Excel文件
    df.to_excel("qidian_novels.xlsx", index=False)
