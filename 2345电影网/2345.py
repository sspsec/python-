import requests
from bs4 import BeautifulSoup
import os
import re
import sys
import time

# 确保输出到控制台时支持 UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# 创建存储图片的文件夹
os.makedirs("images", exist_ok=True)

# 基础URL
base_url = 'https://tv.2345.com/-neidi----{}.html'

# 打开文件保存结果
with open('电视剧信息.txt', 'w', encoding='utf-8') as file:
    for page in range(1, 51):  # 爬取 1 到 50 页
        url = base_url.format(page)
        print(f"正在爬取第 {page} 页: {url}")

        # 发送HTTP请求
        response = requests.get(url)
        response.encoding = 'gbk'  # 确保编码正确

        # 解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 找到电视剧列表的容器
        content_list = soup.find('ul', class_='v_picTxt pic180_240 clearfix')
        if not content_list:
            print(f"未找到电视剧列表内容，跳过第 {page} 页")
            continue

        drama_list = content_list.find_all('li')

        for drama in drama_list:
            # 获取电视剧名称
            name_tag = drama.find('span')
            name = name_tag.get_text(strip=True) if name_tag else '未知'

            # 获取评分
            score_tag = drama.find('em')
            score = score_tag.get_text(strip=True) if score_tag else '无评分'

            # 获取电视剧链接
            link_tag = drama.find('a', href=True)
            link = f"https:{link_tag['href']}" if link_tag else '无链接'

            # 获取封面图片链接
            img_tag = drama.find('img')
            img_src = f"https:{img_tag['data-src']}" if img_tag else '无图片链接'

            # 写入文本文件
            file.write(f"电视剧名称：{name}\n评分：{score}\n链接：{link}\n封面图片链接：{img_src}\n\n")
            print(f"电视剧名称：{name}\n评分：{score}\n链接：{link}\n封面图片链接：{img_src}\n")

            # 下载封面图片
            if img_src != '无图片链接':
                try:
                    img_data = requests.get(img_src).content
                    # 替换非法字符，确保文件名合法
                    valid_name = re.sub(r'[\/:*?"<>|]', '', name)
                    img_path = os.path.join('images', f"{valid_name}.jpg")
                    with open(img_path, 'wb') as img_file:
                        img_file.write(img_data)
                    print(f"图片已下载：{img_path}")
                except Exception as e:
                    print(f"图片下载失败：{img_src}，错误：{e}")

        # 延时以避免触发反爬机制
        time.sleep(1)

print("爬取完成！")
