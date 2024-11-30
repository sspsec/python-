import sys
import os
import requests
from bs4 import BeautifulSoup

# 设置编码
sys.stdout.reconfigure(encoding='utf-8')

# 创建会话对象
session = requests.Session()

# 定义请求头和Cookies
headers = {
    "Sec-Ch-Ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Ch-Ua-Platform": "\"macOS\"",
    "Priority": "u=0, i",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Referer": "https://m.fschurun.com/vodtype/1-1454.html",
    "Connection": "keep-alive",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Dest": "document",
    "Pragma": "no-cache",
    "Sec-Fetch-Mode": "navigate",
    "Cache-Control": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-User": "?1",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ee;q=0.6",
    "Sec-Ch-Ua-Mobile": "?0"
}
cookies = {
    "HMACCOUNT": "B7DBA2BC6E7289B9",
    "Hm_lvt_aef90537bd1ea430ecce09938216e2d0": "1732107597",
    "Hm_lpvt_aef90537bd1ea430ecce09938216e2d0": "1732107629"
}

# 存储所有电影信息的列表
all_movies = []

# 爬取前 15 页
for page in range(1, 16):
    url = f"https://m.fschurun.com/vodtype/1-{page}.html"
    response = session.get(url, headers=headers, cookies=cookies)

    # 创建 BeautifulSoup 对象
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取电影信息
    movies = []
    for li in soup.find_all('li', class_='col-md-6 col-sm-4 col-xs-3'):
        title = li.find('h4', class_='title text-overflow').get_text(strip=True)
        actors = li.find('p', class_='text text-overflow text-muted hidden-xs text-actor').get_text(strip=True)
        rating = li.find('span', class_='pic-tag pic-tag-h').get_text(strip=True)
        cover_image = li.find('div', class_='ewave-vodlist__thumb')['data-original']

        movies.append({
            'title': title,
            'actors': actors,
            'rating': rating,
            'cover_image': cover_image
        })

    # 将当前页的电影信息添加到总列表中
    all_movies.extend(movies)

# 创建保存图片的文件夹
if not os.path.exists('images'):
    os.makedirs('images')

# 写入电影信息到文本文件
with open('movies.txt', 'w', encoding='utf-8') as f:
    for movie in all_movies:
        f.write(f"电影名称: {movie['title']}\n")
        f.write(f"演员: {movie['actors']}\n")
        f.write(f"评分: {movie['rating']}\n")
        f.write(f"封面: {movie['cover_image']}\n")
        f.write('-' * 40 + '\n')

        # 下载电影封面图片
        img_response = requests.get(movie['cover_image'])
        if img_response.status_code == 200:
            img_filename = os.path.join('images', f"{movie['title']}.jpg")
            with open(img_filename, 'wb') as img_file:
                img_file.write(img_response.content)

print("电影信息已保存到 movies.txt，封面图片已下载到 images 文件夹。")