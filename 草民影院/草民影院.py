import os
import requests
from bs4 import BeautifulSoup

# 配置
base_url = "https://www.ipehr.com"
target_url_template = base_url + "/vodshow/2--time------{}---.html"  # 分页 URL 模板
output_folder = "movie_data"
image_folder = os.path.join(output_folder, "images")
output_file = os.path.join(output_folder, "movie_info.txt")

# 创建保存目录
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

# 初始化变量
movie_count = 0  # 计数
max_movies = 500  # 目标抓取数量
page = 1  # 起始页
info_list = []  # 存储抓取的信息

print(f"开始爬取目标 {max_movies} 条数据...")

# 爬取多页数据
while movie_count < max_movies:
    target_url = target_url_template.format(page)
    print(f"正在爬取第 {page} 页：{target_url}")

    response = requests.get(target_url)
    response.encoding = 'utf-8'  # 确保中文正常显示
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找影视信息
    movies = soup.find_all('li')  # 根据实际 HTML 调整查找方式
    if not movies:
        print("未找到更多影视信息，爬取结束。")
        break

    for movie in movies:
        if movie_count >= max_movies:
            break

        try:
            # 获取封面图片链接
            image_tag = movie.find('div', class_='tc_img')
            image_url = image_tag['data-original']

            # 获取标题及详情页链接
            title_tag = movie.find('a', title=True)
            title = title_tag['title']
            detail_link = base_url + title_tag['href']

            # 获取演员信息
            actors = movie.find('p', class_='time').text.strip()

            # 获取更新信息
            update_info = movie.find('p', class_='tc_wz').text.strip()

            # 下载封面图片
            image_response = requests.get(image_url)
            image_name = os.path.join(image_folder, f"{title}.jpg")
            with open(image_name, 'wb') as f:
                f.write(image_response.content)

            # 保存信息
            info = f"""
            电视剧名称：{title}
            演员：{actors}
            更新信息：{update_info}
            详情链接：{detail_link}
            封面图片链接：{image_url}
            """
            info_list.append(info)
            movie_count += 1
            print(f"已处理: {title} (累计 {movie_count}/{max_movies})")

        except Exception as e:
            print(f"处理失败: {e}")

    page += 1  # 下一页

# 保存信息到文本文件
with open(output_file, 'w', encoding='utf-8') as f:
    f.writelines(info_list)

print(f"\n影视信息已保存到 {output_file}")
print(f"封面图片已保存到 {image_folder} 文件夹")
print(f"共爬取 {movie_count} 条影视数据。")
