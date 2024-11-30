import os
import requests
from bs4 import BeautifulSoup

# 创建 images 文件夹
if not os.path.exists("images"):
    os.makedirs("images")

# 定义请求头和 Cookies
headers = {
    "Sec-Ch-Ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Sec-Ch-Ua-Platform": "\"macOS\"",
}
cookies = {
    "HMACCOUNT": "B7DBA2BC6E7289B9",
    "Hm_lpvt_a6458082fb548e5ca7ff77d177d2d88d": "1731999463",
    "Hm_lvt_0e023fed85d2150e7d419b5b1f2e7c0f": "1731841537,1731985962,1731999142",
}

# 基础 URL
base_url = "https://www.cnhnb.com/p/sgzw-0-0-0-0-"

# 保存结果的文件
output_file = "result.txt"

# 初始化图片计数器
image_counter = 1

# 打开文件以写入
with open(output_file, "w", encoding="utf-8") as file:
    for page in range(1, 26):  # 爬取 1 至 25 页
        print(f"正在爬取第 {page} 页...")
        url = f"{base_url}{page}/"
        response = requests.get(url, headers=headers, cookies=cookies)

        if response.status_code != 200:
            print(f"第 {page} 页请求失败，状态码: {response.status_code}")
            continue

        soup = BeautifulSoup(response.content, "html.parser")
        items = soup.find_all("div", class_="supply-item")

        for item in items:
            # 商品名称
            name = item.find("h2").get_text(strip=True) if item.find("h2") else "N/A"
            # 价格
            price = item.find("span", class_="sp1").get_text(strip=True) if item.find("span", class_="sp1") else "N/A"
            # 成交额
            turnover = item.find("div", class_="turnover").get_text(strip=True) if item.find("div",
                                                                                             class_="turnover") else "N/A"
            # 图片链接
            image_url = item.find("img")["src"] if item.find("img") else None

            # 保存数据到文件
            file.write(f"商品名称: {name}\n价格: {price}\n成交额: {turnover}\n图片链接: {image_url}\n\n")

            # 下载图片
            if image_url:
                image_name = os.path.join("images", f"{image_counter}.jpg")
                try:
                    img_data = requests.get(image_url).content
                    with open(image_name, "wb") as img_file:
                        img_file.write(img_data)
                    print(f"图片已保存: {image_name}")
                    image_counter += 1  # 更新计数器
                except Exception as e:
                    print(f"图片下载失败: {image_url}, 错误: {e}")

print(f"数据已保存到 {output_file}")
