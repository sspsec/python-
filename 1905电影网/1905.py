import os
import requests
from bs4 import BeautifulSoup

# 创建存储图片的文件夹
os.makedirs("images", exist_ok=True)

session = requests.Session()

headers = {
    "Sec-Ch-Ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Ch-Ua-Platform": "\"macOS\"",
    "Priority": "u=0, i",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Connection": "keep-alive",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Dest": "document",
    "Pragma": "no-cache",
    "Accept-Encoding": "gzip, deflate, br",
    "Sec-Fetch-Mode": "navigate",
    "Cache-Control": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-User": "?1",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ee;q=0.6",
    "Sec-Ch-Ua-Mobile": "?0"
}

# 打开文件保存结果
with open("movies.txt", "w", encoding="utf-8") as file:
    for page in range(1, 51):  # 爬取 50 页
        url = f"https://www.1905.com/vod/list/n_1/o3p{page}.html"
        print(f"正在爬取第 {page} 页: {url}")

        try:
            response = session.get(url, headers=headers)
            response.encoding = 'utf-8'
            page_text = response.text
            soup = BeautifulSoup(page_text, 'lxml')
            movie_all = soup.find_all('div', class_="grid-2x grid-3x-md grid-6x-sm")

            for single in movie_all:
                part_html = str(single)
                part_soup = BeautifulSoup(part_html, 'lxml')

                # 提取电影名称
                name = part_soup.find('a')['title']

                # 提取评分
                try:
                    score = part_soup.find('i').text
                except:
                    score = "1905暂无评分"

                # 提取电影链接
                path = part_soup.find('a', class_="pic-pack-outer")['href']

                # 提取图片链接
                img_src = part_soup.find('img')['src']

                # 下载图片
                try:
                    img_data = session.get(img_src).content
                    img_name = os.path.join("images", f"{name}.jpg")  # 使用电影名称作为图片文件名
                    with open(img_name, 'wb') as img_file:
                        img_file.write(img_data)
                    print(f"图片已下载: {img_name}")
                except Exception as e:
                    print(f"下载图片失败: {img_src}, 错误: {e}")

                # 写入结果到文件
                file.write(f"电影名: {name}\n评分: {score}\n链接: {path}\n图片链接: {img_src}\n\n")
                print(f"电影名: {name}, 评分: {score}, 链接: {path}, 图片链接: {img_src}")

        except Exception as e:
            print(f"爬取第 {page} 页失败，错误: {e}")

print("爬取完成！")
